# Rate limiter

## Requirements

### Questions

- What kind of rate limiter are we designing? Is it on the client side or server side.
  - Server side API rate limiter

- Does the rate limiter throttle API requests based on IP, user ID or other properties?
  - The rate limiter should be flexible enough to support different sets of throttle rules

- Will the system be in a distributed environment?
  - Yes

### Functional

- The rate limiter will limit the number of requests an entity can send to an API within a time window, e.g., 15 requests per second.
- The user should get an error message whenever the defined threshold is crossed within a single server or across a combination of servers. 

- The rate limiter will be in a distributed system and on the server-side
- The rate limiter will support different kinds of throttle rules
- The rate limiter should use as little memory as possible

### Non-functional

- Availability:
  - The rate limiter should always work since it protects the services from external attacks

- Low latency:
  - Responses from the rate limiter shouldn't have substantial affect on the application's latency

## Rate limiter 101

Rate limiting is also used to prevent revenue loss, to reduce infrastructure costs, to stop spam, and to stop online harassment. Following is a list of scenarios that can benefit from Rate limiting by making a service (or API) more reliable:

### Misbehaving clients/scripts

Either intentionally or unintentionally, some entities can overwhelm a service by sending a large number of requests. Another scenario could be when a user is sending a lot of lower-priority requests and we want to make sure that it doesn’t affect the high-priority traffic. For example, users sending a high volume of requests for analytics data should not be allowed to hamper critical transactions for other users.

### Security

By limiting the number of the second-factor attempts (in 2-factor auth) that the users are allowed to perform, for example, the number of times they’re allowed to try with a wrong password.

### To prevent abusive behavior and bad design practices

Without API limits, developers of client applications would use sloppy development tactics, for example, requesting the same information over and over again.

### To keep costs and resource usage under control

Services are generally designed for normal input behavior, for example, a user writing a single post in a minute. Computers could easily push thousands/second through an API. Rate limiter enables controls on service APIs.

### Revenue

Certain services might want to limit operations based on the tier of their customer’s service and thus create a revenue model based on rate limiting. There could be default limits for all the APIs a service offers. To go beyond that, the user has to buy higher limits

### To eliminate spikiness in traffic

Make sure the service stays up for everyone else.

<br/>

The following are some key concepts for rate limiting:

### Throttling and rules

Throttling is the process of controlling the usage of the APIs by customers during a given period. Throttling can be defined at the application level and/or API level. When a throttle limit is crossed, the server returns HTTP status “429 - Too many requests".

- A rate limiter can perform hard throttling, soft throttling or elastic/dynamic throttling where the rate limiting limit can change over time or if resources are available on the server-side

- Additionally, the rules and algorithms of the rate limiter may be applied differently for different userIDs, IP_addresses, requests, etc

### Client / middleware / server side rate limiter

- A rate limiter can be placed at either the client or server side. A client side rate limiter is generally unreliable because the client can modify the requests, and will also have access to the rate limiting logic which is not safe

- A server side rate limiter is preferred, as the clients won’t have direct access to the rate limiting logic, however a server side rate limiter can still slow down the API servers, as the servers now need to also maintain the rate limiting

- A rate limiter as a middleware is another approach, and will ensure that only unthrottled requests are sent to the API servers

- Overall, the rate limiter can be placed in the client side, middleware, server side, depending on multiple different factors, such as:
  - The rate limiting algorithm. Some rate limiting algorithms may be better on the server side
  - If there are not enough resources to build a rate limiter, a commercial rate limiter may be better

### API gateway

- If a microservice architecture is used and it includes an API gateway, then a rate limiter on the API gateway (middleware)	may be better

- Cloud based microservices have become popular and so a rate limiter is also often implemented in an API gateway. An		API gateway is a middleware service that provides rate limiting, authentication, encryption of requests, and so on.

### Rate limiter DB

The rate limiter can either use a centralized database or a distributed database:

- Centralized database:
  - Using a centralized database allows the rate limiter to interact with one data source, which is simpler, however			there will be an increase in latency if a burst of requests hit the centralized database, which may cause a SPOF
- Distributed database:
  - Using replica sets for the same data, and performing sharding by the userID, IP_address, etc, a distributed				database may be more complex to implement, but will prevent SPOFs. Using a distributed database, the replicas			will need to be consistent and have the same counter values, as multiple requests go to them. This can cause				inconsistency issues, where a quorum approach or vector clocks may be used.
 

## Data model / entities

