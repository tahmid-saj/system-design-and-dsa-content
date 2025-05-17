# FB news feed

Facebook is a social network which pioneered the News Feed, a product which shows recent stories from users in your social graph.

## Requirements

### Questions

- Are we handling a uni-directional "follow" relationship, or a bi-directional "friend" relationship, which were more important for the earliest versions of Facebook?
  - Let's assume we're handling the uni-directional "follow" relationship

- In this system, users can create posts, follow other users, and view their own feed consisting of posts from other users they follow. Are these all the features we're designing?
  - Yes

- Can users have a limited number of followers?
  - No, the follower count is unlimited

- Are we handling attachments in our posts?
  - Yes
 
- Will the feed be created by posts from a group, page, etc as well?
  - For simplicity, let's leave out groups, page, etc. But a group and page could still simply be thought of as a user itself

- Can we assume that the feed's posts are returned in chronological order by using the post's creation timestamp?
  - Yes

### Functional

- Users can create posts
- Users can follow other users
- Users can view a feed of posts from other users they follow, in some chronological order
  - Users can page through their feed

### Non-functional

- Availability > consistency:
  - Users' feeds don't necessarily need to update immediately when another user creates a post, we can tolerate up to 2 mins, and follow an eventual consistency model
- Low latency:
  - Posting and viewing results of the feed should be fast, between 10 - 500 ms
- The system should be able to support large amounts of following / follower relationships between users

## Data model / entities

- Users:
  - userID
  - userName
  - userEmail
 
- Posts:
  - postID
  - userID
  - post
  - s3AttachmentURLs
  - metadata: { createdAt }

- Follows:
  - A single entry in the Follows table will contain the below fields
    - userID (PK)
    - userIDFollowing (SK)

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Create posts

Request:
```bash
POST /posts
{
  post
}
```

### Follow / unfollow other users

- Note that the follow / unfollow action will be idempotent in that instead of a new resource being created each time, multiple requests will only create one follow / unfollow relationship. Multiple requests won't produce unwanted behavior.

Request:
```bash
POST /users/:userID?op={ FOLLOW / UNFOLLOW }
```

### Retrieve feed

- Note that the createdAt parameter in the request will be used to perform cursor based pagination, where the nextCursor in the query paraneters points at the current paginated result's oldest createdAt value that will be used to find the next paginated posts which are older than the createdAt provided in the query parameters

Request:
```bash
GET /feed?nextCursor={ current oldest post's createdAt in viewport }&limit
```

Response:
```bash
{
  posts: [ { postID, userID, userName, post, createdAt } ],
  nextCursor, limit
}
```

### Add attachment to post

- When uploading binary data, multipart/form-data / multipart/mixed or another MIME	type such as image/png is usually used

- The content type is set to multipart/mixed which means that the request contains	different inputs and each input can have a different encoding type (JSON or binary).	The metadata sent will be in JSON, while the file itself will be in binary. 

- The placeholder {---xxBOUNDARYxx—} will contain a text string for the boundary	that differentiates one part of the body from another. For example				“__the_boundary__” could be used as the string. Boundaries must also start with		double hyphens and end with double hyphens too.

- Note that since this design is using a pre-signed URL to upload files, the client will	first request for a pre-signed URL from the servers, then make a HTTP PUT request	with the file data in the request body to the pre-signed URL 

#### Request for a pre-signed URL

