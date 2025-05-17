# Transactions and locking

This resource note goes over the different types of transactions and locking techniques.

**Note that the following concepts are taken from the SDI 'Hotel reservation system' and 'Ticketmaster - general events'**

## Transaction techniques

### Creating a transaction in SQL to select and update a table

In SQL, a transaction groups a set of operations so that they are executed as a single unit of work. If any operation fails, the transaction can be rolled back to maintain data integrity.

Here’s how you can create a transaction to SELECT and then UPDATE a table:

```sql
BEGIN;

-- Lock the row for update
SELECT * FROM my_table
WHERE id = 1
FOR UPDATE;

-- Update the locked row
UPDATE my_table
SET column_name = 'new_value'
WHERE id = 1;

-- Commit the transaction
COMMIT;
```

- BEGIN:
  - Starts the transaction.
    
- SELECT ... FOR UPDATE:
  - Locks the selected row(s) to ensure no other transaction modifies it until the current transaction ends.
    
- UPDATE:
  - Modifies the locked rows.
    
- COMMIT:
  - Confirms the changes made in the transaction.
    
- ROLLBACK (if needed):
  - Reverts changes if an error occurs.

### Different types of SQL transactions


Let's first go over the different types of reads. Transaction isolation levels are a measure of the extent to which transaction isolation succeeds. In particular, transaction isolation levels are defined by the presence or absence of the following phenomena:

**Dirty Reads**:
- A dirty read (uncommitted change) occurs when a transaction reads data that has not yet been committed. For example, suppose transaction 1 updates a row. Transaction 2 reads the updated row before transaction 1 commits the update. If transaction 1 rolls back the change, transaction 2 will have read data that is considered never to have existed.

**Nonrepeatable Reads**:
- A nonrepeatable read occurs when a transaction reads the same row twice but gets different data each time. For example, suppose transaction 1 reads a row. Transaction 2 updates or deletes that row and commits the update or delete. If transaction 1 rereads the row, it retrieves different row values or discovers that the row has been deleted.

