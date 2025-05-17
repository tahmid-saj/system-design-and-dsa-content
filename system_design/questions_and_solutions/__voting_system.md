# Voting system

Design a voting system which will allow voting for a period of time. The system should capture all votes made by users, and allow users to see the current number of votes for different items.

Note that this design is somewhat similar to the SDI 'Top K YouTube videos', and it's real-time view is similar to the leaderboard in the SDI 'Leetcode'

## Requirements

### Questions

- We don't want vote events to result in race conditions, so how frequently are votes coming in?
  - Votes will be coming in very frequently, likely 10-30k votes per second

- How long will the voting last, can it a few hours to days?
  - Yes, it can last anywhere from a few hours to days
  
- Should we also allow users to create a poll for different items?
  - Yes, design the poll creation

- Do we want to share a real-time view of the votes to the user?
  - Yes, share a real-time view of the votes to users

- During some spikes in high write traffic, some votes might take some time to be registered. Can our real-time view of the votes have just some slight delays?
  - Yes, that's fine as long as votes register in a few seconds or so
 
- Should the real-time view sort the items by their votes?
  - Yes, we want to show the real-time view in a sorted order by the items' votes

- What is the DAU and number of concurrent users per second?
  - Assume 100M DAU and 20k concurrent users per second

### Functional

- Users should be able to create a poll for different items
- Polls should last for a certain period, and allow users to vote for different items
- Users should be able to see a sorted real-time view of votes (may have some slight delay during high write traffic)

<br/>

- Assume 100M DAU and 20k concurrent users per second

### Non-functional

- Consistency of votes count:
  - All votes should be registered properly, and the system should prevent race conditions
- Throughput of votes:
  - Votes will be coming in very frequently, at 10-20k votes per second
- Low latency of real-time view is somewhat needed (a few second delay is fine) - thus, we will need to favor precomputed sorting of votes

## Data model / entities

