# Nearby friends

For an opt-in user who grants permission to access their location, the client presents a list of friends who are geographically nearby, and their locations.

Note: In proximity services, the addresses for businesses are static as their locations do not change, while in "nearby friends", data is more dynamic because user locations change frequently.

## Requirements

### Questions

- How geographically close is considered to be nearby?
  - 5 miles, and this number can be configured by the user

- Is the distance calculated as a straight line between the users?
  - Yes

- How many users does the app have, and how many are actively using it every day?
  - 1B users in total, and 100M DAU

- Do we need to store location history?
  - Yes, location history may be used for ML

- If a friend is in-active, should we remove them from the nearby friends list OR should we display their last known location?
  - Display their last known location

- Do we need to update the nearby friends list in real-time within maybe 10-30 seconds?
  - Yes, real-time

### Functional

- Users can see nearby friends, and also the distance and the last timestamp that the distance was updated
- Nearby friends should be updated every few seconds (10 - 30 seconds)
- Radius for finding nearby friends can be configured
- We're using a straight line to calculate the distance
- The system stores location history
- Last location update will be shown for in-active users

### Non-functional

- Low latency:
  - Location updates from friends should be received in 10 - 30 seconds, in near real-time
- Eventual or weak consistency for the location data:
  - Location data may be updated within a few		seconds
- Throughput:
  - Throughput from multiple clients will need to be handled efficiently

## Nearby friends 101

- In apps like Nearby friends, there is usually an intermediary server which receives the messages from the client, and sends the message to the recipients. The servers also establish the connection between the client and recipient

There are different ways in which the communication between the client and recipient could be done:

### HTTP

- HTTP creates a connection each time a HTTP request is sent. Using the keep-alive	header, the client can maintain a persistent connection with the servers, which		reduces the number of HTTP connections and TCP handshakes that need to be set 	up.
- However, HTTP is not bidirectional, and so both the client and server cannot send	messages using the same connection.

### Polling / long polling

- In polling, the client periodically sends requests to the server to check if there are	new messages or data available. Usually, the server won’t have any messages, and	so polling will be costly.
- In long polling, the client holds the connection open for a while and requests the		server to check if there are new messages. The server responds with any new		messages or the connection times out and closes. Long polling will still be costly and inefficient	as it creates multiple connections and waits for them to be timed out or for new 		messages to be sent. Also polling is not a bidirectional communication approach, 	which will be needed in this app.

### Websocket

- Websockets will be a good choice for bidirectional communication, and it will operate	over a TCP connection. A websocket connection is initiated by the client, which		requests for a connection upgrade via the HTTP headers. The server then			acknowledges the upgrade, and the websocket connection is established.
- Websockets also work over firewalls because they use port 80 or 443 which are		used by HTTP/HTTPS connections

- Websockets also communicates over an encrypted TLS connection, where the		messages sent are encrypted. TLS provides secure communication for bi-directional	communication, and is built on top of and supports both HTTP and HTTPS.

### Peer-to-peer communication

- Conceptually, a user would like to receive location updates from every active friend nearby. It could in theory be done purely peer-to-peer, that is, a user could maintain a persistent connection to every other active friend in the vicinity. This solution is not practical for a mobile device with sometimes flaky connections and a tight power consumption budget:

<img width="441" alt="image" src="https://github.com/user-attachments/assets/855097e2-4979-4d6a-90e1-800c215fcbe0" />

- A more practical design would have a shared backend and look like this:

<img width="623" alt="image" src="https://github.com/user-attachments/assets/996a6961-07b3-47fd-b0da-205f3ec16e1a" />

- This sounds pretty simple. What is the issue? Well, to do this at scale is not easy. We have 100 million active users. With each user updating the location information every 30 seconds, there are 3.3M updates per second. If on average each user has 400 friends, and we further assume that roughly 10% of those friends are online and nearby, every second the backend forwards 3.3M * 400 * 10% = 140 million location updates per second. That is a lot of updates to forward.

## Data model / entities

- Users:
  - userID
  - userName
  - userEmail

- Friendships:
  - A single entry in the Friendships entity will contain the below fields
    - friendshipID
    - friends: { userID_1, userID_2 }

