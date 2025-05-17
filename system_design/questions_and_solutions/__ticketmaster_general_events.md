# Ticketmaster general events

## Requirements

We’ll design an online ticketing system like Ticketmaster or BookMyShow that sells tickets for events. Ticket booking systems allow users to purchase seats for events and browse through events currently happening

### Questions

- Should we design for different entities such as venues, events, tickets?
  - Yes, consider all of these entities

- Users can browse venues, browse events, select a venue and get all the events currently happening, select an event and find venues for it, and book a seat at a venue. Should our system support all of this?
  - Yes

- Multiple users can “reserve” the same seat - how long should we “reserve” it for them once the booking process starts?
  - 5 mins, then “un-reserve” the seat if they don’t complete the booking process. However, look to improve the design for the	booking experience

- Should we return the exact available seat numbers vs booked seat numbers for a venue and event to the user?
  - Yes, and also show the seating arrangement for a event at a venue

- Should we assume the user is already authenticated for the booking process, and assume payment is managed by a separate service which we don’t need to implement?
  - Yes

- How many tickets do we sell per day? Is this system for a global scale?
  - Let’s assume we sell 100k tickets per day, and it operates for a single region. Let’s focus more on the core functionality of the	design, and not so much on the scalability

- Can users view their booked events, and should the system allow admins to add events?
  - No, let’s leave these out

### Functional

- The system should list venues which they partner with
- The system should also allow users to search for events
- Users can select the venue, and the system should display the events happening at the venue
- Users can also search for an event, and the system should also display venues for that event and it’s available times
- Users should be able to choose an event at a venue, and book the tickets
  - The system should show the user the seating arrangement of the venue. Clients should be able to select multiple seats based on the number of tickets
  - The system should be able to return available seats vs booked seats - return the exact seat numbers which are booked /		available
  - Users can “reserve” the seats and tickets for 5 mins once they start the booking process, however we’ll look to improve on	the booking experience

- Maximum of 10 seats per booking process
- 100k tickets sold per day
- Operates within a single region

### Non-functional

- High throughput / concurrency:
	- There could be multiple booking requests for the same seat, but only the first one will be considered.
	- There could also be high throughput / concurrency during popular events
	- The system will also be read heavy, as more users will view events than book them
- Users should see a consistent view of available tickets / seating

## Data model / entities

- Event:
  - This entity stores event info. There will be a unique entry for each event in this entity

    - eventID	
    - title, description
    - startTime, endTime

- Venue:
  - This entity represents the physical location where an event is held, ie a hall within a theatre or soccer field, etc. It will also	contain the specific seating arrangement / map which will be unique to the venue. The SeatingArrangement entity can be a	separate entity managed in the system

	- venueID
	- location
	- title
	- seatingCapacity
	- seatingArrangement: SeatingArrangement entity

- Ticket:
  - This entity contains tickets for events. A single entry includes info about the ticket, and whenever new events come out for a	venue, there will also be new tickets (depending on the seatingCapacity at the venue) added to this entity.
  - During the booking	process, a ticket will first be AVAILABLE, then RESERVED (if the ticket is in the booking process and is using an expirationTime and non-locking approach discussed in DD), and then BOOKED once the	user completes the booking process and pays

	- ticketID
	- eventID
	- venueID
	- seatNumber
	- price
	- ticketStatus: AVAILABLE / RESERVED (if using an expirationTime and non-locking approach discussed in DD) / BOOKED

- Booking:
  - This entity stores info on the tickets booked by a user. The bookingStatus will be used to represent PENDING vs BOOKED bookings

	- bookingID
	- userID
	- ticketIDs
	- price
	- bookingStatus: PENDING / BOOKED

- Performers (Optional):
  - This entity is also optional, however it will store info on the performers for an event. An entry will only be added when there are	new performers within the system

	- performerID
	- performerName
	- performerDescription

## API design

- Note that we’ll use userID if the user is authenticated and will be booking tickets. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed entries quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Search events

- This endpoint allows users to search for events via a search query, start / end date, and cursor based pagination.

Request:
```bash
GET /events?searchQuery&startDate&endDate&nextCursor={ either using viewport's oldest event startTime OR viewport's last eventID }&limit
```