- Rules:
  - ruleID
  - ruleEndpoint
  - ruleLimit
  - ruleInterval

- If using the fixed window country algorithm, the following request data will be stored in memory, likely in a cache such as a Redis sorted set within the Rate limiter middleware or the rate limiter cache:
  - userID
  - requestCount
  - timeWindow (timeWindow will likely be the start of the window - it could be the very first millisecond / second / minute of the window in a UNIX timestamp, and will help to determine which fixed window the requestID is for, and if the requestCount exceeded said window or not)

- If using the sliding window log algorithm, the following request data will be logged (it will be logged likely in a cache such as a Redis sorted set within the Rate limiter middleware or the rate limiter cache):
  - userID
  - requestID
  - timestamp

<br/>

## Rate limiting algorithms

There are multiple different rate limiting algorithms we could use:

### Token bucket

- The token bucket algorithm is widely used and is simple to implement. It is used by Amazon and Stripe.

- In this algorithm, a token bucket is a container that has a pre-defined capacity. Tokens are put into the bucket at preset		rates periodically. Once the bucket is full, no more tokens are added. When a request comes in, it will consume a token		from the bucket. We’ll check if there are enough tokens in the bucket. If there are enough tokens, we’ll take one token out		for each request and the request is processed. However, if there are not enough tokens, the request is dropped

- It usually necessary to have different buckets for different API endpoints or different IP addresses or the request type		depending on the rules we set for the rate limiting

- The token bucket algorithm has two parameters:
  - Bucket size: the maximum number of tokens allowed in the bucket
  - Refill rate: the number of tokens put into the bucket per interval
	
- The algorithm is easy to implement and is memory efficient. The algorithm can also handle bursts of traffic, since a 			request can only go through if there are tokens in the bucket

- The downside to this algorithm is that the bucket size and refill rate needs to be tuned and calculated which may be 		challenging

### Leaking bucket

- The leaking bucket algorithm is similar to the token bucket algorithm, except that requests are processed at a fixed rate.		The algorithm is usually implemented using a FIFO queue.

- When a request arrives, the system checks if the queue is full. If it is not full, the request is added to the queue. If the 		queue is full, the request is dropped. Requests are then pulled from the queue and processed at fixed intervals.
- Shopify uses this algorithm

- The leaking bucket algorithm has two parameters:
  - Bucket size: the maximum queue size
  - Outflow rate: the number of requests that can be processed at a fixed rate
	
- The algorithm is memory efficient, and is suitable for use cases where requests need to be processed at a fixed rate

- The downside to this algorithm is that a burst of traffic can fill up the queue with old requests, and if those requests are		not processed in time, the recent requests will be rate limited

- Another downside is that the two parameters in this algorithm may not be easy to tune and calculate

### Fixed window counter

- The fixed window algorithm divides the timeline into fixed-sized time windows, and assigns a counter for each time			window. Each request for the respective window will increment the counter by 1. Once the counter for the window reaches		a pre-defined threshold, new requests will be dropped until a new time window starts. An example of this algorithm is in ‘Fixed window counter algorithm’.

- This algorithm is memory efficient, and is easy to implement.
- The downside of this algorithm is that a burst of traffic at the edges could cause more requests to go through in the current window, when it should have went through the next window because the requests are at the edge of the window. We can use a sliding window to handle bursts of requests.
- Also, in a distributed environment, the "read and then write" beahvior can create a race condition. If two requests are sent for the same userID concurrently, then those two requests would likely read and write to the same cached entry (entry from the data model) for this algorithm - causing a race condition. We can use a Redis distributed lock with a TTL to address this issue, however the entry would be locked, which may slighly add some latency.

<br/>

- This algorithm could use a Redis sorted set within the rate limiter middleware or the rate limiter cache. An entry (taken from the data model) within a single sorted set, which represents the windows for a user, could look as follows:

```bash
{
  userID, requestCount, timeWindow
}
```

- Let's assume our rate limiter is allowing 3 requests per minute per user, so whenever a new request comes in, our rate limiter will perform the following steps:
  - If userID is not present in cache, we'll insert it and set the requestCount to 1, and set the timeWindow to the current minute as a UNIX timestamp
  - If userID is present in the cache, we'll find it and add 1 to the requestCount if the requestCount is less than 3 for the current timeWindow. Otherwise, we'll throttle the request.


Fixed window counter algorithm:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/84a11967-2a50-4c44-a371-f1214a14d1bd" />


<br/>

### Sliding window log