- Location updates:
  - This entity will store a history of all the location updates from a userID. We'll persist the location updates since the requirement is that these updates will be used later for ML
	- userID
	- long / lat / geohash (if the system is using geohash) / location (if the system is using PostGIS, then location will be of PostGIS's GEOMETRY type)
	- updatedAt

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed messages quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

- Note that websocket requests will contain requests which need bidirectional communication, such as sending and receiving location updates. HTTP requests will be requests where the user sends friend requests to other users, so that they can listen to each other's location updates. HTTP requests could also be used when the user wants to view all of their friends, and get all of their latest location updates when the user first opens the app.

Websocket requests:

### User performs a periodic location update

#### Establish a websocket connection

- This endpoint will be used to establish the websocket connection. The			Sec-WebSocket-Key header will be a value that the server will use to generate a		response key to send websocket requests. The Sec-WebSocket-Version will be the	websocket protocol version, usually 13.

Request:
```bash
GET /location-updates
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

#### Send periodic location update

- Clients will send periodic location updates via an established websocket connection

Request:
```bash
WS /location-updates
SEND {
	long / lat
}
```

#### Receive periodic location update

- Clients will receive periodic location updates from other clients

Response:
```bash
RECV {
  userID,
  long / lat,
  updatedAt
}
```

<br/>

HTTP requests:

### Send a friend / unfriend request

Request:
```bash
POST /users/:userID?op={ FRIEND_REQUEST / UNFRIEND }
```

### View all friends + friends' latest location updates (when the client first opens the app)

- Note that we'll use cursor based pagination to retrieve a paginated result of all the friends of a userID. After this endpoint is called, the userID could likely request for all the latest location updates from the Location updates table / cache for their friends in this paginated result. This way, the current viewport could be hydrated with both the friends, and the friends' latest location updates as follows. The two requests could also be combined into one:

Request:
```bash
GET /friends?nextCursor&limit (View all friends)
GET /friends/location-updates?nextCursor={ viewport's oldest updatedAt value for friends' latest location update }&limit (View all friends' location updates)
```

Response:
```bash
View all friends:
{
  friends: [ { userID, userName } ],
  nextCursor, limit
}

View all friends' location updates:
{
  locationUpdates: [ { userID, userName, long / lat, updatedAt } ],
  nextCursor, limit
}
```

## HLD

**Note that a lot of the HLD and DD is similar to that of the SDI for a chat app**

### L4 Load balancer

- We’ll need an L4 load balancer to support traffic at the TCP level. L4 load balancers,	let’s say using ELB in TCP mode can load balance websockets. When client’s need to	connect to a location server, the L4 load balancer will route them to the location server they	previously connected to or to a location server using the load balancing algorithm.		However, if a location server goes down, the L4 load balancer can route the client to		connect to another location server instead.

- When a client needs to connect to the location server, the request will first go to the L4	load balancer, then to the location server. There will actually be a symmetric websocket	connection between both the client to the L4 load balancer, and between the L4 load	balancer to the location server.

- L4 load balancers can be stateful and use sticky sessions to persist the server the	client previously connected to. The sticky session can be implemented by identifying	the user, usually with cookies or their IP address, and storing the user’s connected	server for handling future requests.

- If clients disconnect from a location server, they can automatically reconnect to the		same location server or another one via the L4 load balancer. Reconnecting to the same	location server may be easier, as the session data in the L4 load balancer doesn’t have to	be updated.

### Location servers

The location servers can be used in the following ways to send location updates to friends. We can either use Redis PubSub, and allow friends of a user to subscribe to topics to receive location updates, OR use a location based search approach via geohash vs PostGIS vs quadtree:

#### Friends of a user will subscribe to Redis PubSub topics and receive location updates

- The client maintains a websocket connection with the Location servers to send		location updates to other clients. The Location servers will store the location updates in the Location updates	table asynchronously, and also forward the updates to the appropriate recipient via	Redis PubSub.

- Also, if any location updates are lost in Redis PubSub, due to let’s say the recipient not	being subscribed, the location updates will still be persisted in the Location updates table, so that the recipient can view the latest updated location of other users when they're back online

- Once the Location servers receive the location updates from the client's friends, the Location servers will likely store a cache of the client's latest updated location, and then compare it against the friend's latest updated locations. If the friend's location is too far away (not within the client's configured radius) from the client's cached location, then the Location server can choose to not return the friend's location to the client.	

#### Location servers using Geohash service vs PostGIS service vs Quadtree service

- In this location based search approach, the Location servers will first store the location updates from users in the Location updates table. During this time, separate services such as a Geohash service vs PostGIS service vs Quadtree service will use this Location updates table, and have their own quadtree / cache that they'll query nearby friends from. These location based services will use the Location updates table to build the quadtree / cache.
- By using these approaches, Redis PubSub is no longer needed. However, this approach might seem be quite slow, mainly for the Geohash and PostGIS approaches, since we'll have to look up all the nearby friends likely within a cache or table.
- The location based search approaches will be disucssed more in the DD.

#### Workflow of sending location updates

The workflow of sending location updates is as follows:

1. The client will establish a websocket connection with an appropriate Location server routed by the L4 load balancer
2. The client will then forward the location updates to the Location server
3. The location server will publish the location update to the client's Redis PubSub channel in the Redis PubSub server. Also, the location server will store the location update in the Location updates table / cache
4. When a Redis PubSub server receives a location update on the client's channel, it will send the location updates to all the current subscribers, which are other Redis PubSub servers. These subscribers will be the client's friends
5. After the friend's Location servers receive the location update from it's Redis PubSub server, it will first check if the client's location update is within the friend's radius, and if so, the location update will be sent to the friend. The Location server of the friend will also store the friend's latest location update to verify if the client's location is within the friend's radius. On average, a user might have about 400 friends, and 10% will likely be nearby friends - thus computing if the friend is within the user's radius is not as compute intensive. The Location server will also only forward the location updates for those 10% nearby friends to the user (via the websocket).

### Geohash service (if using geohash)

- The Geohash service will search for friends within a search radius using a geohash based approach, and return them to the Location service service. The Geohash service will take a geohash of the search radius (using a geohash converter) and find friends within the specified radius by comparing their geohash strings.
- The geohash converter, which could be PostgreSQL's PostGIS geohash conversion functionality shown in 'PostGIS geohash conversion function', will take a long / lat coordinate of either a radius or friend, and then convert it to a geohash string. This geohash string will be compared against the geohash strings in the Location updates table / cache to find nearby friends.
- Because we're using geohash, the Geohash service will compare the prefixes of the search radius' geohash string with the prefixes of the friends' geohash string. If the prefixes are the same, then this means the friend is within the search radius. A query such as the one below can be used to find friends with the same prefix as the search radius' geohash.

```sql
select userID, lat, long, geohash from locationUpdatesTable
where geohash like '${radiusGeohash}'
```

PostGIS geohash conversion function:
```sql
select ST_GeoHash(ST_Point(${long}, ${lat}))
```

- When new friendships are made, we'll also use the Geohash service to generate a geohash string for the new friend, and then store it in the Location updates table.

- Geohash can sometimes be slower than a typical quadtree. It can also be slower than PostGIS's built-in location based search functionalities. This will be discussed more in the DD.

#### Geohash cache

- Because querying the geohash data on disk may be slow, we can store a geohash cache in Redis. Redis provides support for geohashing to encode and index geospatial data, allowing for fast querying. The key advantage of Redis is that it stores data in memory, resulting in high-speed data access and manipulation. Additionally, we can periodically save the in-memory data to the Location updates table using CDC (change data capture).

### Quadtree service (if using quadtree)

- The Quadtree service will recursively build and update the Quadtree table and cache. The Quadtree service will also be used to search the quadtree efficiently by traversing down the tree from the root node to the leaf nodes. The search within a quadtree will be discussed more in the DD.
- A quadtree may be more suitable for this design than a geohashing approach, since there are many high density areas such as NYC, and a quadtree will account for these dense areas by splitting up the quads further.

#### Quadtree table / cache

- Because a quadtree is an in-memory data structure, we can keep both a quadtree table within PostgreSQL as well as a cache using Redis. PostgreSQL provides SP-GiST, which provides functionality for storing and querying a quadtree data structure.
- Although Redis doesn't directly provide quadtree support, we'll use Redis as the quadtree cache since it provides complex data structures such as lists and sorted sets which will be helpful in storing nodes of the quadtree. For example, the leaf node of a quadtree can be a Redis sorted set, where the friends are sorted based on their distances to the leaf node's radius's center point. A leaf node can also contain a Redis list which contains friends from the Location updates table which fall within the leaf node's radius.
- Additionally, a quadtree data structure is not as complex to build, and could be implemented within a memory optimized EC2 instance.

### PostGIS service (if using PostGIS)

- We could also use a PostGIS service which will convert the friend's long / lat values in the Location updates table to a PostGIS GEOMETRY type. We'll then add a new column of this GEOMETRY type (we'll call it the location column) to the Location updates table. This PostGIS service will then be used to query the Location updates table using PostGIS search functions like ST_Intersects (to find if a long / lat value intersects with another point) and ST_DWithin (to find if a long / lat value is within a radius).
- The DD will discuss more on PostGIS and its usage in efficiently searching for friends.


### API servers
  
- The API servers provide endpoints to manage friendships between users, and viewing the latest location updates of friends. The endpoints handled by the API servers will not	require a bidirectional communication.

- The idea is that the client will use the API servers to send friend requests to other clients, and they will use the Location servers to send /	receive location updates from then onwards after a websocket connection is set up.

#### API servers for viewing all latest updated locations from friends

- The API servers can also be used to view all the latest updated locations from friends via cursor based pagination. Since the endpoint corresponding to this request will frequently be called, we can add a GSI on DynamoDB on the Location updates table, where the partition key can likely be a regionID corresponding to the userID, and the sort key can be the updatedAt field. We'll use regionID here instead of userID, since it makes sense that userIDs in a similar region will be in the same shard, and thus will make querying faster since we'll only have to fetch from a few shards when querying for userIDs within the same regionID.

- When the client requests to view all the latest updated locations from friends, the API servers could first check the Location updates cache, and if the friend's entry is not there, then the server could get it from the Location updates table.

### Key value store / cache

- A KV store could store the users, friendships, and location updates data.	A KV store	will be suitable here as the data type is relatively simple and will be		frequently accessed. There will likely be equal number of reads and writes happening	and so a KV store such as DynamoDB will be used here. 
  
- DynamoDB follows a primary-secondary model where it can be used for both read	and write intensive tasks. Also DynamoDB is optimized for low latency reads / writes	via eventual consistency, providing both LSIs and GSIs indexing, and using SSDs - 	which will be beneficial for read latencies

- Also, because the location updates table is write heavy and will likely need to be frequently horizontally scaled, Cassandra is a good option for the location updates entity. Cassandra supports high write workloads, and can be configured to have multiple leaderless replicas - all which could be written to.

#### Cache

- We could also use a cache to store the users, friendships and location updates data using either Memcached or Redis. We could likely store the location updates data with a small TTL value since it is frequently updated.

- If the Redis / Memcached instance goes down, we could replace it with an empty new instance and let the cache be filled as new location updates stream in.

**Note that because we set a TTL on each entry in the Location updates cache, if a friend is inactive then their location will not be in the location cache.**

### Sending location updates from one Location server to another Location server

Because we'll have friends of users connected to different Location servers, to delivery location updates from one Location server to another Location server, we can do the	below and in ‘Sending location update between Location servers’:
- Keep a kafka topic per user:
  - This approach mainly won’t work because Kafka is not built for billions of			topics, and it will carry too much overhead for each topic, which may be			50 KB in size. This will result in terabytes of data to maintain for the Kafka			topics.

  - Kafka is not optimal for short lived “micro topics” which are needed for this app, where there can be numerous topics for friends, and			subscribers	 can subscribe or unsubscribe at any point. 

  - Redis PubSub is a lightweight solution which may be more appropriate	for location update delivery between Location servers, since only currently			subscribed subscribers will receive any updates sent to the topic.

- Consistent hashing of Location servers:
  - By using a separate service discovery service using ZooKeeper to keep			track of which clients should connect to which Location servers, there will still			be an overhead of maintaining those mappings during both disconnections			and scaling events. Clients may frequently disconnect then reconnect to			different Location servers, and all of this will need to be maintained and				updated in service discovery, which will be complex to handle. Additionally,			during scaling events in consistent hashing, Location servers will handle a 			different set of clients in the hash ring - thus the mappings in ZooKeeper			will need to be updated frequently during scaling of Location servers.

- Offload to Redis PubSub:
  - Redis PubSub can maintain a lightweight hashmap of websocket 				connections. With Redis PubSub, a subscription can be created for an			userID, and location updates can be published to that subscription which will be			received at-most-once by the subscribers.

  - Receiving location updates from other clients:
    - When recipient clients connect to the Location server, the Location server will			subscribe to the sender userID’s topic via Redis PubSub. Any			location updates published to that sender userID’s topic will be				forwarded to the recipient client by the recipient’s Location server (since the			Location servers are currently subscribed). 

  - Sending location updates to other clients:
    - The Location server of the sender userID will publish the location updates to			their topic. Any currently subscribed recipient Location servers will receive that			location update published in that topic. The recipient Location servers can then				deliver the location updates to the appropriate recipient userIDs.

Redis PubSub:

<img width="608" alt="image" src="https://github.com/user-attachments/assets/5c75ec17-70ee-408d-8bd3-1ec0b5f2a898" />


- Message queues for 1-1 friendship location updates:
  - We could also place message queues between Location servers only for 1-1 friendship location updates		as there is one producer and consumer only. The mapping between the Location 		servers to the message queues will be maintained in the Location servers				themselves (as they’re stateful) or maintained in service discovery. However, 		maintaining the client to server mappings in service discovery will be an			overhead, as clients will frequently disconnect and reconnect to different Location		servers.

#### Redis PubSub

- The topic represents the sender userID, whenever the userID is sending their location updates to their friends

- Redis PubSub is lightweight and is at-most-once, which means that it			doesn’t guarantee message delivery. If there’s no subscribers listening,			then the message will be lost, and stored in the Location updates				table. 

- Redis PubSub is appropriate for this design because it sends messages	only when there are currently subscribed Location servers, and if there are no	subscribed Location servers, then the message is not received. This is a mock	of how a chat app operates as well.

- One issue with this approach is that there could be an all-to-all relationship		between Location servers and Redis cluster servers, where we’ll need		connections for all those relationships. However, Redis PubSub is much more	lightweight than Kafka, and will not take up as much bandwidth. We'll talk about scaling the Redis PubSub servers in the DD to prevent this all-to-all relationships by routing userIDs of the same regionID to the same PubSub server.

#### Redis cluster

- Topics will also be distributed across nodes within a Redis cluster.

- Also, the Redis clusters could also be replicated - when one cluster is down, another replica can still receive from / send to subscribed Location servers. There may be overhead in replication of Redis clusters, however Redis PubSub is more lightweight than most queue solutions (due to it’s at-most-once delivery) such as Kafka and SQS, thus it will be less complex in replicating it since there’s less persisted data to replicate.

<img width="850" alt="image" src="https://github.com/user-attachments/assets/42704a67-60b8-44a9-825a-a4749e6dd26c" />

## DD

We’ll dive deep into some parts of the system:

### Online presence

- Via the websocket connection to the clients, the Location servers will also update the KV store with the updatedAt timestamp, which will also represent the last time the user was online.

- Using Redis PubSub, friends of users who are subscribed to their friend's topics could also receive location updates on the friend's presence when they go offline or come back online (when they logout / login). Presence could also be fetched only for the userIDs within the viewport via lazy loading.

### Database sharding

We can shard the database tables in the following ways:

#### Partitioning Users table based on userID

- Because the Users table contains the userID, we could likely partition it using either userID or regionID, since it makes sense for nearby userIDs to also be friends and reside in the same regionID. Therefore, we'll only fetch from a few shards when we're querying for specific users.

#### Partitioning Friendships / Location updates table based on "regionID"

- We could likely partition these tables using the regionID, since it makes sense for nearby userIDs to also be friends and reside in the same regionID. Therefore, we'll only fetch from a few shards when we're querying for specific friendships and location updates.

**As a side note, at the scale we are designing for, the user and friendship datasets will likely be managed by a dedicated team and be available via an internal API. In this scenario, the WebSocket servers will use the internal API instead of querying the database directly to fetch user and friendship-related data. Whether accessing via API or direct database queries, it does not make much difference in terms of functionality or performance.**

### Efficiently storing the location data for fast searches

Efficiently storing location data for fast searches can be done using multiple approaches. The resource notes in 'Location based search' goes over all of the main approaches. However, in this DD, we'll use either geohash, quadtree or PostGIS.

#### Geohash service

- Refer to the "Geohash" section in the resource note 'Location based search' for the background on geohash.

<br/>

- Geohash works by converting the long / lat to a string of letters and digits. We first divide the map into 4 grids recursively until the grid size is small enough such that it can contain a relatively small number of friends. As the map gets recursively divided, we'll assign a generated Base-32 geohash string to the grid. Geohash also operates with a fixed precision, where the smallest grids cannot be further divided, and all the smallest grids will have the same size. However, custom dynamic behavior can be added to a geohashing approach, but adding dynamic behavior may be more complex to do.
- Since geohashes represent hierarchical spatial data, shorter geohash strings cover larger areas, and longer geohash strings cover smaller areas with more precision. Therefore, if we keep removing the last character from a geohash string, the new geohash string will be for a larger area. To make geohash filtering more efficient, we can index the geohash column (like in 'Index on geohash') so that queries with the LIKE or WHERE operators will optimize it's prefix based searches.
- An example of using LIKE with a geohash string is given below:

Index on geohash:
```sql
CREATE INDEX idx_geohash ON locationUpdatesTable USING geohash
```

Using LIKE to filter geohash strings:
```sql
select userID, lat, long, geohash from locationUpdatesTable
where geohash like '${radiusGeohash}'
```

Also, let's say we're searching for locations within the geohash radius of "dpz83" - then the query above should return the following:
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

- Geohash works well for majority of the cases, but boundary issues may come up when one friend covers 2 geohash strings. Additionally, in some cases, there could be friends within the border of 2 geohash strings, and so that friend doesn't belong to any geohash string. In these cases, the geohash generation algorithm can be modified to account for such edge cases.
- Also, another issue may be when too few friends appear in the search result. In this case, we can increase the search radius by removing the last digit of the geohash string, and we can continue to increase the radius by removing another digit from the end.

##### Geohash sharding / partitioning

- If we have a table containing the userID and geohash strings, we can easily shard the database and partition the tables based on prefixes of the geohash strings. We'll shard by the prefixes of the geohash strings because friends which are within the same geohash search radius will also be within the same shard. This will make searches faster, since we'll have to look through fewer shards or entries of the table.

#### Quadtree service

- Refer to the "Quadtree" section in the resource note 'Location based search' for the background on quadtrees.

<br/>

- A quadtree also recursively divides the map into 4 grids until the contents of the grids meet a certain criteria, like not having more than 100 friends. A quadtree is an in-memory data structure that helps with location based searching.
- The data on a leaf node (leaf node represents the most granular grid) in a quadtree can contain long / lat and a list of userIDs in the grid. The data on a parent node (parent node represents the parent grid of leaf nodes) contains the parent grid's long / lat values and pointers to the 4 child nodes.
- Assuming a leaf node has at most 100 friends, then to build a quad tree for N friends:
  - It will take (N * 100) * log(N / 100) time complexity, since we're parsing through (N / 100) leaf nodes which contains at max 100 friends each, and we'll also be parsing the height of the tree which will be log(N / 100), where N / 100 is the number of leaf nodes.

- Below is an example of a quadtree quad:
<img width="750" alt="image" src="https://github.com/user-attachments/assets/23144928-0519-46eb-8b49-4dd0cd8c45b5" />

<br/>

- To search in a quadtree, we'll start from the root node and traverse down the tree until we find a node within the search radius. If we find a node within the search radius, we'll traverse the node's child nodes and siblings to see if they're also in the search radius. We'll keep a list of friends in the leaf nodes which are within the search radius, and then return the list of friends. The downside to a quadtree is that searches can be a bit complex to implement.
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
friends: [ { userID, userName, location, long / lat, updatedAt } ],
nodeQuad: { maxLong, maxLat, minLong, minLat },
leafNode: TRUE / FALSE,
childNodePtrs: { childNode_1, childNode_2, childNode_3, childNode_4 }
}
```
- In this entry, the nodeID can represent the node of the quadtree. If a node is a leaf node, we'll set the leafNode to TRUE. Also, if it is a leaf node, then there will be friends populated within this node. The nodeQuad field will also be the quad's max /  min long / lat values.
- When searching for friends within a search radius, we'll first check if the nodeQuad's long / lat values are intersecting with the search radius. If the quad is intersecting, then we'll traverse down the tree to find the leaf nodes. In the leaf nodes, we'll search for userIDs which have long / lat values within the search radius.

##### Building a quadtree

- We will start with one node that will represent the whole world in one quad. Since it will have more than 100 friends, which may be our criteria, we will break it down into four nodes and distribute locations among them. We will keep repeating this process with each child node until there are no nodes left with more than 100 friends.

##### Dynamic quads

- We can use dynamic quads in our quadtree where if the number of friends exceed a threshold in a quad, we'll further split the quad into 4 more quads. In the quadtree, nodes will contain the userIDs and additional user and location info.

##### Searching in a quadtree

- In the quad tree, child nodes will be connected to sibling nodes with a DLL. Using the DLL, we can move left / right / up / down to sibling or child quads to find friends. An alternative to a DLL is to use parent pointers from the child nodes to the parent node.

- When searching in the quadtree, we start searching from the root node and visit child nodes which are in the search radius. If a child node is in the search radius, we can traverse through it’s own child nodes and sibling nodes using the DLL and return them if they are also in the search radius.

- If we don't have enough friends to return after searching a specific node, we can search the node's siblings and also it's parent node to retrieve surrounding friends as well.

##### Adding / updating / removing an entry (friend) in a quadtree

- To add / update a friend in the quad tree, we can search the nodes for the userID and add / update the friend in the node, and also update any neighboring siblings if needed. If after adding the friend, the leaf node reaches the threshold on the number of friends a node can have, we'll need to split this leaf node further into 4 leaf nodes and allocate these 4 leaf nodes with the friends from the original leaf node.
- To remove a friend in the quad tree, we can search the nodes for the userID and remove the friend from the node, and update the neighboring nodes accordingly

##### Quadtree sharding / partitioning

- We can shard the quadtree based on regions on the basis of zip or postal codes, such that all the friends and nodes that belong to a specific region are stored in a single shard. A region in this case will be a branch within a quadtree - therefore, a shard could contain a separate part of a single quadtree (the branch). Some regions could also be combined into a single shard to prevent uneven distributions.
- We can do this since the user’s queries will be based on the location, so sharding this way will cause less inter-shard communication and speed up queries.
- However, this approach will result in slow responses when numerous queries are on the server for a single shard possibly during a tourist season. To prevent hotspots, we can apply replication to the quadtree, as the data is not at all large or updates frequently, making replication very easy to do.
- There could also likely be a mapping maintained within ZooKeeper that keeps track of the mapping between regionID : shardID. regionID or shardID will rarely change (it may change only when a new region or shard is updated), thus this mapping will rarely change.

##### Quadtree replication

- We can replicate both the quadtree table and cache on multiple servers to ensure high availability. This also allows us to distribute the read traffic and decrease the response times.
- Quadtrees should take up relatively little storage, and thus can be backed up easily. In case we may lose the quadtree data, we can use checkpointings at set intervals to backup the data.

##### Fault tolerance of quadtree

- Because the quadtree will likely have both a table and cache, it will be highly available. However, if a single cache server dies, we won't have a way of knowing which quadtree branch or nodes the cache server stored.
- To ensure we know which cache server stores which quadtree branch / nodes, we can store a reverse mapping of cacheServerID: [ quadtreeBranch, nodeIDs ] in a configuration service such as ZooKeeper, or within the Quadtree table itself. This way, if the cacheServerID died, we can rebuild the quadtree branch / nodes using this reverse mapping.

#### PostGIS service

- Refer to the "PostGIS" section in the resource note 'Location based search' for the background on PostGIS.

<br/>

- While PostGIS provide's geohash functionality, PostGIS doesn't necessarily use geohash strings for a lot of it's location based searching operations. PostGIS uses it's built-in geometries which can be created using a location's long / lat value. These geometries are then used to perform spatial operations.

- PostgreSQL's PostGIS extension can significantly optimize geospatial queries. Instead of using geohash strings, PostGIS uses built-in geometries (it's GEOMETRY type, and additional types to represent points, polygons, radius, etc) to perform location based searches which will be more accurate than approximations performed using a geohash. We can first convert a location's long / lat into PostGIS-compatible geometries and use PostGIS functions to efficiently perform spatial operations. This provides faster and more efficient results than just using a LIKE query on the geohash strings in 'Using LIKE to filter geohash strings' (in resource notes), or using a 2D search using long / lat in '2D search using long / lat' (in resource notes).

- PostGIS performs true geospatial calculations on the sphere using it's own built-in algorithms, avoiding errors from geohash approximations. It also provides radius-based queries for precision when we need locations within a specific search radius. For faster searches, we can also index on the location column which is of the GEOMETRY type, where GEOMETRY specifies a specific point using long / lat values.

We can store geometries by using PostGIS, and then query using PostGIS spatial functions using the below steps:

##### 1. Store geometries in table:
  
- We can first convert the geohash into a PostGIS GEOMETRY or bounding box and store it in a GEOMETRY column in a specific table
- For example, we'll first add a location column of type GEOMETRY to the Location updates table as shown below. In here, POINT is a PostGIS type which represents the long / lat, and SRID 4326 specifies the WGS84 coordinates format.

```sql
alter table locationUpdatesTable
add column location GEOMETRY(POINT, 4326)
```

- To populate the location column using a specific long / lat value, we can do the following. ST_MakePoint will return a POINT type using the long / lat values we provide.

```sql
update locationUpdatesTable
set location = ST_SetSRID(ST_MakePoint(long, lat), 4326)
```  

##### 2. We can then query using PostGIS spatial functions:

**If we want to find locations using a specific point, we can do the following:**

- For example, we can use the ST_Intersects function to check if a friend's location (location is PostGIS's GEOMETRY type) intersects with a specific polygon as shown below. For example, we'll input the polygon's max / min long / lat values into the ST_MakeEnvelope function which will create a rectangular polygon. Other polygon based functions are also available in PostGIS. We'll then use the ST_Intersects function, and input the friend's location field (which will be of a PostGIS GEOMETRY type) and also input this polygon.

