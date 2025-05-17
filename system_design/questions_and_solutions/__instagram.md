# Instagram

Instagram is a social networking service that enables its users to upload and share their photos and videos with other users. Instagram users can choose to share information either publicly or privately. Anything shared publicly can be seen by any other user, whereas privately shared content can only be accessed by the user's followers.

## Requirements

### Questions

- Are we handling a uni-directional "follow" relationship, or a bi-directional "friend" relationship?
  - Let's assume we're handling the uni-directional "follow" relationship

- In this system, users can create posts (with photos / videos / captions), follow other users, view users' timelines (any user's profile with posts) or their own feed consisting of posts from other users they follow, search posts, like posts, and comment on posts. Are these all the features we're designing?
	- Yes

- Can users have a limited number of followers?
  - No, the follower count is unlimited

- Are we handling multiple photos / videos in a single post?
  - Yes

- Can we assume that the feed's posts are returned in chronological order by using the post's creation timestamp?
  - Yes

- What is the DAU, and how many posts will be created per day?
  - 500M DAU and 100M posts created per day

### Functional

- Users can create posts containing photos / videos / captions
- Users can follow other users
- Users can view a feed of posts from other users they follow, in some chronological order
- Users can page through their own feed

- Users can search posts
- Users can like posts
- Users can comment on posts

### Non-functional

- Availability > consistency:
  - Users' feeds don't necessarily need to update immediately when another user creates a post, we can tolerance up to 2 mins and follow an eventual consistency model
  - The system should prioritize availability of posts over consistency
- Low latency:
  - Viewing posts, results of the feed, and searching posts should be fast, between 10 - 500 ms
  - The system should also render photos and videos instantly, <200 ms (low latency media delivery)
- The system should be able to support large amounts of following / follower relationships between users
- The system should scale to support 500M DAU, and 100M posts created per day

## Data model / entities

- Users:
  - userID
  - userName
  - userEmail

- Posts:
  - Note that a single post entity will handle photos, videos and captions  
    - postID
    - userID
    - caption
    - s3URLs
    - likes
    - postMetadata: { createdAt, status }

- Media:
  - The media entity represents the actual bytes of the media file (photos / videos). We'll use S3 for storing the media files.

- Follows:
  - A single entry in the Follows table will contain the below fields
    - userID (PK)
    - userIDFollowing (SK)

- Comments:
  - commentID 
  - postID
  - userID
  - comment
  - metadata: { createdAt }

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Create posts

#### Request pre-signed URL for uploading post's photos / videos

- When a user requests to create a post, they will first request for the pre-signed URL for creating the post, and also send the post's caption for the servers to create a new entry in the Posts table

- When uploading binary data, multipart/form-data / multipart/mixed or another MIME	type such as image/png is usually used

- The content type is set to multipart/mixed which means that the request contains	different inputs and each input can have a different encoding type (JSON or binary).	The metadata sent will be in JSON, while the file itself will be in binary. 

- The placeholder {---xxBOUNDARYxx—} will contain a text string for the boundary	that differentiates one part of the body from another. For example				“__the_boundary__” could be used as the string. Boundaries must also start with		double hyphens and end with double hyphens too.

- Note that since this design is using a pre-signed URL to upload files, the client will	first request for a pre-signed URL from the servers, then make a HTTP PUT request	with the file data in the request body to the pre-signed URL 

Request:
```bash
POST /posts/pre-signed-url
{
	caption
}
```

Response:
```bash
{
	pre-signed URL
}
```

#### Upload post's photos and videos to pre-signed URL