- The sliding window log algorithm addresses the time window boundary issue of the fixed window counter algorithm. The		sliding window log algorithm solves this issue by using a log to track the request timestamps. The timestamp data is			usually kept in a cache, such as a sorted set in Redis. 

- When a new request comes in, a timestamp for it is included in the log. The server will process the requests at a preset		rate using the rate limiting rules. If the number of new requests reaches the allowed number of requests, then all new		requests will be not be processed immediately but kept in the log until the server can process them. 

- Also if the total log size reaches a threshold, then the log cannot accept any new request.

- This algorithm is very accurate when it comes to rate limiting.
- The downside of this algorithm is that it consumes a lot of memory because the timestamp and request metadata will		need to be stored in a log until the request can be processed.

<br/>

- We can keep track of each requestID per userID, along with the request's timestamp in a Redis sorted set, as explained in the data model. The entry within this sorted set could look as follows:

```bash
{
  userID, requestID, timestamp
}
```

- Let's assume our rate limiter allows 3 requests per minute per user, so whenever a new request comes in, our rate limiter will perform the following steps:
  - Remove all the entries from the sorted set that are older than the currentTime - 1 minute
  - Count the total number of entries in the sorted set. We'll reject the request if this count is greater than the throttling limit of 3
  - Otherwise if the count of the entries is not greater than 3, we'll record it in the sorted set and accept the request

### Sliding window counter

- The sliding window counter algorithm is a hybrid approach of both the fixed window counter and sliding window log			algorithm. The algorithm can be implemented using a formula, which determines how many requests will be processed.		The algorithm is to the right in ‘Sliding window counter algorithm’.

- The sliding window counter algorithm is used to smooth out traffic using the formula. It is also memory efficient.

- The downside of this algorithm is that it depends on the formula, and the formula is an approximation of how many			requests will be processed. However, Cloudflare uses this algorithm and says it is 99.997% accurate.

Sliding window counter algorithm:

<img width="600" alt="image" src="https://github.com/user-attachments/assets/e2494e5c-910f-46ad-8e2d-97a009c0c6d2" />


## HLD

### Rate limiter middleware

- The rate limiter middleware will contain the rate limiting algorithm and will use the rate limiter cache to retrieve the			counter values for the request, and either approve or reject the request. If the request is approved, it will go to the API		servers

### Rate limiter cache

- The rate limiter counters and it’s associated metadata could be stored in a cache such as Redis or Memcached.	Redis may be preferred here if the rate limiting algorithm we're dealing with requires windows, where the windows would be sorted by time within a sorted set.

- If we’re using Redis, we could use the following commands to keep track of the counter:
  - INCR: Increases the stored request counter by 1
  - EXPIRE: Sets a timeout for the request counter. If the timeout expires, the counter is automatically deleted

### Rules database / cache

- The rules database will store the rules used by the rate limiter middleware and the algorithm. There will be different rules 	for different types of requests. For example, ‘a client can send 5 messages per minute’. As the rules will be relatively			simple, and can be referenced by some ruleID, we can use a KV store such as DynamoDB.

- The rules cache will store the rules in-memory, similar to the counter values. As the rules will be simple, but may need to		be retrieved frequently, a cache such as Memcached can be used which stores the entries as KV pairs where both the		key and value are strings

### Rate limiter headers

- The below rate limiter headers could also be used in the HTTP responses:
  - X-Ratelimit-Remaining (the remaining number of allowed requests within the window)
  - X-Ratelimit-Limit (the number of total requests the client can make within the window)
  - X-Ratelimit-Retry-After (the number of seconds to wait until you can make a request again without being throttled)


<img width="550" alt="image" src="https://github.com/user-attachments/assets/5d138206-bfc7-46c0-a02e-4f98bea64c24" />


## DD

Building a rate limiter in a distributed system has the following problems:

### Race condition on incrementing request counters can happen in a highly concurrent environment

- If two requests to the rate limiter middleware concurrently read the counter value, increment it by 1 and		write it back to the cache, then the request will only be updated by 1 instead of 2 (since there’s two requests	which incremented the counter) as shown to the right in ‘Race condition for two requests’
	
- To solve the issue of race condition, locks are the most obvious choice but locks will significantly slow down	the system

- An additional solution is to use lua scripts or sorted sets data structure in Redis can be used to fix the issue,	which will configure the rate limiter cache to contain the counter values and it’s operations in a sorted order

Race condition for two requests:

<img width="664" alt="image" src="https://github.com/user-attachments/assets/6ba2bfff-2ca3-4192-8e9f-b1ee93d682b6" />