```sql
select * from locationUpdatesTable
where ST_Intersects(location, ST_MakeEnvelope(${minLong}, ${minLat}, ${maxLong}, ${maxLat}, 4326)
```

**If we want to find locations within a specific search radius, we can do the following:**

- We can also use the ST_DWithin PostGIS function to find friends within a specific search radius as shown below. We'll use ST_MakePoint to create a point using a long / lat value of the center of the search radius. In here, the centerLong and centerLat values will be center's long / lat values. The radiusInMeters value will be the actual search radius in meters. ST_DWithin will check if the friend's location is within the specified radius's center point.

```sql
select * from locationUpdatesTable
where ST_DWithin(location, ST_SetSRID(ST_MakePoint(${centerLong, ${centerLat}}), 4326), ${radiusInMeters})
```

### Scaling the system

We can scale the different system components as follows:

#### Location servers

- Location servers are stateful, so care must be taken when removing existing nodes or scaling nodes. Before a node can be removed, all existing connections should be allowed to drain. To achieve that, we can mark a node as “draining” at the L4 load balancer so that no new Location connections will be routed to the draining server. Once all the existing connections are closed (or after a reasonably long wait), the server is then removed.

- Releasing a new version of the application software on a Location server requires the same level of care.

#### Location updates cache

- With around 100M DAU, and each location update entry taking up roughly 100 bytes, 100M * 100 bytes = 10 GB (for total users: 1B total users * 100 bytes = 100 GB), a single Redis server can handle this easily. However, the storage is not the issue - throughput is. There will be 100M users pinging the Location updates cache every 30 seconds, which is about 3.3M requests per second. Therefore, we can shard the Location updates cache servers based on the regionID, where nearby friends will likely request the same server - reducing network request time since servers will likely also be closer to users. Because there are also dense regions, we could further split the shards corresponding to these dense regionIDs OR we could apply replication on these shards explicitly.

