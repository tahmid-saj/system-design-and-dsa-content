# Distributed cache

A distributed cache is a system that stores data as key-value pairs in memory across multiple machines in a network. Unlike single-node caches that are limited by the resources of one machine, distributed caches scale horizontally across many nodes to handle massive workloads. The cache cluster works together to partition and replicate data, ensuring high availability and fault tolerance when individual nodes fail.

## Requirements

### Questions

- Are we following any specific cache eviction policy?
  - Yes, lets follow the LRU eviction policy

- What other features should the cache have? Do we need expiration times (TTL)?
  - Yes, include TTL. Users should be able to set, get and delete KV pairs in the cache

- How much data are we storing in total in this distributed cache?
  - We need to store 1 TB of data in total, and handle a peak of up to 100k requests per second

- Should we prioritize availability over consistency? Does the data in the cache need to be highly consistent with the database?
  - Let's prioritize availability over consistency and follow an eventual consistency model

### Functional

- Users should be able to set, get and delete KV pairs
- Users should be able to configure the expiration time for KV pairs
- Data should be evicted according to LRU
- If data is not found in cache, data from database is returned

- 1 TB of data in total is being stored, and 100k requests per second should be served

### Non-functional

- Availability > consistency
- Low latency:
  - Low latency should be prioritized with responses in 10-100 ms for get and set requests
- Throughput:
  - The system should support 100k requests per second

## Caching 101

- A distributed cache is a caching system where multiple cache servers coordinate to store frequently accessed data
- Distributed caches are needed in environments where a single server isn’t enough to store all the data, as it may cause a SPOF. At the same time, it’s scalable and guarantees a higher degree of availability

- Caching can also happen at different layers of a system, where each layer may contain a different type of data in the cache:
  - Web:
	  - HTTP cache headers, key value stores within clients and CDNs may be used here to retrieve static web content and manage			sessions
  - Application:
	  - Server based and key value stores may be used here to retrieve results from computations and other data
  - Database:
	  - A database cache and key value store may be used here to reduce data retrieval latency and I/O load on the database
  - DNS and browsers:
	  - Caching is also performed at DNS and browsers

### Caching policies

In general, there is no optimal choice when it comes to writing policies, but it depends on the application and preference
- Write through: 	
  - The write through approach writes data to the database and cache. The writing on both storages can happen concurrently, or one		after the other. This will have strong consistency between the two storages but high latency.
- Write back: 
  - The write back approach writes data to the cache, then asynchronously to the database. This will have low latency but low			consistency if outdated data is read from the database before the data is asynchronously being written to the database from the cache.
- Write around: 
  - The write around approach writes data to the database, then if there is a cache miss, the data is written to the cache. This will have		low latency but low consistency as the cache will only have the updated data on a cache miss.
- Cache aside:
	- The cache aside approach loads data into a cache only when it’s requested rather than automatically writing it to the cache. When a		request comes in, the cache is first checked to see if the item is there or not, then it is retrieved from the database if the item was not in	the cache. If there is a cache miss, the item is stored in the cache from the database. This will have low latency, but may also have low	consistency. 
  - In cache-aside, the client moves the data to the cache as opposed to a read-through cache where the database or server moves the		data to the cache. 
- Read through:
	- A read through cache is where the cache is an intermediary between the client and database. The client first goes to the cache, and if	there is a cache miss, the data is retrieved from the database. The database or server loads the data into the cache. A read-through		cache also has low latency, but may have low consistency sometimes.
  - In cache-aside, the client moves the data to the cache as opposed to a read-through cache where the database or server moves the		data to the cache. 

### Eviction policies

MRU / MFU / LRU / LFU:
- MRU:
	- Stands for most recently used, and this policy prioritizes data that was accessed most recently. This means that the policy			evicts the most recently used data, and this policy is often used to evict very dynamically changing data.
- MFU:
	- Stands for most frequently used, and this policy prioritizes data that is accessed most often. This means that the policy evicts			the most frequently used data, and this policy is used to evict very dynamically changing data.

### Cache invalidation

We can maintain cache invalidation by:
- Active expiration: 
  - Active expiration actively checks the TTL of cache entries through a daemon process or thread
- Passive expiration: 
  - Passive expiration checks the TTL of a cache entry at the time of access

### Hash function

