# Airbnb

**Note that this design is similar to the SDI 'Ticketmaster - general events', 'Hotel reservation system', and 'Yelp - business proximity'**

## Requirements

### Questions

- Airbnb has two sides: a host-facing side and a renter-facing side. Are we designing both of these sides or just one of them?
  - Let’s design both sides

- The system should allow hosts to perform CRUD operations on their listings, and allow renters to browse listings, book them, and manage their bookings. Is this correct?
  - Yes, this is correct for hosts - but for renters, let’s only focus on browsing and booking them. Let’s ignore	what happens after booking, such as payments - and treat it as a separate service.

- When multiple users concurrently browse listings, the listings shouldn’t get “reserved” for them. However, if a user starts the booking process, the listing should get temporarily “reserved” for that user, let’s say for 5 mins. Is this correct?
  - Yes, if a user starts the booking process for a listing for a specific date range. Then it should be reflected	as “reserved” for that date range if other users try to book it.

- If two users are looking at the same listing for conflicting date ranges, and if one of the users starts the booking process, we should immediately “reserve” the listing for that user for lets say 5 mins. Is this correct?
  - Yes, for simplicity, let’s assume this

- Users can browse listings based on fields like location, date range, pricing, property type, bedrooms, etc, and then book a listing. Hosts can perform CRUD operations on listings. Is this correct?
  - Yes, but let’s only focus on browsing by location and date range, not pricing, property type, bedrooms, etc.

- Do we want to design any additional features like contacting hosts, authentication, payment services, etc?
  - Let’s just focus on browsing and booking, and ignore the rest

- Are we supporting multiple regions? How many listings and renters can we expect?
  - Let’s only consider designing for a single country / region
  - There will be 50M users, there will be 1M listings

### Functional

- Users can browse listings with low latency and book them:
  - Users can browse using location and date range
  - When users start the booking process, the listing is “reserved”
- Hosts can perform CRUD on their listings

<br/>

- Single country / region
- 50M users, 1M listings

### Non-functional

- High throughput / concurrency:
  - There could be multiple booking requests for the same listing, but only the first one will be considered.
  - There could also be high throughput / concurrency during holidays
  - The system will also be read heavy, as more users will view listings than book them
- Consistent:
  - Users should see a consistent view of available listings

- Low latency:
  - Search results should be returned with low latency (10 - 500 ms)
- Efficiently returning location based search results

## Airbnb 101

We’ll have 2 parts of Airbnb as follows:

- Host side can perform CRUD on listings
- Renter side can browse listings, get a single listing and book listings:
  - When listings are “reserved” for a specific date range, they will not be browsable if users try to view them
		
  - We’ll divide the renter side as follows:
    - Browsing listings
    - Getting a single listing
    - Booking a listing

## Data model / entities

Majority of the entities are mainly read heavy, as opposed to being write heavy. This is because fewer users make bookings as opposed to searching for listings. A SQL database works well here, as it provides more optimized ACID properties which will support consistency between listing availability and reservations, and help in preventing double bookings or double charging.

<br/>

