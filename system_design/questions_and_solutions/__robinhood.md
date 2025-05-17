# Robinhood (stock trading platform)

Robinhood is a commission-free trading platform for stocks, ETFs, options, and cryptocurrencies. It features real-time market data and basic order management. Robinhood isn't an exchange in its own right, but rather a stock broker; it routes trades through market makers ("exchanges") and is compensated by those exchanges via payment for order flow.

## Financial markets 101

There's some basic financial terms to understand before jumping into this design:

- **Symbol**: An abbreviation used to uniquely identify a stock (e.g. META, AAPL). Also known as a "ticker".

- **Order**: An order to buy or sell a stock. Can be a market order or a limit order.

- **Market Order**: An order to trigger immediate purchase or sale of a stock at the current market price. Has no price target and just specifies a number of shares.

- **Limit Order**: An order to purchase or sell a stock at a specified price. Specifies a number of shares and a target price, and can sit on an exchange waiting to be filled or cancelled by the original creator of the order.

Outside of the above financial details, it's worth understanding the responsibilities of Robinhood as a business / system. Robinhood is a brokerage and interfaces with external entities that actually manage order filling / cancellation. This means that we're building a brokerage system that facilitates customer orders and provides a customer stock data. We are not building an exchange.

For the purposes of this problem, we can assume Robinhood is interfacing with an "exchange" that has the following capabilities:

- **Order Processing**: Synchronously places orders and cancels orders via request/response API.

- **Trade Feed**: Offers subscribing to a trade feed for symbols. "Pushes" data to the client every time a trade occurs, including the symbol, price per share, number of shares, and the orderID.

<img width="750" alt="image" src="https://github.com/user-attachments/assets/dd0b84e7-10ec-41b3-8aba-777988718eef" />

## Requirements

### Functional 