Response:
```bash
{
  events: [ { eventID, title, description, startTime, endTime } ],
  nextCursor, limit
}	
```

### Get event and tickets

- This endpoint will return the event details and the venue the event will be at, as well as tickets and their statuses for clients to book them.
- We could also return the seating arrangement for the event, so that the client can render the seating arrangement on the UI.

Request:
```bash
GET /events/:eventID
```

Response:
```bash
{
	event: { eventID, title, description, startTime, endTime },
	venue: { venueID, location, title, seatingCapacity, seatingArrangement, ticketsAvailable },
	tickets: [ { ticketID, seatNumber, price, ticketStatus } ]
}
```

### Book ticket

- Usually the booking process is a 2 step process, where the user will first reserve a ticket / seat in the first step, then in the	second step they’ll input their payment details into the provided payment URL within the time limit. Thus we have 2 individual endpoints for these steps below.

#### Reserving a ticket

Request:
```bash
POST /bookings/:eventID
{
	ticketIDs
}
```

Response:
```bash
{
	paymentInputURL
}
```

#### Paying for ticket

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
	bookingIDs, bookingStatus
}
```

## HLD

### API gateway

- As the system will likely use multiple services via a microservice architecture, the API gateway will route requests to the		appropriate service, handle rate limiting and authentication

### Event service

- The event service will handle requests which require querying the database for event, venue, performer, etc data. It will also handle the endpoint 'GET /events/:eventID'

### Database / cache

- The event database will store tables for events, venues, performers (optional), tickets and bookings. Because we’ll benefit	from the ACID guarantees in a SQL database as opposed to a NoSQL database where ACID may be more difficult to set up, we’ll use PostgreSQL. The writes on the		tables requiring transactions / isolation will likely use row-level locking (pessimistic locking) or OCC (optimistic concurrency	control / optimistic locking) via database constraints or another locking approach like a Redis distributed lock. This will prevent	double bookings for the same ticket.

- Additionally, PostgreSQL will provide custom data types and good JSON compatibility for the seating arrangement entity, which will likely	be unique and unstructured for each venue.

#### Cache

- We could maintain a cache, however storing the ticket availability in the cache would be difficult since the ticket status could change frequently, and not be consistent with the database - the DD talks more about data inconsistency between the cache and the database.

- However, we could still cache the event, venue, and performers data which don't change frequently or have concurrency issues behind them. We could likely use Redis for this, since the cached data will likely rely on startTimes, where Redis sorted sets will be helpful in returning events at venues by the startTimes. Additionally, the seating arrangement which will rarely change in a venue can be cached via Redis' maps and lists data structures.

### Search service

- The search service will connect to the database and handle any search queries (in the API endpoint for searching events).	The search service will likely use an inverted index mapping on text based fields such as the events, venues, dates, performers, etc and perform		efficient searching using the mappings. Thus, it could use a tool such as Apache Lucene or Elasticsearch which can maintain	an inverted index mapping for a data store.

### Booking service
  
- The booking service will handle requests for the booking process. It will communicate with the database and a separate		payment service. Once a payment is confirmed, the booking service will update the ticketStatus to BOOKED.

- When a user sends a request to book a ticket, the booking service will likely first check the availability of the ticketID, and	then allocate a lock for the ticketID and add a new entry to the Bookings table (setting the bookingStatus to PENDING). If the	booking is completed, the ticketID will change it’s status to BOOKED and the bookingStatus will change to BOOKED		within a single transaction. If the transaction failed, the whole transaction will be rolled back

<img width="800" alt="image" src="https://github.com/user-attachments/assets/9fb9acad-4c59-495f-b77e-7c78369a1749" />

## DD

### Improving booking process
  
- Setting the seatStatus to RESERVED and starting a timer once a user initiates their booking process is a common approach	in multiple booking / ordering / payment processing apps. This approach is used because no user wants to enter their payment	info, then find out later that a seat has already been booked. Thus we have a timer and temporarily “reserve” their seats.

- To design for this 5 min timer and temporarily setting the seat to “RESERVED”, we can try out the below solutions	and in ‘Temporarily reserving seat / ticket solutions’:
  - Pessimistic locking:
    - Pessimistic locking is usually not a good approach as it can cause deadlocks if there’s high concurrency. Also the			locked rows within the “SELECT FOR UPDATE” or data locking mechanism will prevent other processes from				reading ("SELECT FOR UPDATE" blocks the reads) the locked rows which the user is updating via the “SELECT FOR UPDATE”. Also, if database instances			crashed during the pessimistic locking process, then some rows may still be in a locked state.
		
  - Status and expiration time with cron
  - Implicit status with status and expiration time:
    - In this approach, the ticket entry will contain both the ticketStatus (AVAILABLE / RESERVED / BOOKED) and 			expirationTime. When a booking process starts, it will check if the ticketStatus is either AVAILABLE OR if it is				RESERVED but the expirationTime has already passed. If either of these two options is the case, then the				transaction will be committed. The SQL transaction for these two checks is shown in ‘SQL transaction for				ticketStatus and expirationTime’. A separate cron job could also clean up any rows with old expirationTimes to 				improve read times. To improve reads, we can also index on the ticketStatus.

  - Redis distributed lock with TTL:
    - Redis allows us to implement a distributed lock with a TTL, where a lock for a ticketID could be acquired in Redis			with a TTL,	and this TTL will act as the expiration time. If the lock expires, Redis will release the lock and other				processes could operate on the entry. This way, the ticketStatus only has two states: AVAILABLE / BOOKED.
			During the booking process, the ticketStatus will remain AVAILABLE, but the lock will prevent other	processes from			updating that ticketID.
    - The Redis lock will be for a ticketID and userID, and it will prevent other processes from updating the ticketID				during the TTL. This way, the ticketID is locked only	for that specific userID, as it should be.
			
    - However, if a lock goes down, then there will be some time until a new lock is up - in this time, the first user to 			complete their booking process and pay will get the ticket, so if the lock is down, it’s first come first serve. However,			there will still be no double bookings since the database will use OCC or database constraints to ensure any writes			do not produce double bookings. We’ll go with this Redis distributed lock with TTL approach where the lock will			be for a userID and ticketID.

    - Using the Redis distributed lock with TTL approach, when a user wants to book a ticket, they’ll select a seat with a ticketID	from the seat map, and send a request to the booking service. The booking service will lock that ticketID with a TTL by adding	it to our Redis Distributed Lock. The booking service will also add a new entry to the Bookings table with a bookingStatus of 	PENDING. The user’s request will then be routed to a payment service, and if the user cancels or doesn’t complete the 		booking process, the lock will be released after the TTL. If the booking process completes, the ticketStatus will change to		BOOKED, and the bookingStatus will change to BOOKED within a single transaction.

SQL transaction for ticketStatus and expirationTime:
```sql
–- Serializable is usually the highest isolation level provided by most SQL transactions and will prevent: 
-- Dirty reads (reads in a transaction, during the time the read data has been modified by another transaction)
-- Non-repeatable reads (when the same transaction reads the same row twice, but gets 2 different results because of some		change)
-- Phantom reads (when the same transaction returns different results for the same query multiple times - it usually occurs when		other transactions modify the same data concurrently)