- Listings:
	- listingID
	- hostID
	- location / long / lat / geohash (if the system is using geohash) / location (if the system is using PostGIS, then location will be of PostGIS's GEOMETRY type)
	- title, description
	- listingImageS3URL

- Listings availability:
  - This entity contains the availability of the listings for all dates. A single entry includes info about the listing for the date, and whenever new listings are added to the Listings entity, there will also be new records, likely for the next 1-2 years, in this Listings availability entity
  - During the booking process, an entry here will first be AVAILABLE, then RESERVED (if the listing is in the booking process and is using an expirationTime and non-locking approach discussed in DD), and then BOOKED once the user completes the booking process and pays
  - The composite key will be { listingID, date }

    - listingID
    - date
    - listingStatus: AVAILABLE / RESERVED (if using an expirationTime and non-locking approach discussed in DD) / BOOKED

- Reservations:
  - This entity will store info on the reservations booked by a user. The reservationStatus will be used to represent PENDING vs BOOKED reservations

	- reservationID
  	- listingID
	- userID
	- startDate, endDate
	- price
  	- reservationStatus: PENDING / BOOKED / CANCELED

## API design

- Note that we’ll use userID if the user is authenticated and will be booking listings. The userID could be placed in a session token or JWT in the Authentication header as such:
  - Authentication: Bearer

- The below caching header could also be applied to fetch frequently accessed entries quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
  - Cache-Control: no-cache max-age Private/Public

<br/>

Renters side:

### Search listings

- This endpoint allows users to search for listings via a search query, location, start / end date, and cursor based pagination. Additionally, we can incorporate lazy loading on the viewport and only retrieve the listings on the viewport

- If we want to get search results based on the location, this request can be routed to a Geohash vs PostGIS vs Quadtree service, which will return the listings within a specific radius.
- Also, if we want to get search results based on availability times (from the startDate and endDate parameters), then we could set the nextCursor value to the viewport's oldest availability time using the date field from the Listings availability table - this way, we could retrieve the paginated results based on the available time of the listingIDs.

<br/>

Request:
```bash
GET /listings?query={ text search or location based search }&startDate&endDate&nextCursor={ 
viewport's oldest availability time using the date field from the Listings availability table }&limit
```

Response:
```bash
{
  listings: [ { listingID, location, title } ],
  nextCursor, limit
}
```

### Get listing
  
- This endpoint will use the listingID and fetch the listing from the Listings table.

Request:
```bash
GET /listings/:listingID
```

Response:
```bash
{
  listingID, location, title, description, listingImageS3URL
}
```

### Book listing

- Usually the booking process is a 2 step process, where the user will first reserve a listing in the first step, then in the second step they’ll input their payment details into the provided payment URL within the time limit. Thus we have 2 individual endpoints for these steps below.

#### Reserving a listing

Request:
```bash
POST /listings/:listingID/reservations
{
  startDate, endDate
}
```

Response:
```bash
{
  paymentInputURL
}
```

#### Paying for reservation

Request:
```bash
POST /<paymentInputURL>
```

Response:
```bash
{
  reservationID, reservationStatus
}
```

<br/>

Host side:

- createListing(hostID, location, title, description, listingImageURL)
- updateListing(listingID, hostID, location, title, description, listingImageURL)
- deleteListing(listingID)

## HLD

### API gateway

- The API gateway will provide rate limiting, authentication, and route requests to the specific services. For example, for a reservation request, the API gateway could get the listing details from the Listings service, then make a reservation using the Reservation service

### Microservice architecture

- A microservice architecture is suitable for this system, as the system requires independent services such as the Listings, Reservation, and Listings management where each service has it’s own resource requirements and can be scaled and managed separately.

- Microservices can benefit from a gRPC communication as there will be multiple channels of requests being sent / received in inter-service communication between microservices. Thus, gRPC could be the communication style between microservices, as it supports a higher throughput, and is able to handle multiple channels of requests as opposed to REST, which uses HTTP, that is not optimized for multi-channel communication between services.

### Listings service

- The Listings service provides detailed information on listings, and could possibly handle additional operations such as rating a listing

**Note that 1M listings is not large, and could be directly queried from an in-memory cache without using a location based search service, however since latency is still a top priority, a separate location based search service might help but makes the design more complex**

#### Listings service using Geohash service vs PostGIS service vs Quadtree service (if location based search is in scope)

- The Listings service will also use either the Geohash service or the PostGIS service or the Quadtree service to efficiently search listings using geohash strings, PostGIS, or a quadtree respectively, and return the paginated results of the listings within a search radius. The specifics of the approaches, and additional approaches which can be used are discussed in the DD.

### Database / cache

- The database will store the listings, listings availability and reservations data. As the listings availability and reservations data requires consistency, more complex date range queries, and may require transactions or locking, a SQL database such as PostgreSQL may be preferred over NoSQL, which is more optimized for maintaining consistency. Additionally, the listings availability and reservation data will need to be consistent to prevent double bookings and double charging, so SQL is preferred.

#### Sharding may not be necessary

- If the reservation data grows too large for a single database, older reservations could be moved to a cold storage in S3, as they will not be frequently accessed. Additionally the SQL database / tables could be sharded by a "regionID", since it makes sense for reads to access entries within the same regionID and listingID - this way, there's fewer shards which need to be communicated with.
- However, if we have 1M listings, then:
  - 1M * 1 KB = 1 GB is the storage needed for all listings
  - 365 days * 10 years * 1 GB = 3650 GB = 3.650 TB space needed for Listings availability and Reservations table
  - It's very unlikely that we need sharding for these tables, however even sharding might still not be super helpful for the Listings availability and Reservations tables, which are much larger.
 
#### Cache

- We could maintain a cache, however storing the Listings availability table in the cache would be difficult since the listing availability data could change frequently, and not be consistent with the database - the DD talks more about data inconsistency between the cache and the database.

- However, we could still cache the listings data which don't change frequently or have concurrency issues behind them. We could use either Redis or Memcached for this. Redis sorted sets will likely be helpful in caching the listing's availability for the next few weeks or so in the cache with a TTL.

### Reservation service

- The Reservation service will handle requests for the booking process. It will communicate with the database and a separate		payment service. Once a payment is confirmed, the Reservation service will update the listingStatus in the Listings availability table to BOOKED.

- When a user sends a request to book a listing, the Listing service will likely first check the availability of the listingID, and	then allocate a lock for the listingID and add a new entry to the Reservations table (setting the reservationStatus to PENDING). If the	booking is completed, the listingID will change it’s status to BOOKED and the reservationStatus will change to BOOKED		within a single transaction. If the transaction failed, the whole transaction will be rolled back


### Listings management service

- The Listings management service provides API endpoints which are only available to the hosts for managing their listings.

- When hosts modify their listings, it will first be performed on the SQL database and the changes will be			asynchronously replicated using CDC to the geohash cache, quadtree cache or whichever location based storage is being used.

<br/>

If location based search is in scope:

### Geohash service (if using geohash)

- The Geohash service will search for listings within a search radius using a geohash based approach, and return them to the Listing service. The Geohash service will take a geohash of the search radius (using a geohash converter) and find listings within the specified radius by comparing their geohash strings.
- The geohash converter, which could be PostgreSQL's PostGIS geohash conversion functionality shown in 'PostGIS geohash conversion function', will take a long / lat coordinate of either a radius or listing, and then convert it to a geohash string. This geohash string will be compared against the geohash strings in the Listings table / cache to find relevant listings.
- Because we're using geohash, the Geohash service will compare the prefixes of the search radius' geohash string with the prefixes of the listing's geohash string. If the prefixes are the same, then this means the listing is within the search radius. A query such as the one below can be used to find listings with the same prefix as the search radius' geohash.

```sql
select listingID, lat, long, geohash from listingsTable
where geohash like '${radiusGeohash}'
```

PostGIS geohash conversion function:
```sql
select ST_GeoHash(ST_Point(${long}, ${lat}))
```

- When new listings are added, we'll also use the Geohash service to generate a geohash string for the new listing, and then store it in the Listings table.

- Geohash can sometimes be slower than a typical quadtree. It can also be slower than PostGIS's built-in location based search functionalities.

#### Geohash cache

- Because the querying the geohash data on disk may be slow, we can store a geohash cache in Redis. Redis provides support for geohashing to encode and index geospatial data, allowing for fast querying. The key advantage of Redis is that it stores data in memory, resulting in high-speed data access and manipulation. Additionally, we can periodically save the in-memory data to the listings table using CDC (change data capture).

### Quadtree service (if using quadtree)

- The Quadtree service will recursively build and update the Quadtree table and cache. The Quadtree service will also be used to search the quadtree efficiently by traversing down the tree from the root node to the leaf nodes.
- A quadtree may be more suitable for this design than a geohashing approach, since there are many high density areas such as NYC, and a quadtree will account for these dense areas by splitting up the quads further.

#### Quadtree table / cache

- Because a quadtree is an in-memory data structure, we can keep both a quadtree table within PostgreSQL as well as a cache using Redis. PostgreSQL provides SP-GiST, which provides functionality for storing and querying a quadtree data structure.
- Although Redis doesn't directly provide quadtree support, we'll use Redis as the quadtree cache since it provides complex data structures such as lists and sorted sets which will be helpful in storing nodes of the quadtree. For example, the leaf node of a quadtree can be a Redis sorted set, where the listings are sorted based on their distances to the leaf node's radius's center point. A leaf node can also contain a Redis list which contains listings from the Listings table which fall within the leaf node's radius.
- Additionally, a quadtree data structure is not as complex to build, and could be implemented within a memory optimized EC2 instance.

### PostGIS service (if using PostGIS)

- We could also use a PostGIS service which will convert the listing's long / lat values in the Listings table to a PostGIS GEOMETRY type. We'll then add a new column of this GEOMETRY type (we'll call it the location column) to the Listings table. This PostGIS service will then be used to query the Listings table using PostGIS search functions like ST_Intersects (to find if a long / lat value intersects with another point) and ST_DWithin (to find if a long / lat value is within a radius).

<br/>

### Search service

- The Search service will connect to the database and handle any search queries (in the API endpoint for searching listings). The Search service will likely use an inverted index mapping on text based fields, and perform efficient searching using the mappings. Thus, it could use a tool such as Apache Lucene or Elasticsearch which can maintain an inverted index mapping for a data store.

<img width="800" alt="image" src="https://github.com/user-attachments/assets/5c1e5c9b-abdb-4cec-ab31-235360a7b63f" />


## DD

### Improving booking process
  
- Temporarily setting the listingStatus as RESERVED (or setting ticketStatus to RESERVED temporarily during the booking process as in the SDI 'Ticketmaster - general events') in the Listings availability table and starting a timer once a user initiates their booking process is a common approach	in multiple booking / ordering / payment processing apps. This approach is used because no user wants to enter their payment	info, then find out later that a listing has already been booked. Thus we have a timer and temporarily “reserve” their listing.

- To design for this 5 min timer and temporarily reserve the listingID, we can try out the below solutions	and in ‘Temporarily reserving listings / ticket solutions’ (these approaches are taken from the SDI 'Ticketmaster - general events'):
  - Pessimistic locking:
    - Pessimistic locking is usually not a good approach as it can cause deadlocks if there’s high concurrency. Also the			locked rows within the “SELECT FOR UPDATE” or data locking mechanism will prevent other processes from				reading the locked rows which the user is updating via the “SELECT FOR UPDATE”. Also, if database instances			crashed during the pessimistic locking process, then some rows may still be in a locked state.
		
  - Status and expiration time with cron
  - Implicit status with status and expiration time:
    - In this approach, the ticket entry will contain both the listingStatus (AVAILABLE / RESERVED / BOOKED) and 			expirationTime. When a booking process starts, it will check if the listingStatus is either AVAILABLE OR if it is				RESERVED but the expirationTime has already passed. If either of these two options is the case, then the				transaction will be committed. The SQL transaction for these two checks is shown in ‘SQL transaction for				listingStatus and expirationTime’. A separate cron job could also clean up any rows with old expirationTimes to 				improve read times. To improve reads, we can also index on the listingStatus.

  - Redis distributed lock with TTL:
    - Redis allows us to implement a distributed lock with a TTL, where a lock for a listingID in the Listings availability table could be acquired in Redis			with a TTL,	and this TTL will act as the expiration time. If the lock expires, Redis will release the lock and other				processes could operate on the entry. This way, the listingStatus only has two states: AVAILABLE / BOOKED.
			During the booking process, the listingStatus will remain AVAILABLE, but the lock will prevent other	processes from			updating that listingID.
    - The Redis lock will be for a listingID and userID, and it will prevent other processes from updating the listingID				during the TTL. This way, the listingID is locked only	for that specific userID, as it should be.
			
    - However, if a lock goes down, then there will be some time until a new lock is up - in this time, the first user to 			complete their booking process and pay will get the ticket, so if the lock is down, it’s first come first serve. However,			there will still be no double bookings since the database will use OCC or database constraints to ensure any writes			do not produce double bookings. We’ll go with this Redis distributed lock with TTL approach where the lock will			be for a userID and listingID.

    - Using the Redis distributed lock with TTL approach, when a user wants to book a ticket, they’ll select a listingID, and send a request to the Reservation service. The Reservation service will lock that listingID with a TTL by adding	it to our Redis Distributed Lock. The Listing service will also add a new entry to the Reservations table with a listingStatus of 	PENDING. The user’s request will then be routed to a payment service, and if the user cancels or doesn’t complete the 		booking process, the lock will be released after the TTL. If the booking process completes, the listingStatus will change to		BOOKED, and the reservationStatus will change to BOOKED within a single transaction.

<br/>

SQL transaction for listingStatus and expirationTime:

```sql
-- Serializable is usually the highest isolation level provided by most SQL transactions and will prevent: 
-- Dirty reads (reads in a transaction, during the time the read data has been modified by another transaction)
-- Non-repeatable reads (when the same transaction reads the same row twice, but gets 2 different results because of some		change)
-- Phantom reads (when the same transaction returns different results for the same query multiple times - it usually occurs when		other transactions modify the same data concurrently)

set transaction isolation level serializable;
begin;

-- run the below query for all ${date} between startDate to endDate:
select * from listingsAvailabilityTable
where listingID = ${listingID} and date = ${date} and (listingStatus = 'AVAILABLE' or (listingStatus = ‘RESERVED’ and (time.now() - expirationTime) > 5))

-- if the query above doesn't produce any output, then rollback

update listingsAvailabilityTable set listingStatus = 'RESERVED' and expirationTime = time.now() + 5
where listingID = ${listingID} and date = ${date} and (listingStatus = 'AVAILABLE' or (listingStatus = ‘RESERVED’ and (time.now() - expirationTime) > 5))

insert into reservationsTable values (${listingID}, ${userID}, ‘BOOKED’, ${price}, ${startDate}, ${endDate})

commit;
```

<br/>

Temporarily reserving listings / ticket solutions:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/49ac5025-e397-4919-a806-89ebd93c48b2" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/c876b85a-218f-4474-8084-b301b87404a4" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/b6c984f7-3ae2-45a3-96b7-75074a6211a9" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/8829d991-ff39-4ac3-869b-574af86ee6c5" />

<br/>

### Scaling the system to support high concurrency of booking listings

- Under a high concurrency of booking processes, the listing availability data will become stale very quickly. Note	that the admins will only enable these below to support very high concurrency, thus these approaches can be enabled only for	very high concurrency cases. We can ensure this data is up to date by using the below and in ‘Supporting high concurrency of	booking listings / tickets’ (these approaches are taken from the SDI 'Ticketmaster - general events'):
  - SSE for real-time seat updates:
    - SSE events will be pushed to the clients in real-time to update the listing availability as soon as a listing is booked or 				available. Thus, the user wouldn’t need to refresh their page.
    - SSE events will work well for moderately popular listings, but for listings with high concurrency such as one with a very high rating, the SSE approach will be slow to update the clients since it is still using HTTP, which will be slower than using websockets.

  - Virtual waiting queue and websocket for extremely popular listings and high concurrency of bookings:
    - Users requesting to view the booking page for a very popular listing will be placed in a virtual waiting queue, and			they will request to establish a websocket connection with the Reservation service. Dequeued users will be notified				using the websocket that they can proceed with the booking process. The			queued users will also be notified of their position of the queue and estimated wait times (wait time calculated	using 5 min * user's queue position) using the websocket. 

    - The queue could be implemented using traditional message queues such as SQS. The Reservation service can likely maintain workers (containers) which will pull from SQS, where the message will have a visibility timeout applied to ensure exactly-once delivery. When the worker pulls the message, the booking process can initiate via the worker, and if the booking process completes, then the message will be deleted by default. However, if the worker doesn't complete the booking process, then the message could likely be deleted OR sent to the back of the queue using SQS's delayed message delivery feature.
		
  - Note that we could also use long polling to get updates from the server about listing availability,		which is simple. However, if users sit on the “listing availability page” for a long time, then it will eat up resources on the		server.

Supporting high concurrency of booking	listings / tickets:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/f998b898-8533-41a7-bc39-d3630aab6a70" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/0f89e9b2-e043-4ce0-9267-7e16ad012a8b" />

<br/>

### Concurrency issues during bookings and different types of locking techniques

Concurrency issues might arise during double bookings where different users could book the same listingID for the same time concurrently. If same listingID and date is reserved at the same time by 2 different users, a race condition will likely be produced. The solution to these concurrent issues might require some form of locking:

#### Pessimistic locking

- Pessimistic locking also called pessimistic concurrency control prevents simultaneous updates by placing		a lock on a record as soon as a user starts updating it. Other users trying to update the record will have to		wait for the user to release the lock on the record. Both PostgreSQL and MySQL provides the “SELECT			FOR UPDATE” clause. The syntax is shown in ‘SELECT FOR UPDATE SQL’. This clause locks the			selected rows and prevents other transactions from updating them until the transaction is committed or			rolled back. This process is shown in ‘SELECT FOR UPDATE Pessimistic locking’

- The pros of this approach is that is uses strict locking on rows and ensures highly consistent data.

- The cons of this approach is that deadlocks may occur when multiple resources are being locked.				However, writing deadlock-free code can be challenging. When multiple transactions need to be made, this		approach is not scalable as multiple records will be locked. Also, if database instances			crashed during the pessimistic locking process, then some rows may still be in a locked state.

SQL FOR UPDATE SQL:

```sql
-- Serializable is usually the highest isolation level provided by most SQL transactions and will prevent: 
-- Dirty reads (reads in a transaction, during the time the read data has been modified by another transaction)
-- Non-repeatable reads (when the same transaction reads the same row twice, but gets 2 different results because of some		change)
-- Phantom reads (when the same transaction returns different results for the same query multiple times - it usually occurs when		other transactions modify the same data concurrently)

set transaction isolation level serializable;
begin;

-- run the below query for all ${date} between startDate to endDate:
select * from listingsAvailabilityTable
where listingID = ${listingID} and date = ${date} and (listingStatus = 'AVAILABLE' or (listingStatus = ‘RESERVED’ and (time.now() - expirationTime) > 5))

-- if the query above doesn't produce any output, then rollback

update listingsAvailabilityTable set listingStatus = 'RESERVED' and expirationTime = time.now() + 5
where listingID = ${listingID} and date = ${date} and (listingStatus = 'AVAILABLE' or (listingStatus = ‘RESERVED’ and (time.now() - expirationTime) > 5))

insert into reservationsTable values (${listingID}, ${userID}, ‘BOOKED’, ${price}, ${startDate}, ${endDate})

commit;
```

<br/>

SELECT FOR UPDATE pessimistic locking:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/fb6baa1c-2434-4d68-8914-abef09c3ac41" />

<br/>

#### Optimistic locking

- Optimistic locking also called optimistic concurrency control allows multiple concurrent users to update the		same record. Optimistic locking can be implemented using either a version number or timestamp. A version		number may be preferred since clocks need to be synchronized. If 2 users read the same record, and			update it at the same time, the version numbers will be used to determine if there was a conflict.

- Let’s say user1 and user2 reads and updates the same record with version1, and the version increases to		version2 at the same time. Upon committing the transaction, the transaction will check if version2 does not		already exist - and rollback if version2 exists. This is shown in ‘Optimistic locking’

- Optimistic locking is usually faster than pessimistic locking since the rows do not need to be locked.			However, optimistic locking can cause repeated retries on the client side if the transactions are rolled back.

- The pros of optimistic locking is that it prevents concurrent write conflicts, and we don’t need to lock the			selected rows. Optimistic locking is preferred when the number of concurrent operations are not very large.

- The con of optimistic locking is that it can cause repeated retries if transactions are rolled back and the			number of concurrent operations is high.

Instead of locking rows, use a version column or a timestamp to detect conflicts during updates:

```sql
-- Read with version
SELECT id, name, version
FROM users
WHERE id = 1;

-- Update only if version matches
UPDATE users
SET name = 'new_name', version = version + 1
WHERE id = 1 AND version = 5;
```

<br/>
<br/>

Optimistic locking:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/c521cd6b-d957-4068-92dd-49904ac72d35" />

<br/>

#### Database constraints

- Using database constraints is similar to optimistic locking. The SQL constraint shown in ‘Database			constraint’ is added to the Listings availability table. When transactions are being made, and they violate the		constraint, the transaction is rolled back. This is shown in ‘Database constraint’

- The pros of database constraints is that it’s easy to implement and works well when the number of			concurrent operations is not as high.

- The cons of database constraint is similar to optimistic locking, where it can cause repeated retries if			transactions are rolled back. Also, the updates from database constraints cannot be versioned like				optimistic locking. Additionally, not all databases provide database constraints, however PostgreSQL and		MySQL both support it.

<br/>

Database constraint:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/cb112e11-e93b-453e-937e-166f080ad248" />

#### Expiration time based locking and distributed locks

- We've already talked about these 2 different locking approaches above in 'Improving booking process'.

<br/>

Overall, after exploring all of these different transactions and locking approaches, we'll go with using the Redis distributed lock in this design.

<br/>

### Efficiently storing the location data for fast searches

Efficiently storing location data for fast searches can be done using multiple approaches. The resource notes in 'Location based search' goes over all of the main approaches. However, in this DD, we'll use either geohash, quadtree or PostGIS.

#### Geohash service

- Refer to the "Geohash" section in the resource note 'Location based search' for the background on geohash.

<br/>

- Geohash works by converting the long / lat to a string of letters and digits. We first divide the map into 4 grids recursively until the grid size is small enough such that it can contain a relatively small number of listings. As the map gets recursively divided, we'll assign a generated Base-32 geohash string to the grid. Geohash also operates with a fixed precision, where the smallest grids cannot be further divided, and all the smallest grids will have the same size. However, custom dynamic behavior can be added to a geohashing approach, but adding dynamic behavior may be more complex to do.
- Since geohashes represent hierarchical spatial data, shorter geohash strings cover larger areas, and longer geohash strings cover smaller areas with more precision. Therefore, if we keep removing the last character from a geohash string, the new geohash string will be for a larger area. To make geohash filtering more efficient, we can index the geohash column (like in 'Index on geohash') so that queries with the LIKE or WHERE operators will optimize it's prefix based searches.
- An example of using LIKE with a geohash string is given below:

Index on geohash:
```sql
CREATE INDEX idx_geohash ON listings USING geohash
```

Using LIKE to filter geohash strings:
```sql
select listingID, lat, long, geohash from listingTable
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

- Geohash works well for majority of the cases, but boundary issues may come up when one listing covers 2 geohash strings. Additionally, in some cases, there could be listings within the border of 2 geohash strings, and so that listing doesn't belong to any geohash string. In these cases, the geohash generation algorithm can be modified to account for such edge cases.
- Also, another issue may be when too few listings appear in the search result. In this case, we can increase the search radius by removing the last digit of the geohash string, and we can continue to increase the radius by removing another digit from the end.

##### Geohash sharding / partitioning

- If we have a table containing the listingIDs and geohash strings, we can easily shard the database and partition the tables based on prefixes of the geohash strings. We'll shard by the prefixes of the geohash strings because listings which are within the same geohash search radius will also be within the same shard. This will make searches faster, since we'll have to look through fewer shards or entries of the table.
- In general, tables containing location data for listings take up very little storage, thus sharding or partitioning may not even be needed, but will help to support the read load and fault tolerance.

#### Quadtree service

- Refer to the "Quadtree" section in the resource note 'Location based search' for the background on quadtrees.

<br/>

- A quadtree also recursively divides the map into 4 grids until the contents of the grids meet a certain criteria, like not having more than 100 listings. A quadtree is an in-memory data structure that helps with location based searching.
- The data on a leaf node (leaf node represents the most granular grid) in a quadtree can contain long / lat and a list of listingIDs in the grid. The data on a parent node (parent node represents the parent grid of leaf nodes) contains the parent grid's long / lat values and pointers to the 4 child nodes.
- Assuming a leaf node has at most 100 listings, then to build a quad tree for N listings:
  - It will take (N * 100) * log(N / 100) time complexity, since we're parsing through (N / 100) leaf nodes which contains at max 100 listings each, and we'll also be parsing the height of the tree which will be log(N / 100), where N / 100 is the number of leaf nodes.

- Below is an example of a quadtree quad:
<img width="750" alt="image" src="https://github.com/user-attachments/assets/23144928-0519-46eb-8b49-4dd0cd8c45b5" />

<br/>

- To search in a quadtree, we'll start from the root node and traverse down the tree until we find a node within the search radius. If we find a node within the search radius, we'll traverse the node's child nodes and siblings to see if they're also in the search radius. We'll keep a list of listings in the leaf nodes which are within the search radius, and then return the list of listings. The downside to a quadtree is that searches can be a bit complex to implement.
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
listings: [ { listingID, name, location, long / lat } ],
nodeQuad: { maxLong, maxLat, minLong, minLat },
leafNode: TRUE / FALSE,
childNodePtrs: { childNode_1, childNode_2, childNode_3, childNode_4 }
}
```
- In this entry, the nodeID can represent the node of the quadtree. If a node is a leaf node, we'll set the leafNode to TRUE. Also, if it is a leaf node, then there will be listings populated within this node. The nodeQuad field will also be the quad's max /  min long / lat values.
- When searching for listings within a search radius, we'll first check if the nodeQuad's long / lat values are intersecting with the search radius. If the quad is intersecting, then we'll traverse down the tree to find the leaf nodes. In the leaf nodes, we'll search for listingIDs which have long / lat values within the search radius.

##### Building a quadtree

- We will start with one node that will represent the whole world in one quad. Since it will have more than 100 listings, which may be our criteria, we will break it down into four nodes and distribute locations among them. We will keep repeating this process with each child node until there are no nodes left with more than 100 listings.

##### Dynamic quads

- We can use dynamic quads in our quadtree where if the number of listings exceed a threshold in a quad, we'll further split the quad into 4 more quads. In the quadtree, nodes will contain the listingIDs such that the listingID can be used to query the listing info from a table containing the listing data.

##### Searching in a quadtree

- In the quad tree, child nodes will be connected to sibling nodes with a DLL. Using the DLL, we can move left / right / up / down to sibling or child quads to find listings. An alternative to a DLL is to use parent pointers from the child nodes to the parent node.

- When searching in the quadtree, we start searching from the root node and visit child nodes which are in the search radius. If a child node is in the search radius, we can traverse through it’s own child nodes and sibling nodes using the DLL and return them if they are also in the search radius.

- If we don't have enough listings to return after searching a specific node, we can search the node's siblings and also it's parent node to retrieve surrounding listings as well.

##### Adding / updating / removing an entry (listing) in a quadtree

- To add / update a listing in the quad tree, we can search the nodes for the listingID and add / update the listing in the node, and also update any neighboring siblings if needed. If after adding the listing, the leaf node reaches the threshold on the number of listings a node can have, we'll need to split this leaf node further into 4 leaf nodes and allocate these 4 leaf nodes with the listings from the original leaf node.
- To remove a listing in the quad tree, we can search the nodes for the listingID and remove the listing from the node, and update the neighboring nodes accordingly

##### Quadtree sharding / partitioning

- We can shard the quadtree based on regions on the basis of zip or postal codes, such that all the listings and nodes that belong to a specific region are stored in a single shard. A region in this case will be a branch within a quadtree - therefore, a shard could contain a separate part of a single quadtree (the branch). Some regions could also be combined into a single shard to prevent uneven distributions.
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
- For example, we'll first add a location column of type GEOMETRY to the listings table as shown below. In here, POINT is a PostGIS type which represents the long / lat, and SRID 4326 specifies the WGS84 coordinates format.

```sql
alter table listings
add column location GEOMETRY(POINT, 4326)
```

- To populate the location column using a specific long / lat value, we can do the following. ST_MakePoint will return a POINT type using the long / lat values we provide.

```sql
update listings
set location = ST_SetSRID(ST_MakePoint(long, lat), 4326)
```  

##### 2. We can then query using PostGIS spatial functions:

**If we want to find locations using a specific point, we can do the following:**

- For example, we can use the ST_Intersects function to check if a listing's location (location is PostGIS's GEOMETRY type) intersects with a specific polygon as shown below. For example, we'll input the polygon's max / min long / lat values into the ST_MakeEnvelope function which will create a rectangular polygon. Other polygon based functions are also available in PostGIS. We'll then use the ST_Intersects function, and input the listing's location field (which will be of a PostGIS GEOMETRY type) and also input this polygon.

```sql
select * from listings
where ST_Intersects(location, ST_MakeEnvelope(${minLong}, ${minLat}, ${maxLong}, ${maxLat}, 4326)
```

**If we want to find locations within a specific search radius, we can do the following:**

- We can also use the ST_DWithin PostGIS function to find listings within a specific search radius as shown below. We'll use ST_MakePoint to create a point using a long / lat value of the center of the search radius. In here, the centerLong and centerLat values will be center's long / lat values. The radiusInMeters value will be the actual search radius in meters. ST_DWithin will check if the listing's location is within the specified radius's center point.

```sql
select * from listings
where ST_DWithin(location, ST_SetSRID(ST_MakePoint(${centerLong, ${centerLat}}), 4326), ${radiusInMeters})
```

<br/>

### Improving search latencies

- Queries on the database and performing the “LIKE” clause will be very slow for searches because it causes a full table scan. We can improve the search by		using the following and in ‘Improving search latencies’ (these approaches are taken from the SDI 'Ticketmaster - general events'):
  - Indexing and SQL query optimization
  - Full-text indexes in the database
  - Full-text search engine like Elasticsearch:
    - The overall inverted index mappings could be built using the text based listings data.

Improving search latencies:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/babcfe37-e54c-49b5-a586-099d39f3dc3b" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/981fb13b-eadc-4caa-9e78-2c37d396b2e3" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/75f5eaff-8632-4602-beb2-ff17abdaf732" />

<br/>
<br/>

- Also, the frequent search queries could be cached to improve latencies using the below and in ‘Caching search queries’ (these approaches are taken from the SDI 'Ticketmaster - general events'):
  - Implement caching strategies using Redis / Memcached
  - Implement query result caching and edge caching:
    - Elasticsearch has built-in node level caching that can store search query results. AWS Opensearch, which can			run an instance of Elasticsearch also provides node level caching of search query results. Also we could utilize				CDNs to cache search results geographically closer to the user.

Caching search queries:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/b84bd197-fb69-4a8e-892b-2973c33d2d14" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/bcbab7ff-0098-4def-8b5f-7d872ae9342f" />

<br/>

### Efficiently searching for listings using full text search

- Searching by long / lat in a traditional database without a proper indexing is very inefficient for large datasets. When using simple comparison operators to find listings based on long / lat within a search radius or box, the database has to perform a full table scan to check every single entry which matches these conditions. This is also true when searching for terms in the name or description. This would require a wild card search across the entire database via a LIKE clause.

Inefficient way of searching for listings:
```sql
select * from listingTable
where lat > 10 and lat < 20 and long > 10 and long < 20 and name like '%2 bedroom 1 bathroom%'
```

- We can efficiently search for listings using the below approaches, and in 'Efficiently searching for listings using full text search':
  - Basic database indexing
  - Elasticsearch
  - PostgreSQL with extensions:
    - While pg_trgm is great for full text searches, it still may not perform as well as Elasticsearch which is more optimal for searching through text.

In some cases, interviewers will ask that you don't use Elasticsearch as it simplifies the design too much. If this is the case, they're often looking for a few things in particular:

1. They want you to determine and be able to talk about the correct geospatial indexing strategy. Essentially, this usually involves weighing the tradeoffs between geohashing and quadtrees, though more complex indexes like R-trees could be mentioned as well if you have familiarity. In my opinion, between geohashing and quadtrees, I'd opt for quadtrees since our updates are incredibly infrequent and listings are clustered into densely populated regions (like NYC).

2. Next, you'll want to talk about second pass filtering. This is the process by which you'll take the results of your geospatial query and further filter them by exact distance. This is done by calculating the distance between the user's lat/long and the listing lat/long and filtering out any that are outside of the desired radius. Technically speaking, this is done with something called the Haversine formula, which is like the Pythagorean theorem but optimized for calculating distances on a sphere.

3. Lastly, interviewer will often be looking for you to articulate the sequencing of the phases. The goal here is to reduce the size of the search space as quickly as possible. Distance will typically be the most restrictive filter, so we want to apply that first. Once we have our smaller set of listings, we can apply the other filters (name, category, etc) to that smaller set to finalize the results.

<br/>

### Data inconsistency between cache and database

- If using the cache, when the Reservation service looks for listing availability in the cache, 2 operations	happen:
1. Querying the cache for listing availability
2. Updating the listingID's listingStatus field in the Listing availability table to BOOKED after the booking process completes.

- If the cache is asynchronously updated as shown in ‘Hotel / listing caching’, there may be some			inconsistency between the cache and database. However, this inconsistency will not matter since			reservation requests will still make the final update to the database via the Redis distributed lock. The cache is only there to help in speeding up listing			availability searches, not storing the exact listing availability data is fine. Some data inconsistencies between the cache and database will be fine depending on the consistency we want for displaying listing availability. If we want users to always see the latest listing availability value in the UI, then the cache can be omitted from the design.

<br/>

Hotel / listing caching:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/b346c2c5-5715-463a-b575-1a43bf7083d8" />

<br/>

### Microservice vs monolithic

- When using a microservice architecture, a service usually has it’s own database it manages. In a monolithic		architecture, multiple services could manage the same database. This is shown in ‘Microservice vs		monolithic’.

- Our design has a hybrid approach, where a single service could still access databases / tables other services could		manage or access. For example, the Reservation service accesses both the Listings availability and Reservations tables.
	We have a hybrid approach, because a pure microservice approach can have consistency issues when			managing transactions. The reservation service accesses multiple databases / tables, and if a transaction fails, then it will	need to roll back the changes in those respective databases / tables. 

- If we used a pure microservice approach, the changes will need to be rolled back in all the databases / tables BY THE SERVICES which manage them instead of by only the reservation service. We cannot only just use a single transaction (within the reservation service) in a pure microservice approach, we’ll need multiple transactions happening within those services as shown in ‘Microservices transactions’. This causes an overhead and may lead to inconsistency issues.

Microservice vs monolithic:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/3ade0c8e-9ae6-48a2-9c86-97686ec1ccd1" />

<br/>
<br/>

Microservices transaction:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/2608a3b6-d161-4205-86ea-5d015a3b5f43" />

### Scaling the system to support large number of users

The stateless servers for the Listings, Reservation, Listings management services could be scaled as follows as in 'Scaling API to support high concurrency' (these approaches are taken from the SDI 'Ticketmaster - general events'):

- To scale the API for high concurrency for popular listings, we’ll use a combination of load balancing, horizontal scaling	and caching as shown in ‘Scaling API to support high concurrency’. To scale, we can cache static data with high reads such as listings, white are not as frequently written to.

Scaling API to support high concurrency:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/a187b31b-c583-4929-9894-25bdf597455a" />

<br/>
<br/>

The stateless servers could be scaled by adding more servers, but the database and cache will need to be		scaled differently:

#### Database

- We don't necessarily need sharding because the data is small, but if we want to apply sharding, we can apply sharding on the databases by using the "regionID" on the Listings and Listings availability tables. We can likely do this because listings within the same regionID will be within the same shard. This way, we'll search through fewer shards during reads. However, we'll also need to ensure that the data is spread evenly across shards, and possibly allocate more shards for more dense regionIDs like NYC.

#### Caching

- In the cache, only the frequently accessed listings should be cached using a TTL.				Additionally, the Listings availability data for the next 1-2 years could also be cached as the Reservation service		will use the Listings availability data frequently to check if the listing is available or not. Caching the Listings availability might be preferable if we have large read operations for checking listings availability.
	
- If we use both a database and cache, the Reservation service could first check the listing availability	in the cache, then update the Listings availability data in the database. Afterwards, the		database could asynchronously update the cache. In this caching scenario, the cache is used		for fast searches, while the database is the single source of truth. This logic is shown in ‘Hotel / listing caching’





