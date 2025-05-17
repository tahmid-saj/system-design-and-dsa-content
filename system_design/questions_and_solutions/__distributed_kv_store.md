# Distributed key value store

## Requirements

### Questions
- Do we want to prioritize consistency or availability?
  - Try to prioritize both

### Functional

- The storage contains key-value pairs where:
  - Keys are strings
  - Values are strings, int, lists, objects etc

- It can store frequently used data like session info
- It may provide data compression
- It should be a configurable service:
  - We can tune trade-offs between:
    - Availability
    - Consistency
    - Low latency

- We should use encryption for the data stored

### Non-functional

- Availability
  - Fault and update domains can be used
  - The system should respond, even during failures
- Scalability
  - We want the ability to add and remove servers, and	be able to handle a large number of users
- Tunable consistency
  - We can use a quorum based approach for a tunable	consistency
- Low latency

## API design

### Putting a data entry

- Note that the API servers will keep a hash of the value + key in the metadata for any data integrity checks and		ensuring the entry for the key is idempotent. Additionally, the key can also be hashed prior to storing and look-ups in		the storage servers. 
- DynamoDB uses MD5 hash on the key to generate a unique 128-bit identifier, to uniquely identify the keys in the		storage servers.

Request:
```bash
POST /entry
{
  key
  value
  metadata: { valueVersion }
}
```

### Getting a data entry

Request:
```bash
GET /entry/:key
```

Response:
```bash
{
  value
  metadata: { valueVersion }
}
```

### Deleting a data entry

Request:
```bash
DELETE /entry/:key
```

Response:
```bash
{
  value
  metadata: { valueVersion }
}
```

## HLD - KV store 101

- Developing a KV store in a single server is easy, and this is similar to a hash table which keeps everything in memory. However, storing everything in memory may be impossible due to the space constraint, therefore we could store only frequently accessed data in memory, and the rest in disk. Even with this approach, a distributed key value store is needed because a single server can reach it’s capacity quickly.

- The content below is based on the popular KV stores: DynamoDB, Cassandra and BigTable

### Data partitioning

- We can partition the key-value pairs based on the hashed value of the key. DynamoDB uses MD5 hash to hash the	key and generate a 128-bit identifier to uniquely identify the key.

### Consistent hashing

- In consistent hashing, we have a hash ring containing hashed values referencing the servers by taking a unique 		identifier for the server, such as serverID and applying a hash function on it. When a request comes in, the key for the	request is hashed, and then mapped to the hash ring. The next server we encounter in the hash ring going clockwise	from the hashed request will serve the request. Using consistent hashing, it’s easy to scale servers and evenly			distribute requests across servers.

- Consistent hashing using virtual nodes can provide scaling and replication, and tackle the issue where there are hot	spots in the hash ring. Using virtual nodes, instead of having one hash function, we’ll use multiple hash functions on		the same server’s unique identifier and map the hashed value to the hash ring. When a request comes in, we apply a	hash function on the key of the request, and map it to the hash ring. The closest virtual node going clockwise from the	hashed key of the request will serve the request. Virtual nodes ensure the requests are distributed evenly, and if a 		server can handle more requests, it may have more virtual nodes.

### Consistent hashing with replication (databases)

- If the database is using consistent hashing, to replicate the data, we can map the data record’s key to the hash ring,	then we can find the first N (usually 3) nodes to replicate the data to by going clockwise from the data record’s key		position in the hash ring. This is further shown to the right in ‘Data replication using consistent hashing’.

- If the database is using consistent hashing with virtual nodes, to replicate the data, we can choose the first N distinct	nodes, where the nodes or virtual nodes we choose do not reference the same node.

- Using a primary-secondary replication approach, we can only write from the primary node. 

- If a primary node fails, during the time that a secondary node will be elected as the primary node, we won’t be able		to perform writes as there won’t be a primary node to handle the writes for us
	
- Using a peer-to-peer replication approach (leaderless approach), we can achieve high availability (to always write		and read), but will have low consistency as there may be data inconsistencies when multiple nodes in a replica set		are being used for writes. 

