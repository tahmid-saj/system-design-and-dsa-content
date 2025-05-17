# Top K YouTube videos

## Requirements

This system is also called a heavy-hitters problem.

Let's assume we have a very large stream of views on YouTube (our stream is a firehose of videoIDs and their viewCounts). At any given moment we'd like to be able to query, precisely, the top K most viewed videos for a given time period (say 1 hour, 1 day, 1 month, all time) together with their counts.

The word precisely here has dramatic implications on this problem. It's a bit unrealistic for most applications, but an approximate solution leans heavily into probabilistic/approximate solutions which, for many roles, rely on esoteric knowledge of e.g. count-min sketch. Except in specialist situations, most reasonable interviewers are going to test general knowledge rather than something you'd learn on the job after reading some papers.

### Questions

- Are we designing the overall data structure / solution which will return the top K videos?
  - For the data structure - it should be designed using distributed system components. We don’t have to		explicitly design the entire data structure, but cover the main parts.

- What is the delay we can expect when querying for the top K videos?
  - 10’s of millisecs (10 - 300 ms)

- Should we support data range queries as well, or only support queries where the starting time is the current timestamp?
  - We’ll assume that all queries are looking back starting from the current timestamp

- Is there a limit on the K value?
  - 1000

### Functional

- Let’s assume we have a very large stream of views on YouTube (our stream is a firehose of videoIDs and their viewCounts). At any given moment, we’d like to be able to query precisely the top K most viewed videos for a given time period (let’s say 1 hr, 1 day, 1 month, all time) together with their counts

- Clients should be able to query the top K videos (max 1000) for a given time period:
  - Time periods should be limited to 1 hr, 1 day, 1 month and all time
  - We’ll assume that all queries are looking back starting from the current timestamp
  
- We should choose between different window types, ie: tumbling window vs sliding window for tracking the view counts for different time windows

<br/>

- YouTube shorts had 70M views per day and approx 1 hr of content uploaded per second

### Non-functional

- Low latency:
  - We’ll tolerate at most 1 min delay between when a view occurs and when it should be tabulated
  - Query results should be returned within 10’s of millisecs (10 - 300 ms)
- Throughput:
  - We will have a massive amount view events for both view events (700k / sec of view events) and videos (4B videos)
- Data accuracy:
  - Our results should be precise, so we should not approximate

**Having quantities on your non-functional requirements will help you make decisions during your design. Note here that a system returning within 10's of milliseconds eliminates many candidates from the solution space - we'll need to favor precomputation.**

## Estimations

We'll look at the number of views per second, then the storage needed for all the videoIDs:

<br/>

We’ll first look at throughput of views per second:
  - (70B views / day) / (100k seconds / day) = 700k views / sec
  - This is a lot of throughput, and thus we’ll need to look for ways to shard the view counts across many hosts

We’ll now look at the storage needed to hold the counts:
  - Videos / day = ( 1 hr of content uploaded / second ) / ( 6 min of content on average / video ) * (100k seconds / day) = 1M videos / day
  - Total videos = 1M videos / day * 365 days / year * 10 years = 3.6B videos

  - 4B videos * (8 bytes / videoID + 8 bytes / videoViewCount) = 64 GB

  - Since the values of the videoID and counts are relatively simple and small, we can keep it in-memory with appropriate replication

## Top K YouTube videos 101

- We’ll need to fetch data from a very high throughput volume stream. Most quantities will need to be precomputed in order to meet the latency requirements of returning the results - such as precomputing the top K values within a heap
  
- We’ll have different viewCounts for videoIDs, different view events coming in, and different time windows. Thus, we’ll have the entities:
  - Video views
  - View event
  - Time window


## Data model / entities

- Video views:
  - This entity could likely be maintained in a database and the top K results could be maintained separately in a heap

	- videoID
	- viewCount