- It does not make sense to shard by userID, since a single userID who is requesting for their friends' location updates will need to request multiple shards, where different friends could be in different shards. This will further increase the latency, and cause more network requests to be made instead of only requesting a few shards if we shard by regionID.

#### Redis PubSub servers

- A new channel is created when someone subscribes to it. If a message is published to a channel that has no subscribers, the message is dropped, placing very little load on the server. When a channel is created, Redis uses a small amount of memory to maintain a hash table and a linked list to track the subscribers. If there is no update on a channel when a user is offline, no CPU cycles are used after a channel is created. We take advantage of this in our design in the following ways:
  - Assign a unique channel to every user who uses the "nearby friends" feature:
    - When a user opens the app, they would subscribe to each of their friend's channel, whether the friend is online or not. This will actually simplify the backend since the Location servers don't need to check if the friend is online or not, or handling unsubscribing when the friend is not online, or subscribing when the friend is online. Subscribing / unsubscribing when the friend's online state changes will actually complicate the backend.
    - Because we'll subscribe the user's Location server to all of their friend's channels, regardless if the friend is online / offline, it will use up more memory. But, memory is not a major issue because we'll store 10 GB of the location updates in the Location updates cache, and likewise similar data in the Redis PubSub servers (since Redis PubSub will also store 100M DAU channels with around 100 bytes or so).

