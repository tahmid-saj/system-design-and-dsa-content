# Hotel reservation and management system

Note: Parts of this design was taken from the SDI 'Ticketmaster - general events'

## Requirements

### Questions

- Should we design for different entities such as hotels, rooms, room inventory, reservations, etc?
  - Yes

- Users can browse hotels, browse rooms in a hotel, and make a reservation at a room. Should our system support all of this?
  - Yes

- Multiple users can "reserve" the same room - how long should we "reserve" it for them once the booking process starts?
  - 5 mins, then "un-reserve" the room if they don't complete the booking process. However, look to improve the design for the booking experience.

- Should we return the exact number of available rooms available for a specific hotel and roomType?
  - Yes

- Do customers pay when they make reservations or when they arrive at the hotel?
  - For simplicity, let’s say they pay in full when they make reservations

- Can customers cancel their reservations?
  - Yes

- How many hotels and rooms will the system support?
  - 5000 hotels and 1M rooms in total

- Can users view their reservations?
  - No, let's leave these out

- Should we consider any other things like overbooking?
  - Yes, let’s say we have 10% overbooking. Overbooking is where the hotel will sell	more rooms than they actually have. Hotels do this in anticipation that some		customers will cancel their reservations

### Functional

- Users can search for hotels, and view rooms of a hotel:
  - Users should also see the number of rooms available in a hotel
- Reserve a room in a hotel
- Admin to add / remove / update hotel or room info
- Support overbooking

- 5000 hotels, and 1M rooms in total

### Non-functional

- High throughput / concurrency:
  - There could be multiple booking requests for the same room, but only the first one will be considered.
  - There could also be high throughput / concurrency during holidays
  - The system will also be read heavy, as more users will view rooms than book them
- Consistent:
  - Users should see a consistent view of available rooms

## Data model / entities

Majority of the entities are mainly read heavy, as opposed to being write heavy. This is because fewer users make reservations as opposed to searching for hotels and rooms. A SQL database works well here, as it provides more optimized ACID properties which will support consistency between room availability and reservations, and help in preventing double bookings or double charging.

<br/>

The system should support the below queries:
- Search hotels
- Find available rooms within a date range in a hotel
- Book a reservation

<br/>
<br/>

