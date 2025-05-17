- if the ML models are loaded onto the worker containers, then this will be more efficient because the workers don't have to load the model every single time when generating predictions

# ML predictor

Design a system which will use multiple ML models (different models such as class ML models, NLP models, etc) as a blackbox to perform and return predictions.

## Requirements

### Questions

- To confirm, should we treat the actual models as a black box, and treat it like a separate service?
  - Yes, let's not focus on the actual specifics of the models

- Can the models accept any kind of input, such as text, images, videos, etc?
  - Let's assume the model will only accept just text based data

- What is the latency requirement for users getting responses back from the models - will the model response generation take a while, let's say 3 - 10 secs? Do we also want to send back periodic response updates every few seconds (like GPT), so that the user knows the model is working on the request?
  - Let's say the response generation takes anywhere from 1 sec to a few mins depending on the request itself
  - We could also send back periodic response updates every few seconds like GPT - this will ensure better user experience

- Should users also be able to view previous responses, and do we need to store model requests and responses?
  - Yes, let's store the model requests and responses to let users view the models' previous responses
    
- How many users can we expect?
  - Let's assume there's 1M users in total, and around 50k requests per second

- Are the models themselves stored within a blob store, or can we assume that they're hard-coded, and we have access to the model's code?
  - Let's assume that the models are stored within the blob store, and the models' code will load / use the models stored within the blob store to make predictions.

### Functional

- Users can send requests to the model and get responses back, and also view past requests / responses
- Users should get back responses within 1 sec - a few mins, but needs to get back periodic response updates
- 1M users in total, 50k requests per second

### Non-functional

- Latency:
  - Although latency is not a strict requirement (the model responses might take some time), we still want to send back periodic response updates every few seconds to keep the user updated on the response
- Throughput:
  - The system should efficiently handle the numerous requests which will likely be sent to workers containing the model code, and having access to the stored models in the blob store

## Data model / entities

- Requests:
  - This entity will store all the requests sent by the user, along with the responses sent by the models. Either the requestID could be used to sort the requests on the client-side if using a numeric timestamp value such as UNIX within the ID (Twitter snowflake provides this) OR the createdAt can be used to sort the requests on the client-side
    - requestID
    - userID
    - modelID
    - request
    - responses: Array containing responses sent by the model [ { response, sentAt } ]
    - createdAt

- Models:
  - Because there could be multiple models, we'll be storing these models in a blob store, where depending on the request's modelID selected, the request could be handled by different models stored in the blob store
  - We're also assuming that the models' code is written in the workers which will likely handle the client's requests. If the ML models are loaded onto the worker containers, then this will be more efficient because the workers don't have to load the model every single time when generating predictions

    - modelID
    - lastHeartbeat
    - s3URL

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
  - Authentication: Bearer

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
  - Cache-Control: no-cache max-age Private/Public

### Retrieving previous requests and responses

- We can set the nextCursor value (via cursor based pagination) to the viewport's oldest sentAt time for the requestID. This way, we'll return the next paginated results with requests which are older than the viewport's oldest sentAt time

Request:
```bash
GET /requests?nextCursor={ viewport's oldest sentAt for requestID }&limit
```

Response:
```bash
{
  requests: [ { requestID, modelID, request, responses: [ { response, sentAt } ], sentAt } ],
  nextCursor, limit
}
```

### Send a request

- This endpoint will be handled by the Live response servers when clients send their initial request
- Note that after the client sends a request, the client will likely either poll vs get SSEs vs establish a websocket connection with the servers to get updates about the response. The maximum handle time of the request is around a few mins, so these types of connections should be fine and not take up too much bandwidth

Request:
```bash
POST /requests
{
  modelID
  request: Request object likely containing { requestID, requestText / requestInput }
}
```

### Receive response updates

- After clients send an initial request to the Live response servers, they'll use this endpoint to establish a SSE connection to receive updates from the server (we're assuming we'll use SSE here)
- Note that we need to have 2 different endpoints, the above one for sending an initial request, and this one for establishing a SSE connection right after, because SSE doesn't allow clients to send requests by default.

#### Establish a SSE connection

- This endpoint will be used to establish the SSE connection. The header "Connection: keep-alive" will be used to establish a long-lived connection with the server (default value for keep-alive is 2 hrs, but it's more appropriate to have a much smaller value to reduce taking up unnecessary bandwidth)

- The text/event-stream indicates that the client expects a SSE based data stream

Request:
```bash
GET /requests/:requestID/events
Accept: text/event-stream
Connection: keep-alive
```

- The server will respond to the client with response updates when the model has generated new updates

Response:
```bash
HTTP/1.1 200 OK
Content-Type: text/event-stream
Connection: keep-alive
{
  id: 101
  event: responses
  data: { response, sentAt }

  retry: 500
}
```

### Workflow

The workflow of the system is as follows:

1. The client can send their request (via the Live response servers). This request will then likely be sent to a Chatbot queue via the Live response servers.
2. After the client sends the request, they will also either use polling vs SSE vs websocket to get back response updates from the Live response servers
3. Separate "Model workers" (which can be containers) with the ML code or access to the models will pull from the Model queue (via the modelID provided in the request), and generate the response. As it's generating the response, it will update the response to the Requests table over time - and also request the Live response servers to send a SSE to the client with the response updates (assuming we're using SSE here)
4. The servers which have a connection with the client will send back the response updates received from the Model workers
5. When the request has been fully handled, the servers will close the connection with the client

