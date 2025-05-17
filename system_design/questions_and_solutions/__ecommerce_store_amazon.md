# E-commerce store like Amazon

## Requirements

### Questions

Features:

- What are some of the features we should consider?
  - For simplicity let’s assume the home page consists of just the search bar.
  - It should support:
    - Searching for items
    - Adding items to cart (let’s assume a user only has a single cart)
    - Submitting orders
    - Initiating the checkout process
    - Canceling orders (optional)

- Should we design the recommendation engine that displays recommended items to the user?
  - Let’s assume there is a recommendation engine that uses the search parameters	in the search bar, however let’s not focus on the recommendation engine

- Should we handle additional Amazon features like Prime, used vs new items, etc?
  - No

- Should we design just amazon.com, or consider regional websites like amazon.ca, amazon.fr, etc?
  - For simplicity, let’s just design amazon.com, and assume the design is applicable to	other regional websites

<br/>

Stock:

- Should we handle item stock, ie check if an item is in stock or not when the user is placing something into the cart?
  - Yes, the orders should naturally “consume” stock

- How should we handle items that have low stock and are being viewed by multiple people at the same time? Should we reserve extra items in some sense?
  - Let’s keep it simple: if an item is in stock and is in the carts of multiple users, the 	stock will be “consumed” only when when the user completes the checkout process. 	Once the user begins the checkout process, the system should alert the user if the	item has gone out of stock since it was added to their cart. It can “reserve” the item	during the duration of the checkout process, say for 5 minutes.

<br/>

Warehouses:

- Should we design the part of the system after an order is submitted, ie when orders are dispatched to Amazon warehouses, workers are assigned to packages, etc?
  - You should think about how warehouses will be notified of orders or suborders, but	you don’t have to worry about what happens after a warehouse has been assigned	an order or suborder

- How should our system figure out which warehouse to route the order to?
  - Let’s assume that we have access to a service that handles assigning orders to		warehouses. Let’s not focus on this service itself - just focus on how it interacts with	parts of the system. You should still think about how item stock in individual			warehouses come into play here.

<br/>

Functional and non-functional:

- Is it ok if there’s a little bit of loading time when searching for items, submitting orders, etc?
  - Ideally, searching for items should have low latency, however submitting orders		may have a higher latency.

- How many customers are we dealing with and how many orders can we expect per day?
  - Amazon supports roughly 300 million customers and 20 or so orders per second.	Let’s assume a much lower number of customers like 10 million for simplicity, and		focus more on core functionality rather than scalability

### Functional

- The system should support:
	- Searching for items
	- Adding items to cart
	- Submitting orders
	- Initiating the checkout process
	- Canceling orders (optional)
	- Orders will be assigned to relevant warehouses for shipment

- Additional service the system will interact with:
	- Recommendation engine
	- Warehouse service

- Stock inventory data should be maintained

### Non-functional

- High throughput / concurrency:
  - There could be multiple requests to initiate the checkout process, but if the stock is let's say 1, then only the first request will be considered on a first-come first-serve basis
  - There could also be high throughput / concurrency for popular items
  - The system will also be read heavy, as more users will view items than buy them
- Consistent:
  - Users should see a consistent view of items and stock

## Data model / entities

Majority of the entities are mainly read heavy, as opposed to being write heavy. This is because fewer users buy items as opposed to searching for items. A SQL database works well here, as it provides more optimized ACID properties which will support consistency of item's stock availability, and help in preventing inconsistencies during the checkout process.

- Items:
  - This table will store all the items - each row will be an item
  - Note that we won’t store the stock numbers on the Items table, since there are different kinds of stock, ie	stock in a warehouse, aggregated stock, etc. Also, the Items table will likely already be very large, and		updating and keeping all the stock data in the Items table will make the updates more complex.

	- itemID
	- name, description
	- price

- Carts:
  - This table will store all the carts - each row will be a cart belonging to a user
	
	- cartID
	- userID
	- items: [ { itemID, quantity } ]