We can use hashing in two different scenarios of a distributed cache:
- Identifying the cache server in a distributed cache to store and retrieve data:
	- In this scenario, we can use different hashing algorithms or consistent hashing as it performs better in distributed systems when		scaling multiple servers. The cache client can use consistent hashing to identify the correct cache server to forward the request to
- Locating cache entries inside each cache server:
	- In this scenario, we can use typical hash functions to locate a cache entry in a cache server. However, we’ll also need a data structure	to manage the data in the cache server once we know where the cache entry is inside the server.

### Doubly linked list

The data structure we’ll use to store the data is a double linked list to add and remove data from the linked list when we’re performing cache eviction

### Cache client

- There will be separate hosting servers containing cache clients, which will perform the hash computations to store and retrieve data from the cache servers. Also cache clients may perform other tasks such as monitoring and configuration of the cache servers.
- All cache clients will also need to be programmed so that the same PUT or GET operations from different clients return the same results.
- Each cache client will know about all the cache servers and will use lightweight protocols such as TCP or UDP to communicate with the cache servers

## Data model / entities

- The core entities are very simple, we are building a cache to store KV pairs: we need keys (likely a string) which are mapped to a value (could be different data types from int / string / boolean / list / set / map / etc). We'll also store the expirationTime for TTLs.

```bash
key: { value, expirationTime }
```

## API design

### Inserting a KV pair

Request:
```bash
POST /entry
{
  key
  value
  expirationTime
}
```

### Getting a KV pair

Request:
```bash
GET /entry/:key
```

Response:
```bash
{
  value
}
```

### Deleting a KV pair

Request:
```bash
DELETE /entry/:key
```

## HLD

### Implementation

- To first sketch out some pseudocode for the cache, we might have the below. This code will likely be maintained in the cache servers which will perform operations on the in-memory storage.

#### Expiration time

- We'll need to also store an expiration timestamp in each KV pair, and check it during reads to clean up expired entries. This will allow us to support TTLs.
- Even if we delete expired KV pairs only during reads, the cache can still fill up with expired entries and cause storage issues. We'll also need a background process (called a janitor) that periodically scans for and removes expired entries. The cleanup function will run every N mins or so to remove expired KV pairs OR when the storage in the cache hits a certain threshold, and expired entries need to be removed.

#### LRU eviction

- A LRU policy is typically implemented using a hash map (which contains KV pairs of the key to the node in a DLL) and a DLL (containing nodes with the key, value and expiration timestamps). The nodes in the DLL maintain access order, where the most recently used node is at the head, and least recently used node is at the tail. This allows us to perform the get, set and delete operations in O(1) time.

##### Setting an item

1. To set an item, we'll first check if the item already exists. If the item exists, we'll update the node and hash map's value and expiryTime. If the item doesn't exist, we'll create a DLL node containing the key, value and expiration timestamp
2. We'll then add the KV pair (key, node's reference) to the hash map
3. We'll insert the node at the head of the DLL
4. If we're at the capacity, we'll remove the least recently used node in the DLL (at the tail) and also remove the corresponding KV pair from the hash map

##### Getting an item

1. Get the node for the key via the hash map O(1)
2. Check if the node expired or not - if the node expired, we'll have to delete it and end the operation.
3. Remove the node from it's current position O(1)
4. Move the node to the head of the list O(1)
5. Return the node's value

##### Deleting an item

1. Get the node for the key via the hash map O(1)
2. Remove and delete the node from it's current position, and delete the KV pair from the hash map O(1)

```python
class Node # Node in our DLL storing (key, val, expiryTime, next, prev)

class DLL # DLL containing the nodes, size, head, tail

class Cache:
	def __init__(self, capacity):
		self.lruCache = {}
		self.capacity = capacity

	def get(self, key):
		node = self.lruCache[key]

		# check if the node expired or not
		if node.expiryTime and time.now() > node.expiryTime:
			self.delete(key)
			return null

		DLL.moveToHead(node)
		return node.val

	def set(self, key, val, ttl):
		expiryTime = time.now() + ttl if ttl else null

		if key in lruCache:
			# update the expiryTime if TTL is provided
			node = lruCache[key]
			node.val = val
			node.expiryTime = expiryTime
			DLL.moveToHead(node)
		else:
			node = Node(key, val, expiryTime)
			self.lruCache[key] = node
			DLL.addNodeToHead(node)

			if DLL.size > self.capacity:
				delNode = DLL.tail.prev
				self.delete(delNode.key)

	def delete(self, key):
		del self.lruCache[key]
		DLL.deleteNode(node)

	def cleanup(self):
		expiredKeys = []

		# scan from the DLL's tail and towards head, removing expired nodes
		curr = DLL.tail.prev
		while curr != DLL.head:
			if curr.expiryTime and time.now() > curr.expiryTime: expiredKeys.append(curr.key)
			curr = curr.prev

		# remove the nodes appended to expiredKeys
		for key in expiredKeys:
			node = self.lruCache[key]
			self.delete(node.key)
```