## HLD

### Microservice vs monolithic

- Majority of large scale systems with multiple required services and entities may be better managed using a microservice architecture. However, a monolithic architecture might be more appropriate for a ML predictor. Excluding the ML parts, the system is small enough that it can be managed in a single codebase, and it will create more overhead to manage multiple services.

### API servers

- The API servers will handle requests for viewing past requests and stateless operations - the API servers will essentially handle operations which don't directly require a SSE connection or serving the client's request to the models (such as read heavy requests). The API servers will also frequently communicate with the database to retrieve past requests. The API servers will not handle the stateful connections with the clients, where the client is waiting to hear response updates from the chatbot.

### Database

- The database will contain the requests and models data. The database will also store response updates from the Model workers in the Requests table.

- Most modern databases will work for storing this kind of data. We also do have a few relationships, but nothing too complex. Either PostgreSQL or DynamoDB will work just as well with a few modifications such as indexing and partitioning to speed up queries.

- We'll use DynamoDB, where the primary key (partition key + sort key) could be as follows:
  - Requests table:
    - Partition key: (userID + requestID) + Sort key: (sentAt)
- This way, we can quickly query the requests for a specific userID + requestID, and also return the paginated results in a sorted order by time.

### Live response servers

- Clients will first send their initial request to the Live response servers, and then send another request right after to establish a SSE connection. The Live response servers will then enqueue the client requests to the Model queue, and allow the Model workers to handle the request. The Live response servers will also store the client's initial request in the database.

- The Live response servers will handle requests such as establishing the SSE connection with the clients, after the clients have sent an initial request to the Live response servers. GPT actually also uses SSE, and we'll use it too, but below are some of the other options:
  - Polling:
    - Clients can poll for response updates from the Live response servers every few seconds. Clients can send a request to the servers for any new updates after a specific sentAt field, which was returned previously by the servers.
    - Polling can lead to bandwidth issues on the server-side, since connections will need to be opened and closed frequently when there are no new updates - making unnecessary network requests.
  - Websockets:
    - Since the communication is not necessarily bidirectional after the client sends an initial request, websockets are not optimal here. Websockets are optimal when there is frequent bidirectional communication. However, in this case, only the server will be sending back updates to the client, making it a unidirectional communication.
  - SSE:
    - Since we're using SSEs, the API design for sending requests and receiving responses will use the EventSource API provided in JS. Clients will send the request to the Live response servers, and connect to these servers via a long-lived HTTP connection using the header "Connection: keep-alive". The client will then receive SSE updates from the Live response servers. When the Model worker has new response updates, it will store it in the database, and request the Live response servers to send these response updates to the client via SSE.

### Model queue

- We mainly want to ensure that a client's request (which may take a few seconds to a couple minutes to serve) doesn't block another user's request from being served. Thus, it's much more efficient to distribute the users' requests across Model workers via a queue like SQS which ensures exactly-once delivery. Note that if the client's request on average took a few milliseconds to handle, then we wouldn't need this queue and workers. However, because different client requests could take very long, we don't want to block other client requests from being handled by the chatbot, thus we'll use this queue + workers approach.

- The Model queue will contain the enqueued client requests, which can be handled via the Model workers. The Live response servers will first enqueue the client's initial request to this queue, then Model workers will pull the message and generate the response updates. Because we'll want exactly-once delivery, where one single Model worker works on handling a specific client request, we can use SQS, since it provides a visibility timeout, which will also further support in re-tries via exponential backoff. Additionally, the client request can be queued by priority as well if needed using SQS's delayed message delivery feature. SQS also stores messages for at least 4 days, thus it is a highly persistent solution.

- Additionally, we could also have separate Model queues for different modelIDs and for different scaling events since clients are already specifying which modelID they want to use.

### Model workers

- These workers are stateless containers which will continuously pull client requests from the Model queue. These workers will also contain the ML code, or have access to it (model might likely be in a blob store). The Live response servers or these workers can also batch client requests together prior to enqueing, such that a single worker generates the responses in parallel for different clients via multi-processing.

- We're using separate workers here because the response generation by far will take the longest time in the system, therefore we want it to be done separately for different clients, rather than blocking other requests from the client.

