# Twitter

Note that this SDI is similar to the FB news feed one, however the design contains a few more requirements such as liking / disliking tweets, searching tweets, retweeting / replying, etc

## Requirements

### Questions

- Are we handling a uni-directional "follow" relationship, or a bi-directional "friend" relationship?
  - Let's assume we're handling the uni-directional "follow" relationship. Twitter actually follows this.

- In this system, users can create tweets, like / dislike / retweet / reply to tweets, follow other users, view their own feed consisting of tweets from other users they follow, and search tweets. Are these all the features we're designing?
  - Yes

- Can users have a limited number of followers?
  - No, the follower count is unlimited
 
- Are we handling attachments in our tweets?
  - Yes
 
- Will the feed be created by tweets from a group, page, etc as well?
  - For simplicity, let's leave out groups, page, etc. But a group and page could simply be thought of as a user itself

- Can we assume that the feed's tweets are returned in chronological order by using the tweet's creation timestamp?
  - Yes

### Functional

- Operations on tweets:
  - Users can create tweets, retweet, delete their tweets, like or	dislike tweets, reply to tweets
- View user timeline and tweet feed:
	- Users can view their timelines, which contain their own tweets, and also view a tweet feed in a chronological order
- Follow or unfollow users
- Search tweets

### Non-functional

- Availability > consistency:
  - Users' feeds don't necessarily need to update immediately when another user creates a tweet, we can tolerance up to 2 mins and follow an eventual consistency model
- Low latency:
  - Posting tweets, viewing results of the feed, and searching tweets should be fast, between 10 - 500 ms
- The system should be able to support large amounts of following / follower relationships between users

## Data model / entities

- Note that twitter uses Twitter Snowflake to generate unique IDs for many of it’s services such as tweets

- User:
	- userID
	- userName
	- userEmail

- Tweets:
  - tweetID
  - tweet
  - s3AttachmentURLs
  - likes / dislikes / retweet counts
  - tweetMetadata: { createdAt }

- Follows:
  - A single entry in the Follows table will contain the below fields
    - userID (PK)
    - userIDFollowing (SK)

- Retweets:
	- retweetID
	- tweetID
        - retweet
	- s3AttachmentURLs
        - likes / dislikes / retweet counts
	- tweetMetadata: { createdAt }

- Replies:
        - replyID 
	- tweetID
	- userID
	- reply
	- metadata: { createdAt }

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Create tweets

Request:
```bash
POST /tweets (Used for creating a tweet)
POST /tweets/:tweetID?op={ RETWEET } (Used for creating a retweet)
{
	tweet
}
```

### Follow / unfollow a user

- Note that the follow / unfollow action will be idempotent in that instead of a new resource being created each time, multiple requests will only create one follow / unfollow relationship. Multiple requests won't produce unwanted behavior.

Request:
```bash
PATCH /users:/userID?op={ FOLLOW / UNFOLLOW }
```

### View user timeline or feed (feed is in the home page of twitter)

- Note that if we wanted to render the tweet's attachments (such as photos) for the paginated results on the client side, then there would be 2 requests being made instead, where the client would first request for the paginated tweets with the pre-signed URLs to the attachments. Afterwards, the client will use the pre-signed URLs to fetch the tweet's attachments from the blob store.

Request:
```bash
GET /users/:userID/timeline?nextCursor={ current oldest tweet's createdAt in viewport }&limit (Used to view user timeline)
GET /feed?nextCursor={ current oldest tweet's createdAt in viewport }&limit (Used to view feed)
```

Response:
```bash
{
  tweets: [ { tweetID, userID (if returning a feed instead of a timeline, tweet, createdAt), userName, tweet, createdAt } ],
  nextCursor, limit
}
```

### Liking / disliking a tweet
  
- Note that we’re using PATCH here as it's mainly used to only update a small	portion of an entry, while PUT is used to update the full entry

Request:
```bash
PATCH /tweets/:tweetID?op={ LIKE / DISLIKE }
```