- Orders:
  - This table will store all orders - each row represents an order

	- orderID
	- userID
	- items: [ { itemID, quantity } ]
	- price
	- orderedDate, arrivalDate
	- orderStatus: PENDING / SHIPPED / DELIVERED
  	- shippingAddress

- Aggregated stock:
  - This table will store all the item stocks, with each row representing an item. The Aggregated stocks will aggregate all the stocks from the warehouses for the itemID
  - When the checkout process initiates, the stock field for the itemID will be decreased. If the checkout process doesn't get completed, then the stock field will be rolled back and incremented. If the checkout process succeeds, then an orderID entry will be created, and during the delivery of the order, the orderID will be added to the Warehouse orders table, and the availableStock in the Warehouse stock table will be decreased. If the order's items have been shipped from the warehouse, then the physicalStock in the Warehouse stock table will be decreased.

	- itemID
	- stock

- Warehouse orders:
  - This table will store all the orders that warehouses get, with each row representing a warehouse order using orderID.		These orders could be single orders or suborders

	- orderID
	- parentOrderID:
  	  - If suborders is in scope, there will likely be a parentOrderID for orderIDs which are suborders
	- warehouseID
	- shippingAddress
  	  - The shippingAddress could be another warehouse or the user's shipping address itself

- Warehouse stock:
  - This table stores all the item stocks in warehouses, with each row representing a { itemID, warehouseID }	pairing. The physicalStock represents the actual physical stock in the warehouse, while the availableStock	represents the available stock, which could be decreased when orders with items get assigned to	warehouses because someone purchased those items.

  - If new stocks show up within a warehouse, both the physicalStock and availableStock will increase for that	warehouseID

	- itemID
	- warehouseID
	- physicalStock
	- availableStock


## API design

- Note that we’ll use userID if the user is authenticated and will be purchasing items. The userID could be placed in a session token or JWT in the Authentication header as such:
  - Authentication: Bearer

- The below caching header could also be applied to fetch frequently accessed entries quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
  - Cache-Control: no-cache max-age Private/Public

**Note: We’ll focus on the searching items, cart, checkout and order based endpoints. Other endpoints such as modifying the customer profile and preferences may not be the major focus of the system**

### Search items
  
- This endpoint will return the search results via cursor based pagination and additional filtering.
- This endpoint will also use the recommendation engine, search service, items table, and	cache popular item searches.

Request:
```bash
GET /items?query&nextCursor&limit&filter
```

Response:
```bash
{
  items: [ { itemID, name, price } ],
  nextCursor, limit
}
```

### Add / remove items from cart
  
- Users will only be able to call this endpoint when there is enough stock for the itemID. This endpoint will first verify if there is enough stock for the itemID within the Aggregated stock table

Request:
```bash
PATCH /cart?op={ ADD or REMOVE }
{
  itemID, quantity
}
```

### Checkout process

- Usually the checkout / order process is a 2 step process, where the user will first reserve the itemIDs' stocks within their cart (user will send the cart's items), then in the second step, they'll input their payment details (and shippingAddress) into the provided payment URL within the time limit. Thus we have 2 individual endpoints for these steps

#### Begin checkout / cancel checkout

- This endpoint will trigger another read on the Aggregated stock table for the itemID. If the items in the cart	don’t have enough stock anymore, an appropriate response can be returned. If all the items do have enough	stock in the Aggregated stock table, the endpoint will decrease the stock in the Aggregated stock table, and	“reserve” the items during the checkout process. After the default time limit of 5 minutes, the cancel		checkout endpoint will be triggered which will “un-reserve” the items and increase the stock in the			Aggregated stock table.

Request:
```bash
POST /checkout?op={BEGIN or CANCEL}
{
	cart: [ { itemID, quantity } ],
}
```

Response:
```bash
{
  paymentInputURL
}
```