##### Distributing channels to multiple Redis PubSub servers

- Users' channels will be independent from each other, thus we can easily spread the channels among multiple Redis PubSub servers, by using the userID's regionID. Therefore, userIDs within the same regionID will likely have channels within the same Redis PubSub server. This greately reduces the amount of requests which needs to be made between PubSub servers. Since if two userIDs are in the same regionID, they'll likely be nearby friends, and send / receive messages from the same PubSub server. Therefore, nearby friends will be contained within a single PubSub server.

- However, if we instead spread the users' channels by userID, we'll have a lot more PubSub servers communicating with one another since userIDs will be spread out across multiple PubSub servers, which will further increase the latency.

##### Service discovery to manage connection mappings between Redis PubSub servers

- We can also include a service discovery component to manage the mappings between Redis PubSub servers, such that a single PubSub server will know which other PubSub servers to forward the location updates to. We can use ZooKeeper for this, which will provide the following features:
  - ZooKeeper will allow us to keep a list of servers in the service discovery component, and an API to update it. Fundamentally, ZooKeeper has a KV store for holding the PubSub server connection mappings. A single mapping entry could look as follows:

```bash
{
  pubsubServer1: [ pubsubServer2, pubsubServer3 ]
}
```
  - A single Redis PubSub server will only need to connect to other PubSub servers if there is a friendship relation between users for those two servers. Thus, if there is a friendship relationship created between two users, where the two users are on different PubSub servers, then the connection mappings for those two PubSub servers will be updated. This is still fine because it's more likely for friends to be within the same regionID, and connected to the same PubSub server, as opposed to friends being in different regionIDs.
  
  - When a location update comes into a user's channel in a Redis PubSub server, that PubSub server will likely already be connected to the other PubSub servers in it's mapping list in ZooKeeper. This way, the PubSub server can forward the location update to the other PubSub servers it's already connected to.

