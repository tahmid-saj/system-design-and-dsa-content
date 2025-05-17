# Coupon provider

Design a coupon provider for generating a set amount of coupons and keeping track of the generated coupons. Users should also be able to redeem the coupons (in exchange for a product / service) they retrieved from the system.

## Requirements

### Questions

- Are we designing both coupon generation and redeeming of coupons?
  - Yes, design both

- For a specific coupon, are we generating a fixed amount of coupon instances and giving them to different users?
  - Yes
 
- By tracking the generated coupons, are we tightly linking the generated coupons to a specific userID, or is this like a coupon code that anyone can receive (and isn't tightly linked to any specific userID)?
  - Because these will be digital coupons, let's tightly link them to users

- When are coupons no longer valid, is it after an expirationTime, after they've been redeemed of course, etc?
  - Coupons past the expirationTime or if redeemed already won't be valid

- What is the DAU and how many concurrent users will there be?
  - Assume 100M DAU and 20k concurrent users

### Functional

- The system should generate a fixed amount of coupon instances
- Users should be able to retrieve and redeem coupons which are tightly linked to said user
- When users redeem a coupon, validate if it's expired or was already redeemed

<br/>

- Assume 100M DAU and 20k concurrent users

### Non-functional

- Throughput / consistency in users retrieving and redeeming coupons:
  - When users retrieve coupons, we need to make sure the coupon is valid and are still "in-stock" - and we also need to update our coupon inventory (we don't want a user to retrieve a coupon, then later find out that they can't redeem it because it was not in-stock or was not valid when they retrieved it)
  - When users redeem coupons, we need to make sure the coupon is valid
- Concurrency conflicts in coupon retrieval / redeeming

## Data model / entities

- Users:
  - userID
  - userName
  - userEmail
    
- Coupons:
    - Contains the coupon "blueprint" with the couponID, totalGenerated, totalRedeemed fields
    - When a userID is using the coupon, the server needs to check if totalRetrieved < totalGenerated and totalRedeemed < totalGenerated so we know that the same amount of generated coupons are being used and users aren’t cheating the system via race conditions
    - If the couponID was not linked to the userID, then verifying if totalRetrieved < totalGenerated and totalRedeemed < totalGenerated could also be used in this case to ensure the same number of generated coupons are redeemed
    - When a new coupon "blueprint" is added to this entity, then a user can retrieve a coupon instance - then the coupon instance retrieved by the user will be populated in the Users coupons entity
      - couponID
      - totalGenerated, totalRetrieved, totalRedeemed
      - couponCode (ask the interviewer if the couponCode is the same or different for every coupon instance), details
      - expirationTime

- Users coupons:
    - This entity contains the coupon instances belonging to a userID, and will be used to set the couponStatus to REDEEMED when it’s redeemed by the userID
      - couponInstanceID
      - couponID
      - userID
      - couponStatus: NOT_REDEEMED / REDEEMED

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed messages quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### System generates coupons

- This endpoint will allow admins to generate new coupon blueprints in the Coupons entity

Request:
```bash
POST /coupons -> true / false
{
  totalGenerated,
  couponCode, details,
  expirationTime
}
```

### Retrieve coupon instance

- This endpoint will allow users to retrieve a coupon (retrieving a coupon is not the same as redeeming a coupon - retrieval means that the coupon's instance is now linked to the user)
- This endpoint will also create a new entry for the coupon instance in the Users coupons entity, and will increase the Coupons entity's totalRetrieved field by 1

Request:
```bash
POST /coupons/:couponID/instances -> true / false
```

### Redeem coupon instance

- Users can redeem a coupon instance with this endpoint. If the coupon instance is valid, then the couponStatus will change to REDEEMED, and the totalRedeemed field of the Coupons entity will be increased by 1. Otherwise, if not valid, the couponStatus will remain as NOT_REDEEMED (or REDEEMED if it was already REDEEMED).

Request:
```bash
PATCH /coupons/:couponID/instances/:couponInstanceID
```

Response:
```bash
{
  success / failure depending on if the coupon instance is valid
}
```

<br/>

Note: We could also have more endpoints for searching available coupons, listing the user's coupons, viewing a coupon's details, etc, but this is not a focus for this system

## HLD

### API gateway

- As the system will likely use multiple services via a microservice architecture, the API gateway will route requests to the appropriate service, handle rate limiting and authentication

### Coupon service

- The Coupon service will handle generating and retrieving coupons, via the endpoints 'POST /coupons' and 'POST /coupons/:couponID/instances'. When new coupons are generated, new coupon entries will be added to the Coupons table. When new coupon instances are retrieved by users, new coupon instance entries will be added to the Users coupons table, and the totalRetrieved is increased by 1.

### Database

- The database will store the Coupons and Users coupons tables. Because we'll benefit from the ACID guarantees in a SQL database as opposed to a NoSQL database where ACID may be more difficult to set up, we'll use PostgreSQL. The writes on the tables requiring transactions / isolation (when users retrieve OR redeem a coupon) will likely use row-level locking (pessimistic locking) or OCC (optimistic concurrency control / optimistic locking) via database constraints or another locking approach like a Redis distributed lock.
- This will prevent race conditions when multiple users try updating the totalRedeemed field for the same coupon. Using transactions / locking will also ensure the couponStatus can either fail / succeed by going from NOT_REDEEMED to REDEEMED when users redeem a coupon instance.

- When a user has already retrieved a coupon instance for a specific couponID, then depending on our product choice, we could allow it or allow only a single coupon instance per couponID for each user. 

### Redeem service

- The Redeem service will allow users to redeem a coupon instance via the endpoint 'PATCH /coupons/:couponID/instances/:couponInstanceID'. The Redeem service will also validate if the coupon instance is valid or not (if it's past the expirationTime or if the coupon instance was already REDEEMED). The Redeem service will also increase the totalRedeemed by 1.

- The totalRetrieved and totalRedeemed is there to ensure we're not allowing users to retrieve / redeem more coupons than we generated (or we might be losing money because our system allows users to retrieve an infinite amount of coupons) 

<br/>

The process for generating a coupon, retrieving a coupon instance and redeeming a coupon instance will then be as follows:

1. Admins will generate new coupons in the Coupons table via the Coupon service

2. Users will retrieve a couponID from the Coupons table via the Coupon service, and thus create a new entry in the Users coupons table (and increase totalRetrieved by 1) for the coupon instance. The Coupon service might also validate if the user had already retrieved a coupon instance before for the same couponID.

3. Users will redeem a couponInstanceID from the Users coupons table via the Redeem service. The Redeem service will set the couponStatus to REDEEMED if the coupon instance is valid. The Redeemed service will also increase totalRedeemed by 1 in a transaction.

<img width="1000" alt="image" src="https://github.com/user-attachments/assets/90c81aeb-85f0-4e06-af9d-61a681eb148f" />

## DD

### Admins generating new coupons

- Either admins or a cron job could regularly generate new coupon blueprints in the Coupons table. The cron job could use a similar insert statement below:

```sql
insert into coupons (couponID, totalGenerated, totalRetrieved, totalRedeemed, couponCode, expirationTime)
values (:couponID, 100, 0, 0, :couponCode, :expirationTime)
```

<br/>

### Concurrency issues when retrieving and redeeming coupon instances, and different types of locking techniques

Concurrency issues might arise when retrieving and redeeming coupon instances, where the same user might try to retrieve multiple coupon instances for the same couponID, or when multiple users might update the totalRetrieved and totalReserved for the same couponID, etc. In these scenarios, a race condition might happen, and the solution to it might require some form of locking:

#### Pessimistic locking

- Pessimistic locking also called pessimistic concurrency control prevents simultaneous updates by placing		a lock on a record as soon as a user starts updating it. Other users trying to update the record will have to		wait for the user to release the lock on the record. Both PostgreSQL and MySQL provides the “SELECT			FOR UPDATE” clause. The syntax is shown in ‘SELECT FOR UPDATE SQL - for retrieving coupon instances’ and 'SELECT FOR UPDATE SQL - for redeeming coupon instances' (taken from the SDI 'Hotel reservation system'). This clause locks the			selected rows and prevents other transactions from updating them until the transaction is committed or			rolled back.

- Pessimistic locking is usually not a good approach as it can cause deadlocks if there’s high concurrency. Also the locked rows within the “SELECT FOR UPDATE” or data locking mechanism will prevent other processes from reading ("SELECT FOR UPDATE" blocks the reads) the locked rows which the user is updating via the “SELECT FOR UPDATE”. Also, if database instances crashed during the pessimistic locking process, then some rows may still be in a locked state.

- The pros of this approach is that is uses strict locking on rows and ensures highly consistent data.
- The cons of this approach is that deadlocks may occur when multiple resources are being locked.				However, writing deadlock-free code can be challenging. When multiple transactions need to be made, this		approach is not scalable as multiple records will be locked. Also, if database instances			crashed during the pessimistic locking process, then some rows may still be in a locked state.

SQL FOR UPDATE SQL - for retrieving coupon instances:
```sql
begin;

select couponID, totalRetrieved, totalRedeemed from coupons
where couponID = :couponID and totalRetrieved < totalGenerated and totalRedeemed < totalGenerated
for update

update coupons
set totalRetrieved = totalRetrieved + 1
-- we need to check if the totalRetrieved < totalGenerated
where couponID = :couponID and totalRetrieved < totalGenerated;
-- if nothing was updated from the previous step, then rollback:
rollback;

insert into usersCoupons (couponInstanceID, couponID, userID, couponStatus)
values (:couponInstanceID, :couponID, :userID, 'NOT_REDEEMED');

commit;
```

SQL FOR UPDATE SQL - for redeeming coupon instances:
```sql
begin;

select couponID, totalRetrieved, totalRedeemed from coupons
where couponID = :couponID and totalRetrieved < totalGenerated and totalRedeemed < totalGenerated
for update

update coupons
set totalRedeemed = totalRedeemed + 1
-- we need to check if the totalRedeemed < totalGenerated
where couponID = :couponID and totalRedeemed < totalGenerated;
-- if nothing was updated from the previous step, then rollback:
rollback;

update usersCoupons
set couponStatus = 'REDEEMED'
-- we need to check if the couponInstanceID expired or was already RESERVED;
where couponInstanceID = :couponInstanceID and couponStatus = 'NOT_REDEEMED' and time.now() <= expirationTime
-- if nothing was updated from the previous step, then rollback:
rollback;

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

- Using database constraints is similar to optimistic locking. A SQL constraint similar to the one shown in ‘Database			constraint’ (taken from the SDI 'Hotel reservation system') could be added to the Coupons table, where we check that the Coupons table doesn't have totalRetrieved > totalGenerated or totalRedeemed > totalGenerated (we could also check if the Users coupons table contains a userID with multiple coupon instances for the same couponID) - which means that there might've been race conditions. When transactions are being made, and they violate the		constraint, the transaction is rolled back. This is shown in ‘Database constraint’ (taken from the SDI 'Hotel reservation system')

- The pros of database constraints is that it’s easy to implement and works well when the number of			concurrent operations is not as high.

- The cons of database constraints is similar to optimistic locking, where it can cause repeated retries if			transactions are rolled back. Also, the updates from database constraints cannot be versioned like				optimistic locking. Additionally, not all databases provide database constraints, however PostgreSQL and		MySQL both support it.

Database constraints:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/324c1cce-4a3b-4869-b8a6-464d474d4e99" />

<br/>
<br/>

A database constraint for the Coupons and Users tables could look like:

```sql
-- Coupons table:
constraint 'checkTotalRetrieved' check((totalRetrieved < totalGenerated))
constraint 'checkTotalRedeemed' check((totalRedeemed < totalGenerated))

-- Users coupons table:
constraint 'checkDuplicateCouponInstance'
check(couponInstanceID not in (select instanceID from usersCoupons where userID = :userID))
```

<br/>

#### Expiration time based locking and distributed locks

- These locking strategies might not be relevant for this design, however, they're discussed in the Resource notes.

<br/>

Overall, after exploring all of these different transactions and locking approaches, we could go with using either OCC or database constraints as they don't directly lock rows, and allow us to rollback transactions if certain constraints were not met. The downside to them would be that they require the user to send retries, but write latency increases for a few users might be more favorable than locking a single couponID entry when multiple users might be waiting to update the couponID's fields like totalRetrieved, totalRedeemed, etc.

<br/>
<br/>

### Caching recent and popular coupons for read latency

- Recent and popular coupons could also be cached to improve the read latency, however storing the coupon availability data (from the Coupons table) in the cache would be difficult since the totalRetrieved and totalRedeemed fields could change frequently, and not be consistent with the database.

- However, we could still cache the static content of the Coupons table, like the couponID, couponCode, description, etc, if we need to allow the Coupon service to support listing and searching coupons.

#### Data inconsistency between cache and database

If we are storing the coupon availability data in the cache, when the Coupon service looks for coupon availability in this cache, 2 operations	happen:

1. Querying the cache for coupon availability
2. Updating the database with the coupon availability (totalRetrieved and totalRedeemed) and couponStatus after a coupon is redeemed.

- If the cache is asynchronously updated as shown in ‘Hotel / coupon caching’ (taken from the SDI 'Hotel reservation system'), there may be some			inconsistency between the cache and database. However, this inconsistency will not matter as much since			redeem requests will ultimately still make the final update to the database via OCC / database constraints. The cache is only there to help in speeding up coupon			availability searches, not storing the exact coupon availability data is fine depending on the consistency we want for displaying coupon availability. If we want users to always see the latest coupon availability value in the UI, then the cache can be omitted from the design.

Hotel / coupon caching:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/b45f477c-737f-47d1-baed-dfbfe36cf43d" />

<br/>
<br/>

### Microservice vs monolithic

- When using a microservice architecture, a service usually has it’s own database it manages. In a monolithic		architecture, multiple services could manage the same database. This is shown in ‘Microservice vs		monolithic’ (taken from the SDI 'Hotel reservation system').

- Our design has a hybrid approach, where a single service could still access databases or tables other services could		manage or access. For example, the Coupon service accesses both the Coupons and Users coupons tables.
	We have a hybrid approach, because a pure microservice approach can have consistency issues when			managing transactions. The Coupon service accesses multiple tables / databases, and if a transaction fails, then it will	need to roll back the changes in those respective databases / tables. 

- If we used a pure microservice approach, the changes will need to be rolled back in all the databases BY THE SERVICES which manage them instead of by only the Coupon service. We cannot only just use a single transaction (within the Coupon service) in a pure microservice approach, we’ll need multiple transactions happening within those other services as shown in ‘Microservices transactions’ (taken from the SDI 'Hotel reservation system'). This causes an overhead and may lead to inconsistency issues.

Microservice vs monolithic:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/3ade0c8e-9ae6-48a2-9c86-97686ec1ccd1" />

<br/>
<br/>

Microservices transaction:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/2608a3b6-d161-4205-86ea-5d015a3b5f43" />

<br/>
<br/>

### Scaling the API to support large number of users

- To scale the API for high concurrency during popular events, we’ll use a combination of load balancing, horizontal scaling	and caching as shown in ‘Scaling API to support high concurrency’ (taken from the SDI 'Ticketmaster'). To scale, we can cache static data from the Coupons table (couponID, couponCode, description) which might have high reads.

Scaling API to support high concurrency:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/a187b31b-c583-4929-9894-25bdf597455a" />

#### Sharding / partitioning database

- We could likely shard / partition the Coupons table by a "topic" field, so that if a user does search for available coupons for a specific topic, then the request will only be sent to a single shard / partition.

- We could also shard / partition the Users coupons table by the userID, so that if a user wants to view all their coupon instances, then the request will only be sent to a single shard / partition. It might not help if we shard / partition the users coupons table by the couponID because there will always be a distinct couponID for a specific userID - the same userID can't retrieve multiple coupon instances for the same couponID.














