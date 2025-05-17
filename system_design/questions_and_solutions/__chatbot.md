# Chatbot system

## Requirements

### Questions

- The system should allow users to send messages to the chatbot, get responses back, rate responses, and view their past messages. Are we designing all of this?
  - Yes
 
- Should we treat the actual LLM / ML model behind the chatbot as a black box, and treat it like a separate service?
  - Yes, let's not focus on the actual specifics of the LLM / ML model
 
- Can we send attachments to the chatbot?
  - Yes
 
- What is the latency requirement for users getting responses back from the chatbot - will the LLM / ML model response generation take a while? Do we also want to send back periodic response updates every few seconds, so that the user knows the chatbot is working on the request?
  - Let's say the response generation takes anywhere from 1 sec to a few mins depending on the request itself
  - We could also send back periodic response updates every few seconds like GPT - this will ensure better user experience

- How many users can we expect?
  - Let's assume there's 1M users in total, and around 50k requests per second

### Functional

- Users can send messages to the chatbot, get responses back, rate responses, and view past messages
- Users can also send attachments

- Users should get responses within 1 sec - a few mins, but needs to get back periodic response updates
- 1M users in total, 50k requests per second

### Non-functional

- Latency on periodic response updates:
  - Although latency is not a strict requirement, we still want to send back periodic response updates every few seconds to keep the user updated on the response
- Throughput:
  - The system should efficiently handle the numerous requests which will likely be sent to workers containing the LLM / ML models

## Data model / entities

- Conversations:
  - This entity is optional, and is used to group the messages within a conversation. GPT has this feature, where messages created within a few hours of each other are in a single conversation.
    
    - conversationID
    - userID
    - createdAt

- Messages:
  - This entity will store all the messages sent by both the user and the chatbot. Either the messageID could be used to sort the messages on the client-side if using a numeric timestamp value such as UNIX within the ID (Twitter snowflake provides this) OR the sentAt can be used to sort the messages on the client-side.
  - Note that for a single request, the chatbot could still return multiple messages, which we'll add to this entity
    
    - messageID
    - conversationID
    - senderID: { userID or chatbotID }
    - message, s3AttachmentURLs
    - sentAt
    - rating (optional)

- Chatbot:
  - We're assuming there could be multiple chatbotTypes (this is optional), where depending on the inquiry of the user's message, the message could be handled by different chatbotIDs of a chatbotType.
  - We're also assuming that the chatbot's LLM / ML code is within the workers which will likely handle the client's message. If the ML models are loaded onto the worker containers, then this will be more efficient because the workers don't have to load the model every single time when generating predictions
    
    - chatbotID
    - lastHeartbeat
    - s3URL
    - chatbotType (optional)

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
  - Authentication: Bearer

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
  - Cache-Control: no-cache max-age Private/Public

### Retrieving messages in a conversation

- We can set the nextCursor value (via cursor based pagination) to the viewport's oldest sentAt time for the messageID. This way, we'll return the next paginated results with messages which are older than the viewport's oldest sentAt time

Request:
```bash
GET /conversations/:conversationID/messages?nextCursor={ viewport's oldest sentAt for messageID }&limit
```

Response:
```bash
{
  messages: [ { messageID, senderID, message, s3AttachmentURLs, sentAt } ],
  nextCursor, limit
}
```

### Send a message

- This endpoint will be used by the client and chatbot workers to send messages for the current conversation

- Note that after the client sends a message, the client will likely either poll vs get SSEs vs establish a websocket connection with the servers to get updates about the response. The maximum handle time of the request is around a few mins, so these types of connections should be fine and not take up too much bandwidth

Request:
```bash
POST /conversations/:conversationID/messages
{
  message
}
```

### Receive response updates

- After clients send an initial message to the Live response servers, they'll use this endpoint to establish a SSE connection to receive updates from the server (we're assuming we'll use SSE here).
- Note that we need to have 2 different endpoints, the above one for sending an initial message, and this one for establishing a SSE connection right after, because SSE doesn't allow clients to send requests by default.

#### Establish a SSE connection