- View event:
  - This entity will likely come from a view stream source such as Kafka, which will send how much the viewCount field		in the Video entity should be incremented for a specific videoID, whenever clients view a video

	- videoID
	- viewIncrementValue

- Time window:
  - This may not be an explicit entry we need to maintain in a database, however clients will still request the system		with a time window entity similar to an enum (1 hr, 1 day, 1 month, all-time).


## API design

### Get top K videos

- This endpoint will retrieve the top K videos using K and the time window

Request:
```bash
GET /video-views?k&window={ 1 hr, 1 day, 1 month, all-time }
```

Response:
```bash
{
  videoViews: [ { videoID, viewCount } ]
}
```

## HLD

### Handling query for view counts of all-time

To handle the query for getting the viewCounts of all-time, we'll first go over a basic solution, then look into improving it:

#### Basic solution

- To store the videoIDs and viewCounts for the "all-time" case, we can maintain a table which contains these values,		however iterating	 through all the 4B rows of videoIDs to find the top K viewCounts on every query is not efficient, thus we can			instead maintain a heap of the top K videos which we can update if the smallest viewCount in the heap is smaller		than an updated viewCount from a view event (similar to how we update a heap in code). Majority of the view counts will never reach		this heap since only the top 1000 (the max K value) will be stored in the heap.

- To store the viewCounts of a videoID, we can store the data within a KV store such as DynamoDB which operates		similar to a hash table. This will allow us to increment the viewCount for a videoID, when view events come in for a specific videoID. When a user views a video, the view events will likely come from a source		such as Kafka or another queue which is used to forward millions of viewIncrementValues for videoIDs asynchronously to the KV		store.

- When a viewCount increment request comes in from the view stream (Kafka), there will be Counter servers which		will consist of the KV store, heap, and workers. The workers which will increment the videoID's viewCount in the KV store, then we’ll test the incremented viewCount against the minimum viewCount in our max heap. If the incremented viewCount is higher than our minimum viewCount in the heap (the incremented viewCount belongs in the top K max heap), then we’ll insert the			videoID and it’s viewCount into the heap and heapify. The clients will query directly from the heap to retrieve the top		K videos. Note that if we need to return the top K for all-time, we’ll just return all the top K entries in the heap

- The Basic solution above is simple and operates within a single server, but it doesn’t consider supporting a high throughput when we’ll have 700k		view events / sec	for which we increment the view counts in the KV store, and update the heap. The KV store won't be able to handle 700k writes per second - on average a DynamoDB instance can handle 40k writes and reads per second.

#### Improving the Basic solution’s fault tolerance

- Fault tolerance is one of the things we need to improve on in this basic solution. We can improve on the fault			tolerance by using following and in ‘Basic solution fault tolerance improvements’:
  - Writing view counts and heap to a database
  - Maintain replicas of the Counter servers which contains the KV store, heap, and workers which updates the			KV store and heap
  - Maintain replicas of the Counter servers (containing KV store, heap, workers), and also maintain snapshots			of the operations performed and state of the server’s components in a blob store

<br/>

Basic solution fault tolerance improvements:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/f3438399-0088-4775-ab8a-aa286488c5a9" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/539a67ac-d5e0-4cf7-8484-24e3a88f499a" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/f86b57b0-5199-4187-9455-e3f0f533a23b" />

#### Improving the Basic solution’s write throughput

- The write throughput is another thing we need to improve on in the basic solution. A primary node (primary node only accepts writes) of the replicas themselves without sharding / partitioning won't be able to handle as much of the write throughput in a single KV store or heap. Thus, we’ll need sharding / partitioning of the replica’s components to handle the write throughput, as shown below and in		‘Basic solution write throughput improvements’:
  - Fixed partitioning by ID
  - Elastic partitioning
  - Note that we don’t necessarily need to shard / partition the top K heap, as we’re only storing 1000 entries at			maximum, thus the value is not large enough where sharding / partitioning is needed

<br/>