### Searching tweets

- Note that we’ll use cursor based pagination to search for tweets as the number of	tweets returned may be very large, and as such we’ll return paginated results which	will use lazy loading and fetch the results only for current viewport
- Searching for tweets will likely be handled by a search service, which will use the inverted index mappings to return search results

Request:
```bash
GET /tweets?query&sort={ LIKES / DATE }&nextCursor={ last tweetID on viewport if using LIKES as sort order OR oldest createdAt value on viewport if using DATE as sort order }&limit
```

Response:
```bash
{
  tweets: [ { tweetID, userID, userName, tweet, likes / dislikes / retweets, createdAt } ],
  nextCursor, limit
}
```

### Replying to a tweet

Request:
```bash
POST /tweets/:tweetID/op={ REPLY }
{
	reply
}
```

### Add attachment to tweet

- When uploading binary data, multipart/form-data / multipart/mixed or another MIME	type such as image/png is usually used

- The content type is set to multipart/mixed which means that the request contains	different inputs and each input can have a different encoding type (JSON or binary).	The metadata sent will be in JSON, while the file itself will be in binary. 

- The placeholder {---xxBOUNDARYxx—} will contain a text string for the boundary	that differentiates one part of the body from another. For example				“__the_boundary__” could be used as the string. Boundaries must also start with		double hyphens and end with double hyphens too.

- Note that since this design is using a pre-signed URL to upload files, the client will	first request for a pre-signed URL from the servers, then make a HTTP PUT request	with the file data in the request body to the pre-signed URL 

#### Request for a pre-signed URL

Request:
```bash
POST /tweets/pre-signed-url
{
	fileType
}
```

Response:
```bash
{
	pre-signed URL
}
```

#### Upload to pre-signed URL

Request:
```bash
PUT /<pre-signed URL>
Content-Type: multipart/form-data; boundary={---xxBOUNDARYxx—}
{
—xxBOUNDARYxx–
<HEADERS of the boundary go here>

We’ll put the file binary data in this boundary:

<attachment contents go here>

—xxBOUNDARYxx–
}
```

Response:
```bash
Content-Type: application/json
{
	UPLOADED / FAILED
}
```

## Questions

Q: It’s New Year’s Eve, and Twitter is expecting a huge surge in traffic. As a system design engineer, what changes would you make to the high-level design to ensure the system is ready for this traffic and does not experience downtime?

A: 
- Caching:
  - Implement caching strategies for frequently accessed data to reduce the load on the database and ensure faster response times. Database Scaling: Add more database servers to distribute the load more effectively. This helps in managing the increased traffic without any single point of failure.
- Load Balancing:
  - Optimize the load balancers to distribute incoming traffic evenly across all servers. This ensures no single server is overwhelmed, maintaining the system’s availability and responsiveness.
- Failover Strategy:
  - Have a robust backup plan in case of a failure. This includes having standby systems that can quickly take over without disrupting the service.
- Sharded Counters:
  - Increase the number of shards for sharded counters, which are used to manage high volumes of write operations, such as likes or retweets, to prevent bottlenecks.

## HLD

### Microservice architecture

- A microservice architecture is suitable for this system, as the system requires independent services such as tweet creation, feed retrieval, user relationships management, etc. These are all independent operations which could potentially be managed by separate services.

- Microservices can benefit from a gRPC communication as there will be multiple channels of requests	being sent / received in inter-service communication between microservices. Thus, gRPC could be the	communication style between microservices, as it supports a higher throughput, and is able to handle multiple channels of requests as opposed to REST, which uses HTTP, that is not optimized for		multi-channel communication between services.

### API gateway

- The API gateway will provide rate limiting, authentication, and route requests to the specific services.	For example, for a tweet creation request, the API gateway could route the request to the Tweets service.

### Tweets service