#### Submit order / cancel order

- Both of these endpoints will write to the orders table, and the cancel order endpoint will write to the		Aggregated stock table, and increase the stocks for the items using the orderID which was generated when the order was submitted before.

- Note that an order can only be cancelled if it hasn’t been shipped yet, which we can tell from the			orderStatus in the orders table. If cancelling the order, the orderStatus will likely change to CANCELLED.

Request:
```bash
Enter payment details and shippingAddress:
POST /<paymentInputURL>
{
	paymentDetails (the payment details will be encrypted or retrieved by a separate payment service entirely)
	shippingAddress
}

Submit or cancel the order after entering in payment details into the paymentInputURL:
POST /checkout?op={SUBMIT or CANCEL}
{
	orderID (if the order is being cancelled)
}
```

### Get my orders

- This endpoint reads all the user’s orders from the orders table via cursor based pagination / lazy loading, and filtering such	as reading from the past 3 months. We’ll set the nextCursor value to the viewport's oldest orderedDate value, so that the next paginated result which is older than the viewport's oldest orderedDate can be returned.

Request:
```bash
GET /orders?nextCursor={ viewport's oldest orderedDate of orderID }&limit&filtering
```

Response:
```bash
{
  orders: [ { orderID, orderedDate, arrivalDate, cart: [ { itemID, quantity } ] } ],
  nextCursor, limit
}
```


## HLD

### API gateway

- The API gateway will route client requests to the appropriate services, and provide rate limiting and		authentication. API gateways also are more beneficial when working with a microservice architecture, where	there are multiple services and a single client request can be handled by those different services.

- We’ll be using a microservice based architecture as there are individual services managing their separate	resources such as databases. Using a microservice architecture will allow separate services to be scaled	independently. For example, if we have additional warehouses or items, the warehouse service can be		scaled separately by adding additional servers. 

### Database / cache

- The database will store items, carts, orders and stock data. A lot of the entities are relational, and might require complex queries, and transactions / locking during the checkout process. A SQL database such as PostgreSQL might be preferred over NoSQL, however NoSQL can definitely carry out the same database requirements we have. But because consistency is a strict requirement for the system during the checkout process, we'll want a DB that is optimized for it. 

#### Cache

- We could maintain a cache of the items data, which is static, in Redis lists which could group similar items together. However, caching the other entities such as carts, orders, aggregated stock, warehouse orders, warehouse stock, which are frequently changing might be difficult, since the cache will not be consistent with the database. But, we could still assign a small TTL for these frequently changing entities - the DD talks more about data inconsistency between the cache and the database.

#### Search results cache

- The search results cache will store frequent search results to improve latency of the searches. Because search results are usually returned with some form of ranking, whether it is sorting by date, price, etc, we can use Redis sorted sets to maintain the search results with an appropriate score based on the ranking.

### Warehouse service
  
- The warehouse service will read from the Orders table once orders are made, and determine the best way	to split the orders up and assign them to warehouses based on shipping address of the orderID, and the item stocks in the warehouses, etc. The		Warehouse service will also write the final warehouse orders to the Warehouse orders table.

- The Warehouse service will use the availableStock field in the Warehouse stock table to assign orders to	specific warehouses, and decrease the availableStock of the items in the Warehouse stock table. If an order	is cancelled, these availableStock values will be re-increased by the Warehouse service.

- When the orders are shipped from the relevant warehouses, the physicalStock for the warehouseID in the	Warehouse stock table will be decreased. If new stock comes, the physicalStock and availableStock fields in the		Warehouse stocks table, and the stock in the Aggregated stock table will be updated by the Warehouse service.

- The Warehouse service will likely have queues and workers, where jobs like updating the stock, routing orders to warehouses, etc will be pushed to the queues. Afterwards workers (containers) will pull the job from the queue and make the updates to the tables. We can likely use SQS as the queue with it's visibility timeout and delayed message delivery feature.