- Hotels:
	- hotelID
	- name
	- location / long / lat / geohash (if the system is using geohash) / location (if the system is using PostGIS, then location will be of PostGIS's GEOMETRY type)

- Room:
	- roomID
	- hotelID
	- roomType
	- roomNumber

- Room Inventory:
  - Note that if we want to maintain the room inventory and number of reservations for a roomType, we	can have a room inventory table. This table can be used by the reservation service to find if the specific	roomType is available or not for the specific date using the totalReserved field in the table.
	
  - This room inventory table can be pre-populated for the next 1-2 years, and can be updated when a reservation is made after a booking process completes

  - During the booking process, we can increment the totalReserved field of the hotelID's roomType that is being reserved. During this booking process, we'll also likely create an entry in the Reservations table. If the booking process doesn't complete, then the totalReserved value will be decremented and rolled back.

  - To support overbooking, either the totalInventory field could be increased by 10% or so, or the SQL	query to check if there are enough rooms available during reservations could be adjusted to incorporate	the 10% overbooking logic as shown in ‘Overbooking query logic’

	- hotelID
	- roomType
	- date
	- totalInventory
	- totalReserved

Overbooking query logic:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/69aff160-5240-4ebb-9aba-ea71d7479cdd" />

<br/>
<br/>

- Reservations:
  - This entity stores info on the reservations booked by a user. The reservationStatus will be used to represent PENDING vs BOOKED reservations
    
	  - reservationID
	  - roomIDs
	  - userID
	  - startDate, endDate
	  - roomCount
	  - price
	  - reservationStatus: PENDING / BOOKED / CANCELED

## API design

- Note that we’ll use userID if the user is authenticated and will be booking rooms. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed entries quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

**Note: We’ll focus on the hotel, room and reservation related endpoints. Other endpoints such as modifying the customer profile and preferences may not be the major focus of the system**

<br/>

Hotel endpoints:

### Search hotels

- Note that we’ll use cursor based pagination and filter options to retrieve a list of hotels. As we’re		dealing with 5000 hotels, we’ll use cursor based pagination which is more suitable for larger results.	Additionally, we can incorporate lazy loading on the viewport and only retrieve the hotels info for the	displayed hotels on the viewport.

- If we want to get search results based on the location, this request can be routed to a Geohash vs PostGIS vs Quadtree service, which will return the hotels within a specific radius.
- Also, if we want to get search results based on availability times, then we could set the nextCursor value to the viewport's oldest availability time using the date field from the Rooms inventory table - this way, we could retrieve the paginated results based on the available time of the hotelIDs. This is only necessary if we want to return the hotels by their room availability times, so some joining will need to be done in the backend between the Hotels and Rooms inventory tables. 

<br/>

Request:
```bash
GET /hotels/?query={ text search or location based search }?nextCursor={ viewport's oldest availability time using the date field from the Rooms inventory table }&limit&filter={ search radius or roomType }
```

Response:
```bash
{
  hotels: [ { hotelID, name, location, totalAvailable (totalInventory - totalReserved from the Room inventory table), latestAvailabilityTime (taken from date field in Rooms inventory table) } ],
  nextCursor, limit
}
```

Additional hotel based endpoints include (mainly done by an admin):

- GET /hotels/:hotelID - Get hotel detail
- POST /hotels - Add a new hotel
- PUT /hotels/:hotelID - Update hotel info
- DELETE /hotels/:hotelID - Delete a hotel

<br/>

Room endpoints:

### Get rooms in hotel

- Note that we’ll use cursor based pagination and filter options to retrieve a list of rooms. As we’re		dealing with 200 rooms or so per hotel, we’ll use cursor based pagination which is more suitable for larger results.		Additionally, we can incorporate lazy loading and only retrieve the rooms for the	displayed rooms on the viewport.

- Also, we could set the nextCursor value to the viewport's oldest availability time using the date field from the Rooms inventory table - this way, we could retrieve the paginated results based on the available time of the roomIDs. This is only necessary if we want to return the rooms by their room availability times. 

Request:
```bash
GET /hotels/:hotelID/rooms?nextCursor={ viewport's oldest availability time using the date field from the Rooms inventory table }&limit&filter={ roomType }
```

Response:
```bash
{
  rooms: [ { roomID, location, roomNumber, roomType, latestAvailabilityTime (taken from date field in Rooms inventory table) } ],
  nextCursor, limit
}
```

Additional room based endpoints include:

- GET /hotels/:hotelID/rooms/:roomID - Get room detail
- POST /hotels/:hotelID/rooms - Add a new room
- PUT /hotels/:hotelID/rooms/:roomID - Update room info
- DELETE /hotels/:hotelID/rooms/:roomID - Delete a room

<br/>

Reservation endpoints:

### Make a reservation

- Usually the booking process is a 2 step process, where the user will first reserve a room in the first step, then in the second step they’ll input their payment details into the provided payment URL within the time limit. Thus we have 2 individual endpoints for these steps below.

#### Reserving a room

Request:
```bash
POST /hotels/:hotelID/rooms/reservations
{
	roomIDs
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
{
  paymentDetails (the payment details will be encrypted or retrieved by a separate payment service entirely)
}
```

Response:
```bash
{
	reservationIDs, reservationStatus
}
```

Additional reservation based endpoints include:

- GET /users/:userID/reservations - Get the user’s history of reservations
- GET /users/:userID/reservations/:reservationID - Get user’s past reservation detail
- DELETE /users/:userID/reservations/:reservationID - Cancel a reservation

## HLD

### API gateway

- The API gateway will provide rate limiting, authentication, and route requests to the specific services.	For example, for a reservation request, the API gateway could get the room details from the hotel		service, then make a reservation using the reservation service

### Microservice architecture

- A microservice architecture is suitable for this system, as the system requires independent services	such as the hotel, reservation, hotel management, payment service where each service has it’s	own resource requirements and can be scaled and managed separately.

- Microservices can benefit from a gRPC communication as there will be multiple channels of requests	being sent / received in inter-service communication between microservices. Thus, gRPC could be the	communication style between microservices, as it supports a higher throughput, and is able to handle	multiple channels of requests as opposed to REST, which uses HTTP, that is not optimized for		multi-channel communication between services.

### Hotel service

- The hotel service provides detailed information on hotels and rooms, and could possibly handle additional		operations such as rating a hotel.

**Note that 5000 hotels is not large, and could be directly queried from an in-memory cache without using a location based search service, however since latency is still a top priority, a separate location based search service might help but makes the design more complex**

#### Hotel service using Geohash service vs PostGIS service vs Quadtree service (if location based search is in scope)

- The Hotel service will also use either the Geohash service or the PostGIS service or the quadtree service to efficiently search hotels using geohash strings, PostGIS, or a quadtree respectively, and return the paginated results of the hotels within a search radius. The specifics of the approaches, and additional approaches which can be used are discussed in the DD of the SDI 'Yelp - business proximity'.

### Hotel database / cache

- The hotel database will store the hotels, rooms, rooms inventory, reservations, etc data. As the hotel and room data requires consistency, more complex date range queries, and may require transactions or locking, a SQL database such as PostgreSQL may be preferred over NoSQL, which is more optimized for maintaining consistency. Additionally, the hotel, room, reservation data will need to be consistent to prevent	double bookings and double charging, so SQL is preferred.

- Additionally, PostgreSQL will provide custom data types and good JSON compatibility for the hotel's room arrangement data (although it's not included in this design), which will likely be unique and unstructured for each hotel.