<br/>

### Synchronization issue when clients send requests to different rate limiters for the same task

- When there are multiple rate limiter middleware servers being used, clients may send requests to different 	rate limiter servers, and there won’t be synchronization between the rate limiter servers to the clients.

- To solve the issue of synchronization, sticky sessions could be used on load balancers to route the client	requests to specific rate limiter servers (using the sticky sessions).

- A better approach to solve the issue of synchronization is to use a separate cache which contains the		mapping between the client to the rate limiter server (clientID : rateLimiterServerID). Since the data type is 	simple and may be accessed frequently, Memcached will be suitable here

- Sticky sessions, also known as session persistence or session affinity, is a feature that routes all requests	from a client to the same server for the duration of a user's session. This is done by assigning a unique		identifier to a user, usually through a cookie or IP address tracking. 

- Sticky sessions can be useful for stateful applications that need a consistent connection to the same server,	such as those that need to keep track of personalized user data like shopping cart items or chat 			conversations. Sticky sessions can improve user experience and optimize network resource usage.

- Sticky sessions can limit an application's scalability because the load balancer can't distribute the	load evenly. 

- Also, if the server goes down, the session is lost, which can be problematic if the session contains 	important user information. 

- If sticky sessions are based on IP addresses, attackers can hijack sessions through IP spoofing. To mitigate the risk of IP spoofing, you can use cookies or other methods of session persistence that are		harder to spoof.

### Updating the counter value each time for multiple requests may have latency issues

- When a request is made, the algorithm will first fetch the counter value and allow/reject the request, then it	will update the counter value in the cache. 

- The updating part is part of the client’s critical path and could cause latency issues. Therefore, the updates	for the counter values in the cache could be done asynchronously

<br/>
<br/>

Data and rate limiter sharding will also look as follows:

### Data and rate limiter sharding of rate limiter cache, Rules DB / cache and rate limiter middleware

- We can shard based on the userID to distribute the user's data. If we want to have different throttling limits for different APIs, we can choose to shard per userID per API. Take the example of 'URL Shortener'; we can have different rate limiters for createURL() and deleteURL() APIs.

- If our APIs are partitioned, a practical consideration could be to have a separate (somewhat smaller) rate limiter for each API shard as well. Let's take the example of our URL Shortener where we want to limit each user not to create more than 100 short URLs per hour. Assuming we are using sharding for our createURL() API servers, we can rate limit each shard to allow a user to create not more than three short URLs per minute in addition to 100 short URLs per hour.

### Should we rate limit by IP or by userID?

Let's discuss the pros and cons of using each one of these schemes:

#### IP

In this scheme, we throttle requests per-IP; although it’s not optimal in terms of differentiating between ‘good’ and ‘bad’ actors, it’s still better than not have rate limiting at all. The biggest problem with IP based throttling is when multiple users share a single public IP like in an internet cafe or smartphone users that are using the same gateway. One bad user can cause throttling to other users. Another issue could arise while caching IP-based limits, as there are a huge number of IPv6 addresses available to a hacker from even one computer, it's trivial to make a server run out of memory tracking IPv6 addresses!

#### User

Rate limiting can be done on APIs after user authentication. Once authenticated, the user will be provided with a token which the user will pass with each request. This will ensure that we will rate limit against a particular API that has a valid authentication token. But what if we have to rate limit on the login API itself? The weakness of this rate-limiting would be that a hacker can perform a denial of service attack against a user by entering wrong credentials up to the limit; after that the actual user will not be able to log-in.

#### Hybrid

How about if we combine the above two schemes?

A right approach could be to do both per-IP and per-user rate limiting, as they both have weaknesses when implemented alone, though, this will result in more cache entries with more details per entry, hence requiring more memory and storage.

<br/>

## Questions

<img width="749" alt="image" src="https://github.com/user-attachments/assets/f727b8f1-a1cf-4e2d-bd88-e598313a74c3" />

<img width="665" alt="image" src="https://github.com/user-attachments/assets/d9f512bd-6d68-4cf6-851a-2d3af317f03b" />

## Wrap up

- Multi-data center setup for rate limiters across different geographies
- Monitoring system to check if the rate limiter is effective
- Hard vs soft rate limiting vs elastic limiting
- Rate limiting on different OSI levels, HTTP, TCP / UDP, IP

- Data could be cached on the client side using Cache-Control to avoid making frequent API calls

- Exponential back-off could also be applied as clients keep requesting a specific endpoint