**Note that the code is only to show clarity for the implementation - however multiple additional things need to be handled such as thread safety, error handling, monitoring capacity, performance optimizations, etc**

The code below is for a LFU cache:

```py
from collections import OrderedDict, defaultdict

class Node:
    def __init__(self, key=None, val=None):
        self.key = key
        self.val = val
        self.freq = 1
        self.next = self.prev = None

class DLL:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0
    
    def __len__(self):
        return self.size
    
    def add(self, node):
        nextNode = self.head.next
        node.prev = self.head
        node.next = nextNode
        self.head.next = node
        nextNode.prev = node

        self.size += 1
    
    def remove(self, node):
        if self.size == 0: return
        prevNode = node.prev
        nextNode = node.next
        prevNode.next = nextNode
        nextNode.prev = prevNode
        node.next = node.prev = None

        self.size -= 1
        return node

class LFUCache:
    def __init__(self, capacity: int):
        # Manual DLL approach
        self.freq = defaultdict(DLL)
        self.lfu = {}
        self.capacity = capacity
        self.minFreq = 0

        # OrderedDict approach
        # self.cache = {}
        # self.frequencies = defaultdict(OrderedDict)
        # self.minf = 0
        # self.capacity = capacity

    # OrderedDict approach
    # def insert(self, key, frequency, value):
    #     # Manual DLL
    #     self.cache[key] = (frequency, value)
    #     self.frequencies[frequency][key] = value

    def get(self, key: int) -> int:
        # Manual DLL approach
        if key not in self.lfu: return -1

        node = self.lfu[key]
        self.freq[node.freq].remove(node)

        if len(self.freq[node.freq]) == 0: 
            self.freq.pop(node.freq)
            # The DLL needs to be deleted if it's size is 0. If the freq of the DLL is equal to the minFreq, 
            # then we need to increase minFreq by 1 since freq == minFreq (and we're performing a get operation, so we increase the freq by 1)
            if node.freq == self.minFreq: self.minFreq += 1

        node.freq += 1
        self.freq[node.freq].add(node)
        return node.val

        # OrderedDict approach
        # if key not in self.cache: return -1
        # frequency, value = self.cache[key]
        # del self.frequencies[frequency][key]

        # if not self.frequencies[frequency]:
        #     del self.frequencies[frequency]
        #     if frequency == self.minf: self.minf += 1

        # self.insert(key, frequency + 1, value)

        # return value

    def put(self, key: int, value: int) -> None:
        # Manual DLL approach
        if self.capacity == 0: return
        if key in self.lfu:
            self.lfu[key].val = value
            self.get(key)
            return
        
        if len(self.lfu) == self.capacity:
            dll = self.freq[self.minFreq]
            toDelete = self.freq[self.minFreq].remove(dll.tail.prev)
            self.lfu.pop(toDelete.key)
            del toDelete
        
        node = Node(key, value)
        self.lfu[key] = node
        self.freq[1].add(node)
        self.minFreq = 1

        # OrderedDict approach
        # if self.capacity <= 0: return
        # if key in self.cache:
        #     frequency = self.cache[key][0]
        #     self.cache[key] = (frequency, value)
        #     self.get(key)
        #     return

        # if self.capacity == len(self.cache):
        #     key_to_delete, frequency = self.frequencies[self.minf].popitem(last=False)
        #     del self.cache[key_to_delete]

        # self.minf = 1
        # self.insert(key, 1, value)

# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```

### Hash function

