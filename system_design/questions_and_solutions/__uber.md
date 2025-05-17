# Uber

Uber is a ride-sharing platform that connect passengers with drivers who offer transportation services in personal vehicles. It allows users to book rides on-demand from their smartphones, matching them with a nearby driver who will take them from their location to their desired destination.

## Requirements

- Are we designing the system for both sides, the rider and driver?
  - Yes

- Will we support different vehicle types?
  - Yes, sedan, SUV, etc
 
- Are we incorporating payments into the design?
  - No, ignore payments

- Do we want to render the rider, driver and map on the UI?
  - No, thats fine

### Functional

- Riders should be able to input a start and destination, and get a fare estimate
- Riders should be able to request a ride after receiving an estimated fare
- Upon request, riders should be matched with a driver who is nearby and available
- Drivers should be able to accept / decline a request and navigate to pickup / drop-off

- Update driver location:
  - The driver’s location should be automatically updated in the system
- Show driver ETA and location updates:
  - The rider should see the ETA and location updates during the ride
- End the trip:
  - The driver marks the ride as complete upon reaching the destination, and they are available for other riders

### Non-functional

- Low latency:
  - The system should prioritize low latency driver location updates (10 seconds or so), and also rider-driver matching (<1 min or so)
- Consistency:
  - The system should ensure strong consistency in ride matching to prevent any driver from being assigned multiple rides simultaneously
- Throughput:
  - The system should be able to handle high throughput, especially during peak hours, where drivers are frequently updating their locations, and riders are frequently sending ride requests

## Data model / entities

- Riders:
	- riderID
	- riderName
	- riderEmail

- Drivers:
	- driverID
	- driverName
	- driverEmail
	- vehicleType

- Fare:
  - This entity represents an estimated fare for a ride. It includes the pickup and destination locations. The estimated fare, and the ETA. This could also just be put on the ride entity, but we'll keep it a separate entity to normalize the data.
    - fareID
    - rideID
    - start, destination, vehicleRequired
    - fareCost
    - eta