#### Sharding may not be necessary

- If the reservation data grows too large for a single database, older reservations could be moved to a	cold storage in S3, as they will not be frequently accessed. Additionally, the SQL database / tables could be	sharded by a "regionID" or hotelID, since it makes sense for reads to access entries within the same regionID and hotelID - this way, there's fewer shards which need to be communicated with.
- However, if we have 5000 hotels, and 1M rooms, then:
  - 5000 * 1 KB = 5 MB is the storage needed for all hotels
  - 1M * 1 KB = 1 GB is the storage needed for all rooms
  - It's very unlikely that we need sharding for the hotels and rooms tables, however even sharding might still not be super helpful for the rooms inventory and reservations tables which are much larger, likely 365 days * 10 years * 1 GB = 3650 GB = 3.650 TB space needed for Rooms inventory and reservations tables.

#### Cache

- We could maintain a cache, however storing the room availability from the Rooms inventory table in the cache would be difficult since the room availability could change frequently, and not be consistent with the database - the DD talks more about data inconsistency between the cache and the database.

- However, we could still cache the hotels and rooms data which don't change frequently or have concurrency issues behind them. We could use either Redis or Memcached for this. Additionally, the hotel rooms arrangement data, which will rarely change in a hotel can be cached via Redis' maps and lists data structures.

### Reservation service

- The reservation service handles reservation requests and initiates the booking process. It also updates the reservationStatus and the reservation entry in the	database as users make reservations

- The reservation service will likely increment the totalReserved field in the Rooms inventory table once the booking process initiates. During the booking process, a new entry for the reservations will be added to the Reservations table. If the booking process is not completed, the totalReserved field will be rolled back and decremented. If the booking process does complete via the Payment service, then the totalReserved value will stay as is.

### Hotel management service

- The hotel management service provides internal API endpoints which are only available to admins for 	updating hotel and room data, manually updating reservations, etc.

### Payment service

- The payment service executes the payment transaction once a customer make a reservation

<br/>

If location based search is in scope:

### Geohash service (if using geohash)

- The Geohash service will search for hotels within a search radius using a geohash based approach, and return them to the hotel service. The Geohash service will take a geohash of the search radius (using a geohash converter) and find hotels within the specified radius by comparing their geohash strings.
- The geohash converter, which could be PostgreSQL's PostGIS geohash conversion functionality shown in 'PostGIS geohash conversion function', will take a long / lat coordinate of either a radius or hotel, and then convert it to a geohash string. This geohash string will be compared against the geohash strings in the hotels table / cache to find relevant hotels.
- Because we're using geohash, the Geohash service will compare the prefixes of the search radius' geohash string with the prefixes of the hotels' geohash string. If the prefixes are the same, then this means the hotel is within the search radius. A query such as the one below can be used to find hotels with the same prefix as the search radius' geohash.