- The Tweets service will handle tweet creation requests, liking / disliking / retweeting / replying to tweets, etc, and store the tweet in the Tweets table. Also, this service could potentially provide pre-signed URLs to the clients for them to upload attachments for tweets. Overall, this service will be stateless and can be easily scaled horizontally.
- Because tweet creation may likely need to be fed into different components like the Tweets table, Feeds cache, etc to perform a push based model (fan-out on write), we'll need additional queues and workers between the Tweets service to the relevant consumers as discussed in the DD. Also, as users may be frequently liking / retweeting / replying to tweets, we can use similar queues and workers between the Tweets service and relevant consumers as discussed in the DD.

### Tweets table / cache

- The Tweets table will store all the created tweets from all users. We can use either a SQL or NoSQL database such as DynamoDB here. The data doesn't necessarily contain that many relationships, such that a SQL database would be the most optimal here, thus we'll use DynamoDB because it's more optimal for horizontal scalability, and for performing low latency queries using GSI, which will support faster reads. However, SQL can also be used here.
- For faster lookups to get tweets from a specific userID, we'll set the userID as a partition key in the Tweets table, and set the createdAt field as the sort key to return the tweets in chronological order.

#### Tweets cache

- In the Tweets cache, we can store frequently accessed tweets with an appropriate TTL, so that the Tweets, Feed and Timeline services could retrieve the cached posts.
- We can use Redis for both the Tweets and Feed cache, since we can benefit from Redis's support for complex data structures such as lists / sorted sets, which will further help in storing the feed and tweets in a sorted fashion using the createdAt field. If we use a Redis sorted set, when we add or retrieve a post, the posts within the sorted set for a specific userID will always remain sorted by the createdAt field.
- Redis also provides Redis cluster which will help to scale the Tweets and Feed cache, as opposed to Memcached which doesn't provide direct built-in replication support. To scale for viral or hot key tweets, the Tweets cache can replicate it's instances to solve hot key issues for viral tweetIDs as discussed in the DD.

### Follows table

- The follows entity contains many-to-many relationships between users. Usually relationships like this can be modeled in a Graph DB such as Gremlin, Neptune, Neo4j, etc. However, a simple KV store such as DynamoDB also works, and can model the relationships.
- Graph databases may be more useful when there is a need to do traversals or analysis on the relationships, where there are DFS / BFS algorithms which perform traversals through the graph's nodes, like finding the friends of friends, or recommending users to follow specific users in their network, etc. Graph databases are also usually harder to scale and partition than traditional NoSQL databases, and requires more domain level knowledge.
- Our use case follows a simple requirement, which involves creating feeds based on who the user is following. Thus, we'll use DynamoDB, where the userID and userIDFollowing fields is the full primary key (composite key) of the Follows table. This will quickly allow us to check if a user is following another user. We can also set the userID as the partition key to ensure lookups are fast for a single userID. Also, the userIDFollowing can be a secondary index to allow us to look up who the userID is following quickly.

### Feed service

- The feed service should allow the client to retrieve their feed, thats developed by compiling the tweets of the users the client is following. We can compile the user's feed and store it in the Feed cache. This way, the feed isn't generated on each response, but generated in the background and stored in the Feed cache beforehand. Clients will then request the Feed service to return their feed that's stored in the Feed cache

- To return the paginated tweets to the user (via cursor based pagination), and return tweets in their feed as they're scrolling, we can use the oldest createdAt field in their viewport. This can be done because users are viewing tweets from the earliest to the oldest in their viewport, and these tweets will also be returned by using the createdAt as the sort key in the Tweets table.
- Everytime the user scrolls down, we'll return a new paginated result of the tweets with the cursor pointing at the current viewport's oldest createdAt value.
- We'll also store the previously viewed tweets in the client's browser within a cache of a small TTL value. This way, when the user scrolls up, they'll still be able to see the previously returned tweets.

- However, if the feed isn't created ahead of time, the Feed service will build it (using the Tweets and Follows tables) and place it temporarily in the Feed cache, then return the paginated tweets of the feed to the user. The feed can be periodically built for the user, let's say every 15 mins or so, and then updated in the Feed cache