- Users can see live prices of stocks
- Users can manage orders for stocks (market / limit orders, create / cancel orders

#### Out of scope

- Users can trade outside of market hours
- Users can trade ETFs, options, crypto
- Users can see the order book in real-time

<img width="750" alt="image" src="https://github.com/user-attachments/assets/7437794a-2277-4ada-8a0c-ecf23cb506dd" />

### Non-functional

- Strong consistency for order management:
  - The system prefers high consistency for order management; it's essential for users to see up-to-date order information when making trades.
- Scaling to a high number of trades per day:
  - The system should scale to a high number of trades per day (20M daily active users, 5 trades per day on average, 1000s of symbols).
- Low latency when reflecting symbol price updates:
  - The system should have low latency when reflecting symbol price updates and when placing orders (under 200ms).
- The system should minimize the number of active clients connecting to an external exchange API. Exchange data feeds / client connections are typically expensive.

#### Out of scope

- The system connects to multiple exchanges for stock trading
- The system manages trading fees / calculations (we can assume fees are not in scope)
- The system enforces daily limits on trading behavior
- The system protects against bot usage

<img width="750" alt="image" src="https://github.com/user-attachments/assets/f836693b-1d7f-42ae-a199-e1c3f09a9959" />

## Data model / entities

- Users:
  - userID
  - userName
  - email
 
- Symbol:
  - ticker

- Order:
  - orderID
  - userID
  - ticker
  - type: BUY / SELL
  - shares
  - orderStatus: PENDING / SUBMITTED / COMPLETED

## API design

We just need to define an endpoint for each of our functional requirements.

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

<br/>
<br/>

SSE endpoints:

### Get symbol data

- Let's start with an endpoint to get a symbol's price updates via SSE, which will include details and price data. We might have an endpoint like this, where we first establish a SSE connection with the backend servers. The header "Connection: keep-alive" will be used to establish a long-lived connection with the server (default value for keep-alive is 2 hrs, but it's more appropriate to have a much smaller value to reduce taking up unnecessary bandwidth)
- The text/event-stream indicates that the client expects a SSE based data stream

Request:
```bash
POST /subscribe
Accept: text/event-stream
Connection: keep-alive
{
  symbol (symbols the client wants to subscribe to via an SSE connection)
}
```

- The server will send to the client a list of new price updates via the established SSE connection

Response:
```bash
HTTP/1.1 200 OK
Content-Type: text/event-stream
Connection: keep-alive
{
  id: 101
  event: symbol_updates
  data: [ { symbol, price, timestamp } ]

  retry: 500
}
```

<br/>
<br/>

Order endpoints:

### List orders for a user

Request:
```bash
GET /orders?nextCursor={ viewport's oldest order's timestamp }&limit -> Order[]
```

### Create order for a user

- Note we're using priceInCents instead of price to avoid floating point precision issues. Especially for financial application it's better to use integers to avoid errors and financial scams.

Request:
```bash
POST /order
{
  type: BUY / SELL,
  symbol,
  priceInCents: 52210,
  numShares: 10
}
```

### Cancel an order

Request:
```bash
DELETE /order/:orderID -> true / false
```

## HLD

### API gateway

- As the system will likely use multiple services via a microservice architecture, the API gateway will route requests to the appropriate service, handle rate limiting and authentication

### Symbol service

- The first requirement of Robinhood is allowing users to see the live price of stocks. This might be one stock or many stocks, depending on what the user is viewing in the UI. To keep our design extensible, let's assume a user can see many live stock prices at once. To support this design, we can do the following (discussed in 'Allow viewing of live price updates of stocks'):
  - Polling exchange directly
  - Polling internal cache:
    - Note that the client could still poll the Symbol service, where the Symbol service will check if there are updates in the Symbol cache for the symbol requested. If we're pursuing a polling solution, even with the integration of the Symbol cache, we'll still see slower updates than we'd like to see for price updates - because the price updates will depend on the polling interval, which could be 500ms - 1 s. In the non-functional requirements, we indicated we wanted a reasonably short SLA to update clients about symbol prices (under 200ms), and the only way we'd guarantee that with this solution is if we poll data every 200ms, which is unreasonable.
    - Also, even if the price has not changed within the Symbol cache (because the Symbol processor first checks if the price changed from the previous price or not), clients will still indiscriminately poll, leading to some wasted HTTP traffic.
  - Server sent event (SSE) price updates
 
- The Symbol service will allow clients to initially retrieve initial symbol price updates, and also to establish a SSE connection to listen to symbol price updates. The Symbol service will allow clients to request the endpoint 'POST /subscribe' with a body containing a list of symbols they want to subscribe to by establishing a SSE connection.

- After the SSE connection is established, the Symbol service can first fetch the initial list of prices from the Symbol cache for the symbols the client wants to subscribe to (where the price updates in the Symbol cache are kept updated by the Symbol processor listening to the exchange). This way, the client will first have the initial price updates from the Symbol cache once the SSE connection is established. Afterwards, the Symbol processor (that is sending price updates to the Symbol cache) could also send the same price updates to the Symbol service for the symbols in which clients are subscribed to. This way, the client will have updated prices from the Symbol processor.

- The reason we're using SSE is because we can significantly reduce the number of price updates the Symbol service sends to the clients: if we used polling and 5000 clients are requesting a price at the same time, the price isn't different per client, yet we're expending 5000 calls (repeatedly using the polling interval) to disperse this information. However, if we used SSE, then we'll only send price updates to those 5000 clients when the price changes determined by the Symbol processor.

### Symbol cache

- The Symbol cache will store the price updates in-memory sent from the Symbol processor. The reason we want to store the data in-memory is because there will be a large number of writes coming from the Symbol processor where a cache will be effective. Also, if we don't store the price updates somewhere, and just allow the Symbol service to receive the price updates from the Symbol processor using the client's subscribed symbols, then we'll have redundant exchange calls we'll need to make, which will be inefficient.
- We can likely use a cache such as Redis, where it offers built-in data structures such as lists and sorted sets for handling ordered and sorted data. Also, because Redis is single-threaded, it will work the best since we want to accept only a single price update at a time for a symbol, without potential concurrency issues.

### Symbol price processor

- The Symbol processor will perform a KV lookup for the symbol in the Symbol cache, and it will keep the symbol's prices updated in the cache. The price updates will ultimately be coming from the exchange API, where the Symbol processor will be an intermediary service that updates the Symbol cache, and sends price updates for subscribed symbols to the Symbol service.
  
- The Symbol processor also prevents excess connections or requests being received from the exchange API, where if the symbol's price has not changed at all, then the Symbol processor doesn't necessarily need to update the Symbol cache or send the price update to the Symbol service. It could essentially "filter out" this unnecessary update from the exchange API.

### Order service

- The second requirement of Robinhood is allowing users to manage orders for stocks. Users should be able to create orders (limit or market order types), cancel outstanding orders, and list user orders. We can meet this requirement using the following (discussed in 'Allowing users to manage orders'):
  - Send orders directly to exchange
  - Send orders to dispatch service via queue
  - Order gateway:
    - Note that the orders created / cancelled by users will always happen synchronously between the Order service and the exchange API. This is to prevent showing the user an acknowledgement when in-fact the order was not processed correctly. Most high-frequency trading services also provide this synchronous nature, because most orders will usually take < 200 ms, thus asynchronous behaviour for orders is not necessary.
    - Note that since we're using an Order gateway, this approach requires our Order service to do more to manage orders, meaning it will need to be written in a way that is both efficient for client interaction and efficient for exchange interaction (e.g. potentially batching orders together).

### Order gateway

- The Order service will send orders directly to the Order gateway, where the Order gateway will enable external internal internet communication with the exchange API via the Order service. The gateway would make the requests to the exchange API appear as if they were originating from a small set of IPs. This gateway can be an AWS NAT gateway, which would allow the Order service to make requests to the exchange API, but then appear under a single or small number of IPs (elastic IPs in AWS terms).

- Given that the gateway is managing outbound requests, this approach relies on the Order service that is accepting requests from the client to play a role in actually managing orders. This service will run business logic to manage orders and will scale up / down as necessary given order volume. Given this request is being routed to from clients, we might make the auto-scaling criterion for this service quite sensitive (e.g. auto-scale when average 50% CPU usage is hit across the fleet) or we might over-provision this service to absorb trading spikes.

### Orders database

- Now that we know how we'll dispatch orders to the exchange, we also must consider how we'll store orders on our side for the purposes of exposing them to the user. The user should be able to request the endpoint 'GET /orders' to list all their orders.

- In order to track orders, we'll use the Orders database that is updated when orders are created or cancelled. The Orders database will be a relational database to promote consistency via ACID guarantees, and will be partitioned on userID (the ID of the user submitting order changes). This will make querying orders of a userID fast, as the query will go to a single node and requests will also be distributed across the partitions.

- The order itself will contain information about the order created / cancelled. It will also contain data about the state of the order (PENDING prior to being submitted to the exchange API, and SUBMITTED when it's submitted to the exchange API). The order will contain an orderID field, which will be populated by the ID that the exchange API responds with when the Order service submits the order synchronously.

### Trade processor

- To keep the orders in the Orders database updated, we'll need some sort of Trade processor that will receive trade updates from the exchange API to see if the orders maintained in the Order database needs to be updated.

<img width="750" alt="image" src="https://github.com/user-attachments/assets/f0dfc48b-9766-45eb-b8e4-7659b2024169" />

<img width="1450" alt="image" src="https://github.com/user-attachments/assets/99434822-1cb3-4a45-a8be-60be9cb7a80b" />

## DD

### Ensuring live price updates

It's worth considering how the system will scale live price updates. If many users are subscribing to price updates from several stocks, the system will need to ensure that price updates are successfully propagated to the user via SSE.

The main problem we need to solve is: how do we route symbol price updates to the Symbol service servers connected to users who care about those symbol updates?

To enable this functionality in a scalable way, we can leverage Redis pub/sub to allow the Symbol service to publish / subscribe to price updates from the Symbol price processor. Users can subscribe to price updates via the Symbol service and the Symbol service can ensure it is subscribed to symbol price updates via Redis pub/sub for all the symbols the users are subscribed to. 

Thus, Redis pub/sub will sit in-between the Symbol service and the Symbol price processor. Because the Symbol service is managing SSE connections, it will store in-memory the mapping between the symbol : Set(userID) (which will map the symbol to the subscribed userIDs). The Symbol service will then subscribe to the appropriate channels for the symbols via Redis pub/sub. The Symbol price processor will also publish price updates to those channels (when price updates come in), where Redis pub/sub will then provide the price updates to the Symbol service.

#### Workflow of live price updates

Let's walk through the full workflow for price updates:

1. A user subscribes via a Symbol service server. The server tracks the symbol : Set(userId) mapping in-memory as it's establishing SSE connections with clients, so it adds an entry for each symbol the user is subscribed to.

2. The Symbol service server is managing subscriptions to Redis pub/sub for channels corresponding to each symbol. It ensures that it has an active subscription for each symbol the user is subscribed to. If it lacks a subscription, it subscribes to the channel for the symbol.

3. When a symbol changes price, that price update is processed by the Symbol price processor, which publishes that price update to Redis. Each Symbol service server that is subscribed to that symbol's price updates get the price update via subscription. The Symbol service servers then fan-out and send that price update to all users who care about that symbol's price updates via the SSE connection.

4. If a user unsubscribes from symbols or disconnects (detected via some heartbeat mechanism), the Symbol service server will go through each symbol they were subscribed to and removes them from the Set(userId) stored in-memory. We can also store a reverse mapping of userID : Set(symbol) to quickly find the symbols the unsubscribed / disconnected userID had subscribed to. This way, we can remove the userID from both mappings for the appropriate symbols efficiently. If the Symbol service server no longer has any users subscribed to a symbol, it can unsubscribe from the Redis channel for that symbol.

The above would scale as it would enable our users to evenly distribute load across the Symbol service. Additionally, it would be self-regulating in managing what price updates are being propagated to Symbol service servers.

### Tracking order updates from the exchange API

When digging into the order creation / deletion flow, it's worth clarifying how we'll ensure our Orders DB is updated as orders are updated on the exchange.

Firstly, it's not clear from our current design how the Trade processor might reflect updates in the Orders DB, based off just a trade. There's no efficient way for the trade processor to look-up a trade via the orderId to update a row in the Orders table, given that the table is partitioned by userID. This necessitates a separate KV data store mapping orderId to the userID that is corresponds to. For this KV store, we could use something like DynamoDB or PostgreSQL with an index on the orderID - the main purpose of this KV data store is to have a very quick lookup, thus we could also instead set an index on the orderID in the Orders table (instead of using this KV store). This KV store would be populated by the Order service after an order is submitted to the exchange synchronously.

This new KV store enables the Trade processor to quickly determine whether the trade involved an order from our system, and subsequently look up the order in the Orders table using the userID corresponding to the orderID in the KV store to update the Order's details. The Trade processor will then:

1. Lookup the orderID for the trade in the KV store containing the mapping orderID : userID -> the Trade processor will retrieve the userID from this KV store
2. The Trade processor will then use the userID to query the Orders table and update the orderID for this userID

### Managing order consistency

Order consistency is extremely important and worth deep-diving into. Order consistency is defined as orders being stored with consistency on our side and also consistently managed on the exchange side. As we'll get into, fault-tolerance is important for maintaining order consistency.

Before we dig in, we firstly can revisit our order storage mechansim. Our Order database is going to be a horizontally partitioned relational database (e.g. Postgres). All order updates will happen on a single node (the partition that the order exists on). All order reads will also occur on a single node, as we'll be partitioning by userID.

When an order is created, the system goes through the following workflow:

1. The Order service will first store an order in the Orders database with the orderStatus = PENDING. It's important that this is stored first because then we have a record of the PENDING order for consistency purposes. If we didn't store this first, then the client could create an order on the exchange, the system could fail, and then our system has no way of knowing there's an outstanding order since we didn't store this order entry in the Orders DB first.

2. The Order service will submit the order to the exchange via the Order gateway. The Order service will also get back the orderID immediately from the exchange (the order submission is synchronous).

3. The Order service will write the orderID to our KV store and update the order in the Orders database with status as SUBMITTED and orderID as the ID received from the exchange.

4. The Order service will then respond to the client that the order was successful.

#### Fault tolerance for order consistency

The above workflow seems very reasonable, but it might break down if failures occur at different parts of the process. Let's consider several failures, and ways we can mitigate these failures if they pose a risk to our consistency:

- **Failure storing order**: If there's a failure storing the order in the Orders DB, then we can respond with a failure to the client and stop the workflow. The client could then re-try the order. This will be a safer approach than continuing the workflow with a failure when storing the order in the Orders DB.

- **Failure submitting order to exchange**: If there's a failure submitting the order to the exchange, then we can mark the orderStatus as FAILED and respond to the client.

- **Failure processing order after exchange submission**: If there's an error updating the database after an exchange submission, we might consider having a "clean-up" job (cron job) that deals with outstanding, PENDING orders in the database that failed after receiving an update from the exchange. Most exchange APIs offer a clientOrderId metadata field when submitting an order (see E*TRADE example in https://apisb.etrade.com/docs/api/order/api-order-v1.html#/definitions/PreviewOrderRequest) so the "clean-up" job can asynchronously query the exchange to see if the order went through via this clientOrderId identifier, and do one of two things:
  - Record the orderID if the order did go through
  - Mark the order as FAILED if the order didn't go through determined by the response from the exchange

<br/>

Now that we've considered the order creation flow, let's consider the cancel flow. When an order is cancelled, the system goes through the following workflow:

1. The Order service will update orderStatus to PENDING_CANCEL. We do this first to enable resolving failed cancels later - which are cancellations which failed mid-way

2. The Order service will submit the order cancellation to the exchange, and synchronously wait for the response

3. The Order service will then record the order cancellation in the database, and set orderStatus = CANCELLED

4. The Order service will respond to the client that the cancellation was successful

<br/>

Let's walk through different failures to ensure we are safe from inconsistency:

- **Failure updating orderStatus to PENDING_CANCEL**: If there's a failure updating the orderStatus upfront, we respond with a failure to the client and stop the workflow.

- **Failure cancelling order**: If there's a failure cancelling the order via the exchange (the exchange failed to cancel the order), we can respond with a failure to the client and rely on a "clean-up" process to scan PENDING_CANCEL orders in the Orders DB to ensure they are set as CANCELLED if enough time passes.

- **Failure storing cancelled status in Orders DB**: If there's a failure updating the orderStatus in the Orders DB, we can rely on a "clean-up" process to set the orderStatus of PENDING_CANCEL orders to CANCELLED (ensure they are cancelled, or no-op and just update the orderStatus to CANCELLED if they have already been cancelled after getting the response from the exchange).

Based on the above analysis, we have 1) a clear understanding of the order creation and cancel workflows, and 2) identified the need for a "clean-up" background process to ensure our orders become consistent in the face of failures at different points in our order create / cancel workflows.

<br/>
<br/>

Additional deep dives:

Robinhood, like most fintech systems, is a complex and interesting application, and it's hard to cover every possible consideration in this guide. Here are a few additional deep dives you might consider:

- **Excess price updates**: If a set of stocks has a lot of trades or price updates, how might the system handle the load and avoid overwhelming the client? This might be interesting to cover.

- **Limiting exchange correspondence**: While we certainly covered ways we'd "proxy" the exchange and avoid excess concurrent connections / clients, it might be worthwhile to dive into other ways the system might limit exchange correspondence, while still scaling and serving the userbase (e.g. perhaps considering batching orders into single requests).

- **Live order updates**: It might be worthwile to dive into how the system would propagate order updates to the user in real time (e.g. if the user is looking at orders in the app, they see their orders get filled in real time if they're waiting on the exchange).

- **Historical price / portfolio value data**: In this design, we didn't focus on historical price / portfolio data at all, but some interviewers might consider this a requirement. It's worthwhile to ponder how a system would enable showing historical price data (over different time windows) and historical user portfolio value.