**Note that we won't go more in depth on the warehouse service, we're treating it as a separate service**

### Cart service

- The Cart service allows users to add and remove items from their cart, thus writing to the Carts table. Once	a user is ready to begin the checkout process, they can initiate the checkout via the Orders service and 		complete the payment process using the Payment service. Before a user adds an item to their cart, we'll first check if the item has enough stock in the Aggregated stock table.

### Orders service

- The Orders service allows users to begin the checkout process using the user’s cart. During the checkout	process, the payment process will also begin within the default 5 minutes time limit or so.

- If the items in the cart don’t have enough stock in the Aggregated stock table anymore after the checkout	process begins, the Orders service will reject the checkout. If all the items in the cart do have enough stock in	the Aggregated stock table, the stock in the Aggregated stock table will decrease, and “reserve” the items	during the checkout process. After the default time limit of 5 minutes, the items will be “un-reserved” and	increase the stock in the Aggregated stock table.

### Search service

- The search service works closely with the Recommendation engine to return items for the user’s search		queries. The Search service could use a tool such as Elasticsearch or Lucene to develop inverted	index mappings of the text based fields of the items for providing fast search results.

### Recommendation engine
  
- The recommendation engine will gather data on the user’s search results within the Search results cache, and their past orders in the Orders table to 	suggest	items to the user via recommendation algorithms, ML, etc

### Payment service

- The payment service initiates and completes the payment transaction during the checkout process. It will handle withdrawing money from the user’s account using the payment info they provided. We’ll treat this as a separate service and not focus on this.

<img width="600" alt="image" src="https://github.com/user-attachments/assets/1f006dc2-2b38-453a-a769-70207c6ca764" />

## DD

### Improving checkout process
  
- Decreasing the stock field (or setting ticketStatus to RESERVED temporarily during the booking process as in the SDI 'Ticketmaster - general events') in the Aggregated stock table and starting a timer once a user initiates their checkout process is a common approach	in multiple booking / ordering / payment processing apps. This approach is used because no user wants to enter their payment	info, then find out later that an item is sold out. Thus we have a timer and temporarily “reserve” the item's stocks.

- To design for this 5 min timer and temporarily decreasing the stock field, we can try out the below solutions	and in ‘Temporarily reserving stock / ticket solutions’ (these approaches are taken from the SDI 'Ticketmaster - general events'):
  - Pessimistic locking:
    - Pessimistic locking is usually not a good approach as it can cause deadlocks if there’s high concurrency. Also the			locked rows within the “SELECT FOR UPDATE” or data locking mechanism will prevent other processes from				reading ("SELECT FOR UPDATE" blocks the reads) the locked rows which the user is updating via the “SELECT FOR UPDATE”. Also, if database instances			crashed during the pessimistic locking process, then some rows may still be in a locked state.
    - Because pessimistic locking might cause more deadlocks, and might actually cause more locking issues if database instances are down, we'll look into optimistic locking OR database constraints later on in the DD.
		
  - Status and expiration time with cron
  - Implicit status with status and expiration time:
    - This approach might not be directly applicable to this design since we don't have a field like ticketStatus or itemStockStatus which specifies if a single instance of an item is available or not. We have an Aggregated stock table to check if there is available stock for an itemID using the stock field instead of itemStockStatus.

  - Redis distributed lock with TTL:
    - This approach might also not be directly applicable to this design since we don't have a specific field like aggregatedStockID which represents a single instance of an item that is available / unavailable. We have an Aggregated stock table to check if there is enough stock using the stock field instead of using an aggregatedStockID. If we had a aggregatedStockID, then a Redis distributed lock with TTL could be applied

<br/>

Temporarily reserving stock / ticket solutions:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/49ac5025-e397-4919-a806-89ebd93c48b2" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/c876b85a-218f-4474-8084-b301b87404a4" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/b6c984f7-3ae2-45a3-96b7-75074a6211a9" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/8829d991-ff39-4ac3-869b-574af86ee6c5" />