- Ride:
  - This entity represents an individual ride from the moment a rider requests an estimated fare all the way until the ride completes. It records all details of the ride, including the riderID, driverID, rideStatus, routeDetails (if necessary - when the driver is moving, we'll update routeDetails of the route the driver is taking), and additional metadata.
    - rideID
    - fareID
    - riderID, driverID
    - rideStatus: enum MATCHING / PENDING_PICKUP / PENDING_RIDE / COMPLETED
    - routeDetails: [ { pointA, pointB, ts, PICKUP }, { pointC, pointD, ts, RIDE }, { pointE, pointF, ts, DROPOFF } ]
    - metadata: { createdAt, vehicleDetails }

- Drivers location:
  - Note that this entity will likely be only stored within a cache, since the drivers location data is very short lived and frequently updated - it doesn't make sense to store it in a DB
 
  - This entity stores the real-time location of drivers. It updates frequently as drivers are moving. This entity is used to match riders with nearby drivers, and also to track the progress of a ride.
    - driverID
    - long / lat / geohash (if using a geohashing approach) / location (if the system is using PostGIS, then location will be of PostGIS's GEOMETRY type)
    - updatedAt

## Workflow

1. The rider will first request for a fare estimate for a ride
2. After the rider sees the fare estimate, they'll request a ride and initiate the driver matching process
3. Once the driver is matched, they can accept / decline. If the driver declines, then the matching process is resumed
4. After a driver accepts, the backend will notify the rider of the driver, vehicle details, ETA, etc
5. After the driver picks up the rider, they'll update the database and start the actual ride
6. Once the driver gets to the destination, they'll update that the ride is completed

**Note that the driver will always periodically update their location to the database. However, if the driver is handling a ride, then the driver's location and ETA will also be sent to the rider**

## API design

- Note that we’ll use riderID / driverID if the user is authenticated to send requests to the endpoints. The riderID / driverID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Retrieve fare estimate

- This endpoint is used by the rider to request for the fare estimate for a ride, using the rider's current location and desired destination. Afterwards, this endpoint will return the estimated fareCost and ETA. Here, a new fare entry will also be created in the database.

Request:
```bash
POST /fare
{
  pickupLocation, destination, vehicleRequired
}
```

Response:
```bash
{
  fareID,
  fareCost, eta
}
```

### Request ride and initiate ride matching process

- This endpoint is used by the rider to send their ride request after reviewing the estimated fare details. The rider will call this endpoint to initiate the ride matching process by signaling the backend to find a suitable driver, thus creating a new ride entry in the database (status will be MATCHING) using the fareID.
- The matching process will happen in the backend, where a matched driver will be notified of the ride request, and they could accept or decline.

- Note that we won't put the fareID in the query parameters because the driver will also request a similar "/rides" endpoint - and so the fareID should only be accessible by the actual rider, not the driver

Request:
```bash
POST /rides
{
  fareID
}
```

**Note that at this point in the flow, we match them with a driver who is nearby and available. However, this is all happening in the backend, so we don't need to explicitly list out an endpoint for this.**

### Driver to accept / decline ride request

- After the matching process is completed, the matched driver will be notified of the ride details, and this endpoint will allow the driver to accept or decline the ride request.
- If the ride request is declined, the matching process will resume and the rider will also see in the UI that the matching process is still pending.
- If the ride request is accepted, the rider will be notified, and the rideStatus will change to PENDING_PICKUP. The ride entry in the database will also be updated using the rideID to update the driverID, routeDetails, status, metadata. The driver will periodically update their location so that the rider can see their location and ETA to the pickup location. The driver will also receive the pickup location.

<br/>

- Note that drivers will have a limited amount of time (let's say 30 secs) to accept / decline. Otherwise, the matching process will resume.
- Note that we won't put the fareID in the query parameters because the driver will also request a similar "/rides" endpoint - and so the fareID should only be accessible by the actual rider, not the driver

Request:
```bash
PATCH /rides/:rideID?op={ ACCEPT / DECLINE }
```

Response:
```bash
{
  pickupLocation's long / lat
}
```

### Driver to update their location

**Note that we'll use a websocket connection to send the driver's location updates to the backend. The backend will then send these location updates and ETA to the rider during a ride via another websocket connection with the rider (websocket connection with the rider will be persisted only during the duration of the ride)**

#### Driver and rider will establish a websocket connection 

- This endpoint will be used to establish the websocket connection. The			Sec-WebSocket-Key header will be a value that the server will use to generate a		response key to send websocket requests. The Sec-WebSocket-Version will be the	websocket protocol version, usually 13.

Request:
```bash
GET /drivers/location (Driver requests this endpoint to set up a websocket)
GET /rides/:rideID/location (Rider requests this endpoint to set up a websocket)
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: xyz
Sec-WebSocket-Version: 13
```

- In the response, the Sec-WebSocket-Accept header will usually be generated by	combining the Sec-WebSocket-Key from the client with another hashed value. This	resulting value will be returned to the client

Response:
```bash
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: xyz + hash value
```

#### Driver sends location updates

- The drivers will periodically update their location for the below cases:
  - Not handling a ride:
    - Regardless if the driver has a current ride request or not, they'll still update their location, so that the driver can be matched for a ride request
  - Picking up rider:
    - Once the driver accepts the ride request, they'll request this endpoint to update their location so that the rider can see their location and a computed ETA generated by the backend. The routeDetails will also be updated during a ride using the driver's location update.
  - During actual ride:
    - During the actual ride, the driver will also update their location so that an ETA can be generated by the backend and sent to the driver and rider

- Also, because some drivers may not frequently change their location, we can likely store the driver's previous location in the client's cache with a TTL, and only request this endpoint if the previous location changed from the new location after 10 secs or so. This will prevent unnecessary network requests being made.

Request:
```bash
{
  long / lat
}
```

#### Riders to receive location updates and ETA after driver updates location during a ride

Location and ETA update from backend to rider via websocket connection:
```bash
{
  location, ETA
}
```

### Driver to confirm pickup of rider

- Once the driver picks up the rider, they'll request this endpoint to confirm the pickup. The rideID will then update it's rideStatus to PENDING_RIDE.

Request:
```bash
PATCH /rides/:rideID?op={ CONFIRMED_PICKUP }
```

### Driver to complete the ride

- Once the driver reaches the destination, the driver will request this endpoint. The driver will then be shortly available to take on new rides by updating their location periodically. After the driver requests this endpoint, any payment processes will be initiated likely by a separate payment service.

Request:
```bash
PATCH /rides/:rideID?op={ COMPLETE_RIDE }
```

**Remember that you can't trust any data sent from the client as it can be easily manipulated. User data should always be passed in the session or JWT, while timestamps should be generated by the server. Data like fareCost should be retrieved from the database and never passed in by the client.**

## HLD

### Microservice architecture

- A microservice architecture is suitable for this system, as the system requires independent services such as searching drivers, requesting a ride, etc. These are all independent operations which could potentially be managed by separate services.

- Microservices can benefit from a gRPC communication as there will be multiple channels of requests	being sent / received in inter-service communication between microservices. Thus, gRPC could be the	communication style between microservices, as it supports a higher throughput, and is able to handle multiple channels of requests as opposed to REST, which uses HTTP, that is not optimized for		multi-channel communication between services.

### API gateway

- The API gateway will provide rate limiting, authentication, and route requests to the specific services.	For example, for requesting rides, the Ride service can handle the requests.
- The API gateway will also allow initiating 2 requests to separate services via 1 single request. For example, the rider can request for a ride, and the matching process will then start and notify the matched driver.

### Rider client

- The primary touchpoint for users is the Rider Client, available on iOS and Android. This client interfaces with the system's backend services to provide a seamless user experience.

### Driver client

- In addition to the Rider Client, we introduce the Driver Client, which is the interface for drivers to receive ride requests and provide location updates. The Driver Client communicates with the Location Service to send real-time location updates.

### Ride service

- The first thing that riders will do when they open the app is to request for a fare estimation. The rider will then receive the fare estimate, and choose to request a ride or not. The fare estimation and ride request initiation will be handled by the Ride service.
- The Ride service will also manage the ride entries in the database, and calculate the fare estimates. It will also communicate with 3rd party mapping APIs such as Google's Maps API to determine the distance and travel time between the start and destination to calculate the fare estimation.

#### Workflow of fare estimation requests

The workflow of fare estimation requests will be as follows:

1. The rider will first send their pickup location and destination to the Ride service (via the API gateway)
2. The Ride service will make a request to the 3rd party mapping API to calculate the distance and ETA between the pickup and destination, and then calculate the fare estimate.
3. The Ride service will add a new fare entry in the Fares table with the fare details (start, destination, vehicleRequired, etc).
4. The Ride service will then return the fare entity (fareCost, eta, etc) to the API gateway, which will forward it to the rider so that they can accept the fare (then request a ride) or not

#### Workflow of ride requests

- Once a rider reviews the fare estimate and ETA, they can request a ride via the Ride service. The Ride service will then add an entry for the ride to the Rides table.

The workflow of ride requests will be as follows:

1. The rider will confirm the fare estimate and ETA, then send a ride request to the Ride service using the fareID (via the API gateway)
2. The Ride service will create a new ride entry in the Rides table, and link it to the fareID.
3. The matching process will also be initiated by requesting the Ride Matching service, and the rideStatus will also be updated to MATCHING

### 3rd party Mapping API (Google's Maps API)

- We'll use a 3rd party mapping API such as Google's Maps API to provide the mapping and routing functionality. It will be used by the Ride service and potentially Location service to calculate the distance and ETA between locations.

### Database / cache

- The database will be responsible for storing Riders, Drivers, Fare, Ride data (not including the drivers location updates). Fare and ride entries, when created will be stored here, along with the periodic updates of the driver's location. We could use either a SQL DB like PostgreSQL or a NoSQL DB like DynamoDB / MongoDB / Cassandra. The relationships between the data is fairly simple, and could also be implemented in a NoSQL DB like DynamoDB or Cassandra. Because there could be a high frequency in write requests for fares / rides, we could use either DynamoDB or Cassandra which both provides high horizontal scalability.

#### Cache

- A separate cache can also store the riders, drivers, fare, rides and drivers location data. The cache could be either maintained in Memcached or Redis, however since we'll be using a location based search approach (either geohash vs quadtree vs PostGIS), Redis will be more suitable since it provides additional support for working with geospatial data from the drivers location updates. Also, since Redis is single-threaded, updates to the same ride entry within the a cache instance will have a low chance of deadlocks.

### Ride Matching service

- The Ride Matching service begins the matching process from a ride request from the Ride service. This service will use a rider-driver matching algorithm (not focused in this SDI) to match the ride requests with the best available drivers based on distance, availability, driver rating, vehicle type, etc.
- The Ride Matching service will likely use a location based search approach to efficiently find nearby available drivers for a ride request as discussed in the DD.
- The Ride Matching service will also need to ensure that the same ride request is not sent to multiple matched drivers, it should only be sent to one matched driver at a time, and that driver could either accept / decline - we'll likely apply a Redis distributed lock here as discussed in the DD.
- The Ride Matching service will likely also update the rideID's driverID, routeDetails, rideStatus (update it to PENDING_PICKUP), metadata, etc, in the Rides table once the driver accepts the ride request.

#### Workflow of matching process

The workflow of the matching process will be as follows:

1. The matching process will be initiated by the Ride service for a ride request. The actual design of the matching process will be discussed in the DD.
2. Drivers are also periodically sending their location updates to the Location service, which will update the Drivers location cache data
3. The Ride Matching service will then use the latest location updates, either via the Geohash OR Quadtree OR PostGIS service to find nearby available drivers, and decide on the top matched driver (discussed more in the DD)
4. The matched driver will then be notified about the ride details via the Notification service, and they could accept / decline the ride request

### Geohash service (if using geohash)

- The Geohash service will search for drivers within a search radius using a geohash based approach, and return them to the Ride Matching service. The Geohash service will take a geohash of the search radius (using a geohash converter) and find drivers within the specified radius by comparing their geohash strings.
- The geohash converter, which could be PostgreSQL's PostGIS geohash conversion functionality shown in 'PostGIS geohash conversion function', will take a long / lat coordinate of either a radius or driver, and then convert it to a geohash string. This geohash string will be compared against the geohash strings in the Drivers location cache data to find nearby drivers.
- Because we're using geohash, the Geohash service will compare the prefixes of the search radius' geohash string with the prefixes of the drivers' geohash string. If the prefixes are the same, then this means the driver is within the search radius. A query such as the one below can be used to find drivers with the same prefix as the search radius' geohash.

```sql
select driverID, lat, long, geohash from driversLocationTable
where geohash like '${radiusGeohash}'
```

PostGIS geohash conversion function:
```sql
select ST_GeoHash(ST_Point(${long}, ${lat}))
```

- Geohash can sometimes be slower than a typical quadtree. It can also be slower than PostGIS's built-in location based search functionalities. This will be discussed more in the DD.

#### Geohash cache

- Because the querying the geohash data on disk may be slow, we can store a geohash cache in Redis. Redis provides support for geohashing to encode and index geospatial data, allowing for fast querying. The key advantage of Redis is that it stores data in memory, resulting in high-speed data access and manipulation. Additionally, we can periodically save the in-memory data to disk in Redis Database (RDB) if we want to ensure fault tolerance of the geohash cache.

### Quadtree service (if using quadtree)

- The Quadtree service will recursively build and update the Quadtree table and cache. The Quadtree service will also be used to search the quadtree efficiently by traversing down the tree from the root node to the leaf nodes. The search within a quadtree will be discussed more in the DD.

- A downside to a quadtree is that updating the tree when drivers' locations changes may be a bit complex. Thus if there is a high frequency of updates, then a quadtree may not be the best, and a geohashing approach may be more simpler since the geohash value only needs to be changed for a single entry, as opposed to updating the sibling nodes and leaf node in a quadtree. Thus, we'll use a geohashing approach, with a geohash cache in this design.

#### Quadtree table / cache

- Because a quadtree is an in-memory data structure, we can keep both a quadtree table within PostgreSQL as well as a cache using Redis. PostgreSQL provides SP-GiST, which provides functionality for storing and querying a quadtree data structure.
- Although Redis doesn't directly provide quadtree support, we'll use Redis as the quadtree cache since it provides complex data structures such as lists and sorted sets which will be helpful in storing nodes of the quadtree. For example, a leaf node can contain a Redis list which contains driverIDs which fall within the leaf node's radius.
- Drivers will send location updates to the Location service via a websocket connection, and the Location service will then update the quadtree table / cache - update the leaf node the driver is currently in. If a driver leaves the leaf node's radius, then the driverID could be moved to the leaf node's sibling nodes.
- Additionally, a quadtree data structure is not as complex to build, and could be implemented within a memory optimized EC2 instance.

### PostGIS service (if using PostGIS)

- We could also use a PostGIS service which will convert the driver's long / lat values in the Drivers location cache data to a PostGIS GEOMETRY type and store it in a Drivers location table. We'll then add a new column of this GEOMETRY type (we'll call it the location column) to the Drivers location table. This PostGIS service will then be used to query a Drivers location  using PostGIS search functions like ST_Intersects (to find if a long / lat value intersects with another point) and ST_DWithin (to find if a long / lat value is within a radius).
- Because we now need to query the data on disk (Drivers location table), PostGIS will be slow and not suitable for this design.

### Location service

- The Location service will manage the real-time location data of drivers. It will receive location updates from drivers, then store it in the Drivers location cache data.
- During a ride and when a driver is going to the pickup location, the Location service will also send to the rider, the driver's latest location update and ETA (calculated using the 3rd party mapping API).

This means that when the driver is not handling a ride, they will still need to send real-time location updates frequently, and when the driver is handling a ride, the rider will receive the same location updates. Thus, we'll need real-time communication between the clients and the Location service, either using websockets or polling or SSE:

#### WebSockets vs polling vs SSE

##### Websockets

- Websockets may be the most suitable communication style between clients and the Location service. Only the driver clients will send location updates to the Location service via websockets, and the other rider clients could also receive these same location updates and ETA via a websocket connection. Websockets can also help render the UI after the driver clients receive data to change the map on the UI. Likewise, the rider's map can also be rendered by using the websocket connection.
- If a driver also has a slow or disconnecting network, we could fallback to polling OR store the driver's location updates in the client's local storage. Once the driver has a stable connection, the data in the local storage could be sent to the Location service.

##### Polling

- Polling may not be as suitable, since the driver client will frequently need to ping the Location service and update it's location. Additionally, the rider client will need to frequently request the Location service for location updates during the ride. However, if a websocket connection cannot be created, we can fallback to polling.

##### SSE

- SSE may also not be suitable here, since the driver client can only request to establish the SSE based connection, but cannot directly update their locations. SSE only allows the server to send messages within the long-lived HTTP connection. The rider client could still receive location updates, however the driver client has no way to send location updates via SSE.

### Notification service

- The Notification service will deliver real-time notifications (either APN or Firebase Cloud Messaging notifications for iOS and Android devices respectively - or a Web Push Notification if using a web app) to drivers when a ride request is matched. Once the driver accepts the ride request, the notification service will send a notification of the ride and driver's details to the rider to inform them the driver accepted.
- The Ride Matching service will likely also update the rideID's driverID, routeDetails, rideStatus (update it to PENDING_PICKUP), metadata, etc, in the Rides table once the driver accepts the ride request.

#### Workflow of notifying ride request to driver, and notifying rider after driver accepts the ride

1. The Ride Matching service will first determine the ranked list of matched drivers, and it will send a notification to the top driver on the list via the Notification service
2. The matched driver will receive the notification of the ride request via APN, FCM, Web Push Notification, etc, and they could accept / decline the ride
3. If the driver accepts the ride, they'll send a request the Ride Matching service to update the rideID's driverID, routeDetails, rideStatus (update it to PENDING_PICKUP), metadata, etc in the Rides table. If the driver declines, the Notification service will just send a notification to the next top driver in the matched list.
4. Since the ride has been accepted, the Notification service will send a notification to the rider to inform them about the driver's details (rider will set up a websocket connection with the Location service here)
5. The driver will then navigate to the rider's pickup location, then confirm the pickup, then complete the ride

### L4 Load balancer

- We’ll need an L4 load balancer to support traffic at the TCP level. L4 load balancers,	let’s say using ELB in TCP mode can load balance websockets. When client’s need to	connect to a Location service server via websocket, the L4 load balancer will route them to the Location service server they	previously connected to or to a server using the load balancing algorithm.		However, if a server goes down, the L4 load balancer can route the client to		connect to another Location service server instead.

- When a client needs to connect to the Location service server, the request will first go to the L4	load balancer, then to the Location service server. There will actually be a symmetric websocket	connection between both the client to the L4 load balancer, and between the L4 load	balancer to the Location service server.

- L4 load balancers can be stateful and use sticky sessions to persist the server the	client previously connected to. The sticky session can be implemented by identifying	the user, usually with cookies or their IP address, and storing the user’s connected	server for handling future requests.

- If clients disconnect from a server, they can automatically reconnect to the		same server or another one via the L4 load balancer. Reconnecting to the same	server may be easier, as the session data in the L4 load balancer doesn’t have to	be updated.

<img width="750" alt="image" src="https://github.com/user-attachments/assets/9841a033-99d9-4a76-9ccc-d4865b1c4578" />

## DD

### Handling frequent driver location updates and ensuring efficient searches on location data

- We'll need to handle the frequent driver location updates, and efficiently search the location data to match nearby ride requests.

Below are 2 main problems we'll need to solve: 
1. High frequency of location update writes 
2. Efficiently searching location data

#### High frequency of location update writes

- Let's say we have 10M drivers, who will send location updates roughly every 10 seconds - then we'll have 10M / 10 seconds = 1M requests per second!

<br/>

- Even if we choose a SQL or NoSQL DB like PostgreSQL or DynamoDB respectively, they would still be overwhelemed with the write load, and would need to be scaled so much that it becomes expensive to manage them. For DynamoDB in particular, 2M writes a second of ~100 bytes would cost you about 100k a day!

#### Efficiently searching location data

- Without any optimizations, to query a table based on the long / lat values, we would need to perform a full table scan to calculate the distance between each nearby driver and the rider's location when performing the matching process. Even with indexing on long / lat, traditional B-tree indexes are still not suitable for multi-dimensional data like geospatial data.

#### Solving for the issues

- To solve for the above 2 issues, we can try the following and in 'Handling frequent driver location updates and ensuring efficient searches on location data':
  - Direct database writes and proximity queries
  - Batch processing and specialized geospatial database
  - Real-time in-memory geospatial data store:
    - We'll use this approach, consisting of a Redis in-memory data store containing the geohash data. Additionally, we'll also use Redis persistence to periodically save the in-memory data to disk using Redis Database or AOF (append only file). Redis Sentinel can also be used to configure automatic failover if the master node goes down, ensuring that a replica is promoted to a master.

### Efficiently storing the location data for fast searches

Efficiently storing location data for fast searches can be done using multiple approaches. The resource notes in 'Location based search' goes over all of the main approaches. However, in this DD, we'll use either geohash, quadtree or PostGIS.

#### Geohash service

- Refer to the "Geohash" section in the resource note 'Location based search' for the background on geohash.

<br/>

- Geohash works by converting the long / lat to a string of letters and digits. We first divide the map into 4 grids recursively until the grid size is small enough such that it can contain a relatively small number of drivers. As the map gets recursively divided, we'll assign a generated Base-32 geohash string to the grid. Geohash also operates with a fixed precision, where the smallest grids cannot be further divided, and all the smallest grids will have the same size. However, custom dynamic behavior can be added to a geohashing approach, but adding dynamic behavior may be more complex to do.
- Since geohashes represent hierarchical spatial data, shorter geohash strings cover larger areas, and longer geohash strings cover smaller areas with more precision. Therefore, if we keep removing the last character from a geohash string, the new geohash string will be for a larger area. To make geohash filtering more efficient, we can index the geohash column (like in 'Index on geohash') so that queries with the LIKE or WHERE operators will optimize it's prefix based searches.
- An example of using LIKE with a geohash string is given below:

Index on geohash:
```sql
CREATE INDEX idx_geohash ON driversLocationTable USING geohash
```

Using LIKE to filter geohash strings:
```sql
select driverID, lat, long, geohash from driversLocationTable
where geohash like '${radiusGeohash}'
```

Also, let's say we're searching for locations within the geohash redius of "dpz83" - then the query above should return the following:
- dpz83a
- dpz83b
- dpz83xyz

<br/>
<br/>

- We can also generate a geohash string using PostgreSQL's PostGIS extension as follows:

PostgreSQL geohash conversion function:
```sql
select ST_GeoHash(ST_Point(${long}, ${lat}))
```

<br/>
<br/>

- Geohash works well for majority of the cases, but boundary issues may come up when one driver covers 2 geohash strings. Additionally, in some cases, there could be drivers within the border of 2 geohash strings, and so that driver doesn't belong to any geohash string. In these cases, the geohash generation algorithm can be modified to account for such edge cases.
- Also, another issue may be when too few drivers appear in the search result. In this case, we can increase the search radius by removing the last digit of the geohash string, and we can continue to increase the radius by removing another digit from the end.

##### Geohash sharding / partitioning

- If we have a table containing the driverIDs and geohash strings, we can easily shard the database and partition the tables based on prefixes of the geohash strings. We'll shard by the prefixes of the geohash strings because drivers which are within the same geohash search radius will also be within the same shard. This will make searches faster, since we'll have to look through fewer shards or entries of the table.

#### Quadtree service

- Refer to the "Quadtree" section in the resource note 'Location based search' for the background on quadtrees.

<br/>

- A quadtree also recursively divides the map into 4 grids until the contents of the grids meet a certain criteria, like not having more than 100 drivers. A quadtree is an in-memory data structure that helps with location based searching.
- The data on a leaf node (leaf node represents the most granular grid) in a quadtree can contain long / lat and a list of driverIDs in the grid. The data on a parent node (parent node represents the parent grid of leaf nodes) contains the parent grid's long / lat values and pointers to the 4 child nodes.
- Assuming a leaf node has at most 100 drivers, then to build a quad tree for N drivers:
  - It will take (N * 100) * log(N / 100) time complexity, since we're parsing through (N / 100) leaf nodes which contains at max 100 drivers each, and we'll also be parsing the height of the tree which will be log(N / 100), where N / 100 is the number of leaf nodes.

- Below is an example of a quadtree quad:
<img width="750" alt="image" src="https://github.com/user-attachments/assets/23144928-0519-46eb-8b49-4dd0cd8c45b5" />

<br/>

- To search in a quadtree, we'll start from the root node and traverse down the tree until we find a node within the search radius. If we find a node within the search radius, we'll traverse the node's child nodes and siblings to see if they're also in the search radius. We'll keep a list of drivers in the leaf nodes which are within the search radius, and then return the list of drivers. The downside to a quadtree is that searches can be a bit complex to implement.
- A quadtree is also an in-memory data structure, thus it will likely be stored within a cache or in-memory database. Therefore, we'll need to invalidate any nodes within the quadtree, and frequently perform updates to it.

- Below is an example of a quadtree, along with the DLL data structure consisting of sibling nodes. The DLL will help with searching sibling nodes when traversing the quadtree and finding nodes / siblings within a search radius:
<img width="800" alt="image" src="https://github.com/user-attachments/assets/9b53efa6-5790-4a6a-97d2-961ba90a0af5" />

<br/>

##### Quadtree table / cache

- An entry in the quadtree table / cache can be as follows:

Quadtree node's entry in table / cache:
```bash
{
nodeID,
drivers: [ { driverID, long / lat, vehicleDetails } ],
nodeQuad: { maxLong, maxLat, minLong, minLat },
leafNode: TRUE / FALSE,
childNodePtrs: { childNode_1, childNode_2, childNode_3, childNode_4 }
}
```
- In this entry, the nodeID can represent the node of the quadtree. If a node is a leaf node, we'll set the leafNode to TRUE. Also, if it is a leaf node, then there will be drivers populated within this node. The nodeQuad field will also be the quad's max / min long / lat values.
- When searching for drivers within a search radius, we'll first check if the nodeQuad's long / lat values are intersecting with the search radius. If the quad is intersecting, then we'll traverse down the tree to find the leaf nodes. In the leaf nodes, we'll search for driverIDs which have long / lat values within the search radius.

##### Building a quadtree

- We will start with one node that will represent the whole world in one quad. Since it will have more than 100 drivers, which may be our criteria, we will break it down into four nodes and distribute locations among them. We will keep repeating this process with each child node until there are no nodes left with more than 100 drivers.

##### Dynamic quads

- We can use dynamic quads in our quadtree where if the number of drivers exceed a threshold in a quad, we'll further split the quad into 4 more quads.

##### Searching in a quadtree

- In the quad tree, child nodes will be connected to sibling nodes with a DLL. Using the DLL, we can move left / right / up / down to sibling or child quads to find drivers. An alternative to a DLL is to use parent pointers from the child nodes to the parent node.

- When searching in the quadtree, we start searching from the root node and visit child nodes which are in the search radius. If a child node is in the search radius, we can traverse through it’s own child nodes and sibling nodes using the DLL and return them if they are also in the search radius.

- If we don't have enough drivers to return after searching a specific node, we can search the node's siblings and also it's parent node to retrieve surrounding drivers as well.

##### Adding / updating / removing an entry (driver) in a quadtree

- To add / update a driver in the quad tree, we can search the nodes for the driverID and add / update the driver in the node, and also update any neighboring siblings if needed. If after adding the driver, the leaf node reaches the threshold on the number of drivers a node can have, we'll need to split this leaf node further into 4 leaf nodes and allocate these 4 leaf nodes with the drivers from the original leaf node.
- To remove a driver in the quad tree, we can search the nodes for the driverID and remove the driver from the node, and update the neighboring nodes accordingly

##### Quadtree sharding / partitioning

- We can shard the quadtree based on regions on the basis of zip or postal codes, such that all the drivers and nodes that belong to a specific region are stored in a single shard. A region in this case will be a branch within a quadtree - therefore, a shard could contain a separate part of a single quadtree (the branch). Some regions could also be combined into a single shard to prevent uneven distributions.
- We can do this since the user’s queries will be based on the location, so sharding this way will cause less inter-shard communication and speed up queries.
- However, this approach will result in slow responses when numerous queries are on the server for a single shard possibly during a tourist season. To prevent hotspots, we can apply replication to the quadtree.
- There could also likely be a mapping maintained within ZooKeeper that keeps track of the mapping between regionID : shardID. regionID or shardID will rarely change (it may change only when a new region or shard is updated), thus this mapping will rarely change.

##### Quadtree replication

- We can replicate both the quadtree table and cache on multiple servers to ensure high availability. This also allows us to distribute the read traffic and decrease the response times.
- Quadtrees should take up relatively little storage, and thus can be backed up easily. In case we may lose the quadtree data, we can use checkpointings at set intervals to backup the data.

##### Fault tolerance of quadtree

- Because the quadtree will likely have both a table and cache, it will be highly available. However, if a single cache server dies, we won't have a way of knowing which quadtree branch or nodes the cache server stored.
- To ensure we know which cache server stores which quadtree branch / nodes, we can store a reverse mapping of cacheServerID: [ quadtreeBranch, nodeIDs ] in a configuration service such as ZooKeeper, or within the Quadtree table itself. This way, if the cacheServerID died, we can rebuild the quadtree branch / nodes using this reverse mapping.

### Reducing number of location updates from drivers

- High frequency location updates from drivers can lead to a system overload, and also use up unnecessary bandwidth. We can do the following to reduce the number of location updates drivers need to send to the backend (and in 'Reducing number of location updates from drivers'):
  - Adaptive location update intervals:
    - In addition to this approach, the client could cache / store the previous location update sent, and compare the previous location update to the current driver's location. If the location did not change, then there is no need for the client to update the backend about the driver's location. This will reduce the number of network calls being made to the server, and also free up unnecessary bandwidth, while ensuring accuracy of location updates.

### Preventing multiple ride requests from being sent to the same driver simultaneously

- We'll need to request only one matched driver at a time from a "matched drivers list" for a single ride request. The driver would then have about 30 secs or so to accept / decline the request before the Ride Matching service moves on to the next matched driver in the list. This concurrency issue is similar to the Ticketmaster SDI, where a single driver can be matched to the same rider at a time.
- To ensure a single driver is matched to the same rider at a time, we can do the following, and in 'Preventing multiple ride requests from being sent to the same driver simultaneously':
  - Application-level locking with manual timeout checks
  - Database status update with timeout handling
  - Distributed lock with TTL:
    - We'll use this approach. This way, once the lock is acquired, no other process can send a ride request to the same driver until the lock is released. Any process handling the ride request for a matched driver would need a lock entry within the Redis distributed lock data store, before updating the ride entry within the Rides table. The lock entry could also contain additional metadata which would be needed to update the relevant tables about the ride as shown below.

```bash
{
  lockID: { rideID, riderID, driverID, ttl }
}
```

### Ensuring no ride requests are dropped during peak demand periods

- During peak demand periods, the system may receive a high volume of ride requests, which can lead to dropped requests. Instances of the Ride Matching service could crash if there are too many ride requests, or the ride requests could also be dropped. We can do the following to ensure scalability, and in 'Ensuring no ride requests are dropped during peak demand periods':
  - First-come, first-served with no queue
  - Queue with dynamic scaling:
    - We'll use this approach with a "Match queue" positioned between the Ride service and Ride Matching service. To ensure the ride requests are delivered in a FIFO basis, we can use a SQS FIFO queue. For scalability purposes, we could instead use Kafka, since a SQS FIFO queue only supports a throughput up to 70k messages per second, while sometimes we might expect 100k messages per second. Therefore, Kafka may actually be a better choice to support scalability.
    - We could also further partition the queue based on region, where for dense areas like NYC, there would be more fine-grained areas corresponding to partitions of the queue. And a larger area (less dense) could correspond to another partition.

### Scaling to reduce latency and improve throughput

- We can further scale the system to reduce latency and improve throughput by doing the following, and in 'Scaling to reduce latency and improve throughput':
  - Vertical scaling
  - Geo-sharding with read replicas