#### Naive feed generation

- A naive way to view the feed of tweets for a specific userID is as follows:
1. We get all the users who the userID is following
2. We get all of the tweets from those users
3. We sort the tweets by createdAt OR rank them, and return paginated results to the userID
- The steps above for this naive solution has a lot of issues which will be discussed in the DD, such as:
  - The userID may be following lots of users
  - The userID may have a lot of followers
  - A userID may have millions of tweets
  - The number of tweets in the Feed cache may be large because of the above issues (we'll likely need a Feed table instead of a Feed cache)

- A naive feed generation query in SQL would look as follows. The result from this query could then be stored in the Feed cache:
```sql
select tweetID, tweet, createdAt from tweetsTable
where userID in (select userIDFollowing from followsTable where userID = ${userIDGeneratingFeedFor})
and createdAt >= ${nextCursorCreatedAt}
order by createdAt desc
limit 200
```

#### Frequently online vs offline users

- It's also likely a lot of users don't frequently log-in, and thus we don't need to store their generated feed in the Feed cache. If a user hasn't logged in for a long time, the feed could be generated when they request for it, but if the user frequently logs in, the feed could be pre-generated and stored in the Feed cache. The Feed service could implement the logic to regularly pre-generate the feed for frequently online users.

### Feed cache

- We can compile the user's feed and store it in the Feed cache. This way, the feed isn't generated on each response, but generated in the background and stored in the Feed cache beforehand.

- A feed entry for a userID may look as follows (TTL may be a small value like 2 mins - which is the amount of time we can tolerate for the feed to update):
```bash
userID: { tweets: [ { tweetID, userID, tweet, likes / dislikes / retweet count, createdAt } ], TTL }
```

- We can use Redis for both the Tweets and Feed cache, since we can benefit from Redis's support for complex data structures such as lists / sorted sets, which will further help in storing the feed and tweets in a sorted fashion using the createdAt field

### Timeline service

- The timeline service will handle requests for viewing the user's timeline. To generate the user's timeline, we'll fetch the user's tweets from the Tweets table, and apply pagination to the results

### Search service

- The search service will search for tweets via inverted index mappings built using the the Tweets table, most likely using both a creation and likes inverted index using a Redis list and sorted set respectively. The design for the search service is in the SDI 'Twitter search'. The DD will also go over scalability of the writes on tweets / retweets / replies, likes, and searching tweets.

### Blob store

- The blob store will contain the attachments uploaded by users. The Tweets service will provide pre-signed URLs to this blob store (S3), such that the user can upload the attachments.

Aditional components:

### Notification service

- The notification service will send optional push notifications when new tweets are available. The Tweets service can asynchronously request the notification service to send a push notification to the userID's followers (if the userID doesn't have numerous amounts of followers) that the userID created a tweet

### Twitter's client side load balancer

- Twitter uses a client-side load balancer specifically able to route twitter requests: https://www.educative.io/courses/grokking-the-system-design-interview/client-side-load-balancer-for-twitter

### Twitter's actual data stores

- Twitter uses various data stores as explained below. The idea of “one size fits all” is not applied in this design as Twitter uses services specifically catered for their use cases.

#### Google Cloud

- Twitter uses HDFS (Hadoop distributed file system) which consists of tens of thousands of servers to host data. The data are mostly compressed by LZO, which is a data compression algorithm, because LZO works efficiently in Hadoop.
- The data includes logs from client events, tweets and timeline events, ad targeting and analytics, MySQL databases, user profiles and social graphs. In 2018, Twitter decided to shift the data from Hadoop clusters to Google cloud to better analyze and manage their data in a hybrid cloud environment. Twitter also stores it’s big data in BigQuery, which is a scalable serverless data warehouse service. Twitter also uses Presto which is a SQL query engine to access data from Google cloud (BigQuery, Google cloud storage and so on).