<br/>

### Scaling the system to support high concurrency of checkout processes

- Under a high concurrency of checkout processes, the item's stock data will become stale very quickly. Note	that the admins will only enable these below to support very high concurrency, thus these approaches can be enabled only for	very high concurrency cases. We can ensure this data is up to date by using the below and in ‘Supporting high concurrency of checkout processes / tickets’ (these approaches are taken from the SDI 'Ticketmaster - general events'):
  - SSE for real-time seat updates:
    - SSE events will be pushed to the clients in real-time to update the item's stock as soon as an item's stock is "reserved" or 				available. Thus, the user wouldn’t need to refresh their page.
    - SSE events will work well for moderately popular items, but for items with high concurrency and purchase rates, such as a new iPhone, the SSE approach will be slow to update the clients since it is still using HTTP, which will be slower than using websockets.

  - Virtual waiting queue and websocket for extremely popular items and high concurrency of checkout processes:
    - Users requesting to initiate the checkout process for a very popular item will be placed in a virtual waiting queue, and			they will request to establish a websocket connection with the Orders service. Dequeued users will be notified				using the websocket that they can proceed with the checkout process (checkout process will likely be performed via optimistic locking OR database constraints). The			queued users will also be notified of their position of the queue and estimated wait times (wait time calculated	using 5 min * user's queue position) using the websocket. 

    - The queue could be implemented using traditional message queues such as SQS. The Orders service can likely maintain workers (containers) which will pull from SQS, where the message will have a visibility timeout applied to ensure exactly-once delivery. When the worker pulls the message, the checkout process can initiate via the worker, and if the checkout process completes, then the message will be deleted by default. However, if the worker doesn't complete the checkout process, then the message could likely be deleted OR sent to the back of the queue using SQS's delayed message delivery feature.
		
  - Note that we could also use long polling to get updates from the server about the item's stock data,		which is simple. However, if users sit on the “item's page” for a long time, then it will eat up resources on the		server.

Supporting high concurrency of checkout processes / tickets:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/f998b898-8533-41a7-bc39-d3630aab6a70" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/0f89e9b2-e043-4ce0-9267-7e16ad012a8b" />

<br/>

### Concurrency issues during checkout process and different types of locking techniques

Concurrency issues may arise during the checkout process where different users could reserve the item's stock concurrently (and the item's stock value in the Aggregated stock table could be at 1, where it's first come first serve) - which might produce a race condition. The solution to this concurrency issue will likely require some form of locking discussed below:

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

- Using database constraints is similar to optimistic locking. The SQL constraint shown in ‘Database			constraint’ could be added to the Aggregated stock table - where we check that the stock field in the Aggregated stock table doesn't contain a negative count - which means that there is not enough stock for the item. When transactions are being made, and they violate the		constraint, the transaction is rolled back. This is shown in ‘Database constraint’

- The pros of database constraints is that it’s easy to implement and works well when the number of			concurrent operations is not as high.

- The cons of database constraint is similar to optimistic locking, where it can cause repeated retries if			transactions are rolled back. Also, the updates from database constraints cannot be versioned like				optimistic locking. Additionally, not all databases provide database constraints, however PostgreSQL and		MySQL both support it.

<br/>

Database constraint:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/cb112e11-e93b-453e-937e-166f080ad248" />

<br/>

Overall, optimistic locking or database constraints may be suitable for this system as concurrency may be high but not very large - since unavailable item stocks may still be rare with an E-commerce store as opposed to Ticketmaster.

#### Expiration time based locking and distributed locks

- We've already talked about these 2 different locking approaches above in 'Improving booking process'.

### Data inconsistency between cache and database

- If using the cache, when the Orders service looks for stock availability in the cache, 2 operations	happen:
1. Querying the cache for stock availability
2. Updating the Aggregated stock table with the updated stock value for the item

- If the cache is asynchronously updated as shown in ‘Hotel / item stock caching’ (note that this diagram is from the SDI 'Hotel reservation system'), there may be some			inconsistency between the cache and database. However, this inconsistency will not matter as much since			checkout process requests will ultimately still make the final update to the database via a locking approach. The cache is only there to help in speeding up item stock availability searches, not storing the exact stock availability data is fine depending on the consistency we want for displaying stock availability. If we want users to always see the latest stock availability value in the UI, then the cache can be omitted from the design.

<br/>

Hotel / item stock caching:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/b346c2c5-5715-463a-b575-1a43bf7083d8" />

<br/>

### Improving search latencies

- Queries on the database and performing the “LIKE” clause will be very slow for searches because it causes a full table scan. We can improve the search by		using the following and in ‘Improving search latencies’ (these approaches are taken from the SDI 'Ticketmaster - general events'):
  - Indexing and SQL query optimization
  - Full-text indexes in the database
  - Full-text search engine like Elasticsearch:
    - The overall inverted index mappings could be built using the text based data on the items.

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

- When using a microservice architecture, a service usually has it’s own database it manages. In a monolithic		architecture, multiple services could manage the same database. This is shown in ‘Microservice vs		monolithic’ (note that this diagram is from the SDI 'Hotel reservation system').

- Our design has a hybrid approach, where a single service could still access databases or tables other services could		manage or access. For example, the Orders service accesses both the Aggregated stock and Cart tables.
	We have a hybrid approach, because a pure microservice approach can have consistency issues when			managing transactions. The Orders service accesses multiple tables / databases, and if a transaction fails, then it will	need to roll back the changes in those respective databases / tables. 

- If we used a pure microservice approach, the changes will need to be rolled back in all the databases BY THE SERVICES which manage them instead of by only the Orders service. We cannot only just use a single transaction (within the Orders service) in a pure microservice approach, we’ll need multiple transactions happening within those other services as shown in ‘Microservices transactions’ (note that this diagram is from the SDI 'Hotel reservation system'). This causes an overhead and may lead to inconsistency issues.

Microservice vs monolithic:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/3ade0c8e-9ae6-48a2-9c86-97686ec1ccd1" />

<br/>
<br/>

Microservices transaction:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/2608a3b6-d161-4205-86ea-5d015a3b5f43" />

### Scaling the system to support large number of users

The stateless servers for the Cart, Orders and Warehouse services could be scaled as follows as in 'Scaling API to support high concurrency' (these approaches are taken from the SDI 'Ticketmaster - general events'):

- To scale the API for high concurrency for popular items, we’ll use a combination of load balancing, horizontal scaling	and caching as shown in ‘Scaling API to support high concurrency’. To scale, we can cache static data with high reads such as items and search query results.

Scaling API to support high concurrency:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/a187b31b-c583-4929-9894-25bdf597455a" />

<br/>
<br/>

The stateless servers could be scaled by adding more servers, but the database and cache will need to be		scaled differently:

#### Database

- We can apply sharding on the databases likely by using an "itemType" field, which would allow similar itemIDs to be on the same shard. In this way, when searching for similar items, we'll only search through one shard, and when processing the checkout or orders by increasing / decreasing the stock on the itemIDs, we can do it in parallel across all the shards. However, we'll also need to ensure that the data is spread evenly across shards, and possibly allocate more shards for more dense itemTypes.

#### Caching

- In the hotel cache, only the frequently accessed items, and possibly the item's stock should be cached using a TTL. Caching the item's stock might be preferable if we have large read operations for checking stock availability.
	
- If we use both a database and cache, the Orders service could first check the stock availability	in the cache, then update the Aggregated stock data in the database. Afterwards, the database could asynchronously update the cache. In this caching scenario, the cache is used		for fast searches, while the  database is the single source of truth. This logic is shown in ‘Hotel / item stock caching’