```sql
select hotelID, lat, long, geohash from hotelTable
where geohash like '${radiusGeohash}'
```

PostGIS geohash conversion function:
```sql
select ST_GeoHash(ST_Point(${long}, ${lat}))
```

- When new hotels are added, we'll also use the Geohash service to generate a geohash string for the new hotel, and then store it in the hotels table.

- Geohash can sometimes be slower than a typical quadtree. It can also be slower than PostGIS's built-in location based search functionalities.

#### Geohash cache

- Because the querying the geohash data on disk may be slow, we can store a geohash cache in Redis. Redis provides support for geohashing to encode and index geospatial data, allowing for fast querying. The key advantage of Redis is that it stores data in memory, resulting in high-speed data access and manipulation. Additionally, we can periodically save the in-memory data to the hotels table using CDC (change data capture).

### Quadtree service (if using quadtree)

- The Quadtree service will recursively build and update the Quadtree table and cache. The Quadtree service will also be used to search the quadtree efficiently by traversing down the tree from the root node to the leaf nodes.
- A quadtree may be more suitable for this design than a geohashing approach, since there are many high density areas such as NYC, and a quadtree will account for these dense areas by splitting up the quads further.

#### Quadtree table / cache

- Because a quadtree is an in-memory data structure, we can keep both a quadtree table within PostgreSQL as well as a cache using Redis. PostgreSQL provides SP-GiST, which provides functionality for storing and querying a quadtree data structure.
- Although Redis doesn't directly provide quadtree support, we'll use Redis as the quadtree cache since it provides complex data structures such as lists and sorted sets which will be helpful in storing nodes of the quadtree. For example, the leaf node of a quadtree can be a Redis sorted set, where the hotels are sorted based on their distances to the leaf node's radius's center point. A leaf node can also contain a Redis list which contains hotels from the hotel table which fall within the leaf node's radius.
- Additionally, a quadtree data structure is not as complex to build, and could be implemented within a memory optimized EC2 instance.

### PostGIS service (if using PostGIS)

- We could also use a PostGIS service which will convert the hotel long / lat values in the hotels table to a PostGIS GEOMETRY type. We'll then add a new column of this GEOMETRY type (we'll call it the location column) to the hotels table. This PostGIS service will then be used to query the hotels table using PostGIS search functions like ST_Intersects (to find if a long / lat value intersects with another point) and ST_DWithin (to find if a long / lat value is within a radius).

### Search service

- The search service will connect to the database and handle any search queries (in the API endpoint for searching hotels and rooms). The search service will likely use an inverted index mapping on text based fields such as the hotels, rooms, etc and perform efficient searching using the mappings. Thus, it could use a tool such as Apache Lucene or Elasticsearch which can maintain an inverted index mapping for a data store.

<img width="900" alt="image" src="https://github.com/user-attachments/assets/bd953ea3-b1b6-4408-88eb-3ce66b3032f0" />

## DD

### Improving booking process
  
- Incrementing the totalReserved field (or setting ticketStatus to RESERVED temporarily during the booking process as in the SDI 'Ticketmaster - general events') in the Rooms inventory table and starting a timer once a user initiates their booking process is a common approach	in multiple booking / ordering / payment processing apps. This approach is used because no user wants to enter their payment	info, then find out later that a room has already been booked. Thus we have a timer and temporarily “reserve” their room.