- This endpoint will be used to establish the SSE connection. The header "Connection: keep-alive" will be used to establish a long-lived connection with the server (default value for keep-alive is 2 hrs, but it's more appropriate to have a much smaller value to reduce taking up unnecessary bandwidth)

- The text/event-stream indicates that the client expects a SSE based data stream

Request:

```bash
GET /conversations/:conversationID/messages/events
Accept: text/event-stream
Connection: keep-alive
```
- The server will respond to the client with response updates when the Chatbot workers have generated new updates

Response:

```bash
HTTP/1.1 200 OK
Content-Type: text/event-stream
Connection: keep-alive
{
  id: 101
  event: messages
  data: { messageID, message, s3AttachmentURLs }

  retry: 500
}
```

### Upload attachments

- When uploading binary data, multipart/form-data / multipart/mixed or another MIME	type such as image/png is usually used

- The content type is set to multipart/mixed which means that the request contains	different inputs and each input can have a different encoding type (JSON or binary).	The metadata sent will be in JSON, while the file itself will be in binary. 

- The placeholder {---xxBOUNDARYxx—} will contain a text string for the boundary	that differentiates one part of the body from another. For example				“__the_boundary__” could be used as the string. Boundaries must also start with		double hyphens and end with double hyphens too.

- Note that since this design is using a pre-signed URL to upload files, the client will	first request for a pre-signed URL from the servers, then make a HTTP PUT request	with the file data in the request body to the pre-signed URL 

#### Request for a pre-signed URL

Request:
```bash
POST /conversations/:conversationID/pre-signed-url
{
	attachmentName, fileType
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

### Download attachments

- Downloads an attachment via the attachmentID (we're using attachmentIDs instead of sending the pre-signed URLs ahead of time to the client because the pre-signed URLs have an expiration time)

- When downloading binary content using HTTP, application/octet-stream can be		used to receive binary data

- The application/octet-stream MIME type is used for unknown binary files. It		preserves the file contents, but requires the receiver to determine file type, for		example, from the filename extension. The Internet media type for an arbitrary byte	stream is application/octet-stream.

- The */* means that the client can accept any type of content in the response -		which could also be used for sending / receiving binary data

- Note that to download files, we could use either a pre-signed URL or a URL the		client can request to download from the CDN (let’s call it CDN URL). The process is	similar to uploading files, where the client first requests the servers for a pre-signed	URL OR CDN URL, then the client will download the file from the pre-signed URL /	CDN URL. However, using a CDN may be an overkill for this design.

#### Request for a pre-signed URL / CDN URL

Request:
```bash
GET /conversations/:conversationID/attachments/:attachmentID/pre-signed-url OR cdn-url
```

Response:
```bash
{
	pre-signed URL or CDN URL
}
```

#### Download from pre-signed URL / CDN URL

Request:
```bash
GET /<pre-signed URL or CDN URL>
Accept: application/octet-stream or */*
```

Response:
```bash
Content-Type: application/octet-stream or */*
Content-Disposition: attachment; filename=”<FILE_NAME>”
{
	attachment’s binary data used to generate the attachment on the client side
}
```

### Rating a response

Request:
```bash
PATCH /conversations/:conversationID/messages/:messageID?op={RATE_UP or RATE_DOWN}
```

### Workflow

The workflow of the system is as follows:

1. The client can send their message (via the Live response servers) and upload attachments (via pre-signed URLs retrieved from the API servers). This request will then likely be sent to a Chatbot queue via the Live response servers.
2. After the client sends the request, they will also either use polling vs SSE vs websocket to get back response updates from the Live response servers
3. Separate "Chatbot workers" (which can be containers) with the LLM / ML model or access to the models will pull from the Chatbot queue, and generate the response. As it's generating the response, it will update the response to the Messages table over time - and also request the Live response servers to send a SSE to the client with the response updates (assuming we're using SSE here)
4. The servers which have a connection with the client will send back the response updates received from the Chatbot workers
5. When the request has been fully handled, the servers will close the connection with the client

## HLD

### Microservice vs monolithic

- Majority of large scale systems with multiple required services and entities may be better managed using a microservice architecture. However, a monolithic architecture might be more appropriate for a chatbot. Excluding the LLM / ML parts, the system is small enough that it can be managed in a single codebase, and it will create more overhead to manage multiple services.

### API servers

- The API servers will handle requests for viewing past messages, uploading / downloading attachments and rating a message (stateless operations) - the API servers will essentially handle operations which don't directly require a SSE connection or serving the client's request to the chatbot (such as read heavy requests). The API servers will also frequently communicate with the database to retrieve past messages, and update the rating for messages. The API servers will not handle the stateful connections with the clients, where the client is waiting to hear response updates from the chatbot.

### Database

- The database will contain the conversations, messages and chatbots data. The database will also store response updates from the Chatbot workers in the Messages table.

- Most modern databases will work for storing this kind of data. We also do have a few relationships, but nothing too complex. Either PostgreSQL or DynamoDB will work just as well with a few modifications such as indexing and partitioning to speed up queries.

- We'll use DynamoDB, where the primary key (partition key + sort key) could be as follows:
  - Conversations table:
    - Partition key: (userID + conversationID) + Sort key: (createdAt)
  - Messages table:
    - Partition key: (userID + conversationID + messageID) + Sort key: (sentAt)
- This way, we can quickly query the conversations for a specific userID, and query the messages for a specific userID + conversationID, and also return the paginated results in a sorted order by time.

### Live response servers

- Clients will first send their initial message for a conversation to the Live response servers, and then send another request right after to establish a SSE connection. The Live response servers will then enqueue the client messages to the Chatbot queue, and allow the Chatbot workers to handle the request. The Live response servers will also store the client's initial message for a conversation in the database.

- The Live response servers will handle requests such as establishing the SSE connection with the clients, after the clients have sent an initial message for the conversation. GPT actually also uses SSE, and we'll use it too, but below are some of the other options:
  - Polling:
    - Clients can poll for response updates from the Live response servers every few seconds. Clients can send a request to the servers for any new updates after a specific sentAt field, which was returned previously by the servers.
    - Polling can lead to bandwidth issues on the server-side, since connections will need to be opened and closed frequently when there are no new updates - making unnecessary network requests.
  - Websockets:
    - Since the communication is not necessarily bidirectional after the client sends an initial message to the chatbot, websockets are not optimal here. Websockets are optimal when there is frequent bidirectional communication. However, in this case, only the server will be sending back updates to the client, making it a unidirectional communication.
  - SSE:
    - Since we're using SSEs, the API design for sending messages and receiving responses will use the EventSource API provided in JS. Clients will send the message to the Live response servers, and connect to these servers via a long-lived HTTP connection using the header "Connection: keep-alive". The client will then receive SSE updates from the Live response servers. When the Chatbot worker has new response updates, it will store it in the database, and request the Live response servers to send these response updates to the client via SSE.

### Chatbot queue

- We mainly want to ensure that a client's request (which may take a few seconds to a couple minutes to serve) doesn't block another user's request from being served. Thus, it's much more efficient to distribute the users' requests across Chatbot workers via a queue like SQS which ensures exactly-once delivery. Note that if the client's request on average took a few milliseconds to handle, then we wouldn't need this queue and workers. However, because different client requests could take very long, we don't want to block other client requests from being handled by the chatbot, thus we'll use this queue + workers approach.

- The Chatbot queue will contain the enqueued client messages, which can be handled via the Chatbot workers. The Live response servers will first enqueue the client's initial message to this queue, then Chatbot workers will pull the message and generate the response updates. Because we'll want exactly-once delivery, where one single Chatbot worker works on handling a specific client message, we can use SQS, since it provides a visibility timeout, which will also further support in re-tries via exponential backoff. Additionally, the client message can be queued by priority as well if needed using SQS's delayed message delivery feature. SQS also stores messages for at least 4 days, thus it is a highly persistent solution.

- Additionally, we could also have separate Chatbot queues for different chatbotTypes and for different scaling events - clients could also potentially specify the chatbotType they want to use.

### Chatbot workers

- These workers are stateless containers which will continuously pull client messages from the Chatbot queue. These workers will also contain the LLM / ML model, or have access to it (model might likely be in a blob store). The Live response servers or these workers can also batch client messages together prior to enqueing, such that a single worker generates the responses in parallel for different clients via multi-processing. The Chatbot workers could also use the uploaded attachments in the blob store to generate the response.

- We're using separate workers here because the response generation by far will take the longest time in the system, therefore we want it to be done separately for different clients, rather than blocking other requests from the client.

#### Scaling Chatbot workers

- Because the Chatbot workers will frequently communicate with the database, and parform parallel operations, an IO optimized EC2 instance might be preferred here, where a single instance could contain multiple workers (containers).

- Chatbot workers can also be easily horizontally scaled by adding or removing containers, or vertically scalled by adding more CPU to the servers which are running the containers. We’ll also prefer a VM based instance like EC2 in which we can manage the infrastructure instead of a serverless service such as AWS Lambda which has a cold start latency. Based on the load, we could have roughly 50 - 100 workers, with a single EC2 instance containing multiple workers.

### Blob store

- The attachments can be uploaded / downloaded directly from the blob store via a pre-signed URL sent by the API servers. The Chatbot workers could also retrieve the client's attachments, or upload any attachments for the response to the blob store.

### L7 load balancer

- Because SSE operates at the HTTP level, the client will likely request a L7 load balancer to be routed to a Live response server, then the SSE connection will be established between the client and the Live response servers.

<img width="850" alt="image" src="https://github.com/user-attachments/assets/43c6a84f-7b05-42ea-acd4-26aecb64db89" />

## DD

### Cache to improve read latency of past requests

- Because the recent conversations and messages data will likely be frequently accessed by both the client and the Chatbot workers, we can also store recent or current conversations and messages data within Redis sorted sets, where the score is the respective timestamp fields, createdAt and sentAt. Also, it may be better to use Redis sorted sets as opposed to DynamoDB's DAX, because Redis sorted sets directly provide sorting capabilities, while DAX is a write-through cache that only caches data on cache misses by default.
- Thus, the Chatbot workers could send the Live response servers the chatbot responses periodically, and then the Live response servers could send these response updates to the client via SSE. Asynchronously, the Chatbot workers could also store the chatbot responses in the DB, and via CDC (DynamoDB streams with Lambda functions), the chatbot responses could then be stored in the Redis sorted set for the current conversation (because it's likely clients will want to read their current convos frequently).

- The Redis Sorted Set with SSE solution offers real-time updates and is more appropriate for this unidirectional communication only coming from the servers. The Chatbot workers will request the Live response servers to send a SSE to the client when there are new response updates added to the DB

- Note that Redis sorted sets are also used in this design to prevent some of the reads being made to the DB, since there will be multiple Chatbot worker containers also reading and writing to the DB periodically as the responses come in for the current conversation - using Redis sorted sets will also reduce the number of reads made by the Chatbot workers on the DB.

### Lost chatbot responses

- During a network partition within the Chatbot workers, we want to avoid having a "lost chatbot response" where we don't know if a Chatbot worker is down or not. Since the worker is down or can't communicate due to a network partition, the response won't be generated.

- To fix this "lost chatbot response" issue, a lastHeartbeat field can be used in the Chatbots table. The lastHeartbeat field will be updated via heartbeats, let's say every 30 secs or so by the Chatbot worker handling the client's message.

- We can also use a separate Monitoring service that polls the Chatbots table, let's say every 1 min to check the lastHeartbeat values, and if the worker's lastHeartbeat wasn't updated for a while, the worker will be considered down. In this case, the Monitoring service can re-enqueue the client's message request with an appropriate visibility timeout to the Chatbot queue.

### Ensuring at-least-once handling of client messages

- If a worker fails to handle a client message, we want to ensure that the request is re-tried a few times before asking the client to re-try sending the message via the SSE. Requests can fail within a Chatbot worker for the below reasons:
  - Visible failure:
    - The execution fails visibly in some way, likely due to a bug in the LLM / ML code or container code.
  - Invisible failure:
    - The request fails invisibly, likely due to the worker crashing

#### Handling visible failures

- Handling visible failures is easier, and can be wrapped up in a try / catch block so that we can log the error. The request can then be re-tried a few times with exponential backoff by increasing the visibility timeout on each re-try as well if needed (SQS provides exponential backoff via its visibility timeout), before asking the client via SSE to re-try sending the message.

#### Handling invisible failures

- When a worker crashes or becomes unresponsive, we need a reliable way to detect this and retry the request using the below approaches, and in 'Handling invisible failures' (taken from the SDI 'Distributed job scheduler'):
  - Heartbeats / health check endpoints
  - Job leasing
  - SQS visibility timeout

### Ensuring the system is scalable to support thousands of client messages per second

We can scale the system by looking from left to right looking for any bottleneck and addressing them:

#### Client message initiation

- To handle a large number of client messages, we can introduce a message queue like Kafka or SQS between the L7 load balancer and Live response servers. The queue acts as a buffer during traffic spikes, allowing the Live response servers to process requests at a sustainable rate rather than being overwhelmed.
- The message queue also allows us to horizontally scale the Live response servers to consume the client's messages, while providing durability to ensure no request is dropped if the Live response servers experience issues.

**Adding a message queue between the L7 load balancer and Live response servers is likely overcomplicating the design. The Live response servers should be able to handle the write throughput and SSE connections directly. Unless there's expensive business logic in the Live response servers that we want to isolate, it's better to keep the architecture simpler and just scale the Live response servers themselves without adding another queue in-between the L7 load balancer and Live response servers.**

**In an interview setting, while this pattern might impress some interviewers, it's worth noting that simpler solutions are often better. Focus on properly scaling your database and workers before adding additional components.**

#### Database

- We could choose either DynamoDB (which we're using here) or Cassandra for storing the conversations and messages data depending on how many writes we'll need to support. If we have a much higher write load, then we could move the conversations and messages data to Cassandra, and provision multiple leaderless replicas to support the write load - because we're mostly dealing with text based data, which will have a high volume and size might be variable, Cassandra could be an option.

- Also, we can move the older conversations and messages to a cheaper cold storage like S3.

#### Chatbot queue capacity

- SQS automatically handles scaling and message distribution across consumers. We don't necessarily need to worry about manual sharding or partitioning of the messages - AWS handles all of that for us under the hood. However, we'll likely need to request for quota increase since the default limit is receiving 3K messages per second with batching within a single queue.
- We might still want multiple queues for either functional separation (like different queues for different chatbotTypes) or for scaling purposes.

**Note: even if we used a Redis sorted set as the Chatbot queue, 3 million jobs would easily fit in memory, so there's nothing to worry about there. You would just end up being more concerned with fault tolerance in case Redis goes down.**

#### Workers

- We can have the workers be either containers (using ECS or Kubernetes) or Lambda functions. These are the main options which can be started up quickly, without much downtime:
  - Containers:
    - Contains tend to be more cost-effective if they're configured properly, and are better for long-running executions since they maintain state between executions inside volumes. However, they do require more operational overhead and don't scale as well as serverless options.
    - In this case, the containers will have code to pull the messages from the SQS queue
  - Lambda functions:
    - Lambda functions provide very minimal operational overhead. They're perfect for short-lived executions under 15 minutes, and can auto-scale instantly to match the workload. However, Lambda functions have a cold start-up time which could impact any latency requirements on returning the chatbot responses.
    - In this case, the Lambda functions will directly pull the messages from the SQS queue

- We went with using a container mainly because the LLM / ML model could take several minutes to handle a request in some cases, and Lambda has a max timeout of 15 mins. Containers also allow us to optimize the configuration such that we can have different types of containers catered to different types of requests (compute, memory, IO, network, etc optimized). We can also set up scaling policies within ECS to start up more containers - such as scaling the containers based on the SQS queue size.

- Note: we could also use spot instances instead of containers to reduce costs by 70%.

<br/>
<br/>

Additional deep dives:

### Efficiently fetching from Redis sorted set

We will use a Redis sorted set to efficiently fetch the recent conversations and messages, however we have the following options, and in ‘Efficiently fetching from the Redis sorted set / live leaderboard’ (taken from the SDI 'Leetcode'):

- Polling with database queries

- Caching with periodic updates:
  - Using this approach, we will still cache majority of the queries, but when there are cache misses,			the API servers will run the query on the database, which may still be expensive. To make sure			there are more cache hits using this approach, we could still use a cron job which runs every 10-20			secs or so and updates the cache. Thus, only the cron job will be running the expensive query on			the database, and clients will have reduced cache misses.

  - The issue with using a cron job is that if it is down, then the cache will not be updated, and it will			cause multiple cache misses OR clients requesting the API servers to			run the expensive database query. Also, the cron job will have to update the cache very frequently (which may not be possible for a single cron job), since the Chatbot workers will update the DB with response updates every few seconds or so.

- Redis sorted set with SSE / periodic polling: 
  - There may be inconsistencies between the database and cache, thus we could add CDC			(change data capture). For different databases like DynamoDB, there is DynamoDB streams, and		for PostgreSQL, there is PostgreSQL CDC. CDC is used to capture updates on the database in		the form of WAL or another operations log, and replay any missed operations on other services. Usually CDC functionalities for various databases will store the operations in the WAL, and push		it to a queue such as Kafka - then there will be lightweight workers within the other service which will pull			operations from the queue and perform the operations on the other service
  - In		this case, we can use CDC to replay operations on the DynamoDB database to the cache using		DynamoDB streams to ensure the cache and database have the same consistent data

- Note that since these approaches are taken from the SDI 'Leetcode', it's using polling. However, in our design, we're using SSE - so just substitute it with SSE.

Efficiently fetching from the Redis sorted set / live leaderboard:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/d5e1c28a-6bce-4801-b146-f55688d3e78b" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/a44ce39d-b012-4e50-957e-14b8baec10af" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/7a420fec-d6be-4908-87db-e28c8e384fde" />

**The Redis Sorted Set with SSE solution offers real-time updates and is more appropriate for this unidirectional communication only coming from the servers. The Chatbot workers will request the Live response servers to send a SSE to the client when there are new response updates in the DB, thus triggering a CDC event from the DB to the Redis sorted set**