#### Manhattan

- As users rapidly grew, in 2010, Twitter used Cassandra to replace MySQL, but could not fully replace all of the MySQL databases due to incompatibility for some of the databases with Cassandra.
- In 2014, Twitter launched it’s own real-time distributed KV store called Manhattan and deprecated Cassandra. Manhattan stores the backend data for tweets, user profile, direct messages, and so on. Manhattan runs different types of clusters depending on the use cases, such as smaller clusters for un-common or read-only data or bigger clusters for heavy read/write traffic.
- The underlying storage engine Manhattan uses was RocksDB, which is a high performance KV store that makes use of fast storage systems like solid state drives. RocksDB is mainly uses for input/outbound workloads.
- As shown in 'Twitter's Manhattan engine', Manhattan uses RocksDB as a storage engine for storing and retrieving data.

Twitter's Manhattan database:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/22aa7799-45a1-4a83-a54b-cf4f8155b284" />

#### Twitter's blob store

- Twitter also uses their own blob store storage system to store attachments in tweets as binary files. After a certain time, the server will move the objects in the blob store to a more cold storage tier.

#### Relational database

- Twitter uses both MySQL and PostgreSQL to store relational data with high consistency but may be tolerable with higher latencies, such as ads and campaigns data.

#### Kafka

- Twitter uses Kafka to stream real-time events asynchronously, and also uses Google Dataflow jobs to handle deduping and real-time aggregation. After the events are aggregated, the results are stored for ad-hoc analysis in BigQuery, and the aggregated counts are stored in BigTable which is a NoSQL database. - Twitter also converts Kafka topics to Cloud Pub-sub topics using an event processor, which helps to avoid data loss and provides more scalability. The workflow of real-time event streaming for Twitter is in 'Twitter real-time event streaming'.

<br/>

Twitter real-time event streaming:

<img width="1026" alt="image" src="https://github.com/user-attachments/assets/60090c1e-f41f-4eca-acfe-ca4faa128787" />

#### FlockDB

- A relationship refers to the user’s followers and who the user also follows. Twitter stores the relationships in the form of a graph using FlockDB, which is a graph DB that is capable of storing large adjacency lists for fast reads / writes, and also provides various graph traversal operations.

#### Apache lucene

- Twitter uses Apache Lucene for real-time search, that uses inverted index mappings of documents. Twitter also caches in Lucene a real-time index of any recent tweets during the past week for low latency reads.

### Twitter's actual cache

- Twitter used Memcached and Redis clusters previously, however due to latency issues, Twitter started using the Pelikan cache.
- Pelikan is a framework for building a local or distributed cache. It is mainly used to replace most of Memcached or Redis clusters. Pelikan is better suited to Twitter’s use case of spinning up cache clusters rapidly, as Pelikan provides an automation script feature for creating clusters and jobs. Redis is better suited for complex data models, and is not easy to rapidly deploy horizontally.

- Additionally, Twitter was also looking to have a smaller size in a cached data entry. As such, Memcached had 56 bytes of metadata per key, while Pelikan has 39 bytes, which provided a lower latency for reads. Twitter essentially reimplemented their Memcached and Redis clusters using Pelikan.

### Twitter's ZooKeeper service

- Twitter also uses Zookeper for service discovery, cluster management and observability on the nodes of different services. Twitter also uses Zookeper to perform leader election on the nodes when a node is down

### Twitter's counters

- Twitter has million of users, and some users may be celebrities having millions of followers. Millions of followers may also engage with the celebrity’s tweets in a short time. This problem is known as a heavy hitter problem.
- Twitter needs multiple distributed counters to manage burst write requests for these tweets. Each counter will have several shards working on different computational units. These distributed counters are known as sharded counters. These sharded counters also help in solving the top K problem, which is to display the top K tweets or trends. Twitter also uses hashtags in in showing the top K tweets or trends.

### Twitter's search service