Request:
```bash
POST /posts/pre-signed-url
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

## HLD

### Microservice architecture

- A microservice architecture is suitable for this system, as the system requires independent services such as post creation, news feed retrieval, user relationships management, etc. These are all independent operations which could potentially be managed by separate services.

- Microservices can benefit from a gRPC communication as there will be multiple channels of requests	being sent / received in inter-service communication between microservices. Thus, gRPC could be the	communication style between microservices, as it supports a higher throughput, and is able to handle	multiple channels of requests as opposed to REST, which uses HTTP, that is not optimized for		multi-channel communication between services.

### API gateway

- The API gateway will provide rate limiting, authentication, and route requests to the specific services.	For example, for a post creation request, the API gateway could route the request to the Post service.

### Posts service

- The Posts service will handle post creation requests, and store the post in the Posts database. Also, this service could potentially provide pre-signed URLs to the clients for them to upload attachments for posts. Overall, this service will be stateless and can be easily scaled horizontally.

### Posts table / cache

- The Posts table will store all the created posts from all users. We can use either a SQL or NoSQL database such as DynamoDB here. The data doesn't necessarily contain that many relationships, such that a SQL database would be the most optimal here, thus we'll use DynamoDB because it's more optimal when performing low latency queries using GSIs, which will support faster reads. However, SQL can also be used here.
- For faster lookups to get posts from a specific userID, we'll set the userID as a partition key in the Posts table, and set the createdAt field as the sort key to return the posts in chronological order.

#### Posts cache

- In the Posts cache, we can store frequently accessed posts with an appropriate TTL, so that the Posts and Feed services could retrieve the cached posts.
- We can use Redis for both the Posts and Feed cache, since we can benefit from Redis's support for complex data structures such as lists / sorted sets, which will further help in storing the feed and posts in a sorted fashion using the createdAt field. If we use a Redis sorted set, when we add or retrieve a post, the posts within the sorted set for a specific userID will always remain sorted by the createdAt field.
- Redis also provides Redis cluster which will help to scale the Posts and Feed cache, as opposed to Memcached which doesn't provide direct built-in replication support. To scale for viral or hot key posts, the Posts cache can replicate it's instances to solve hot key issues for viral postIDs as discussed in the DD.

### Follows table

- The follows entity contains many-to-many relationships between users. Usually relationships like this can be modeled in a Graph DB such as Gremlin, Neptune, Neo4j, etc. However, a simple KV store such as DynamoDB also works, and can model the relationships.
- Graph databases may be more useful when there is a need to do traversals or analysis on the relationships, where there are DFS / BFS algorithms which perform traversals through the graph's nodes, like finding the friends of friends, or recommending users to follow specific users in their network, etc. Graph databases are also usually harder to scale and partition than traditional NoSQL databases, and requires more domain level knowledge.
- Our use case follows a simple requirement, which involves creating feeds based on who the user is following. Thus, we'll use DynamoDB, where the userID and userIDFollowing fields is the full primary key (composite key) of the Follows table. This will quickly allow us to check if a user is following another user. We can also set the userID as the partition key to ensure lookups are fast for a single userID. Also, the userIDFollowing can be a secondary index to allow us to look up who the userID is following quickly.

### Feed service

- The feed service should allow the client to retrieve their feed, thats developed by compiling the posts of the users the client is following. We can compile the user's feed and store it in the Feed cache. This way, the feed isn't generated on each response, but generated in the background and stored in the Feed cache beforehand. Clients will then request the Feed service to return their feed that's stored in the Feed cache

- To return the paginated posts to the user (via cursor based pagination), and return posts in their feed as they're scrolling, we can use the oldest createdAt field in their viewport. This can be done because users are viewing posts from the earliest to the oldest in their viewport, and these posts will also be returned by using the createdAt as the sort key in the Posts table.
- Everytime the user scrolls down, we'll return a new paginated result of the posts with the cursor pointing at the current viewport's oldest createdAt value.
- We'll also store the previously viewed posts in the client's browser within a cache of a small TTL value. This way, when the user scrolls up, they'll still be able to see the previously returned posts.

- However, if the feed isn't created ahead of time, the Feed service will build it (using the Posts and Follows tables) and place it temporarily in the Feed cache, then return the paginated posts of the feed to the user. The feed can be periodically built for the user, let's say every 15 mins or so, and then updated in the Feed cache

#### Naive feed generation

- A naive way to view the feed of posts for a specific userID is as follows:
1. We get all the users who the userID is following
2. We get all of the posts from those users
3. We sort the posts by createdAt OR rank them, and return paginated results to the userID
- The steps above for this naive solution has a lot of issues which will be discussed in the DD, such as:
  - The userID may be following lots of users
  - The userID may have a lot of followers
  - A userID may have millions of posts
  - The number of posts in the Feed cache may be large because of the above issues (we'll likely need a Feed table instead of a Feed cache)

- A naive feed generation query in SQL would look as follows. The result from this query could then be stored in the Feed cache:
```sql
select postID, post, createdAt from postsTable
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
userID: { posts: [ { postID, userID, post, createdAt } ], TTL }
```

- We can use Redis for both the Posts and Feed cache, since we can benefit from Redis's support for complex data structures such as lists / sorted sets, which will further help in storing the feed and posts in a sorted fashion using the createdAt field

### Blob store

- The blob store will contain the attachments uploaded by users. The Post service will provide pre-signed URLs to this blob store (S3), such that the user can upload the attachments.

### Notification service

- The notification service will send optional push notifications when new posts are available. The Post service can asynchronously request the notification service to send a push notification to the userID's followers (if the userID doesn't have numerous amounts of followers) that the userID created a post

<img width="900" alt="image" src="https://github.com/user-attachments/assets/bd2628d4-9b38-46aa-9798-dda4913382b5" />

## DD

### Handling users who are following a large number of users (fan-out issue)

- If a user is following a large number of users, the queries to the Follows table will take a long time to run. Also, we'll make a large number of queries to the Posts table to get the posts of the large number of users. This problem is known as "fan-out" - where a single request fans out to multiple requests
- We can usually solve the fan-out issue by building the user's feed during posts creation by those large number of users, instead of building the feed when the user requests for it.
- Sometimes, apps like FB also limits the number of friends to 5K. This can also help to prevent the fan-out issue
- Additionally, we can solve the issue using the below approaches, and in 'Handling users who are following a large number of users':
  - Horizontal scaling via sharding
  - Adding a feed table:
    - This approach is a push based model (fan-out on write), where upon the post creation, the creator performs the writes to the Feed table if the creator has a follower that is following a large number of users
    - The Feed table in this approach will only contain users following a large number of users. Thus, if a userID only has about 10 users they're following, then that userID will not have an entry in this Feed table. We'll also only store the postIDs, and maybe additional metadata in this table. An entry in the Feed table may look as follows:

```bash
userID (user that's following a large number of users): [ 200 or so postIDs + post metadata ] 
```

### Handling users with a large number of followers (fan-out issue)

- When a user has a large number of followers, we have a similar fan-out issue if a celebrity creates a post, then we would need to write the postID to millions of entries in the Feed table / cache. We can solve this issue using the below approaches, and in 'Handling users with a large number of followers':
  - Shotgun the requests
  - Async workers:
    - There could be load balancers between the Posts service to the queues, and also between the queues to the async workers. Using this approach, the load balancers will route the request to the appropriate queue or worker based on how many requests / messages they are handling. 
    - We could also use consistent hashing instead of load balancing the requests, however, load balancing will route requests based on the capabilities and state of the queues / workers, which consistent hashing won't do.
  - Async workers with hybrid feeds:
    - This approach combines the push based model (fan-out on write) discussed previously, with a pull based model (fan-out on read) - creating a hybrid model.
    - The pull based model occurs when a user with many followers creates a post. This post is not sent to the user's millions of followers, but instead the followers will pull and read this post from the Posts table. Therefore, we'll use a push model for users with multiple users they're following, and use a pull model for users with multiple followers.
    - The number of celebrities (users with multiple followers) won't likely be that high, thus we won't pre-compute and write any of their posts to the Feeds table, since we'll need to write this post to millions of userIDs in the Feeds table. Instead if a userID is following a celebrity, that userID will fetch the celebrity's posts from the Posts table.
    - The Feeds service will need to pull both the userID's feed from the Feeds table / cache, and posts from celebrities they're following from the Posts table. Thus, the Feeds service should have the functionality to verify if the userID is following any celebrities, or if the user themself is a celebrity, or if the user is following many users
    - Because in the pull based model, the userID pulls the posts from the Posts table, instead of a feed being pre-generated for them in a push based model, the pull based model works better for inactive users who rarely login. The pull based model works better for inactive users because it doesn't waste compute by pre-generating a feed in the Feed table / cache for them.
    - The downside of a pull based model is that it will be pulling from a table / cache and creating the feed in real-time, which may take some time, instead of having a feed already built with the push based model.
      - userID following many users -> Followees will pre-generate feed for the userID's entry in the Feed table
      - Celebrity -> Users will pull celebrity's postIDs from Posts table
      - Regular user -> Pre-generate the feed (push based model) if the user is active, otherwise use the pull based model

### Handling uneven reads of posts

- The feed in this system is mainly built using the Posts table, however certain postIDs within the Posts table may be read much more often (like postIDs from celebrities) than other postIDs. This will cause uneven reads of posts, which could also cause hot key problems. This issue can be solved by the below approaches, and in 'Handling uneven reads of posts':
  - Post cache with large keyspace
  - Redundant post cache

### Partitioning and sharding the Posts, Follows and Feed tables

#### Posts table

- For faster lookups to get posts from a specific userID, we'll set the userID as a partition key in the Posts table, and set the createdAt field as the sort key to return the posts in chronological order. The Posts table could also be sharded by userID as well - thus, we'll have shards split by the userID where a single shard will contain a range of userIDs (we'll assign a userID to a shard either with or without a hash function + mod), then partitions further split by the userIDs within the shard, then set the sort key to createdAt to return posts in chronological order.
- We won't shard or partition by the postID since this will mean that a single userID's posts will be spread across different shards / partitions, which means we'll have to query multiple shards / partitions - making it complex.
- We also won't shard or partition by the createdAt timestamp because it's 1) this would mean that the shard with the latest createdAt timestamp values would be requested the most and cause a hot spot, 2) new writes will always go to the shard with the latest createdAt 3) its a very granular value to shard with

#### Follows table

- We can set the userID as the partition key to ensure lookups are fast for a single userID in the Follows table. Also, the userIDFollowing can be a secondary index to allow us to look up who the userID is following quickly.
- Likewise with the Posts table, we can further shard the Follows table by the userID - thus we'll have shards split by the userID where a single shard will contain a range of userIDs (we'll assign a userID to a shard either with or without a hash function + mod), then partitions further split by the userIDs within the shard, then set the secondary index to userIDFollowing for faster lookups when looking up who the userID is following quickly.

#### Feed table

- Because we'll be using the userID as the primary key in the Feed table, we can partition / shard using the userID where a single shard will contain a range of userIDs (we'll assign a userID to a shard either with or without a hash function + mod), which would support faster lookups. This also makes the most sense, since the feeds from different users are independent to one another, and thus the feeds can be fetched in parallel for different userIDs.
- However, some userIDs could still have slighly larger feeds than other users, which might cause some uneven distribution in the Feed table. We can limit the feed size to 200 or so postIDs in this Feed table, so that the feed distribution is more even.

### Ranking posts

- Ranking could be done by a separate algorithm using the createdAt time, likes count, post from a celebrity, etc. When the Feed service is generating the feed, another service called the Ranking service could be used, which assigns a score to each post within a user's feed, and then returns the ranked posts for the feed.
