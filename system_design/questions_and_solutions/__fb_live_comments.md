# FB live comments

Facebook Live Comments is a feature that enables viewers to post comments on a live video feed. Viewers can see a continuous stream of comments in near-real-time.

## Requirements

### Questions

- Can users reply to comments?
  - For simplicity, let's ignore designing replies

- Can users react to comments?
  - For simplicity, let's ignore designing reactions

### Functional

- Users can post comments on a FB live video feed
- Users can see live comments being posted while they're watching the live video
- Users can also see comments posted before they join the live feed

### Non-functional

- Availability > consistency:
  - If we have a strongly consistent system, we may expect higher latencies, thus the system could prioritize availability + low latency over consistency 
- Low latency:
  - Users should see live comments with very low latency (10 - 200 ms)
- Throughput:
  - The system should handle high throughput for posting comments

## Data models / entities

- Users:
  - userID
  - userName
  - userEmail

- Comment:
  - commentID
  - userID
  - videoID
  - comment
  - postedAt

- Live video:
  - This entity is the live video that is being broascasted by a userID, and which comments will be posted to. This entity will still be relevant in our system, so we'll include it here.
  - videoID
  - userID

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Post comment

- This endpoint will be handled by the API servers, as it doesn't directly involve using SSE or reading comments
- The clients will post comments via POST, and other clients will receive the posted comment from the servers using SSE

Request:
```bash
POST /liveVideo/:videoID/comments
{
  comment
}
```

### SSE endpoints

- This endpoint will be handled by the live comments servers, as it involves using SSE and also reading past comments. The system's read traffic will be much higher than the write traffic, thus the live comments servers (read-servers) should be scaled independently from the API servers (write-servers)

#### Establish a SSE connection