- Twitter uses Apache Lucene as the search service. Apache lucene will store the index mappings of the documents and cache the recently published tweets (let’s say in the past week). It may also use an indexer which constantly indexes the tweets asynchronously and pushes the index mappings to Lucene, for them to be searched.

### CDN

- Twitter uses CDN POPs to serve requested content with low latency. When users search for a tweet or profile, the system will first search the CDN PoP servers to see if it exists in there

<img width="900" alt="image" src="https://github.com/user-attachments/assets/80cd1f8f-4ba1-4aff-b2e6-7455b77d6218" />

## DD

### Handling users who are following a large number of users (fan-out issue)

**Note that the below logic is also applicable to a retweet and a reply. A tweet in this case can refer to both a retweet or a reply**

- If a user is following a large number of users, the queries to the Follows table will take a long time to run. Also, we'll make a large number of queries to the Tweets table to get the tweets of the large number of users. This problem is known as "fan-out" - where a single request fans out to multiple requests
- We can usually solve the fan-out issue by building the user's feed during tweet creation by those large number of users, instead of building the feed when the user requests for it.
- Sometimes, apps like FB also limits the number of friends to 5K. This can also help to prevent the fan-out issue
- Additionally, we can solve the issue using the below approaches, and in 'Handling users who are following a large number of users':
  - Horizontal scaling via sharding
  - Adding a feed table:
    - This approach is a push based model (fan-out on write), where upon the tweet creation, the creator performs the writes to the Feed table if the creator has a follower that is following a large number of users
    - The Feed table in this approach will only contain users following a large number of users. Thus, if a userID only has about 10 users they're following, then that userID will not have an entry in this Feed table. We'll also only store the tweetIDs, and maybe additional metadata in this table. An entry in the Feed table may look as follows:

```bash
userID (user that's following a large number of users): [ 200 or so tweetIDs + tweet metadata ] 
```

### Handling users with a large number of followers (fan-out issue)

**Note that the below logic is also applicable to a retweet and a reply. A tweet in this case can refer to both a retweet or a reply**

- When a user has a large number of followers, we have a similar fan-out issue if a celebrity creates a tweet, then we would need to write the tweetID to millions of entries in the Feed table / cache. We can solve this issue using the below approaches, and in 'Handling users with a large number of followers':
  - Shotgun the requests
  - Async workers:
    - There could be load balancers between the Tweets service to the queues, and also between the queues to the async workers. Using this approach, the load balancers will route the request to the appropriate queue or worker based on how many requests / messages they are handling. 
    - We could also use consistent hashing instead of load balancing the requests, however, load balancing will route requests based on the capabilities and state of the queues / workers, which consistent hashing won't do.
  - Async workers with hybrid feeds:
    - This approach combines the push based model (fan-out on write) discussed previously, with a pull based model (fan-out on read) - creating a hybrid model.
    - The pull based model occurs when a user with many followers creates a tweet. This tweet is not sent to the user's millions of followers, but instead the followers will pull and read this tweet from the Tweets table. Therefore, we'll use a push model for users with multiple users they're following, and use a pull model for users with multiple followers.
    - The number of celebrities (users with multiple followers) won't likely be that high, thus we won't pre-compute and write any of their tweets to the Feeds table, since we'll need to write this tweet to millions of userIDs in the Feeds table. Instead if a userID is following a celebrity, that userID will fetch the celebrity's tweets from the Tweets table.
    - The Feeds service will need to pull both the userID's feed from the Feeds table / cache, and tweets from celebrities they're following from the Tweets table. Thus, the Feeds service should have the functionality to verify if the userID is following any celebrities, or if the user themself is a celebrity, or if the user is following many users
    - Because in the pull based model, the userID pulls the posts from the Tweets table, instead of a feed being pre-generated for them in a push based model, the pull based model works better for inactive users who rarely login. The pull based model works better for inactive users because it doesn't waste compute by pre-generating a feed in the Feed table / cache for them.
    - The downside of a pull based model is that it will be pulling from a table / cache and creating the feed in real-time, which may take some time, instead of having a feed already built with the push based model.
      - userID following many users -> Followees will pre-generate feed for the userID's entry in the Feed table
      - Celebrity -> Users will pull celebrity's tweetIDs from Tweets table
      - Regular user -> Pre-generate the feed (push based model) if the user is active, otherwise use the pull based model