Request:
```bash
PUT /<pre-signed URL>
Content-Type: multipart/form-data; boundary={---xxBOUNDARYxx—}
{
—xxBOUNDARYxx–
<HEADERS of the boundary go here>

We’ll put the a single photo's / video's binary data in every boundary like this:

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

### Follow / unfollow a user

- Note that the follow / unfollow action will be idempotent in that instead of a new resource being created each time, multiple requests will only create one follow / unfollow relationship. This way, multiple requests won't produce unwanted behavior.

- The follower's ID will be extracted from the authentication token (JWT or session), so we don't need to specify it in the request body. This is both more secure and follows the principle of least privilege. In practice, it's fine to include here, you'll just need to compare it to the session before following.

Request:
```bash
PATCH /follows?op={ FOLLOW / UNFOLLOW }
{
	userID (userID to follow / unfollow)
}
```

### View user timeline or feed (feed is in the home page of instagram)

- Viewing a user's timeline or feed is a 2 step process, where the client will first fetch the paginated post's metadata from the DB along with the post's pre-signed URLs. Then the client will retrieve the post's photos / videos from the blob store using the pre-signed URLs.

- When downloading binary content using HTTP, application/octet-stream can be used to receive binary data

- The application/octet-stream MIME type is used for unknown binary files. It preserves the file contents, but requires the receiver to determine file type, for example, from the filename extension. The Internet media type for an arbitrary byte stream is application/octet-stream.

- The "* / *" means that the client can accept any type of content in the response - which could also be used for sending / receiving binary data

- Note that to download files, we could use either a pre-signed URL or a URL the client can request to download from the CDN (let’s call it CDN URL). The process is similar to uploading files, where the client first requests the servers for a pre-signed URL OR CDN URL, then the client will download the file from the pre-signed URL / CDN URL.

#### Request paginated posts' metadata and pre-signed URLs

Request:
```bash
GET /timeline?nextCursor={ current oldest posts's createdAt in viewport }&limit (Used to view user timeline)
GET /feed?nextCursor={ current oldest post's createdAt in viewport }&limit (Used to view feed)
```

Response:
```bash
{
  posts: [ { postID, userID (if returning a feed instead of a timeline), userName, caption, preSignedURLs / CDN URLs, createdAt } ],
  nextCursor, limit
}
```

#### Fetch posts' photos / videos using pre-signed URLs or CDN URLs

Request:
```bash
GET /<pre-signed URL or CDN URL>
Accept: application/octet-stream
```

- The response body contains the file chunks. The chunks can also be returned using multiplexing via HTTP/2.0. Multiplexing will allow the client to send requests for the chunks of a file, then the server will send the responses containing the file chunks in any order. The returned chunks can be used to reconstruct the file on the client side.

Response:
```bash
Content-Type: application/octet-stream
Content-Disposition: attachment; filename=”<FILE_NAME>”
{
	file’s binary data used to generate the file on the client side
}
```

### Liking / disliking a post
  
- Note that we’re using PATCH here as it's mainly used to only update a small	portion of an entry, while PUT is used to update the full entry

Request:
```bash
PATCH /posts/:postID?op={ LIKE / DISLIKE }
```

### Searching posts

- Note that we’ll use cursor based pagination to search for posts as the number of	posts returned may be very large, and as such we’ll return paginated results which	will use lazy loading and fetch the results only for the current viewport
- Searching for posts will likely be handled by a search service, which will use the inverted index mappings to return search results
- Likewise for retrieving a timeline and feed, when searching posts, the clients will request for pre-signed URLs or CDN URLs, then use those urls to fetch the post's photos / videos from the blob store

#### Request paginated posts' seaarch results and pre-signed URLs

Request:
```bash
GET /posts?query&sort={ LIKES / DATE }&nextCursor={ last postID on viewport if using LIKES as sort order OR oldest createdAt value on viewport if using DATE as sort order }&limit
```

Response:
```bash
{
  posts: [ { postID, userID, userName, caption, likes, preSignedURLs, createdAt } ],
  nextCursor, limit
}
```

#### Fetch posts' photos / videos using pre-signed URLs or CDN URLs

Request:
```bash
GET /<pre-signed URL or CDN URL>
Accept: application/octet-stream
```

- The response body contains the file chunks. The chunks can also be returned using multiplexing via HTTP/2.0. Multiplexing will allow the client to send requests for the chunks of a file, then the server will send the responses containing the file chunks in any order. The returned chunks can be used to reconstruct the file on the client side.

Response:
```bash
Content-Type: application/octet-stream
Content-Disposition: attachment; filename=”<FILE_NAME>”
{
	file’s binary data used to generate the file on the client side
}
```

### Commenting on a post

Request:
```bash
POST /posts/:postID/op={ COMMENT }
{
	comment
}
```

## HLD

### Microservice architecture

- A microservice architecture is suitable for this system, as the system requires independent services such as post creation, feed retrieval, user relationships management, etc. These are all independent operations which could potentially be managed by separate services.

- Microservices can benefit from a gRPC communication as there will be multiple channels of requests	being sent / received in inter-service communication between microservices. Thus, gRPC could be the	communication style between microservices, as it supports a higher throughput, and is able to handle multiple channels of requests as opposed to REST, which uses HTTP, that is not optimized for		multi-channel communication between services.

### Client

- The client will be both uploading and downloading files, thus there will be separate sections in	the client code for an “uploader” and “downloader”:

- Both the "uploader" and "downloader" parts of the client will use a chunker functionality that splits the files when uploading to the blob store, and also reconstructs the files from the downloaded chunks

### API gateway

- The API gateway will provide rate limiting, authentication, and route requests to the specific services.	For example, for a post creation request, the API gateway could route the request to the Posts service.

### Posts service

- The Posts service will handle post creation requests, liking / disliking / commenting on posts, etc, and store the post in the Posts table. Also, this service could potentially provide pre-signed URLs to the clients for them to upload photos / videos for posts. The post metadata and captions themselves can be stored in the Posts table, while the actual bytes of the media can be stored in S3. Overall, this service will be stateless and can be easily scaled horizontally.
- We'll also make the initial assumption that our media is small enough to be uploaded directly via a single request.
- Because post creation may likely need to be fed into different components like the Posts table, Feeds cache, etc to perform a push based model (fan-out on write), we'll need additional queues and workers between the Posts service to the relevant consumers as discussed in the DD. Also, as users may be frequently liking / commenting on posts, we can use similar queues and workers between the Posts service and relevant consumers as discussed in the DD.

### Posts table / cache

- The Posts table will store all the created posts' metadata and caption from all users. We can use either a SQL or NoSQL database such as DynamoDB here. The data doesn't necessarily contain that many relationships, such that a SQL database would be the most optimal here, thus we'll use DynamoDB because it's more optimal for performing low latency queries using GSIs / LSIs, which will support faster reads for querying the posts / feed. Also, we may not require features of SQL, such as multi-table transactions and different isolation levels because we won't see many concurrent operations for posts. However, SQL can also be used here.
- For faster lookups to get posts from a specific userID, we'll set the userID as a partition key in the Posts table, and set the createdAt field as the sort key to return the posts in chronological order.

Fun fact: Instagram uses PostgreSQL as its main Post metadata database. This is interesting because if you were following the SQL vs NoSQL debates of yesteryear you may be convinced that a SQL DB could not scale to support our 500M DAU. Clearly not the case!

#### Posts cache

- In the Posts cache, we can store frequently accessed posts with an appropriate TTL, so that the Posts, Feed and Timeline services could retrieve the cached posts.
- We can use Redis for both the Posts and Feed cache, since we can benefit from Redis's support for complex data structures such as lists / sorted sets, which will further help in storing the feed and posts in a sorted fashion using the createdAt field. If we use a Redis sorted set, when we add or retrieve a post, the posts within the sorted set for a specific userID will always remain sorted by the createdAt field.
- Redis also provides Redis cluster which will help to scale the Posts and Feed cache, as opposed to Memcached which doesn't provide direct built-in replication support. To scale for viral or hot key posts, the Posts cache can replicate it's instances to solve hot key issues for viral postIDs as discussed in the DD.

### Follows table

- The follows entity contains many-to-many relationships between users. Usually relationships like this can be modeled in a Graph DB such as Gremlin, Neptune, Neo4j, etc. However, a simple KV store such as DynamoDB also works, and can model the relationships.
- Graph databases may be more useful when there is a need to do traversals or analysis on the relationships, where there are DFS / BFS algorithms which perform traversals through the graph's nodes, like finding the friends of friends, or recommending users to follow specific users in their network, etc. Graph databases are also usually harder to scale and partition than traditional NoSQL databases, and requires more domain level knowledge.
- Our use case follows a simple requirement, which involves creating feeds based on who the user is following. Thus, we'll use DynamoDB, where the userID and userIDFollowing fields is the full primary key (composite key) of the Follows table. This will quickly allow us to check if a user is following another user. We can also set the userID as the partition key, and the userIDFollowing as the sort key to ensure lookups are fast for a single userID, and making sure the users a single userID is following is sorted in the partition.

### Follow service

- We'll add a dedicated Follow service to handle follow / unfollow operations separately from the Posts service. Since following users happens less frequently than posting and viewing content, this separation lets us optimize and scale each service based on its specific needs.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/ad69d333-96eb-456c-a45e-a0f89d0f6008" />

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
select postID, caption, s3URLs, createdAt from postsTable
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
userID: { posts: [ { postID, userID, caption, s3URLs, likes, createdAt } ], TTL }
```

- We can use Redis for both the Posts and Feed cache, since we can benefit from Redis's support for complex data structures such as lists / sorted sets, which will further help in storing the feed and posts in a sorted fashion using the createdAt field. We can store each user's feed as a sorted set (ZSET in Redis). The members in the sorted set will be the postIDs, and the scores will be the createdAt timestamp of the postID.

### Timeline service

- The timeline service will handle requests for viewing the user's timeline. To generate the user's timeline, we'll fetch the user's posts from the Posts table, and apply pagination to the results

### Search service

- The search service will search for posts via inverted index mappings built using the the Posts table, most likely using both a creation and likes inverted index using a Redis list and sorted set respectively. The design for the search service is similar to the SDI 'FB post search and Twitter search'. The DD will also go over scalability of the writes on posts / comments, likes, and searching posts.

### Blob store

- The blob store will contain the photos / videos uploaded by users. The Posts service will provide pre-signed URLs to this blob store (S3), such that the user can upload the attachments.

- The blob store will store the file chunks. The file itself can be uploaded in the below ways and in	‘Uploading file to storage solutions’:
  - Upload file to a single server
  - Store file in blob storage:
    - A lot of the times, having the client upload the file to the API servers, then having the			API servers upload to the blob store is redundant and slow especially for large files because the uploading process has to be done twice. Clients could directly upload to			the blob store via a pre-signed URL, and any security or validation checks can be				performed via the blob store client interfacing the blob store after the user has			 	uploaded to the pre-signed URL.

    - However, in some applications, such as YouTube, where the videos will need				additional transformation, having intermediary API servers may be suitable.

  - Upload file directly to blob storage:
    - We can use pre-signed URLs to upload files directly to the blob store. Pre-signed			URLs can be sent via the servers to the clients. Clients can then use the pre-signed			URL, which may have a TTL to upload / download their files. Pre-signed URLs are			explained in ‘Pre-signed URLs’.

### CDN

- CDNs will support in downloading files, as explained below and in ‘Downloading file solutions’:
  - Download through file server:
    - In this approach the file is downloaded twice, once from the blob store to the servers,			then another time from the servers to the client. This will be both slow and expensive

  - Download from blob storage:
    - This approach will work for small to moderate scale apps, however, for large scale			apps such as Dropbox, Instagram, etc, the files may need to be downloaded from CDN POPs spread			across globally

  - Download from CDN:
    - In this approach, servers can send a CDN URL to the client, similar to a pre-signed			URL of a blob store. The client will request the CDN URL, and download the file. This			CDN URL will give the user the permission to download the file from a specific CDN			POP for a limited time.

    - CDNs are usually expensive, thus the files can be strategically cached using a TTL			and invalidation techniques to remove less frequently accessed files

<img width="1500" alt="image" src="https://github.com/user-attachments/assets/1e0a37bb-a0c9-4fdb-9558-a649e6fad253" />

## DD

### The system should delivery feed content with low latency (< 500 ms)

When it comes to feed content delivery, simply using a SQL query to retrieve the posts of all followees of a user, then returning a sorted subset of those retrieved posts will be very slow. If a user follows thousands of other users, then we need thousands of queries to the Follows and Posts table. DynamoDB does offer batch operations, but each batch is limited to 100 items and 16 MB of data. For a user following 1000 users, we need at least 10 separate batch operations to query the recent posts for generating the feed. While these can operate in parallel, it still creates several major problems:

1. Read amplification: Every time a user refreshes their feed, we generate a large number of database reads. With 500M DAU refreshing their feeds multiple times per day, this quickly becomes unsustainable. This is going to get expensive fast.

2. Repeated work: If two users follow many of the same users (which is common), we're repeatedly querying for the same posts. At Instagram's scale, popular posts might be retrieved millions of times per day.

3. Unpredictable performance: The latency of a feed request would vary dramatically based on how many users a user follows and how active those followees are. This makes consistent performance nearly impossible.

Let's put this in perspective with some numbers:
- Each feed refresh might need to process 10,000 posts (1,000 followed users × 10 posts/day)
- With 500M DAU, if each user refreshes their feed 5 times daily, that's 2.5 billion feed generations per day
- During peak usage (e.g., evenings, major events), we might see 150,000+ feed requests per second

With these numbers, it's evident that even with a well-architected DynamoDB implementation, we'd struggle to maintain our 500ms latency target. We'd either:

1. Need to massively overprovision our database capacity, making the system prohibitively expensive, or

2. Accept higher latencies during peak usage, violating our requirements

This inefficiency is inherent to the fan-out on read model. The core issue is that we're postponing the computational work until read time, which is precisely when users expect immediate results. We could use the following solutions (and in 'Reducing feed content delivery time'):
  - Simple caching (improvement on fan-out on read)
  - Precompute feeds (fan-out on write):
    - Note that originally, our Follow table has the partition key as the userID, and the sort key as the userIDFollowing. In this approach, after a user creates a new post, we'll query the Follow table to get all the users who follow the posting user (this is essentially a fan-out on write approach). We'll then pregenerate the feed for the followers as this new post is created by the posting user. Thus, we'll need to add a GSI to the Follow table, where the partition key is the userIDFollowing, and the sort key is the userID. This way, we can quickly find all the followers of a userIDFollowing who just created a new post. For each follower, we prepend the new postId to their precomputed feed. This precomputed feed can be stored in a dedicated Feeds table (in DynamoDB, for example) or in a cache like Redis.
    - If we use a Redis sorted set to store the pregenerated feed, then the sorted set's data model will look like:
      - Key: feed:{userID}
      - Members: postID
      - Scores: postID's createdAt timestamp
    - When a user requests their feed, we need to read the top N posts from their sorted set in Redis, which is a single fast operation. However, we still need to hydrate the posts based on these postIDs (members in the sorted set). To do this we have 3 options:
      - For each postId in the cache, go fetch the metadata from the Posts table in DynamoDB. This is simple but requires an additional database query for every feed request.
      - Rather than caching the postId, we could cache the entire post metadata in Redis. This way we don't have to make a second query to the Posts table to get the post metadata. This is faster but uses more memory and introduces data consistency challenges.
      - Use a hybrid approach with two Redis data structures: one for the feed's postIds (ZSET) and another for a short-lived post metadata cache (HASH). When we need to hydrate posts for the postIDs retrieved from the sorted set:
        - First, try to get all post metadata from the Redis post cache
        - For any cache misses, batch fetch from DynamoDB using BatchGetItem
        - Update the Redis post cache with the fetched metadata
        - Return the combined results
    - To recap, here is what happens when a new post is created:
      1. We store the post metadata in the Posts table and the media in the blob store like before
      2. We put the postID onto a queue to be asynchronously processed by the Feed workers, where the Feed workers will store the post metadata into the Feed table / cache.
      3. The Feed service will query the Follow table to get all users who follow the posting user
      4. For each follower, the Feed service will prepend the new postID to their pregenerated sorted set that acts as the follower's feed
      5. The Feed service will store the new feed (sorted set) in Redis
    - Then, when a user requests their feed:
      1. The Feed service will read the top N postIDs (members) from their sorted set in the Feed cache
      2. The Feed service will hydrate the posts based on the top N postIDs. We'll first check if the top N postIDs' metadata is in the Post cache. If it is, we'll use that. If it's not, then we'll batch fetch from the Posts table using DynamoDB's BatchGetItem() function.
      3. We'll combine the results from the followers's sorted set, Posts cache and table, then return them to the user.
  - Hybrid approach (precompute + real-time):
    - Because pregenerating the follower's feed for a celebrity will take a lot of time and resources, we'll combine the above fanout-on-write approach with a fanout-on-read approach (for celebrities).
    - Here's how it works: We define a threshold for the number of followers. Let's say, 100,000 followers. For users with fewer than 100,000 followers, we precompute their followers' feeds just like in the "good" approach above. For users with more than 100,000 followers (the "celebrities"), we DON'T precompute their posts into their followers' feeds.
    - Instead:
      - When a "celebrity" posts, we add the post to the Posts table and do not trigger an asynchronous feed update for their followers.
      - When a user requests their feed: We fetch the precomputed portion of their feed from Redis (posts from users with < 100,000 followers). Then, we also query the Posts table for recent posts from the "celebrities" they follow. We then merge the precomputed feed with the recent posts from celebrities, chronologically and return the merged feed.
    - Thus, we end up with an effective mix between pre-computation and real-time merging:
      1. Fanout-on-write for the majority of users (follower count < 100,000)
      2. Fanout-on-read for the few "celebrity" users (follower count > 100,000)
    - Instagram actually uses a similar approach like this hybrid one in production. 

### Handling users who are following a large number of users (fan-out issue)

- If a user is following a large number of users, the queries to the Follows table will take a long time to run. Also, we'll make a large number of queries to the Posts table to get the posts of the large number of users. This problem is known as "fan-out" - where a single request fans out to multiple requests
- We can usually solve the fan-out issue by building the user's feed during post creation by those large number of users, instead of building the feed when the user requests for it.
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

### The system should render photos and videos instantly, supporting photos up to 8 MB and videos up to 4 GB

There are two key challenges to large media files:

1. Upload efficiency
2. Download / viewing latency

As we discussed in both the DropBox and YouTube SDIs, uploading large media files requires chunking. This is because a single HTTP request is usually constrained to a max payload size < 2GB. Thus, in order to upload a 4GB video, we would need to send at least 2 (in practice, more given metadata) requests.

A common solution is to use S3's multipart upload API. At a high level, here is how it works:

1. First, we will call POST /posts to create the post metadata and get a postID, as well as get back a pre-signed URL that can be used to upload the media. This URL is valid for a limited time (e.g., 1 hour) and allows the user to upload directly to S3 without having to go through our servers.
2. At the client-side, we use the multipart upload API to upload the file in chunks to the pre-signed URL.
3. S3 will automatically handle reassembling the chunks and store the final file in S3

When we initially uploaded the post metadata, we would include a media upload status field originally set to PENDING. Once the media is uploaded, we could also optionally update the post metadata with the S3 objectKey and update the media upload status to UPLOADED. There are two main ways to handle the post metadata update after upload completion:

1. Client-driven approach: The client sends a PATCH request to update the post metadata with the S3 objectKey and sets the media upload status to UPLOADED once the multipart upload finished. This client-driven approach is simpler to implement but is less reliable since we have to trust clients to properly report the upload completion.

2. Server-driven approach: We configure S3 event notifications to trigger a Lambda function or background job when the multipart upload completes. This job then updates the post metadata automatically. This server-driven approach is more complex to implement but provides better data consistency guarantees since our backend maintains full control over the metadata updates. Most production systems opt for this option despite the added complexity.

Now that we have all our media uploaded and in S3, let's talk about how we get it to render quickly when a user views it (as discussed in 'Rendering media quickly to users'):
- Direct S3 serving
- Global CDN distribution
- CDN with dynamic media optimization

### Handling uneven reads of posts

- The feed in this system is mainly built using the Posts table, however certain postIDs within the Posts table may be read much more often (like postIDs from celebrities) than other postIDs. This will cause uneven reads of posts, which could also cause hot key problems. This issue can be solved by the below approaches, and in 'Handling uneven reads of posts':
  - Post cache with large keyspace
  - Redundant post cache

### Handling large volume of writes

We have two types of writes - post / comment creations, and like events which we'll need to handle:

#### Post / comment creations

**Edge cases for celebrities and for users following many users is handled by the hybrid push and pull based model. However, scalability of these writes still needs to be addressed when it comes to updating the search service when new posts are created.**

- When a post is created, we'll need to tokenize the post and then write to likely both a creation and likes indexes within the search service so that it can update both the post creation and likes index. If a post has 100 words, we might trigger 100+ writes one for each word (if we use bigrams of shingles, we'll have a lot more writes). With a large number of posts being created concurrently, the search service may become a SPOF.
- To prevent the search service from becomming a SPOF, we can easily horizontally scale the servers as this is a stateless service.

Kafka queues between posts / likes service and search service servers:

- Also, to prevent post creation data from being lost as it is waiting to be indexed via the search service, a Kafka queue can be positioned between the Posts service and the search service's servers. Also Kafka can be configured such that it buffers messages so that the data is not lost within the queue. Buffering in Kafka will also handle bursts of messages being sent since the message data can be stored temporarily to prevent message loss during bursts.
- The Kafka messages could also be deleted periodically via a TTL of a few mins. The number of Kafka queues can be configured according to the number of search service servers (or rather the search service's indexing servers - which will perform the actual indexing), where if the number of workers in an search service server grows, the number of queues will also grow.

Sharding the inverted index mappings:

- Lastly, we can shard the creation and likes indexes on the term, so that queries for a single term will only need to search through a single shard, and the search for multiple terms can be done in parallel by querying all the term's corresponding shards.

#### Likes

- Likes occur much more frequently than post creations (10x more frequently). We can reduce the number of writes we need to do for "like events" by doing the below, and in 'Reducing writes for like events':
  - Batch likes before writing to the database
  - Two stage architecture

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

### Handling large volumes of read requests

- To handle large volumes of read requests, caching the results to handle large volume of read results may be the best solutions as explained below and in 'Handling large volume of search / read requests':
  - Use a distributed cache alongside our search / post service
  - Use a CDN to cache at the edge
 
### Supporting large files

- To support large file uploads, we can chunk the files on the client side, as well as apply compression algorithms before uploading them to the blob store. Additionally, when we download the uploaded files from the blob store, the client can request for chunks of the photos / videos via the pre-signed URLs / CDN URLs.
- The 'Dropbox' SDI goes in depth on supporting large files using chunking, fingerprints, compression, etc.

### The system should be scalable to support 500M DAU

We'll summarize the design choices we've made to enable us to serve 500M DAU while maintaining performance and reliability:

1. Precomputed Feeds (Hybrid Approach): The cornerstone of our scalable feed generation is the hybrid approach. By precomputing feeds for the vast majority of users (those following accounts with fewer than our defined threshold of followers), we drastically reduce read-time load. The real-time merging for "celebrity" posts is a carefully considered trade-off to manage write amplification.
   
2. Content Delivery Network (CDN): Using a CDN like CloudFront for media delivery is essential for global scalability and low-latency access. Dynamic media optimization further improves performance for diverse devices and network conditions.

3. Chunked Uploads: For large files (especially videos), chunking uploads improves reliability and user experience, and allows for parallel uploads.

4. Database Choice and Indexing: Our choice of DynamoDB (or a similarly scalable NoSQL database) provides horizontal scalability for metadata storage. The careful use of partition keys and sort keys ensured efficient queries.

Let's do some math and determine whether our existing scaling strategies are sufficient. For the media files themselves, we can assume an average media size of ~2MB, so 100M * 2MB = 200TB of binary data for posts is created each day.

Starting with the media, this is about 750 PB of data over 10 years. S3 can handle this, but it's not cheap. If we worry about cost, we can always move the media that has not been accessed in a long time to cheaper storage tier in S3.

For the posts metadata, we're looking at 100M * 1KB = 100GB of new (non-binary) data created each day. Similarly, if we grow concerned about the price of DynamoDB, we can move infrequently accessed data over to S3.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/d1863958-3baa-4cad-9a26-152a6d5d8279" />

When it comes to throughput, as always, we can dynamically horizontally scale our microservices to handle the load. This happens automatically with most cloud providers and is triggered based on either CPU or memory usage thresholds. Each set of horizontally scaled microservices thus implicitly has a load balancer in front of it to distribute the traffic.

<br/>
<br/>

Additional deep dives:

### Ranking posts

- Ranking could be done by a separate algorithm using the createdAt time, likes count, post from a celebrity, etc. When the Feed service is generating the feed, another service called the Ranking service could be used, which assigns a score to each post within a user's feed, and then returns the ranked posts for the feed.

### Handling multi-keyword search queries

- To support searches for multi-keyword queries like "This is a multi-keyword query", we can do the following and in 'Handling multi-keyword queries':
  - Intersection and filter:
    - Intersecting the results from a multi-keyword search will be very compute intensive since some results may contain millions of entries. Also, implementing the intersection between the search results would mean that we may need to maintain a hash map of the postIDs - which will further increase both storage and latency as we'll need to perform a complex operation everytime a user searches.
  - Bigrams of shingles

### Fault tolerance of inverted index mappings

- To ensure fault tolerance of the inverted index mappings, we can replicate the inverted index mappings. Redis Cluster provides built-in asynchronous primary-secondary replication by default, which should be suitable here since write inconsistencies via a leaderless approach could have issues in the inverted index mappings (which requires low latency reads).

#### Keeping a reference to the indexServerID in the Posts table to recover when inverted index mappings are down / erased

- If both the primary and secondary nodes for an inverted index mapping shard are down, then it would be really difficult to rebuild the shard's inverted index mappings again without knowing which terms were stored in this crashed shard.
- We can store a reference to the indexServerID for a postID in the Posts table. This will allow us to query the Posts table, and look for posts with the indexServerID that crashed. Afterwards, we can rebuild the index for those posts with the crashed indexServerID.
- However, maintaining this indexServerID field may have some overhead if we need to update the indexServerID during scaling events, but it ensures fast recovery time if the inverted index mappings are down / erased. Thus, this overall mapping between the indexServerID: [ postIDs ] could instead be maintained in a service like ZooKeeper, which provides a KV store for maintaining server-size mappings like these.

### Reduce storage space of inverted index mappings

- Users are usually only interested on a small portion of posts, thus we can do the following optimizations:
  - Put limits on how many postIDs a single term in the inverted index will contain. We probably don't need all postIDs with "dog" in the post content - only about 1k - 10k postIDs for "dog" should be fine.
  - Ignore stopwords like "a", "of", etc (when updating the inverted index) which provide no value in searching.
  - In-frequently accessed terms and their creation / likes index mappings could instead be moved to a cold storage such as in S3 Standard-IA. If there are queries for these in-frequent terms, the query could first check the Redis inverted index mappings, and if results are not in Redis, it could instead be queried from S3 via Athena and returned to the client with a small increase in latency.