- All nodes in a peer-to-peer approach are primary nodes, so a single node can handle both reads and writes

- Usually in a peer-to-peer approach, a single node in a replica will replicate the changes to the other nodes in the replica set when a write request comes to the node

- If we prefer consistency where a single primary node will handle the writes, we can go with a primary-secondary	replication approach. If we prefer availability where we want the ability to read and write at all times, we can go with a peer-to-peer replication approach where all the nodes are primary nodes capable of handling both reads/writes.

Data replication using consistent hashing:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/314a270a-a967-4265-a63c-7d5147a19d4c" />

### Inconsistency resolution

- There are different consistency models, from strong, weak to eventual. DynamoDB and Cassandra has an eventual consistency model. An eventual consistency model will also allow the client to reconcile any inconsistency issues using something like vector locks and versioning.

#### Data versioning using vector clocks

- Vector clocks are a list of (nodeID, version counter) pairs and there is a single vector clock for every event of a		record of data. If a data record has two different vector clocks when the data record is being written to the			database, then there is likely a data inconsistency

- Vector clocks can be used to check if one version precedes, succeeds or is in conflict with another version.			DynamoDB uses vector clocks to determine conflicts for a single data record.

##### Vector clock format

- This is the format of a vector clock: Event_Indicator[(node_number, version counter, timestamp)]

- Let’s say we have the below events:
  - Event_1a[(n_1, 2), (n_2, 2)]
  - Event_1b[(n_1, 2), (n_3, 2)]

- In the above events, there is a conflict since the item is modified by both nodes n_2 and n_3 in version 	 2. It is assumed that node n_1 handled the writes until it crashed, then node_2 and node_3 handled the writes. As such, because 2 different nodes are handling the writes for the same data record, there is a conflict.

- We can use vector clocks to tell if there are conflicts in the record. If there is a conflict, then it is up to the client	(client can be a conflict resolution server or the load balancer) to resolve it, similar to resolving conflicts in Git.

- Note that the size of vector clocks may increase if multiple servers write to the same data record, and this may	add more complexity to reading/writing. We can limit the number of servers writing to the same data record as		well, when the vector clock list reaches a size limit

#### Quorum based approach

- Quorums provide tunable consistency and inconsistency resolution, where r + w > n (r / w are the minimum		number of read and write nodes that need to have the request synchronously replicated to for the request to be 	a success). Additionally, the rest of the nodes after a successfully read/write request can be asynchronously		replicated to in a quorum based approach.

- r + w > n is strong consistency because there must be at least 1 overlapping node that has the latest data		(from both reads/writes) to ensure consistency.

- Usually in a quorum based approach, there is a coordinator node among the nodes which checks which nodes	have the updated data for the request, for the request to be considered successful. An example is to the right in	‘Quorum based approach with coordinator node’

Quorum based approach with coordinator node:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/8a15424f-04ad-464d-b5f3-b54a0a6bde63" />

### Handling failures

#### Sloppy quorum approach

- Because read and writes could be blocked in a strict quorum based approach, there is also a sloppy quorum			approach, where only the first healthy W nodes for writes and R nodes for reads process the request along the			 hash ring, and crashed nodes are ignored

#### Hinted handoff

- Hinted handoff is also used to deal with failure recovery where a node will temporarily serve requests for a			crashed node until that crashed node is up and will get the updated data from the interim node.

#### Gossip protocol
- Gossip protocol can be used to detect failures in nodes where each node maintains a node membership list, 			which	 contains the nodeIDs, the heartbeat counter and last active timestamps of the nodes in the group (which		could be a replica set). 

- A single node randomly pings other nodes in the group, and those nodes ping other nodes in the group. The		heartbeat counter and last active timestamp in the membership list are then incremented on each ping. If the		heartbeat counter has not increased for more than a predefined period, the	node is considered down, and this		info is propagated to the other nodes.