### Handling uneven reads of tweets

- The feed in this system is mainly built using the Tweets table, however certain tweetIDs within the Tweets table may be read much more often (like tweetIDs from celebrities) than other tweetIDs. This will cause uneven reads of tweets, which could also cause hot key problems. This issue can be solved by the below approaches, and in 'Handling uneven reads of tweets / posts':
  - Tweet cache with large keyspace
  - Redundant tweet cache

### Handling large volume of writes

We have two types of writes - tweet / retweet / reply creations, and like events which we'll need to handle:

#### Tweet / retweet / reply creations

**Edge cases for celebrities and for users following many users is handled by the hybrid push and pull based model. However, scalability of these writes still needs to be addressed when it comes to updating the search service when new tweets are created.**

**Note that the below logic is also applicable to a retweet and a reply. A tweet in this case can refer to both a retweet or a reply**

- When a tweet is created, we'll need to tokenize the tweet and then write to likely both a creation and likes indexes within the search service so that it can update both the tweet creation and likes index. If a tweet has 100 words, we might trigger 100+ writes one for each word (if we use bigrams of shingles, we'll have a lot more writes). With a large number of tweets being created concurrently, the search service may become a SPOF.
- To prevent the search service from becomming a SPOF, we can easily horizontally scale the servers as this is a stateless service.

Kafka queues between tweets / likes service and search service servers:

- Also, to prevent tweet creation data from being lost as it is waiting to be indexed via the search service, a Kafka queue can be positioned between the Tweets service and the search service's servers. Also Kafka can be configured such that it buffers messages so that the data is not lost within the queue. Buffering in Kafka will also handle bursts of messages being sent since the message data can be stored temporarily to prevent message loss during bursts.
- The Kafka messages could also be deleted periodically via a TTL of a few mins. The number of Kafka queues can be configured according to the number of search service servers (or rather the search service's indexing servers - which will perform the actual indexing), where if the number of workers in an search service server grows, the number of queues will also grow.

Sharding the inverted index mappings:

- Lastly, we can shard the creation and likes indexes on the term, so that queries for a single term will only need to search through a single shard, and the search for multiple terms can be done in parallel by querying all the term's corresponding shards.

#### Likes

- Likes occur much more frequently than tweet creations (10x more frequently). We can reduce the number of writes we need to do for "like events" by doing the below, and in 'Reducing writes for like events':
  - Batch likes before writing to the database
  - Two stage architecture

### Partitioning and sharding the Tweets, Follows and Feed tables

#### Tweets table

- For faster lookups to get tweets from a specific userID, we'll set the userID as a partition key in the Tweets table, and set the createdAt field as the sort key to return the tweets in chronological order. The Tweets table could also be sharded by userID as well - thus, we'll have shards split by the userID where a single shard will contain a range of userIDs (we'll assign a userID to a shard either with or without a hash function + mod), then partitions further split by the userIDs within the shard, then set the sort key to createdAt to return tweets in chronological order.
- We won't shard or partition by the tweetID since this will mean that a single userID's tweets will be spread across different shards / partitions, which means we'll have to query multiple shards / partitions - making it complex.
- We also won't shard or partition by the createdAt timestamp because it's 1) this would mean that the shard with the latest createdAt timestamp values would be requested the most and cause a hot spot, 2) new writes will always go to the shard with the latest createdAt 3) its a very granular value to shard with

#### Follows table