#### Scaling Redis PubSub servers

- Scaling the PubSub servers up and down depending on the traffic patterns requires a few steps. We'll first have to understand a few properties of the Redis PubSub servers:
  - The messages send on a channel are not persisted in memory or disk. Once a message is sent, if there are no subscribers, then the message will be dropped. 
  - The PubSub server is more or less stateless, however there are still some states such as the channel info and subscriber list for each channel, which is being stored. The actual inter-PubSub server connection mappings are stored in ZooKeeper.

- If a channel is moved from one PubSub server to another, which could happen if a userID changes their regionID, or if a server goes down, or a new server comes up - then every subscriber to the moved channel must know about that move, and the connection mappings should also update. The subscribed PubSub servers should first unsubscribe from the old PubSub server of the moved channel, and resubscribe to the new PubSub server of the moved channel. However, these moving channels will occur less likely, and only when the userIDs change their regionIDs, or when PubSub servers are added / removed. With appropriate monitoring and scaling, the overhead in the moving of channels can be reduced.

### Adding / removing friends

- When a user adds / removes a friend, the user's Location server will subscribe / unsubscribe from the friend's PubSub server. Note that the Location server will only unsubscribe if there are no friends in the PubSub server - by friends, we're refering to the friends of all the connected users of the Location server. A Location server itself is stateful, and thus will also store it's connection mappings for the websocket connections and subscribed PubSub servers.