- Polls:
  - This entity will contain the entire poll data, where there will be multiple itemIDs (and the itemID's votesCount) for a single pollID
  - Note that we'll denormalize some data, such as storing expirationTime for every entry - we'll do this mainly because the votes data will need to be stored in a write optimized DB such as Cassandra, where join operations with other tables is not supported
    - pollID
    - itemID
    - itemName
    - votesCount
    - expirationTime

- Vote event:
  - This entity will likely come from a vote stream such as Kafka, which will send how much the votesCount field in the Polls entity should be incremented for a specific itemID
    - itemID
    - votesIncrementValue

## API design

### Create poll

- This endpoint will allow users to start a poll with the items and expirationTime they provide

Request:
```bash
POST /polls
{
  items: [ itemName ],
  explirationTime
}
```

### Vote on item

- Users can vote on an itemID via this endpoint

Request:
```bash
PATCH /polls/:pollID/votes/:itemID
```

### Get real-time votes view

- Users can get a real-time votes view for a pollID

Request:
```
GET /polls/:pollID/votes
```

Response:
```bash
{
  items: [ { itemID, itemName, votesCount } ]
}
```

## HLD

### API gateway

- As the system will likely use multiple services via a microservice architecture, the API gateway will route requests to the appropriate service, handle rate limiting and authentication

### Votes service

- The Votes will allow users to create polls and make vote events. The Votes service will retrieve the vote events and increment the votesCount field for the itemID and pollID if the pollID hasn't expired yet. The Votes service will likely be IO or memory optimized EC2 instances, since the Votes service will frequently make requests to the database to update the votesCount field.

- Without using a queue in-between the client and the Votes service, it's likely some vote requests might lost or not get served. Because we want to ensure all votes are registered, we'll split the vote event writes from the poll creation by using a queue - discussed in the DD. Using a queue like Kafka will also help us batch vote events and ensure we don't make repeated updates to the databse.

### Database / cache

- The database will contain the polls data, where the votesCount field will be frequently written to. Because we want to ensure all votes are registered, without introducing race conditions in the votesCount field, we'll use Cassandra. Cassandra will allow us to handle a high write load on the votesCount increments, since the data is first written to memtables, then later flushed to SStables. Because Cassandra writes data via append-only to logs, there is a much lower chance for race conditions to occur like in PostgreSQL / DynamoDB which writes to disk.

The CQL create table statement will look as follows:
```cql
create table polls (
  pollID UUID,
  itemID UUID,
  itemName text
  votesCount int,
  expirationTime timestamp
  primary key (pollID, (itemID, votesCount))
with clustering order by (itemID, votesCount desc))
```

- This way, a single partition will contain a pollID (and all the items of the pollID for faster writes to a single partition), while the itemIDs in the partition will be ordered by the clustering keys itemID and votesCount in descending order so that we can retrieve the real-time votes view in sorted order by the votesCount.

#### Redis sorted set

- To retrieve the sorted real-time votes view, it may be inefficient to run the same query every few seconds on the database. While Cassandra is optimized for writes, reads might not perform well if there are multiple nodes in the Cassandra cluster. If a poll's vote data hasn't changed in a few seconds, then running the database query will also be more expensive than checking a cache.

- We'll cache the votes data - a Redis sorted set can easily handle both frequent reads and writes, and store the real-time votes view in a sorted set data structure. Thus the same Cassandra query will not need to be performed repeatedly - the Redis sorted set can be updated by incrementing the votesCount field (score) of itemIDs (members) in a pollID (key) as the database is being updated with incoming votes. Cassandra's CDC can likely be used to send real-time changes to the sorted set - discussed in the DD.

- We’ll use Redis since single-threaded operations within a Redis instance will lead to very rare race conditions - writes are atomic. However, race conditions are still possible in Redis when multiple clients / workers update the same itemID's votesCount, thus locking via a Redis distributed lock could potentially be used when updating votesCount of itemIDs in the cache - however, it might slightly increase latency. Additionally, Redis will provide pipelining which will further speed up write operations.

### Votes view service

- Using a Redis sorted set, clients can poll the Votes view service every few seconds, and the service will return the real-time view from the Redis sorted set. Polling for the real-time view may seem inefficient, however, it's more efficient than using websockets, which is better suited for bidirectional communication.

- SSE could also be used, where the vote events into the database also sends a request to the Votes view service, then the Votes view service will send the real-time votes updates to the client - a cron job could be scheduled in the Votes service to return the real-time view to the client every few seconds or so via SSE. SSE is more complex, and has more overhead in maintaining the connection, however, if users stay on the real-time view page for long periods then SSE might be more suitable because SSE generally takes up less bandwidth.

- Polling may be a more simpler solution, because the client will poll every few seconds, rather than receiving updates whenever votes change (which will occur frequently).

Note: Polling generally consumes more bandwidth than SSE because polling requires the client to repeatedly request data, even when no updates are available, while SSE maintains a persistent connection and only sends data when updates are available. 

<br/>

The workflow when a client sends a new vote event for an itemID in a pollID is as follows:

1. Client sends the vote event for itemID to the Votes service

2. The Votes service (API gateway will likely push the batched vote events by pollID to Kafka and Kafka streams could further batch by itemID -> the Votes service can then receive the batched vote events from Kafka - discussed in the DD) will update the votesCount field for the itemID

3. When the database is updated with these batched vote events, Cassandra's CDC will send real-time updates to the Redis sorted set, which will also update the Redis sorted set with the real-time votes data

4. Clients polling the Votes view service will then see this real-time votes view via the Redis sorted set

<img width="900" alt="image" src="https://github.com/user-attachments/assets/35f418ad-d9ce-48cd-9aae-9a0b55284274" />

## DD

### Separating low volume writes (poll creation) from high volume writes (vote events)

- As discussed in the HLD, because poll creation will happen much less frequently than vote events, it makes sense to separate the low volume writes from the high volume writes. The low volume writes could be written to a Polls service, while the high volume writes could be written to the Votes service.

- As the vote events are sent by users, the API gateway integrated with a Lambda containing the Kafka producer (the Kafka producer will also use the Transactional API to ensure exactly-once delivery of vote events) could publish the batched vote events (batching will be initially done by the pollID) into a "Votes" Kafka topic. Batched vote events for a pollID like look like:

```bash
{
  pollID: 1,
  voteEvents: [
    { itemID: 2, itemName: Toronto, vote: 1 },
    { itemID: 2, itemName: Toronto, vote: 1 }
    { itemID: 3, itemName: New York, vote: 1 }
  ]
}
```

- Kafka streams could then pull from the Votes topic and further transform / batch the vote events by the itemID before sending the batch to another target topic. The Votes service will then have multiple workers (containers) which implements a Kafka consumer to consume from this target topic and update the batched vote events into the votesCount field for the itemIDs in the DB.

- By using Kafka, we ensure that vote events are never lost, and that votes will also be initially batched by the producer via by the pollID (using a Lambda function) and using Kafka's batch settings such as batch.size (the batch size in bytes) and linger.ms (how long Kafka should wait to fill a batch). Kafka streams could then further batch the vote events by the itemID, so that we don't need to make multiple DB requests for vote events linking to the same itemID.

#### Kafka topic partitioning by pollID

- For a single pollID, we want the Kafka consumer to consume from a single partition when writing the batched vote events of all the itemIDs in the pollID. To ensure this, we can set the message key as the pollID, which will mean that a consumer will only read from a single partition when updating the batched votes of a pollID in the DB.

- If a consumer had to read from multiple partitions of the topic, this might slow down the consumption and updates to the DB because the DB requests will be made to multiple partitions, thus it makes sense to partition the topic via pollID.

### Efficiently fetching real-time votes view

To efficiently fetch from the real-time votes view, we can do the following and in ‘Efficiently fetching from the real-time votes view’ (taken from the SDI 'Leetcode'):

- Polling with database queries

- Caching with periodic updates:
  - Using this approach, we will still cache majority of the queries, but when there are cache misses,			the servers will run the query on the database, which may still be expensive. To make sure			there are more cache hits using this approach, we could still use a cron job which runs every 10-20			secs or so and updates the cache. Thus, only the cron job will be running the expensive query on			the database, and clients will have reduced cache misses.

  - The issue with using a cron job is that if it is down, then the cache will not be updated, and it will			cause multiple cache misses OR a thundering herd due to the clients requesting the servers to			run the expensive database query

  - If using another cache such as Memcached, it may cause race conditions if the same entry on			the cache is being updated by multiple processes, however Redis is single threaded, and thus will			likely not have this issue within a single instance

- Redis sorted set with periodic polling: 
  - There may be inconsistencies between the database and cache, thus we could add CDC			(change data capture). For different databases like DynamoDB, there is DynamoDB streams, and		for Cassandra, there is Cassandra's CDC. CDC is used to capture updates on the database in		the form of WAL or another operations log, and replay any missed operations on other services. Usually CDC functionalities for various databases will store the operations in the WAL, and push		it to a queue such as Kafka - then there will be workers within the other service which will pull			operations from the queue and perform the operations on the other service
  - In		this case, we can use CDC to replay operations on the Cassandra database to the cache using	Cassandra's CDC to ensure the cache and database have the same consistent data

- Note that we could also use a websocket connection between the servers and the clients, however this		may be an overkill, because we don’t require very strict low latency updates like 1 sec for the real-time votes view. Also scaling up websocket connections may be more difficult than polling, as we’ll need a		separate service discovery component or an L4 load balancer managing the client to websocket server mappings and any sticky			sessions.

Efficiently fetching from the real-time votes view:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/d5e1c28a-6bce-4801-b146-f55688d3e78b" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/a44ce39d-b012-4e50-957e-14b8baec10af" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/7a420fec-d6be-4908-87db-e28c8e384fde" />

**The Redis Sorted Set with Periodic Polling solution strikes a good balance between real-time updates and simplicity. It's more than adequate for our needs and can be easily scaled up if required in the future. If we find that the 2-3-second interval is too frequent, we can easily adjust it.**

### Scaling the database and services

We'll scale the system from left to right:

#### Scaling the database

- As discussed in the HLD, we'll partition the Polls table via the pollID, where a single request to update the votesCount fields for itemIDs will be routed to a single node (or multiple nodes asynchronously depending on the write consistency and quorum level). This way, we can save some DB requests by batching vote events for itemIDs belonging to the same pollID, and then update a single partition in the Polls table.

#### Scaling the services

- Because all of our services (Polls, Votes, and Votes view service) are stateless, they can be easily horizontally scaled. In particular, because there will be very frequent vote events and requests to view the real-time view, the Votes and Votes view services will mainly be configured with horizontal scaling. 



