- We can set the userID as the partition key to ensure lookups are fast for a single userID in the Follows table. Also, the userIDFollowing can be a secondary index to allow us to look up who the userID is following quickly.
- Likewise with the Tweets table, we can further shard the Follows table by the userID - thus we'll have shards split by the userID where a single shard will contain a range of userIDs (we'll assign a userID to a shard either with or without a hash function + mod), then partitions further split by the userIDs within the shard, then set the secondary index to userIDFollowing for faster lookups when looking up who the userID is following quickly.

#### Feed table

- Because we'll be using the userID as the primary key in the Feed table, we can partition / shard using the userID where a single shard will contain a range of userIDs (we'll assign a userID to a shard either with or without a hash function + mod), which would support faster lookups. This also makes the most sense, since the feeds from different users are independent to one another, and thus the feeds can be fetched in parallel for different userIDs.
- However, some userIDs could still have slighly larger feeds than other users, which might cause some uneven distribution in the Feed table. We can limit the feed size to 200 or so tweetIDs in this Feed table, so that the feed distribution is more even.

### Handling large volumes of read requests

- To handle large volumes of read requests, caching the results to handle large volume of read results may be the best solutions as explained below and in 'Handling large volume of search / read requests':
  - Use a distributed cache alongside our search / tweet service
  - Use a CDN to cache at the edge

Additional deep dives:

### Ranking tweets

- Ranking could be done by a separate algorithm using the createdAt time, likes count, tweet from a celebrity, etc. When the Feed service is generating the feed, another service called the Ranking service could be used, which assigns a score to each tweet within a user's feed, and then returns the ranked tweets for the feed.

### Handling multi-keyword search queries

- To support searches for multi-keyword queries like "This is a multi-keyword query", we can do the following and in 'Handling multi-keyword queries':
  - Intersection and filter:
    - Intersecting the results from a multi-keyword search will be very compute intensive since some results may contain millions of entries. Also, implementing the intersection between the search results would mean that we may need to maintain a hash map of the tweetIDs - which will further increase both storage and latency as we'll need to perform a complex operation everytime a user searches.
  - Bigrams of shingles

### Fault tolerance of inverted index mappings

- To ensure fault tolerance of the inverted index mappings, we can replicate the inverted index mappings. Redis Cluster provides built-in asynchronous primary-secondary replication by default, which should be suitable here since write inconsistencies via a leaderless approach could have issues in the inverted index mappings (which requires low latency reads).

#### Keeping a reference to the indexServerID in the Tweets table to recover when inverted index mappings are down / erased

- If both the primary and secondary nodes for an inverted index mapping shard are down, then it would be really difficult to rebuild the shard's inverted index mappings again without knowing which terms were stored in this crashed shard.
- We can store a reference to the indexServerID for a tweetID in the Tweets table or ZooKeeper. This will allow us to query the Tweets table, and look for tweets with the indexServerID that crashed. Afterwards, we can rebuild the index for those tweets with the crashed indexServerID.
- However, maintaining this indexServerID field may have some overhead if we need to update the indexServerID during scaling events, but it ensures fast recovery time if the inverted index mappings are down / erased. Thus, this overall mapping between the indexServerID: [ tweetIDs ] could instead be maintained in a service like ZooKeeper, which provides a KV store for maintaining server-size mappings like these.

### Reduce storage space of inverted index mappings

- Users are usually only interested on a small portion of tweets, thus we can do the following optimizations:
  - Put limits on how many tweetIDs a single term in the inverted index will contain. We probably don't need all tweetIDs with "dog" in the tweet content - only about 1k - 10k tweetIDs for "dog" should be fine.
  - Ignore stopwords like "a", "of", etc (when updating the inverted index) which provide no value in searching.
  - In-frequently accessed terms and their creation / likes index mappings could instead be moved to a cold storage such as in S3 Standard-IA. If there are queries for these in-frequent terms, the query could first check the Redis inverted index mappings, and if results are not in Redis, it could instead be queried from S3 via Athena and returned to the client with a small increase in latency.