set transaction isolation level serializable;
begin;

select * from tickets
where ticketID in ${ticketIDs} and (ticketStatus = 'AVAILABLE' or (ticketStatus = ‘RESERVED’ and (time.now() - expirationTime) > 5))

-- if the number from the select above is less than the number of tickets we want to reserve, then rollback

update tickets set ticketStatus = 'RESERVED' and expirationTime = time.now() + 5
where ticketID in ${ticketIDs}

insert into bookings values (${ticketIDs}, ${userID}, ‘BOOKED’, ${price})

commit;
```

<br/>

Temporarily reserving seat / ticket solutions:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/49ac5025-e397-4919-a806-89ebd93c48b2" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/c876b85a-218f-4474-8084-b301b87404a4" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/b6c984f7-3ae2-45a3-96b7-75074a6211a9" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/8829d991-ff39-4ac3-869b-574af86ee6c5" />

<br/>

### Scaling the system to support high concurrency of booking tickets

- Under a high concurrency of booking processes, the seat map and ticket availability data will become stale very quickly. Note	that the admins will only enable these below to support very high concurrency, thus these approaches can be enabled only for	very high concurrency cases. We can ensure this data is up to date by using the below and in ‘Supporting high concurrency of	booking tickets’:
  - SSE for real-time seat updates:
    - SSE events will be pushed to the clients in real-time to update the seat map as soon as a seat is booked or 				available. Thus, the user wouldn’t need to refresh their page.
    - SSE events will work well for moderately popular events, but for events with high concurrency such as for				Weeknd’s concerts, the SSE approach will be slow to update the clients since it is still using HTTP, which will be slower than using websockets.

  - Virtual waiting queue and websocket for extremely popular events:
    - Users requesting to view the booking page for a very popular event will be placed in a virtual waiting queue, and			they will request to establish a websocket connection with the booking service. Dequeued users will be notified				using the websocket that they can proceed with the booking process (via the Redis distributed lock approach). The			queued users will also be notified of their position of the queue and estimated wait times (wait time calculated				using	the distributed lock's TTL) using the websocket. 

    - The queue could be implemented using traditional message queues such as SQS. The Booking service can likely maintain workers (containers) which will pull from SQS, where the message will have a visibility timeout applied to ensure exactly-once delivery. When the worker pulls the message, the booking process can initiate via the worker, and if the booking process completes, then the message will be deleted by default. However, if the worker doesn't complete the booking process, then the message could likely be deleted OR sent to the back of the queue using SQS's delayed message delivery feature.
		
  - Note that we could also use long polling to get updates from the server about seat availability,		which is simple. However, if users sit on the “seat availability page” for a long time, then it will eat up resources on the		server.

Supporting high concurrency of booking	tickets:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/f998b898-8533-41a7-bc39-d3630aab6a70" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/0f89e9b2-e043-4ce0-9267-7e16ad012a8b" />

<br/>

### Improving search latencies
  
- Queries on the database and performing the “LIKE” clause will be very slow for searches because it causes a full table scan. We can improve the search by		using the following and in ‘Improving search latencies’:
  - Indexing and SQL query optimization
  - Full-text indexes in the database
  - Full-text search engine like Elasticsearch:
    - The overall inverted index mappings could be built using the event title / description, venue title / location, date,			performer, etc.

Improving search latencies:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/babcfe37-e54c-49b5-a586-099d39f3dc3b" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/981fb13b-eadc-4caa-9e78-2c37d396b2e3" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/75f5eaff-8632-4602-beb2-ff17abdaf732" />

<br/>
<br/>

- Also, the frequent search queries could be cached to improve latencies using the below and in ‘Caching search queries’:
  - Implement caching strategies using Redis / Memcached
  - Implement query result caching and edge caching:
    - Elasticsearch has built-in node level caching that can store search query results. AWS Opensearch, which can			run an instance of Elasticsearch also provides node level caching of search query results. Also we could utilize				CDNs to cache search results geographically closer to the user.

Caching search queries:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/b84bd197-fb69-4a8e-892b-2973c33d2d14" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/bcbab7ff-0098-4def-8b5f-7d872ae9342f" />

<br/>

### Concurrency issues during bookings and different types of locking techniques

Concurrency issues might arise during double bookings where different users could book the same ticketID for the same time concurrently. If same ticketID and date is reserved at the same time by 2 different		users, a race condition will likely be produced. The solution to these concurrent issues might require some form of locking:

#### Pessimistic locking

- Pessimistic locking also called pessimistic concurrency control prevents simultaneous updates by placing		a lock on a record as soon as a user starts updating it. Other users trying to update the record will have to		wait for the user to release the lock on the record. Both PostgreSQL and MySQL provides the “SELECT			FOR UPDATE” clause. The syntax is shown in ‘SELECT FOR UPDATE SQL’ (taken from the SDI 'Hotel reservation system'). This clause locks the			selected rows and prevents other transactions from updating them until the transaction is committed or			rolled back.

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

#### Optimistic locking

- Optimistic locking also called optimistic concurrency control allows multiple concurrent users to update the		same record. Optimistic locking can be implemented using either a version number or timestamp. A version		number may be preferred since clocks need to be synchronized. If 2 users read the same record, and			update it at the same time, the version numbers will be used to determine if there was a conflict.

- Let’s say user1 and user2 reads and updates the same record with version1, and the version increases to		version2 at the same time. Upon committing the transaction, the transaction will check if version2 does not		already exist - and rollback if version2 exists. This is shown in ‘Optimistic locking’ (taken from the SDI 'Hotel reservation system')

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

<img width="700" alt="image" src="https://github.com/user-attachments/assets/e1347317-2d4f-4ff9-af62-1e3ac38b77f8" />

#### Database constraints

- Using database constraints is similar to optimistic locking. A SQL constraint similar to the one shown in ‘Database			constraint’ (taken from the SDI 'Hotel reservation system') could be added to the Tickets and Bookings table, where we check that the Bookings table doesn't contain 2 different rows which have the same ticketID - which means that there is a double booking for the same ticketID. When transactions are being made, and they violate the		constraint, the transaction is rolled back. This is shown in ‘Database constraint’ (taken from the SDI 'Hotel reservation system')

- The pros of database constraints is that it’s easy to implement and works well when the number of			concurrent operations is not as high.

- The cons of database constraints is similar to optimistic locking, where it can cause repeated retries if			transactions are rolled back. Also, the updates from database constraints cannot be versioned like				optimistic locking. Additionally, not all databases provide database constraints, however PostgreSQL and		MySQL both support it.

Database constraints:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/324c1cce-4a3b-4869-b8a6-464d474d4e99" />

#### Expiration time based locking and distributed locks

- We've already talked about these 2 different locking approaches above in 'Improving booking process'.

<br/>

Overall, after exploring all of these different transactions and locking approaches, we'll go with using the Redis distributed lock in this design.

<br/>

### Data inconsistency between cache and database

- If we are storing the tickets and bookings data in the cache, when the Booking service looks for ticket availability in this cache, 2 operations	happen:
1. Querying the cache for ticket availability
2. Updating the database with the ticket availability and booking status after the booking status completes.

- If the cache is asynchronously updated as shown in ‘Hotel / ticket caching’ (taken from the SDI 'Hotel reservation system'), there may be some			inconsistency between the cache and database. However, this inconsistency will not matter as much since			booking requests will ultimately still make the final update to the database via a locking approach. The cache is only there to help in speeding up ticket			availability searches, not storing the exact ticket availability data is fine depending on the consistency we want for displaying ticket availability. If we want users to always see the latest ticket availability value in the UI, then the cache can be omitted from the design.

Hotel / ticket caching:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/b45f477c-737f-47d1-baed-dfbfe36cf43d" />

### Microservice vs monolithic

- When using a microservice architecture, a service usually has it’s own database it manages. In a monolithic		architecture, multiple services could manage the same database. This is shown in ‘Microservice vs		monolithic’ (taken from the SDI 'Hotel reservation system').

- Our design has a hybrid approach, where a single service could still access databases or tables other services could		manage or access. For example, the booking service accesses both the tickets and bookings tables.
	We have a hybrid approach, because a pure microservice approach can have consistency issues when			managing transactions. The booking service accesses multiple tables / databases, and if a transaction fails, then it will	need to roll back the changes in those respective databases / tables. 

- If we used a pure microservice approach, the changes will need to be rolled back in all the databases BY THE SERVICES which manage them instead of by only the booking service. We cannot only just use a single transaction (within the booking service) in a pure microservice approach, we’ll need multiple transactions happening within those other services as shown in ‘Microservices transactions’ (taken from the SDI 'Hotel reservation system'). This causes an overhead and may lead to inconsistency issues.

Microservice vs monolithic:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/3ade0c8e-9ae6-48a2-9c86-97686ec1ccd1" />

<br/>
<br/>

Microservices transaction:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/2608a3b6-d161-4205-86ea-5d015a3b5f43" />

### Scaling the API to support large number of users

- To scale the API for high concurrency during popular events, we’ll use a combination of load balancing, horizontal scaling	and caching as shown in ‘Scaling API to support high concurrency’. To scale, we can cache static data with high reads such as	events, venues, performers, etc.

Scaling API to support high concurrency:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/a187b31b-c583-4929-9894-25bdf597455a" />