We can perform one of the below types of hash operations to find the cache server containing a specific key:
- Simple hash function + mod to locate the cache server for the cache entry using the key: hash(Key) mod (# of servers). Simple hash		function will not perform well when scaling cache servers
- Consistent hashing, where the cache entry (key) will be hashed to a hash ring. This approach will perform better when scaling cache		servers.

### Data structure

We'll also use both a hash map and DLL as our data structures:
- A hash map can store references to nodes in a doubly linked list, which contains the KV pairs. Hash maps will contain the		mapping of key : reference of node in DLL. The nodes in the DLL will be ordered depending on the eviction policy.
- We’ll need a data structure such as a doubly linked list to perform a cache eviction

- Bloom filter (https://www.youtube.com/watch?v=V3pzxngeLqw). We could also use a bloom filter to check if a cache entry is definitely not		present in the cache server, but the possibility of its presence is	probabilistic

### Cache client

-A cache client is different from a frontend client in this design. Other apps, which could also be frontends will request this cache client to initiate requests on the cache servers. The cache client is a library that initiates the API operations. It will perform hash computations to store and retrieve data from the cache servers. The cache clients may also be located very close to the cache servers to reduce latency in network requests.
- To further meet the latency requirements, the cache client can initiate API calls to the cache servers via potentially TCP / UDP which is lightweight and faster than HTTP
- The cache client will also perform eviction via a policy such as LRU, and cache invalidation using active/passive expiration with TTL  on	the cache servers

### Cache servers

- The cache servers maintain the cache of the data using both a hash map and DLL. Each cache server will be	 accessible by all the		cache clients, and if any cache server is down, then requests to those servers will be resolved as a cache miss and may be routed to the DB instead by either the cache client, or the originator of the request (possibly a frontend client or another server)

<img width="562" alt="image" src="https://github.com/user-attachments/assets/389bdb48-2049-4ec8-ad0e-425b932beae9" />

## DD

### The high level design doesn’t highlight the internals of the cache servers, thus the internals of the cache servers are as follows:

- Hash map:
  - A simple cache server will build a hash map to store keys and their locations in the doubly linked list in the RAM of		the cache server
- DLL:
  - To perform cache eviction, we’ll store cache entries in a doubly linked list in the cache server’s RAM
- Eviction policy:
  - The eviction policy such as LRU depends on the application and preference. The cache servers will have rules			associated to the eviction policy
  - The LRU eviction policy also performs the set, get and delete operations in O(1) time.

<img width="517" alt="image" src="https://github.com/user-attachments/assets/92a765c4-e455-4b1b-988e-eb005355b627" />

There are some limitations with the high level design:

### Cache clients have no way of knowing when cache servers are added or down

- We can try 3 things:
  - We can maintain a config file in each cache client, that contains the updated health and metadata of the cache servers:
    - We’ll maintain a config file in each cache client, however, this will have consistency issues in updating all the config			files for all the cache clients via some DevOps tool.

  - We can maintain a config file of the cache server health and metadata in a centralized location. However, the config file will be a SPOF.

  - An automatic way of monitoring the health of cache servers is to use a configuration service that continuously 			monitors the cache servers and ensures that the cache clients see an updated view of the state of cache servers.
    - We can use a configuration service that continuously monitors the cache servers, and will notify the cache clients		when cache servers are added or down. Using this approach, the cache client can be stateless. This approach may be	more 	complex but tackles the main issue of the cache clients not knowing when cache servers are added or down. This configuration service may be a SPOF, however, just like with load balancers having a clone, this configuration service could maintain an operation log which appends the scaling and additional operations made on the cache servers. This operation log could be replicated to a clone configuration service, which can takeover in case the main configuration service is down.

### We have a SPOF in the cache servers since one cache server maintains a set of cached data

- To solve this issue, we can apply sharding (to prevent the hot-key problem for a single node) and replicate nodes of cache	servers, where there will be:
  - Primary-secondary replicas if writing and reading ratios are relatively equal. Leader election will be coordinated by			the secondary nodes
  - Multiple primary replicas if there is write intensity
  - All leaderless replicas if there is read intensity

- If we choose to have geo-replication, we can synchronously replicate within the data center and asynchronously replicate	outside the data center
- For inconsistency resolution, we could also use a quorum based approach and vector clocks / versioning of cache entries

### Handling hot keys being read / written to a lot

**Approaches to handling hot keys are frequently asked in a SDI**

- There are two types of hot keys we need to handle:
  - Hot reads:
    - Hot reads are keys that receive an extremely high volume of read requests, like a tweet's data that millions of users are trying to view concurrently
  - Hot writes:
    - Hot writes are keys that receive many concurrent write requests, like a counter tracking real-time votes.

- Hot reads can be handled using the below approaches, and in 'Handling hot reads':
  - Vertical scaling all nodes
  - Dedicated hot key cache
  - Read replicas
  - Copies of hot keys
 
Handling hot reads:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/8d71e4a6-7437-490f-a983-b802d922296c" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/ec1f7ccf-ea31-44f6-830b-b51e0a26e508" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/64c943bd-df02-4c6c-8227-7614988342f4" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/ed1fe54f-5d49-475f-93c7-ab060d7a10c6" />
<img width="700" alt="image" src="https://github.com/user-attachments/assets/599991d9-5e78-44c5-bd21-c25b6559738c" />

- Hot writes are a bit more complex, but can be handled using the below approaches, and in 'Handling hot writes':
  - Write batching:
    - Batch writes will mainly be implemented via the client side, where the client will batch updates for multiple cache entries before writing the finalized batch update to the cache servers. Write batching also helps by reducing the number of network trips which needs to be made. A single batched network request can be made for compiled requests.
  - Sharding hot key with suffixes

Handling hot writes:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/083f5623-1786-49f2-a867-1c4fe392fc59" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/3416f4ee-932c-42ee-95ed-d317700299ee" />

### Connection pooling to reduce repeated establishing of network connections

- Constantly establishing and closing connections between the client and cache servers can be reduced if requests can happen within one single connection. This will also prevent bandwidth usage on both the client and server, since they don't have to open a new connection everytime or perform a handshake. Connection pooling can be implemented in the below ways:
  - Hanging GET (long polling):
    - A connection remains open for a long time, waiting for the server to send data as it becomes available. The client will send a GET request to the server. The server will delay it's response until new data becomes available or a timeout occurs. After receiving the response, the client could immediately re-establish the connection. However, it can lead to scalability issues if multiple clients establish long-lived connections.
  - Persistent connection pooling (HTTP Keep-Alive):
    - A single connection can be reused for multiple requests instead of being closed after each one. A client will first establish an HTTP connection with the server using the Connection: keep-alive header. The same connection will be reused for subsequent requests until a timeout or Connection: close is received by the client / server. This will further reduce making multiple TCP handshakes for each request.
  - Multiplexed connections (HTTP/2.0 and gRPC):
    - A single connection can handle multiple streams of requests and responses concurrently using multiplexing via HTTP/2.0. Using multiplexing, a single TCP connection will be shared by multiple logical streams. Each stream will be independent, preventing blocking. Multiplexing will reduce the number of connections opened, and can also be implemented via gRPC.
  - Websockets:
    - WebSocket connections will provide bidirectional communication - thus multiple requests and responses can be sent from the client / server at the same time in a single TCP connection.
  - Queue-based connection pooling:
    - In queue-based connection polling, requests will be queued if all connections in the pool are in use. This can be implemented mainly in the client side. When some connections can be opened or are not in use, requests can be dequeued and assigned to the available connections. However, queue-based connection pooling may be complex to implement since both the queue and monitoring of the available connections now need to be implemented.	
  - Lazy connection initialization:
    - In lazy connection initialization, connections will be created only when they are needed, rather than pre-allocated.

- Overall connection pooling can reduce the number of network requests being made, which will usually take the most time for requests within a distributed system. It's also important to specify connection limits (so that there is enough bandwidth on the cache servers), timeouts (in case some requests may take too long), retry logic (requests can instead be retried via exponential backoff), etc.

### Ensuring an even distribution of keys across cache servers

- We can use consistent hashing to distribute keys across the cache nodes / servers. This will help prevent the number of keys which need to be remapped when nodes / servers are added or removed. We can use a consistent hashing function like MurmurHash to get a hashed value in the hash ring for a key. We can move clockwise in the hash ring, until we find the first node (or N virtual nodes if using virtual nodes) to store the KV pair on.
- Consistent hashing also helps reduce latency because requests will not need to query a centralized routing service (such as ZooKeeper) to find out which node has which key.

**Note that while consistent hashing may seem to be suitable for most stateless components, maintaining the correct distribution within stateful components (such as databases, websockets, etc) using consistent hashing usually has some overhead as explained below:**

- When requests for the key comes in, we'll likewise hash the request's key onto the hash ring, then find the first node clockwise - this node should contain the KV pair for the request key since we're using consistent hashing. However, when scaling events occur, the keys will need to be remapped to the appropriate cache servers - this will cause some overhead if using consistent hashing - however, it is still much more efficient than remapping all the keys via the mod operation approach.
- Adding and removing servers may also happen frequently within cache servers, where the stored data may be frequently changing depending on the TTL, hotspots, eviction policy, etc, which will have some overhead if using consistent hashing.

### Ensuring the cache is highly available and fault tolerant

- To ensure the cache is highly available and fault tolerant, we'll need to replicate the copies of the cache across multiple servers. We can try the below or in 'Ensuring the cache is highly available and fault tolerant':
  - Synchronous replication
  - Asynchronous replication
  - Peer-to-peer replication

- All of the above approaches could still work well depending on the use cases. Redis, for example uses asynchronous replication by default, but it also provides a WAIT command that allows clients to wait for a replica acknowledgement if needed (sometimes called "semi-synchronous" behavior). Other distributed tools also allow you to configure the replication type in order to choose the right trade-offs for your workload.
- Because low latency responses are a top priority in a cache, asynchronous replication for a good balance of availability and simplicity + peer-to-peer replication for maximum scalability are two good choices for this design.

Ensuring the cache is highly available and fault tolerant:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/3594418c-e44d-4e51-a5f8-1e3ab6038304" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/982d360c-8c82-4be4-9736-86c2f0b86f29" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/3dc0cd59-f794-4f49-9e4e-463531017532" />

### Ensuring the cache is scalable

- We can't fit 1 TB of data efficiently on a single server without hitting memory and performance limits. We can shard the KV pairs across multiple nodes, where each node would contain an even portion of KV pairs. This will also allow us to prevent hotspots on a single server.
- A typical server and (medium to higher end - ie AWS's r6g.8xlarge EC2 instance with 256 GB of memory) EC2 instance should be able to handle 20K requests per second. If we have 100K requests per second in total, we would need 5 servers to handle this throughput. By accounting for spikes, we might need 8 servers or so.
- A typical memory optimized EC2 instance with 256 GB RAM can use 200 GB to cache data after subtracting the RAM needed for system overhead. If we need to store 1 TB of data in the cache, we would need 1024 GB / 200 GB = 6 EC2 instances just for storage alone. By accounting for spikes in the data growth, we might need 8 instances or so.

**The actual numbers and estimations would vary based on factors including the choice of instance types, the average size of cached values, read / write ratio, replication requirements (how many nodes to replicate to), and the expected growth rate. For now, we can say we'll need 8 or so memory optimized EC2 instances**

<img width="600" alt="image" src="https://github.com/user-attachments/assets/88250295-7924-4bdc-9998-36f1bde70c02" />

### Questions

Q: Assume that a large number of concurrent requests are forwarded to a single shard server. If the server uses the LRU algorithm, some of the requests will result in a cache miss and write a new entry to the cache, while some will result in a cache hit and end up reading from the server. These concurrent requests may compete with each other. Therefore, some locking mechanisms may be required. However, locking an entire data structure for all the reading and writing operations will heavily reduce the performance. How can you solve such a problem?

A: Generally, for concurrent access to shared data, some locking mechanisms like Semaphore, Monitors, Mutex locks, and others are good choices. But as the number of users (readers in case of cache hit or writers in case of a cache miss) grows, locking the entire data structure isn’t a suitable solution. In that case, we can consider the following options: 

- Limited locking:
  - In this strategy, only specific sections of the entire data structure will be locked. While some threads or processes can read from the data structure simultaneously, some threads may temporarily block access to specific sections of the data structure. 

- Offline eviction: 
  - Offline eviction may be a possibility where instead of making actual changes to the data structure, only the required changes will be recorded while performing different operations until it’s necessary to commit the changes. This solution is desirable and easy if the cache hit rate is high because a change to the data structure will likely be required when a cache miss occurs. 

- Vector clocks / versioning and quorum based approach:: 
  - Vector clocks and versioning, and a quorum based approach can be used if working with sharded cache servers.

### Wrap up

- If a cache server is down during a write operation, and a read operation is performed just after the cache server recovered, then we need to not allow the cache server to serve requests until it’s updated via the configuration service

- If a leader node (replica) in a cache server is down, we can use a leader election algorithm within the replicas to elect a new leader OR we can use a separate cluster management service to monitor and select leaders which may be more complex to implement

- Add geo-replication of cache servers for high availability
	- This will provide higher availability but lower consistency