#### Scaling Model workers

- Because the Model workers will frequently communicate with the database, and parform parallel operations, an IO optimized EC2 instance might be preferred here, where a single instance could contain multiple workers (containers).

- Model workers can also be easily horizontally scaled by adding or removing containers, or vertically scalled by adding more CPU to the servers which are running the containers. We’ll also prefer a VM based instance like EC2 in which we can manage the infrastructure instead of a serverless service such as AWS Lambda which has a cold start latency. Based on the load, we could have roughly 50 - 100 workers, with a single EC2 instance containing multiple workers.

### Blob store

- The Model workers will retrieve the model from the blob store via the modelID's s3URL stored in the Models table - since the client will request to use a specific modelID.

### L7 load balancer

- Because SSE operates at the HTTP level, the client will likely request a L7 load balancer to be routed to a Live response server, then the SSE connection will be established between the client and the Live response servers.

<img width="900" alt="image" src="https://github.com/user-attachments/assets/1831483d-72fa-4114-b02a-4bbd9634df70" />

## DD

### Cache to improve read latency of past requests

- Because the recent request and response data will likely be frequently accessed by both the client and the Model workers, we can also store recent request / response data within Redis sorted sets, where the score can be the sentAt field of the requestID. Also, it may be better to use Redis sorted sets as opposed to DynamoDB's DAX, because Redis sorted sets directly provide sorting capabilities, while DAX is a write-through cache that only caches data on cache misses by default.
- Thus, the Model workers could send the Live response servers the response updates periodically, and then the Live response servers could send these response updates to the client via SSE. Asynchronously, the Model workers could also store the response updates in the DB, and via CDC (DynamoDB streams with Lambda functions), the response updates could then be stored in the Redis sorted set for the current request (because it's likely clients will want to read their recent requests frequently).

- The Redis Sorted Set with SSE solution offers real-time updates and is more appropriate for this unidirectional communication only coming from the servers. The Model workers will request the Live response servers to send a SSE to the client when there are new response updates added to the DB

- Note that Redis sorted sets are also used in this design to prevent some of the reads being made to the DB, since there will be multiple Model worker containers also reading and writing to the DB periodically as the responses come in for the current request - using Redis sorted sets will also reduce the number of reads made by the Model workers on the DB.

### Lost chatbot responses

- During a network partition within the Model workers, we want to avoid having a "lost chatbot response" where we don't know if a Model worker is down or not. Since the worker is down or can't communicate due to a network partition, the response won't be generated.

- To fix this "lost chatbot response" issue, a lastHeartbeat field can be used in the Models table. The lastHeartbeat field will be updated via heartbeats, let's say every 30 secs or so by the Model worker handling the client's request.

- We can also use a separate Monitoring service that polls the Models table, let's say every 1 min to check the lastHeartbeat values, and if the worker's lastHeartbeat wasn't updated for a while, the worker will be considered down. In this case, the Monitoring service can re-enqueue the client's request with an appropriate visibility timeout to the Chatbot queue.

### Ensuring at-least-once handling of client requests

- If a worker fails to handle a client request, we want to ensure that the request is re-tried a few times before asking the client to re-try sending the request via the SSE. Requests can fail within a Model worker for the below reasons:
  - Visible failure:
    - The execution fails visibly in some way, likely due to a bug in the ML code or container code.
  - Invisible failure:
    - The request fails invisibly, likely due to the worker crashing

#### Handling visible failures

- Handling visible failures is easier, and can be wrapped up in a try / catch block so that we can log the error. The request can then be re-tried a few times with exponential backoff by increasing the visibility timeout on each re-try as well if needed (SQS provides exponential backoff via its visibility timeout), before asking the client via SSE to re-try sending the request.

#### Handling invisible failures

- When a worker crashes or becomes unresponsive, we need a reliable way to detect this and retry the request using the below approaches, and in 'Handling invisible failures' (taken from the SDI 'Distributed job scheduler'):
  - Heartbeats / health check endpoints
  - Job leasing
  - SQS visibility timeout

### Ensuring the system is scalable to support thousands of client requests per second

We can scale the system by looking from left to right looking for any bottleneck and addressing them:

#### Client request initiation

- To handle a large number of client requests, we can introduce a message queue like Kafka or SQS between the L7 load balancer and Live response servers. The queue acts as a buffer during traffic spikes, allowing the Live response servers to process requests at a sustainable rate rather than being overwhelmed.
- The message queue also allows us to horizontally scale the Live response servers to consume the client's requests, while providing durability to ensure no request is dropped if the Live response servers experience issues.

**Adding a message queue between the L7 load balancer and Live response servers is likely overcomplicating the design. The Live response servers should be able to handle the write throughput and SSE connections directly. Unless there's expensive business logic in the Live response servers that we want to isolate, it's better to keep the architecture simpler and just scale the Live response servers themselves without adding another queue in-between the L7 load balancer and Live response servers.**

**In an interview setting, while this pattern might impress some interviewers, it's worth noting that simpler solutions are often better. Focus on properly scaling your database and workers before adding additional components.**

#### Database

- We could choose either DynamoDB (which we're using here) or Cassandra for storing the requests data depending on how many writes we'll need to support. If we have a much higher write load, then we could move the requests data to Cassandra, and provision multiple leaderless replicas to support the write load - because we're mostly dealing with text based data, which will have a high volume and size might be variable, Cassandra could be an option.

- Also, we can move the older request data to a cheaper cold storage like S3.

#### Chatbot queue capacity

- SQS automatically handles scaling and message distribution across consumers. We don't necessarily need to worry about manual sharding or partitioning of the messages - AWS handles all of that for us under the hood. However, we'll likely need to request for quota increase since the default limit is receiving 3K messages per second with batching within a single queue.
- We might still want multiple queues for either functional separation (like different queues for different modelIDs) or for scaling purposes.

**Note: even if we used a Redis sorted set as the Model queue, 3 million jobs would easily fit in memory, so there's nothing to worry about there. You would just end up being more concerned with fault tolerance in case Redis goes down.**

#### Workers

- We can have the workers be either containers (using ECS or Kubernetes) or Lambda functions. These are the main options which can be started up quickly, without much downtime:
  - Containers:
    - Contains tend to be more cost-effective if they're configured properly, and are better for long-running executions since they maintain state between executions inside volumes. However, they do require more operational overhead and don't scale as well as serverless options.
    - In this case, the containers will have code to pull the messages from the SQS queue
  - Lambda functions:
    - Lambda functions provide very minimal operational overhead. They're perfect for short-lived executions under 15 minutes, and can auto-scale instantly to match the workload. However, Lambda functions have a cold start-up time which could impact any latency requirements on returning the responses.
    - In this case, the Lambda functions will directly pull the messages from the SQS queue

- We went with using a container mainly because the ML model could take several minutes to handle a request in some cases, and Lambda has a max timeout of 15 mins. Containers also allow us to optimize the configuration such that we can have different types of containers catered to different types of requests (compute, memory, IO, network, etc optimized). We can also set up scaling policies within ECS to start up more containers - such as scaling the containers based on the SQS queue size.

- Note: we could also use spot instances instead of containers to reduce costs by 70%.

<br/>
<br/>

Additional deep dives:

### Efficiently fetching from Redis sorted set

We will use a Redis sorted set to efficiently fetch the recent requests, however we have the following options, and in ‘Efficiently fetching from the Redis sorted set / live leaderboard’ (taken from the SDI 'Leetcode'):

- Polling with database queries

- Caching with periodic updates:
  - Using this approach, we will still cache majority of the queries, but when there are cache misses,			the API servers will run the query on the database, which may still be expensive. To make sure			there are more cache hits using this approach, we could still use a cron job which runs every 10-20			secs or so and updates the cache. Thus, only the cron job will be running the expensive query on			the database, and clients will have reduced cache misses.

  - The issue with using a cron job is that if it is down, then the cache will not be updated, and it will			cause multiple cache misses OR clients requesting the API servers to			run the expensive database query. Also, the cron job will have to update the cache very frequently (which may not be possible for a single cron job), since the Model workers will update the DB with response updates every few seconds or so.

- Redis sorted set with SSE / periodic polling: 
  - There may be inconsistencies between the database and cache, thus we could add CDC			(change data capture). For different databases like DynamoDB, there is DynamoDB streams, and		for PostgreSQL, there is PostgreSQL CDC. CDC is used to capture updates on the database in		the form of WAL or another operations log, and replay any missed operations on other services. Usually CDC functionalities for various databases will store the operations in the WAL, and push		it to a queue such as Kafka - then there will be lightweight workers within the other service which will pull			operations from the queue and perform the operations on the other service
  - In		this case, we can use CDC to replay operations on the DynamoDB database to the cache using		DynamoDB streams to ensure the cache and database have the same consistent data

- Note that since these approaches are taken from the SDI 'Leetcode', it's using polling. However, in our design, we're using SSE - so just substitute it with SSE.

Efficiently fetching from the Redis sorted set / live leaderboard:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/d5e1c28a-6bce-4801-b146-f55688d3e78b" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/a44ce39d-b012-4e50-957e-14b8baec10af" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/7a420fec-d6be-4908-87db-e28c8e384fde" />

**The Redis Sorted Set with SSE solution offers real-time updates and is more appropriate for this unidirectional communication only coming from the servers. The Model workers will request the Live response servers to send a SSE to the client when there are new response updates in the DB, thus triggering a CDC event from the DB to the Redis sorted set**












