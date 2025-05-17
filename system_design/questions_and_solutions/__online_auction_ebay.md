# Online auction like eBay

eBay is an online auction service that allows users to buy and sell items.

## Requirements

### Questions

- In this system, users should be able to post an item for auction (with a starting price and end date), should be able to bid on an item (where bids are accepted if they're higher than the current highest bid, and users should be able to view an auction, including the current highest bid. Are we designing all of this?
  - Yes

- Are we designing the system for both the bidders and buyers?
  - Yes

- Should users be able to search for items, maybe also by a category and price?
  - Yes, include this

- Should the bids be updated in real-time, or as real-time as possible?
  - Yes, make bid updates as real-time as possible

- How many concurrent auctions can we expect?
  - 10M concurrent auctions (let's an auction on-average runs for a week)

### Functional

- Users should be able to post an item for auction with a starting price and end date
- Users should be able to bid on an item, where bids are accepted if they're higher than the current highest bid
- Users should be able to view an auction, including the current highest bid

- Users should also be able to search for items, and filter items by category, price range, etc

### Non-functional

<img width="750" alt="image" src="https://github.com/user-attachments/assets/7ef49a9a-a212-4e79-a607-0ff359e2ef5b" />

- Strong consistency:
  - The system should maintain strong consistency for bids to ensure all users see the same highest bid
- Fault tolerant:
  - The system should be fault tolerant and durable. We can't drop any bids
- Real-time view of bids:
  - The system should display the current highest bid in real-time so users know what they're bidding against
- The system should scale to support 10M concurrent auctions

## Data model / entities

- Auction:
  - This entity will represent an auction for an item. It would include info like the starting price, end date and the item being auctioned
    - auctionID
    - itemID
    - startingPrice
    - endDate

- Item:
  - This represents an item being auctioned. It would include info like the name, description and s3 image URL
    - itemID
    - name, description
    - s3URL

- Bid:
  - This represents a bid on an auction. It would include info like the amount bid, the user placing the bid, and the auction being bid on
    - bidID
    - userID
    - auctionID
    - amount
    - status: ACCEPTED / DECLINED

- User:
  - This represents an user of the system who either starts an auction or bids on an auction
    - userID
    - userName
    - userEmail

<img width="750" alt="image" src="https://github.com/user-attachments/assets/15e560cf-9714-47e2-b11d-0782751f1a76" />

## API design

- Note that we’ll use userID if the user is authenticated and will be booking tickets. The userID could be placed in a session token or JWT in the Authentication header as such:
  - Authentication: Bearer

- The below caching header could also be applied to fetch frequently accessed entries quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
  - Cache-Control: no-cache max-age Private/Public

### Search items

- This endpoint allows users to search for items currently being auctioned via a search query, price range and category. We'll retrieve the items via cursor based pagination, where the nextCursor will point to the viewport's highest price of the item OR the last itemID (in the viewport)

Request:
```bash
GET /items?searchQuery&startingPrice&endingPrice&category&nextCursor={ either using viewport's highest price of item or viewport's last itemID }&limit
```

Response:
```bash
{
  items: [ { itemID, name, currentHighestBid } ],
  nextCursor, limit
}
```

### View auction

- For viewing an auction, we need a GET endpoint that takes an auctionID and returns the auction and item details:

Request:
```bash
GET /auctions/:auctionID
```

Response:
```bash
{
  Auction object
  Item object
}
```

### Create auction

- For creating auctions, we need a POST endpoint that takes the auction details and returns the created auction

Request:
```bash
POST /auctions
{
  item: Item object,
  startDate, endDate,
  startingPrice
}
```

Response:
```bash
{
  Auction object
  Item object
}
```

### Create bid

- For placing bids, we need a POST endpoint that takes the bid details and returns the created bid

Request:
```bash
POST /auctions/:auctionID/bids
{
  Bid object
}
```

Response:
```bash
{
  Bid object
}
```

## HLD

### API gateway

- As the system will likely use multiple services via a microservice architecture, the API gateway will route requests to the appropriate service, handle rate limiting and authentication

### Auction service

- The Auction service will be used to request the 'POST /auctions' endpoint for creating auctions using the auction details, including info about the item they're selling. The Auction service can also be used for searching items (the 'GET /items' endpoint) and viewing an auction (the 'GET /auctions/:auctionID' endpoint).
- The Auction service will connect to the database that stores the item and auction entities. 

### Database / cache

- The database will store tables for the item, auction and bid entities. Because we'll benefit from the ACID guarantees in a SQL database as opposed to a NoSQL database where ACID may be more difficult to properly set up, we'll use PostgreSQL. The writes on the tables requiring transactions / isolation will likely use row-level locking (pessimistic locking) or OCC (optimistic concurrency control / optimistic locking) via database constraints or another locking approach like a Redis distributed lock. This will prevent bids being made when the current highest bid is larder than the new bid.
- Note that NoSQL DBs like DynamoDB and Cassandra offer multi-table transactions and light-weight transactions (within a single partition) respectively, however, managing the transactions or OCC will be much simpler using PostgreSQL, where it's specialized for guaranteeing strong consistency during concurrency conflicts using multiple different options a SQL DB provides for locking / transactions.

### Bid service

- Users should be able to bid on an item, where bids are accepted and if the bid is higher than the current highest bid. Bidding is the most interesting part of this problem, and where we will spend the most time in the interview.

- To handle the bidding functionality, we'll introduce a dedicated "Bidding Service" separate from our Auction Service. This new service will:
  - Validate incoming bids (e.g. check bid amount is higher than current max)
  - Update the auction with new highest bid
  - Store bid history in the database
  - Notify relevant parties of bid updates

- We choose to separate bidding into its own service for several key reasons:
  - **Independent Scaling**: Bidding traffic is typically much higher volume than auction creation - we expect ~100x more bids than auctions. Having a separate service allows us to scale the bidding infrastructure independently.
  - **Isolation of Concerns**: Bidding has its own complex business logic around validation, race conditions, and real-time updates. Keeping it separate helps maintain clean service boundaries.
  - **Performance Optimization**: We can optimize the bidding service specifically for high-throughput write operations, while the auction service can be optimized for read-heavy workloads.

- In the simple case, when a bid is placed, the following happens:
  - Client sends a POST request to endpoint 'POST /auctions/:auctionId/bids' with the bid details.
  - API Gateway routes the request to the Bid service.
  - Bid Service queries the database for the highest current bid on this auction. It stores the bid in the database with a status of either ACCEPTED (if the bid is higher than current highest) or DECLINED (if not). The service then returns the bid status to the client.
  - Database bids are stored in a new Bids table, linked to the auction by auctionID.

<img width="691" alt="image" src="https://github.com/user-attachments/assets/66a5b43c-58ac-4fde-827d-1f20d6afdc04" />

#### Users should be able to view an auction, including the current highest bid

- Users need to be able to view an auction for two reasons:
  - They want to learn about the item in case they decide they're interested in buying it.
  - They want to place a bid, so they need to know the current highest bid that they need to beat.

- These two are similar, but have different requirements. The first is a read-only operation. The second requires real-time consistency. We'll offload the depth of discussion here to the DD, but let's outline the basic approach which ensures that the current highest bid is at least reasonably up-to-date.

- When a user first goes to view an auction, they'll make a GET request to the endpoint 'GET /auctions/:auctionId' which will return the relevant auction and item details to be displayed on the page. Great.

- What happens next is more interesting. If we never refresh the maximum bid price, then the user will bid based on a stale amount and be confused (and frustrated) when they are told their bid was not accepted. Especially in an auction with a lot of activity, this is a problem. To solve this, we can simply poll for the latest maximum bid price every few seconds. While imperfect, this ensures at least some degree of consistency and reduces the likelihood of a user being told their bid was not accepted when it actually was.

## DD

### Ensuring strong consistency for concurrent bid requests

Ensuring the consistency of bids is the most critical aspect of designing our online auction system. Let's look at an example that shows why proper synchronization is essential.

Example:
- The current highest bid is $10.
- User A decides to place a bid of $100.
- User B decides to place a bid of $20 shortly after.

Without proper concurrency control, the sequence of operations might unfold as follows:
- User A's Read: User A reads the current highest bid, which is $10.
- User A's Write: User A writes their bid of $100 to the database. The system accepts this bid because $100 is higher than $10.
- User B's Read: User B reads the current highest bid. Due to a delay in data propagation or read consistency issues, they still see the highest bid as $10 instead of $100.
- User B's Write: User B writes their bid of $20 to the database. The system accepts this bid because $20 is higher than $10 (the stale value they read earlier).

As a result, both bids are accepted, and the auction now has two users who think they have the highest bid:
- A bid of $100 from User A (the actual highest bid).
- A bid of $20 from User B (which should have been rejected).

This inconsistency occurs because User B's bid of $20 was accepted based on outdated information. Ideally, User B's bid should have been compared against the updated highest bid of $100 and subsequently rejected.

<img width="750" alt="image" src="https://github.com/user-attachments/assets/24dd5948-d022-4ae5-afcd-ff27d43dcaa6" />

We can solve for strong consistency by doing the following and in 'Ensuring strong consistency for concurrent bid requests':
- Row locking with bids query
- Cache max bid externally
- Cache max bid in database:
  - Note that the OCC steps in this approach will update the auction row only if the max bid hasn't changed. This max bid will be the 'version' in OCC, and will be used to validate if the new bid can be recorded as the max bid in the Auction table. This is done via the following SQL update, where the ":original_max_bid" is first read prior to running the update - this is because we want to make sure the value for max bid hasn't changed.
 
```sql
UPDATE auctions 
SET max_bid = :new_bid 
WHERE id = :auction_id AND max_bid = :original_max_bid
```
  - This approach avoids locks entirely while still maintaining consistency, at the cost of occasional retries when conflicts do occur - when the max bid did in-fact change during the OCC operation.

### Ensuring fault tolerance and durability

Dropping a bid is a non-starter. Imagine telling a user that they lost an auction because their winning bid was "lost" - that would be catastrophic for trust in the platform. We need to guarantee durability and ensure that all bids are recorded and processed, even in the face of system failures.

The best approach here is to introduce a durable message queue and get bids into it as soon as possible. This offers several benefits:

- **Durable Storage**: When a bid comes in, we immediately write it to the message queue. Even if the entire Bid Service crashes, the bid is safely stored and won't be lost. Think of it like writing your name on a waiting list at a restaurant - even if the host takes a break, your place in line is secured.

- **Buffering Against Load Spikes**: Imagine a popular auction entering its final minutes. We might suddenly get thousands of bids per second - far more than our Bid Service can handle. With a message queue, these surge periods become manageable. The queue acts like a buffer, storing bids temporarily until the Bid Service can process them. It's like having an infinitely large waiting room for your bids. Without a message queue, we'd have to either:
  - Drop bids (unacceptable)
  - Crash under the load (also unacceptable)
  - Massively over-provision our servers (expensive)

- **Guaranteed Ordering**: Message queues (particularly Kafka) can guarantee that messages are processed in the order they were received. This is important for fairness - if two users bid the same amount, we want to ensure the first bid wins. The queue gives us this ordering for free.

Note: Apache Kafka guarantees message order, but only within a single partition, meaning messages with the same key are guaranteed to be consumed in the order they were produced within that partition. 

Here's a more detailed explanation:

Partitioning and Ordering:
- Kafka divides topics into partitions, and messages are written to a specific partition based on their key (or randomly if no key is provided). 

Within-Partition Ordering:
- Kafka guarantees that messages written to the same partition are consumed by a consumer in the order they were produced. 

Consumer Groups and Partitions:
- Consumers belong to consumer groups, and each group reads from a unique set of partitions. 

Key-Based Partitioning:
- If you want to ensure the order of messages related to a specific entity, you should assign them the same key, which will cause them to be written to the same partition, ensuring ordered consumption. 

Idempotence:
- Since version 0.11.0.0, the Kafka producer provides an idempotent option for configuring message delivery, which guarantees that resending a message will not result in duplicate entries in the log, and that log order is maintained. 

Global Ordering (Across Partitions):
- Kafka itself does not guarantee global ordering across all partitions, so if you need to ensure ordering across multiple partitions, you need to implement that at the consumer level, potentially using stream processing frameworks like Apache Flink. 

#### Using Kafka as our message queue for the Bid service

For implementation, we'll use Kafka as our message queue. While other solutions like RabbitMQ or AWS SQS would work, Kafka is well-suited for our needs because:

- **High Throughput**: Kafka can handle millions of messages per second, perfect for high-volume bidding periods.
- **Durability**: Kafka persists all messages to disk and can be configured for replication, ensuring we never lose a bid.
- **Partitioning**: We can partition the Kafka topic(s) by auctionID, ensuring that all bids for the same auctionID are processed in order while allowing parallel processing of bids for different auctions.

Here's how the flow works:

1. User submits a bid to our client
2. API Gateway routes to a Kafka producer which immediately writes the bid to the appropriate Kafka topic's partition
3. Kafka acknowledges the write, and we can tell the user their bid was received
4. The Bid service (Kafka consumer) consumes the message from the Kafka topic at its own pace
5. If the bid is valid, it's written to the database
6. If the Bid service fails at any point, the bid remains in the Kafka topic and can be retried via a retry operation

<img width="750" alt="image" src="https://github.com/user-attachments/assets/edab41a1-29e4-4932-b734-53c513f3dfab" />

### Ensuring the system displays the current highest bid in real-time

Going back to the functional requirement of 'Users should be able to view an auction, including the current highest bid,' or current solution using polling, which has a few key issues:

- **Too slow**: We're updating the highest bid every few seconds, but for a hot auction, this may not be fast enough.
- **Inefficient**: Every client is hitting the database on every request, and in the overwhelming majority of cases, the max bid hasn't changed. This is wasteful.

We now need to expand the solution to satisfy the non-functional requirement of 'The system displays the current highest bid in real-time'. Here is how we can do it (discussed in 'Ensuring the system displays the current highest bid in real-time'):
- Long polling for max bid
- Server-sent events (SSE)

### Ensuring the system scales to support 10M concurrent auctions

When it comes to discussing scale, you'll typically want to follow a similar process for every system design question. Working left to right, evaluate each component in your design asking the following questions:

1. What are the resource requirements at peak? Consider storage, compute, and bandwidth.
2. Does the current design satisfy the requirement at peak?
3. If not, how can we scale the component to meet the new requirement?

We can start with some basic throughput assumptions. Our system will have 10M concurrent auctions, and each auction has ~100 bids. That's 1B bids per day. 1B / 100,000 (rounded seconds in day) = 10K bids per second.

#### Message queue

Let's start with our message queue for handling bids. At 10,000 requests per second, and decent hardware, a traditional message queue like Kafka or SQS can handle this without issue. So no need to even partition the queue.

#### Bid service

Next, we consider both the Bid service (consumer of the message queue) and Auction service. As is the case with almost all stateless services, we can horizontally scale these by adding more servers. By enabling auto-scaling, we can ensure that we're always running the right number of servers to handle the current load based on memory or CPU usage.

#### Database

Let's consider our persistence layer. Starting with storage, we can round up and say each Auction is 1 KB. We'll say each Bid is 500 bytes. If the average auction runs for a week, we'd have 10M * 52 = 520M auctions per year. That's 520M * (1 KB + (0.5 KB * 100 bids per auction)) = 25 TB of storage per year.

That is a decent amount for sure, but nothing crazy. Modern SSDs can handle 100+ TBs of storage. While we'd want to ensure the basics with regards to some replication, we're not going to run out of storage any time soon. We'd be wise to shard, but the more pressing constraint is with regards to write throughput.

10k writes per second is at the limit of a well-provisioned single Postgres instance. If we want to stick to our current solution for handling consistency, we'll need to shard our database, again by auctionID, so that we can handle the write load. We don't have any worries about scatter-gathers since all reads / writes for a single auctionID will be on the same shard.

#### SSE

Lastly, we talked about how our SSE solution for broadcasting new bids to users would not scale well. To recap, the problem is that when a new bid comes in, we need to broadcast it to all the clients that are watching that auction. If we have 10M auctions and 100M users, we could have 100M connections. That's a lot of connections and they wont fit on the same server. So we need a way for Bid service servers to coordinate with one another, such that they're aware of which Bid service server is handling which SSE connection to specific clients.

The solution is Pub/Sub. Whether using a technology like Redis Pub/Sub, Kafka, or even a custom solution, we need to broadcast the new bid to all relevant servers so they can push the update to their connected clients. The way this works is simple: when Server A receives a new bid, it publishes that bid to the pub/sub system, essentially putting it on a queue. All other instances (Bid service servers) of the Bid service are subscribed to the same pub/sub channel and receive the message. If the bid is for an auction that one of their current client connections is subscribed to, they send that connection the new bid data.

To see a more thorough solution to this issue, refer to the SDI 'FB live comments', where a similar Pub/Sub system is used between servers handling SSE connections.

Additional deep dives:

There are a lot of possible directions and expansions to this question. Here are a few of the most popular.

1. **Dynamic auction end times**: How would you end an auction dynamically such that it should be ended when an hour has passed since the last bid was placed? For this, there is a simple, imprecise solution that is likely good enough, where you simply update the auction end time on the auction table with each new bid. A cron job can then run periodically to look for auctions that have ended. If the interviewer wants something more precise, you can add each new bid to another queue (in addition to the Kafka queue) like SQS with delayed messages of an hour using SQS's message timers. A worker will then process each item after an hour and check if that bid is still winning. If yes, end the auction. This new SQS queue holding the delayed messages will only store the necessary data about the bid, like the bid amount and bidID, rather than storing the full bid object / details - and this queue will only be used to ensure the auction is dynamically ended.

2. **Purchasing**: Send an email to the winner at the end of the auction asking them to pay for the item. If they fail to pay within N minutes / hours / days, go to the next highest bidder.

3. **Bid history**: How would you enable a user to see the history of bids for a given auction in real-time? This is basically the same problem as real-time updates for bids, so you can refer back to the solution for that.
