**Phantom reads**:
- A phantom is a row that matches the search criteria but is not initially seen. For example, suppose transaction 1 reads a set of rows that satisfy some search criteria. Transaction 2 generates a new row (through either an update or an insert) that matches the search criteria for transaction 1. If transaction 1 reexecutes the statement that reads the rows again within the transaction (re-executes the same read statement again and now get's a different output), it gets a different set of rows.

SQL transactions are categorized based on isolation levels, which determine how transactions interact with each other. These are the different types of transactions:

#### Read Uncommitted

- Allows reading uncommitted changes from other transactions (dirty reads).
- Fastest but least consistent.
- Example issue: A query might see intermediate states of data.

#### Read Committed

Read Committed is the default isolation level in PostgreSQL. When a transaction runs on this isolation level, a SELECT query sees only data committed before the query began and never sees either uncommitted data or changes committed during query execution by concurrent transactions.

- Only reads data committed by other transactions.
- Prevents dirty reads but allows non-repeatable reads (data can change between reads since a transaction could be comitted between two reads).

#### Repeatable Read

Repeatable Read in PostgreSQL provides stronger guarantees than the SQL standard requires. It creates a consistent snapshot of the data as of the start of the transaction, and unlike other databases, PostgreSQL's implementation prevents both non-repeatable reads AND phantom reads. This means not only will the same query return the same results within a transaction, but no new rows will appear that match your query conditions - even if other transactions commit such rows.

- Ensures the same rows read during the transaction cannot change (prevents dirty reads and non-repeatable reads).
- Does not prevent phantom reads (new rows added during the transaction) - however, PostgreSQL's implementation of repeatable read prevents phantom reads.

#### Serializable

Serializable is the strongest isolation level that makes transactions behave as if they were executed one after another in sequence. This prevents all types of concurrency anomalies but comes with the trade-off of requiring retry logic in your application to handle transaction conflicts.

- Highest level of isolation.
- Ensures no other transaction can insert, update, or delete rows being used.
- Prevents all concurrency issues (phantom reads, non-repeatable reads, dirty reads).
- Often slower due to the strict locking.

Note: PostgreSQL's implementation of Repeatable Read is notably stronger than what the SQL standard requires. While other databases might allow phantom reads at this isolation level, PostgreSQL prevents them. This means you might not need Serializable isolation in cases where you would in other databases.

Note: Row-level locking (via SELECT FOR UPDATE) is generally preferred when you know exactly which rows need to be locked. Save serializable isolation for cases where the transaction is too complex to reason about which locks are needed.

Overall, below is a summary:

<img width="800" alt="image" src="https://github.com/user-attachments/assets/fbe75703-3d57-4c0d-a0e8-f58537731190" />

### Different ways of performing transactions

#### SELECT FOR UPDATE

- Locks rows to ensure that no other transaction can modify them until the current transaction ends.
- Use Case: Preventing race conditions when modifying data based on a selection.

```sql
BEGIN;

-- Lock rows for update
SELECT * FROM accounts
WHERE balance > 1000
FOR UPDATE;

-- Perform updates
UPDATE accounts
SET balance = balance - 100
WHERE balance > 1000;

COMMIT;
```

#### Optimistic concurrency control

- Instead of locking rows, use a version column or a timestamp to detect conflicts during updates.

```bash
-- Read with version
SELECT id, name, version
FROM users
WHERE id = 1;

-- Update only if version matches
UPDATE users
SET name = 'new_name', version = version + 1
WHERE id = 1 AND version = 5;
```

#### Savepoints

- Allows partial rollbacks within a transaction.
- Use Case: Complex workflows where you might need to backtrack only part of a transaction.

```sql
BEGIN;

-- Insert a row
INSERT INTO orders (id, status) VALUES (1, 'pending');

SAVEPOINT step1;

-- Try another operation
INSERT INTO payments (order_id, amount) VALUES (1, 100);

-- Rollback to the savepoint if something goes wrong
ROLLBACK TO SAVEPOINT step1;

COMMIT;
```

#### Explicit locking with advisory locks

- Use PostgreSQL-specific advisory locks to ensure application-level locking for resources.

```sql
-- Acquire a lock
SELECT pg_advisory_lock(12345);

-- Perform operations
UPDATE my_table SET status = 'locked' WHERE id = 1;

-- Release the lock
SELECT pg_advisory_unlock(12345);
```

#### Autonomous transactions

- Supported in some databases (like Oracle), these allow running a separate transaction within the context of another.

#### Transactions key considerations

- Atomicity:
  - Ensure the transaction completes entirely or rolls back fully.

- Consistency:
  - Maintain data integrity before and after the transaction.

- Isolation:
  - Choose the appropriate isolation level to prevent concurrency issues.

- Durability:
  - Ensure changes are permanently saved after the transaction commits.

- Error Handling:
  - Use ROLLBACK in case of errors.

## Locking techniques

Concurrency issues might arise during double bookings where different users could book the same ticketID for the same time concurrently. If same ticketID and date is reserved at the same time by 2 different		users, a race condition will likely be produced. The solution to these concurrent issues might require some form of locking:

#### Pessimistic locking

- Pessimistic locking also called pessimistic concurrency control prevents simultaneous updates by placing		a lock on a record as soon as a user starts updating it. Other users trying to update the record will have to		wait for the user to release the lock on the record. Both PostgreSQL and MySQL provides the “SELECT			FOR UPDATE” clause. The syntax is shown in ‘SELECT FOR UPDATE SQL’ (taken from the SDI 'Hotel reservation system'). This clause locks the			selected rows and prevents other transactions from updating them until the transaction is committed or			rolled back. This process is shown in ‘SELECT FOR UPDATE Pessimistic locking’

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

- Let’s say user1 and user2 reads and updates the same record with version1, and the version increases to		version2 at the same time. Upon committing the transaction, the transaction will check if version2 does not		already exist - and rollback if version2 exists. This is shown to the right in ‘Optimistic locking’

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

<br/>
<br/>

#### Database constraints

- Using database constraints is similar to optimistic locking. A SQL constraint similar to the one shown in ‘Database			constraint’ could be added to the Tickets and Bookings table, where we check that the Bookings table doesn't contain 2 different rows which have the same ticketID - which means that there is a double booking for the same ticketID. When transactions are being made, and they violate the		constraint, the transaction is rolled back. This is shown in ‘Database constraint’

- The pros of database constraints is that it’s easy to implement and works well when the number of			concurrent operations is not as high.

- The cons of database constraints is similar to optimistic locking, where it can cause repeated retries if			transactions are rolled back. Also, the updates from database constraints cannot be versioned like				optimistic locking. Additionally, not all databases provide database constraints, however PostgreSQL and		MySQL both support it.

Database constraints:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/324c1cce-4a3b-4869-b8a6-464d474d4e99" />

<br/>
<br/>

#### Implicit status with status and expiration time:
  
- In this approach, the ticket entry will contain both the ticketStatus (AVAILABLE / RESERVED / BOOKED) and 			expirationTime. When a booking process starts, it will check if the ticketStatus is either AVAILABLE OR if it is				RESERVED but the expirationTime has already passed. If either of these two options is the case, then the				transaction will be committed. The SQL transaction for these two checks is shown in ‘SQL transaction for				ticketStatus and expirationTime’. A separate cron job could also clean up any rows with old expirationTimes to 				improve read times. To improve reads, we can also index on the ticketStatus.

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

insert into bookings values (${ticketIDs}, ${userID}, ‘CONFIRMED’, ${price})

commit;
```

<img width="700" alt="image" src="https://github.com/user-attachments/assets/b6c984f7-3ae2-45a3-96b7-75074a6211a9" />

<br/>
<br/>

#### Redis distributed lock with TTL

- Redis allows us to implement a distributed lock with a TTL, where a lock for a ticketID could be acquired in Redis			with a TTL,	and this TTL will act as the expiration time. If the lock expires, Redis will release the lock and other				processes could operate on the entry. This way, the ticketStatus only has two states: AVAILABLE / BOOKED.
			During the booking process, the ticketStatus will remain AVAILABLE, but the lock will prevent other	processes from			updating that ticketID.
- The Redis lock will be for a ticketID and userID, and it will prevent other processes from updating the ticketID				during the TTL. This way, the ticketID is locked only	for that specific userID, as it should be.
			
- However, if a lock goes down, then there will be some time until a new lock is up - in this time, the first user to 			complete their booking process and pay will get the ticket, so if the lock is down, it’s first come first serve. However,			there will still be no double bookings since the database will use OCC or database constraints to ensure any writes			do not produce double bookings. We’ll go with this Redis distributed lock with TTL approach where the lock will			be for a userID and ticketID.

- Using the Redis distributed lock with TTL approach, when a user wants to book a ticket, they’ll select a seat with a ticketID	from the seat map, and send a request to the booking service. The booking service will lock that ticketID with a TTL by adding	it to our Redis Distributed Lock. The booking service will also add a new entry to the Bookings table with a bookingStatus of 	PENDING. The user’s request will then be routed to a payment service, and if the user cancels or doesn’t complete the 		booking process, the lock will be released after the TTL. If the booking process completes, the ticketStatus will change to		BOOKED, and the bookingStatus will change to BOOKED within a single transaction.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/8829d991-ff39-4ac3-869b-574af86ee6c5" />