- The same subscribe / unsubscribe feature for Location servers could also be used if users have opted in / out of sending / receiving location updates.

### Handling users with many friends

- Even if the user has about 5000 friends or so (like the friends limit in FB), it's unlikely to cause hotspots within the PubSub servers. However, if a user has millions of friends, then it might cause some hotspots within the PubSub servers.

- For these celebrity users, instead of sending periodic location updates to millions of their friends, we could instead only store their location updates in the Location updates cache - and then have their friends retrieve the celebrity's location updates from the cache. Likewise, since the celebrity will also have millions of friends, they could also retrieve their friends' location updates from the cache. This concept is very similar to the SDI 'News feed system'.

### Showing nearby random uers

What if the interviewer wants to update the design to show random people who opted-in to location-sharing?

- We can design this feature by adding Redis PubSub channels corresponding to different geohash strings of different regions as shown in 'PubSub channels corresponding to different geohash strings of different regions':

PubSub channels corresponding to different geohash strings of different regions:

<img width="900" alt="image" src="https://github.com/user-attachments/assets/e1ce391f-c4a9-49ba-aab5-97735fed393e" />


- If a user is within a geohash radius, they could send location updates to the geohash's PubSub channel, and subscribed users could receive the location updates.

- To handle people who are close to the border of a geohash grid, every client could subscribe to the geohash the user is in and the eight surrounding geohash grids. An example with all nine geohash grids highlighted is shown below:

<img width="500" alt="image" src="https://github.com/user-attachments/assets/2f36ec93-8bc2-4fb9-aee7-75ce5923a3f2" />

### Database replication
  
- Additionally, we can replicate the database tables / shards to prevent a SPOF


## Wrap up

- Erlang is an alternative to Redis Pub/Sub
- Other geolocation algorithms and methods could be used like Google S2