- When using consistent hashing with virtual nodes, gossip protocol can fail when 2 virtual nodes of the same			node share heartbeats but they don’t know they're on the same node. This issue is called logical partitioning.

- To fix logical partitioning, we can add seed nodes in a node group which acts as a node membership identifier,	A seed node in a group is known to all the nodes of the group, so all virtual nodes know which node they belong	to.

#### Zookeper

- Zookeper is a tool that can be used to detect failures and manage service discovery (maintaining health of			servers)

#### Merkle trees

- In a merkle tree, a hash of the key range for the nodes are used as the leaves for the tree. The hash of the		children nodes are used as the parent nodes, until we reach the root of the tree. 

- Going from the root to the leaves of the tree, we can check if the key range a node is supposed to serves is outdated in the different copies of the merkle tree. If the hashed values of a node in the tree in two different copies are not the same, then there is an inconsistency or failure which happened for one of the nodes. This process is shown to the right in ‘Inconsistency in merkle tree’

- If using virtual nodes, each node will keep a distinct merkle tree for the range of keys that it serves for each		virtual node

- Using a merkle tree, we implement anti-entropy, to keep all the hashed values of the nodes’ key range that it	serves consistent.

- The advantage of a merkle tree is that when checking if the same node’s key range has changed during a crash, we only need to go down a single branch from the root to the leaves, and not check all the nodes. If there is a crash or a new addition of a server in copy B of a merkle tree, then copy B’s root node will always be different than copy A’s (the previous copy before crash or server addition) root node as shown to the right in 'Inconsistency in merkle tree'

Inconsistency in merkle tree:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/3eecd17e-ece2-471e-933d-c7ec7f19a853" />

<br/>

#### API servers

- The API servers will handle the requests for storing / retrieving / updating / deleting a KV pair from the KV store servers

#### KV store servers

- The KV store servers will store the KV pair entries, likely in SSDs

<img width="700" alt="image" src="https://github.com/user-attachments/assets/dc58d4e0-6cd2-4784-89c6-49e47d8a1346" />

<br/>

KV store (Cassandra) write path:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/cbc26ae2-9974-4a4f-b033-a694e663a497" />

<br/>

KV store (Cassandra) read path:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/4efa48a9-c2d3-484d-85a0-ea6a8f75cf03" />

## DD

**The below deep dives and approaches are taken from the Distributed cache SDI, but closely applies to a KV store**

### API servers have no way of knowing when KV store servers are added or down

- We can try 3 things:
  - We can maintain a config file in each API server, that contains the updated health and metadata of the KV store servers:
    - We’ll maintain a config file in each API server, however, this will have consistency issues in updating all the config			files for all the API servers via some DevOps tool.

  - We can maintain a config file of the KV store server health and metadata in a centralized location. However, the config file will be a SPOF.

  - An automatic way of monitoring the health of KV store servers is to use a configuration service that continuously 			monitors the KV store servers and ensures that the API servers see an updated view of the state of KV store servers.
    - We can use a configuration service that continuously monitors the KV store servers, and will notify the API servers		when KV store servers are added or down. Using this approach, the API server can be stateless. This approach may be	more 	complex but tackles the main issue of the API servers not knowing when KV store servers are added or down. This configuration service may be a SPOF, however, just like with load balancers having a clone, this configuration service could maintain an operation log which appends the scaling and additional operations made on the KV store servers. This operation log could be replicated to a clone configuration service, which can takeover in case the main configuration service is down.

### We have a SPOF in the KV store servers since one KV store server maintains a set of keys

- To solve this issue, we can apply sharding (to prevent the hot-key problem for a single node) and replicate nodes of KV store	servers, where there will be:
  - Primary-secondary replicas if writing and reading ratios are relatively equal. Leader election will be coordinated by			the secondary nodes
  - Multiple primary replicas if there is write intensity
  - All leaderless replicas if there is read intensity

- If we choose to have geo-replication, we can synchronously replicate within the data center and asynchronously replicate	outside the data center
- For inconsistency resolution, we could also use a quorum based approach and vector clocks / versioning of entries