- This endpoint will be used to establish the SSE connection. The header "Connection: keep-alive" will be used to establish a long-lived connection with the server (default value for keep-alive is 2 hrs, but it's more appropriate to have a much smaller value to reduce taking up unnecessary bandwidth)
- The text/event-stream indicates that the client expects a SSE based data stream

Request:
```bash
GET /liveVideos/:videoID/comments/events
Accept: text/event-stream
Connection: keep-alive
```

- The server will respond to the client with potentially a list of new comments which other users have posted / sent to the server

Response:
```bash
HTTP/1.1 200 OK
Content-Type: text/event-stream
Connection: keep-alive
{
  id: 101
  event: comments
  data: [ { commentID, userName, comment, postedAt } ]

  retry: 500
}
```

### Get past comments

Request:
```bash
GET /liveVideos/:videoID/comments?nextCursor={last commentID or last postAt value}&limit
```

Response:
```bash
{
  comments: [ { commentID, userName, comment, postedAt } ], nextCursor, limit
}
```

## HLD

### API servers

- The API servers will handle operations which doesn't directly support maintaining SSE connections. We'll split the API servers from the live comments servers, so that the stateless servers (API servers) can be independently scaled from the stateful servers (live comments servers). We'll independently scale them because the live comments servers' bandwidth requirements will likely be much higher as they will ensure frequent low latency responses via either websocket / SSE, thus the live comments servers will need to support more network requests / connections. Also the system's read traffic via the live comments servers will be much higher than the write traffic via the API servers.


### Live comments servers

- The live comments servers will handle requests such as establishing the SSE connection, and requesting past comments for the live video feed when the user first opens the live video page. It will provide endpoints for returning paginated comments to the user.

#### Comments pagination

- As users will need to see previously posted comments, before they joined the live video, they may scroll up to view comments within their viewport. We can use cursor based pagination and lazy loading to only return the comments for the user's viewport via the viewport's current starting commentID OR starting postedAt timestamp. Cursor based pagination will return N comments (using limit) after the starting commentID / postedAt parameter (using nextCursor).
- Pagination such as offset and cursor based pagination are used to return portions of a larger result via API endpoints as explained below and in 'Pagination approaches':
  - Offset pagination
  - Cursor pagination:
    - Cursor based pagination will require us to unique identify every entry via an ID. When the client requests for comments, the cursor will point to the starting ID, and return the number of comments corresponding to the limit.
    - The downside of cursor based pagination is that it still requires a database query to be made to fetch paginated results using the ID. This can sometimes take a long time since we'll have to query the DB directly. However, we can also use a live comments cache to cache frequently accessed past comments.

- We'll use cursor based pagination since we don't need to parse through the preceding rows like we do in offset based pagination. Cursor based pagination also works better with DynamoDB since we can directly use DynamoDB's LastEvaluatedKey feature when making a query via the SDK. LastEvaluatedKey can be set to a specific key (such as commentID), such that the current query should start from this key. This feature works very similarly to how cursor based pagination works

#### SSE connections

- We'll use SSEs, however either polling, SSEs, or websockets could be used to get the comments in real-time, as explained below and in 'Ensuring real-time view of comments':
  - Polling:
    - Clients can poll for new comments from the live comments servers every few seconds either using short or long polling. Clients can send a request to the servers for any new comments since the last received commentID or postedAt timestamp. The servers will respond if there were any new comments or not after the commentID / postedAt timestamp - and send those new comments. Polling can lead to bandwidth issues on the server side, as connections will need to be opened and closed frequently when there are no new comments - making unnecessary network requests. Polling will also not scale properly - as the number of users grow within a live video feed, numerous comments may be posted, and thus the polling frequency will need to increase for all of those users. We may need to poll the servers every few milliseconds or so, which is not feasible for multiple clients.
  - Websockets:
    - Since the read and write ratio is not balanced in this system, we won't use websockets. Websockets are optimal when users will both frequently read and write entries. However, in a system with live comments for a live video feed, many users may read comments, but not frequently post them.
  - SSE:
    - Since we're using SSEs, the API design for viewing and sending comments uses the EventSource API provided in JS. Clients will request the write servers, API servers, (using POST) to post a new comment, and save the comment in the DB asynchronously. At the same time, there will be clients connected to the live comments servers via a long-lived HTTP connection using the header "Connection: keep-alive" for about 30-60 seconds (these clients will be watching the live video feed). These clients will receive the live comments posted by other users using this long-lived HTTP connection.

- The live comments servers will send SSE responses to all other users (via a long-lived HTTP connection) to view the comments in real-time when a comment is posted by a single user. In this case, a single user will post a comment via POST to the API servers, and the live comments servers will send the same posted comment to all clients with open SSE connections.

### Live comments database / cache

#### Database

- The live comments database will store all the comments posted from the API servers
- We can use a fast NoSQL DB such as DynamoDB which is optimal for reading and writing as it provides an eventual consistency model. The design should also prioritize availability over consistency, as users should receive comments with low latency. Also, our data is relatively simple and does not require that many relationships - thus using SQL databases wouldn't be the most optimal for this design.

#### Cache

- To speed up returning paginated results of past comments, we can use a cache such as Memcached or Redis. As the past comments may require frequent reads, and we'll need to sort the past comments based on the postedAt time, we can use Redis sorted sets here.

<img width="650" alt="image" src="https://github.com/user-attachments/assets/5d339f3b-b2eb-4e76-8e05-f7d8cf0df092" />

### Client

- The client (frontend) will likely authenticate the user and allow them to posts comments on a live video feed via the live comments servers. The client will also establish a SSE connection with the live comments servers. Because SSE operates at the HTTP level, it will likely request a L7 load balancer to be routed to a live comments server, then the SSE connection will be established between the client and the live comments servers.

## DD

### Scaling the SSEs and servers to support millions of concurrent users

- Since we're using SSE, we'll need to maintain an open HTTP connection with each client. A modern cloud based server can handle 100k - 1M concurrent HTTP connections on a single port. However, usually hardware and OS limits like CPU, memory management, and file management becomes the bottleneck first.

**Contrary to a common misconception, the capacity isn’t limited to 65,535 connections. That number refers to the range of port numbers, not the number of connections a single server port can handle. Each TCP connection is identified by a unique combination of source IP, source port, destination IP, and destination port. With proper OS tuning and resource allocation, a single listening port can handle hundreds of thousands or even millions of concurrent SSE connections.
In practice, however, the server’s hardware and OS limits—rather than the theoretical port limit—determine the maximum number of simultaneous connections.**

- The live comments servers are stateful, and thus if we have multiple servers, then the info on which user is connected to which live comments server will need to be maintained so that live comments servers can communicate together when sending posted comments. If we have multiple live comments servers, where userA is connected to serverA, and userB is connected to serverB, then if serverA receives a posted comment from userA, serverA will need to send userA's comment to serverB so that userB could receive userA's posted comment. This problem can be solved using the following, and in 'Scaling multiple live comments servers':
<br/>

  - Horizontal scaling with load balancer and PubSub
  - PubSub partitioning into channels per live video:
    - Redis PubSub can be configured such that a single topic could have N channels. In this approach, Redis PubSub will be used between the API servers (stateful servers) and the live comments servers (stateful servers). Using Redis PubSub, there will be multiple channels for a single topic, and when a posted comment comes into an API server, that posted comment will be routed to a channel in the live video's topic ( using hash(videoID) % N_CHANNELS ). Thus, we'll have one topic per live video, and have N channels for a single topic (live video). Once the posted comment is routed to a channel in the live video's topic, there will be live comments servers subscribed to the live video's topic, since they are also serving client's SSE connections for the same live video. These subscribed live comments servers will receive the comments from the topic and deliver the comments to the connected clients via the SSE connections.
    - This approach may seem to scale live comments servers well, as we have multiple channels for a single topic - however there's still a chance a single live comments server will have clients for multiple different live videos, and thus there will be numerous live comments servers subscribed to a single topic. It will essentially be a many-to-many connection between all the live comments servers - the same as the first approach with horizontal scaling.
  - Partitioned PubSub with layer 7 load balancer:
    - Ultimately, we want to reduce the many-to-many connections between all the live comments servers as much as possible. This means that we want a single live comments server to subscribe to as few topics (live videos) in the PubSub servers as possible, so that it doesn't lead to a many-to-many connection issue.
    - The many-to-many connections can be reduced by using a Layer 7 load balancer OR a dynamic lookup via a configuration service (ZooKeeper), where a videoID will always be routed to the same API server (stateles servers) using the videoID parameter in the request (when posting a comment to the API server). When clients try to read comments for the same videoID, they can also be routed via a L7 load balancer using the videoID parameter (and IP address or location if necessary) to a  specific live comments server. This way when a comment is posted for a specific videoID, it will always be routed to the same API server, and that API server will send the posted comment to a channel within the live video's topic ( via hash(videoID) % N_CNANNELS ). The subscribed live comments servers will receive the posted comment, and send the comment to the connected clients (via SSE).
    - There will be fewer subscribed many-to-many connections because all the comments for the same videoID will be routed to the same API server, and likely to the same channel which a live comments server is subscribed to ( since we're using hash(videoID) % N_CHANNELS ). This means that a single live comments server doesn't have to subscribe to all the topics or channels, it will subscribe to only topics / channels (videoIDs) that it's connected users are expecting live comments from.
  - Scalable dispatcher instead of PubSub

Kafka vs Redis tradeoffs in PubSub:


Both the pub/sub approach (putting a single videoID in the same API server (and in fewer live comments servers)) and the dispatcher service approach are great solutions. The pub/sub is typically easier with fewer corner cases, so it may be more preferred in a SDI.