- To design for this 5 min timer and temporarily increment the totalReserved, we can try out the below solutions	and in ‘Temporarily reserving rooms / ticket solutions’ (these approaches are taken from the SDI 'Ticketmaster - general events'):
  - Pessimistic locking:
    - Pessimistic locking is usually not a good approach as it can cause deadlocks if there’s high concurrency. Also the			locked rows within the “SELECT FOR UPDATE” or data locking mechanism will prevent other processes from				reading ("SELECT FOR UPDATE" blocks the reads) the locked rows which the user is updating via the “SELECT FOR UPDATE”. Also, if database instances			crashed during the pessimistic locking process, then some rows may still be in a locked state.
    - Because pessimistic locking might cause more deadlocks, and might actually cause more locking issues if database instances are down, we'll look into optimistic locking OR database constraints later on in the DD.
		
  - Status and expiration time with cron
  - Implicit status with status and expiration time:
    - This approach might not be directly applicable to this design since we don't have a field like ticketStatus or roomBookingStatus which specifies if a single instance of a room is available or not. We have a Rooms inventory table to check if there are available rooms for a hotelID using the totalReserved field instead of roomBookingStatus.

  - Redis distributed lock with TTL:
    - This approach might also not be directly applicable to this design since we don't have a specific field like roomInventoryID which represents a specific room that is available / unavailable. We have a Rooms inventory table to check if there are available rooms using the totalReserved field instead of using a roomInventoryID. If we had a roomInventoryID, then a Redis distributed lock with TTL could be applied

<br/>

Temporarily reserving rooms / ticket solutions:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/49ac5025-e397-4919-a806-89ebd93c48b2" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/c876b85a-218f-4474-8084-b301b87404a4" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/b6c984f7-3ae2-45a3-96b7-75074a6211a9" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/8829d991-ff39-4ac3-869b-574af86ee6c5" />

<br/>

### Scaling the system to support high concurrency of booking rooms