### Handling hot keys being read / written to a lot

**Approaches to handling hot keys are frequently asked in a SDI**

- There are two types of hot keys we need to handle:
  - Hot reads:
    - Hot reads are keys that receive an extremely high volume of read requests, like a tweet's data that millions of users are trying to view concurrently
  - Hot writes:
    - Hot writes are keys that receive many concurrent write requests, like a counter tracking real-time votes.

- Hot reads can be handled using the below approaches, and in 'Handling hot reads':
  - Vertical scaling all nodes
  - Dedicated hot key servers
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
    - Batch writes will mainly be implemented via the API server, where the API server will batch updates for multiple entries before writing the finalized batch update to the KV store servers. Write batching also helps by reducing the number of network trips which needs to be made. A single batched network request can be made for compiled requests.
  - Sharding hot key with suffixes

Handling hot writes:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/083f5623-1786-49f2-a867-1c4fe392fc59" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/3416f4ee-932c-42ee-95ed-d317700299ee" />

### Connection pooling to reduce repeated establishing of network connections

- Constantly establishing and closing connections between the API servers and KV store servers can be reduced if requests can happen within one single connection. This will also prevent bandwidth usage on both the client and server, since they don't have to open a new connection everytime or perform a handshake. Connection pooling can be implemented in the below ways (note that the client refers to the API servers, and the server refers to the actual KV store servers in the approaches below):
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

- Overall connection pooling can reduce the number of network requests being made, which will usually take the most time for requests within a distributed system. It's also important to specify connection limits (so that there is enough bandwidth on the KV store servers), timeouts (in case some requests may take too long), retry logic (requests can instead be retried via exponential backoff), etc.

### Ensuring an even distribution of keys across KV store servers

- We can use consistent hashing to distribute keys across the KV store nodes / servers. This will help prevent the number of keys which need to be remapped when nodes / servers are added or removed. We can use a consistent hashing function like MurmurHash to get a hashed value in the hash ring for a key. We can move clockwise in the hash ring, until we find the first node (or N virtual nodes if using virtual nodes) to store the KV pair on.
- Consistent hashing also helps reduce latency because requests will not need to query a centralized routing service (such as ZooKeeper) to find out which node has which key.

**Note that while consistent hashing may seem to be suitable for most stateless components, maintaining the correct distribution within stateful components (such as databases, websockets, etc) using consistent hashing usually has some overhead as explained below:**

- When requests for the key comes in, we'll likewise hash the request's key onto the hash ring, then find the first node clockwise - this node should contain the KV pair for the request key since we're using consistent hashing. However, when scaling events occur, the keys will need to be remapped to the appropriate KV store servers - this will cause some overhead if using consistent hashing - however, it is still much more efficient than remapping all the keys via the mod operation approach.
- Adding and removing servers may also happen frequently within KV store servers, where the stored data may be frequently changing depending on the TTL, hotspots, eviction policy, etc, which will have some overhead if using consistent hashing.

### Ensuring the KV store is highly available and fault tolerant

- To ensure the KV store is highly available and fault tolerant, we'll need to replicate the copies of the KV store across multiple servers. We can try the below or in 'Ensuring the KV store is highly available and fault tolerant':
  - Synchronous replication
  - Asynchronous replication
  - Peer-to-peer replication

- All of the above approaches could still work well depending on the use cases. Redis, for example uses asynchronous replication by default, but it also provides a WAIT command that allows clients to wait for a replica acknowledgement if needed (sometimes called "semi-synchronous" behavior). Other distributed tools also allow you to configure the replication type in order to choose the right trade-offs for your workload.
- Because low latency responses are a top priority in a KV store, asynchronous replication for a good balance of availability and simplicity + peer-to-peer replication for maximum scalability are two good choices for this design.

Ensuring the KV store is highly available and fault tolerant:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/3594418c-e44d-4e51-a5f8-1e3ab6038304" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/982d360c-8c82-4be4-9736-86c2f0b86f29" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/3dc0cd59-f794-4f49-9e4e-463531017532" />