Basic solution write throughput improvements:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/46d39d5c-c9d4-41a9-86d4-5b62c07f2dcd" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/ce6c6124-4a4e-4354-a5f6-022815c48ec5" />

### Counter servers
  
- The counter servers will contain the KV store, heap and a set of workers (containers) which will retrieve view count increment		events from the view stream (Kafka). The counter servers will likely can be an IO or memory optimized EC2 instance, since the workers in the Counter servers will frequently make requests to the KV store, heap and Kafka.
- When view events come in from Kafka, the workers will retrieve them and aggregate the viewCounts for videoIDs, then update the videoIDs' viewCounts in the KV store, and also update the heap.

### KV store / cache

- The KV store will contain the videoID and it’s viewCount as a KV pair. However, updating the values in a database		will likely be very slow. Thus, a cache such using either Redis or Memcached could be used to store the videoIDs and			viewCounts of the KV store. The videoIDs and viewCounts could also be updated to the KV store asynchronously after it is first updated in the cache.

- We’ll use Redis since single-threaded operations within a Redis instance will lead to very rare race conditions - writes are atomic. However, race conditions are		still possible in Redis when multiple clients / workers update the same videoID, thus locking via a Redis distributed lock could		be used when updating viewCounts of videoIDs in the cache. Additionally, Redis will provide pipelining which will further speed up write operations. 

### Heap data structure

- The heap data structure will maintain the top K viewCounts using a Redis top K data structure. A Redis top K		data structure will work out of the box for this design, since it provides specific commands to find if a key is in the heap, and it can list		all the items in the heap which will be used for viewing the all-time viewCounts, etc.

### Top K API servers

- The Top K API servers will handle requests for the top K viewCounts for different time windows. These servers will		handle the API endpoint for getting the top K viewCounts.

### ZooKeeper
  
- Because we’ll have shards / partitions of the components in the Counter servers, we could maintain the info in a		service such as ZooKeeper, where the mapping of the videoID : shardID is maintained. Thus, the workers within the		Counter servers could use ZooKeeper to lookup the shardID for a videoID when view stream events come in and the workers need to update a specific shard of the KV store / cache

## DD

### Handling query for view counts for different time windows

- The solution for handling queries for all-time can directly fetch the full heap to get the viewCounts, however to handle		different time windows, we need to remove viewCounts which happened outside of the specified time window. For example, if a		view happened at 2010-01-01, and our time window is for a single day, then we’ll need to remove that view for			2010-01-01 from the time window.
	
- To handle these different time windows (1 hr, 1 day, 1 month), we can do the below and in ‘Handling time windows’:
  - Naive micro-buckets
  - Heap expirations
  - Use two pointers

<br/>

Handling time windows:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/d9c97bc6-d31a-4595-90ce-de44d0cff70b" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/3f5bdf54-ad6d-4f33-9c0d-09ca410b8549" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/9acfa7a3-c143-430c-82dc-95b178953113" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/6846e139-ea40-4952-8fa3-75a5da69965b" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/deb5acdb-94e0-432f-a235-c42d789e9f97" />

### Handling large number of query requests with a top K cache

- As we’ll likely have a large number of top K read requests, we can use a cache such as Memcached to store the		top K query results for a videoID and time window, and set a TTL of 1 min for the cached entry. It’ll take 1 min for a		view to happen, then be recorded in the KV store, thus we’ll set the TTL to 1 min so that the cache will never have stale entries. An entry in the cache might look like:

```bash
{
  videoID
  viewCount
  timeWindow: 1DAY
}
```

- When query requests come to the Top K API servers, they could be queried from the top K cache OR from the top		K heap within the Counter servers if there is a cache miss.

![image](https://github.com/user-attachments/assets/63400690-e22f-4179-a427-d70443ccdc90)

<img width="800" alt="image" src="https://github.com/user-attachments/assets/d7e46ee1-8ffa-42e1-9bf6-e5ff446c050f" />