- Under a high concurrency of booking processes, the room availability data will become stale very quickly. Note	that the admins will only enable these below to support very high concurrency, thus these approaches can be enabled only for	very high concurrency cases. We can ensure this data is up to date by using the below and in ‘Supporting high concurrency of	booking rooms / tickets’ (these approaches are taken from the SDI 'Ticketmaster - general events'):
  - SSE for real-time seat updates:
    - SSE events will be pushed to the clients in real-time to update the room availability as soon as a room is booked or 				available. Thus, the user wouldn’t need to refresh their page.
    - SSE events will work well for moderately popular hotels, but for hotels with high concurrency such as a 5 star hotel, the SSE approach will be slow to update the clients since it is still using HTTP, which will be slower than using websockets.

  - Virtual waiting queue and websocket for extremely popular hotels and high concurrency of bookings:
    - Users requesting to view the booking page for a very popular hotel will be placed in a virtual waiting queue, and			they will request to establish a websocket connection with the Reservation service. Dequeued users will be notified				using the websocket that they can proceed with the booking process (booking process will likely be performed via optimistic locking OR database constraints). The			queued users will also be notified of their position of the queue and estimated wait times (wait time calculated	using 5 min * user's queue position) using the websocket. 

    - The queue could be implemented using traditional message queues such as SQS. The Reservation service can likely maintain workers (containers) which will pull from SQS, where the message will have a visibility timeout applied to ensure exactly-once delivery. When the worker pulls the message, the booking process can initiate via the worker, and if the booking process completes, then the message will be deleted by default. However, if the worker doesn't complete the booking process, then the message could likely be deleted OR sent to the back of the queue using SQS's delayed message delivery feature.
		
  - Note that we could also use long polling to get updates from the server about room availability,		which is simple. However, if users sit on the “room availability page” for a long time, then it will eat up resources on the		server.

Supporting high concurrency of booking	rooms / tickets:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/f998b898-8533-41a7-bc39-d3630aab6a70" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/0f89e9b2-e043-4ce0-9267-7e16ad012a8b" />

<br/>

### Concurrency issues during bookings and different types of locking techniques

Concurrency issues may arise during double bookings where:

1. The same user could reserve the same room multiple times for the same date
2. Different users could reserve the same room for the same date at the same time

<br/>

- To solve the first issue, the client can gray out or hide or disable the submit button once the user has already		reserved for the same room for the same date. This will happen on the client side, so it is not reliable as users		can modify the client side code

- Another solution for the first issue is to use an idempotency key such as the reservationID during the			reservation request via the API endpoint. When the client sends a reservation request, a reservationID is stored	in the database. If any clients send a reservation for the same room and date, the	 reservationID will be the same	and thus, will reject the reservation request. The process is shown in ‘reservationID double booking’

<br/>

reservationID double booking:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/50138c98-d970-4d67-984a-59ddb0fa5701" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/0699c334-5b2c-4fd5-ad78-59a1ab67ac67" />

<br/>

- The reservationID could be generated via a unique ID generator similar to Twitter snowflake that can take into		account of the start and end date, and the roomType or roomID, and allocates these fields in some of the bits in	the 64-bit snowflake ID. An example of the reservationID could be:
	- 1 bit for sign value | 8-10 bits roomID / roomType | 13 bits startTime | 13 bits endTime

<br/>

- In the second issue, where the same roomID or roomType and date is reserved at the same time by 2 different		users, a race condition is produced as shown in ‘Concurrent room booking race condition’. Let's first see what the root cause of the issue is, then talk about the types of locking solutions we could implement for this second issue.

<br/>

Concurrent room booking race condition:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/836e1e64-fce5-4959-b448-571032e2249b" />

<br/>
<br/>

- To prevent the race conditions, we'll likely need some form of locking discussed later in the DD, but let's take a look at the SQL code for this transaction to determine what types of locking is best for this issue. The SQL code to check for room availability and update to the Room Inventory SQL table if there are rooms 		available will be similar to ‘Room Inventory update SQL logic’ where we first check the room inventory, then		update the room inventory with the reservation’s room count 


<br/>

Room Inventory update SQL logic:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/2a00a614-9cd2-4884-a974-c431124974ec" />

<br/>
<br/>

The solution to this second issue may require some form of locking, which we'll discuss now:

#### Pessimistic locking

- Pessimistic locking also called pessimistic concurrency control prevents simultaneous updates by placing		a lock on a record as soon as a user starts updating it. Other users trying to update the record will have to		wait for the user to release the lock on the record. Both PostgreSQL and MySQL provides the “SELECT			FOR UPDATE” clause. The syntax is shown in ‘SELECT FOR UPDATE SQL’. This clause locks the			selected rows and prevents other transactions from updating them until the transaction is committed or			rolled back. This process is shown in ‘SELECT FOR UPDATE Pessimistic locking’

- The pros of this approach is that is uses strict locking on rows and ensures highly consistent data.

- The cons of this approach is that deadlocks may occur when multiple resources are being locked.				However, writing deadlock-free code can be challenging. When multiple transactions need to be made, this		approach is not scalable as multiple records will be locked. Also, if database instances			crashed during the pessimistic locking process, then some rows may still be in a locked state.

SQL FOR UPDATE SQL:

```sql
begin;

select date, total_inventory, total_reserved from room_inventory
where room_type_id = ${roomTypeID} and hotel_id = ${hotelID} and date between ${startDate} and ${endDate}
and total_reserved + ${reservationRoomCount} <= 110% * total_inventory
for update

update room_inventory
set total_reserved = total_reserved + ${reservationRoomCount}
where room_type_id = ${roomTypeID} and hotel_id = ${hotelID} and date between ${startDate} and ${endDate};

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

- Using database constraints is similar to optimistic locking. The SQL constraint shown in ‘Database			constraint’ is added to the Room Inventory table. When transactions are being made, and they violate the		constraint, the transaction is rolled back. This is shown in ‘Database constraint’

- The pros of database constraints is that it’s easy to implement and works well when the number of			concurrent operations is not as high.

- The cons of database constraint is similar to optimistic locking, where it can cause repeated retries if			transactions are rolled back. Also, the updates from database constraints cannot be versioned like				optimistic locking. Additionally, not all databases provide database constraints, however PostgreSQL and		MySQL both support it.

<br/>

Database constraint:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/cb112e11-e93b-453e-937e-166f080ad248" />

<br/>

Overall, optimistic locking may be suitable for this system as concurrency may be high but not very large - since	double booking may still be rare with hotel booking as opposed to Ticketmaster.

#### Expiration time based locking and distributed locks

- We've already talked about these 2 different locking approaches above in 'Improving booking process'.

### Data inconsistency between cache and database

- If using the hotel cache, when the reservation service looks for room availability in the hotel cache, 2 operations	happen:
1. Querying the hotel cache for room availability
2. Updating the Room inventory table with the updated totalReserved value after the booking process completes.

- If the hotel cache is asynchronously updated as shown in ‘Hotel caching’, there may be some			inconsistency between the hotel cache and database. However, this inconsistency will not matter since			reservation requests will still make the final update to the database via optimistic locking or database constraints. The hotel cache is only there to help in speeding up room			availability searches, not storing the exact room availability data is fine. Some data inconsistencies between the cache and database will be fine depending on the consistency we want for displaying room availability. If we want users to always see the latest room availability value in the UI, then the cache can be omitted from the design.

<br/>

Hotel caching:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/b346c2c5-5715-463a-b575-1a43bf7083d8" />

<br/>

### Improving search latencies

- Queries on the database and performing the “LIKE” clause will be very slow for searches because it causes a full table scan. We can improve the search by		using the following and in ‘Improving search latencies’ (these approaches are taken from the SDI 'Ticketmaster - general events'):
  - Indexing and SQL query optimization
  - Full-text indexes in the database
  - Full-text search engine like Elasticsearch:
    - The overall inverted index mappings could be built using the text based hotels, rooms, etc data.

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

### Microservice vs monolithic

- When using a microservice architecture, a service usually has it’s own database it manages. In a monolithic		architecture, multiple services could manage the same database. This is shown in ‘Microservice vs		monolithic’.

- Our design has a hybrid approach, where a single service could still access databases / tables other services could		manage or access. For example, the Reservation service accesses both the Room inventory and Reservations tables.
	We have a hybrid approach, because a pure microservice approach can have consistency issues when			managing transactions. The reservation service accesses multiple databases / tables, and if a transaction fails, then it will	need to roll back the changes in those respective databases / tables. 

- If we used a pure microservice approach, the changes will need to be rolled back in all the databases / tables BY THE SERVICES which manage them instead of by only the reservation service. We cannot only just use a single transaction (within the reservation service) in a pure microservice approach, we’ll need multiple transactions happening within those services as shown in ‘Microservices transactions’. This causes an overhead and may lead to inconsistency issues.

Microservice vs monolithic:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/3ade0c8e-9ae6-48a2-9c86-97686ec1ccd1" />

<br/>
<br/>

Microservices transaction:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/2608a3b6-d161-4205-86ea-5d015a3b5f43" />

### Scaling the system to support large number of users

The stateless servers for the Hotels, Reservation, Hotel management services could be scaled as follows as in 'Scaling API to support high concurrency' (these approaches are taken from the SDI 'Ticketmaster - general events'):

- To scale the API for high concurrency for popular hotels, we’ll use a combination of load balancing, horizontal scaling	and caching as shown in ‘Scaling API to support high concurrency’. To scale, we can cache static data with high reads such as hotels, rooms, etc.

Scaling API to support high concurrency:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/a187b31b-c583-4929-9894-25bdf597455a" />

<br/>
<br/>

The stateless servers could be scaled by adding more servers, but the database and cache will need to be		scaled differently:

#### Database

- We don't necessarily need sharding because the data is small, but if we want to apply sharding, we can apply sharding on the databases by using the regionID and hotelID on the Hotels, Rooms and Room inventory tables. We can likely do this because hotels within the same regionID will be within the same shard, and rooms in the same hotelID will be in the same shard. This way, we'll search through fewer shards during reads. However, we'll also need to ensure that the data is spread evenly across shards, and possibly allocate more shards for more dense regionIDs like NYC.

#### Caching

- In the hotel cache, only the frequently accessed hotels and rooms should be cached using a TTL.				Additionally, the room inventory data for the next 1-2 years could also be cached as the reservation service		will use the room inventory data frequently to check if the room is available or not. Caching the room availability might be preferable if we have large read operations for checking room availability.
	
- If we use both a hotel database and cache, the reservation service could first check the room availability	in the hotel cache, then update the room inventory data in the hotel database. Afterwards, the hotel		database could asynchronously update the hotel cache. In this caching scenario, the hotel cache is used		for fast searches, while the hotel database is the single source of truth. This logic is shown in ‘Hotel		caching’



