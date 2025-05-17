# Zookeeper

## What is Zookeeper

ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. All of these kinds of services are used in some form or another by distributed applications. Each time they are implemented there is a lot of work that goes into fixing the bugs and race conditions that are inevitable. Because of the difficulty of implementing these kinds of services, applications initially usually skimp on them, which make them brittle in the presence of change and difficult to manage. Even when done correctly, different implementations of these services lead to management complexity when the applications are deployed.

It provides a simple, tree-structured data model, a simple API, and a distributed protocol to ensure data consistency and availability. Zookeeper is designed to be highly reliable and fault-tolerant, and it can handle high levels of read and write throughput.

## How does it work

Zookeeper is a distributed, open-source coordination service for distributed applications. It exposes a simple set of primitives to implement higher-level services for synchronization, configuration maintenance, and group and naming. 

In a distributed system, there are multiple nodes or machines that need to communicate with each other and coordinate their actions. ZooKeeper provides a way to ensure that these nodes are aware of each other and can coordinate their actions. It does this by maintaining a hierarchical tree of data nodes called “Znodes“, which can be used to store and retrieve data and maintain state information. ZooKeeper provides a set of primitives, such as locks, barriers, and queues, that can be used to coordinate the actions of nodes in a distributed system. It also provides features such as leader election, failover, and recovery, which can help ensure that the system is resilient to failures. ZooKeeper is widely used in distributed systems such as Hadoop, Kafka, and HBase, and it has become an essential component of many distributed applications.

#### Coordination services

The integration/communication of services in a distributed environment.
Coordination services are complex to get right. They are especially prone to errors such as race conditions and deadlock.

#### Race condition

Two or more systems trying to perform some task.

#### Deadlocks

Two or more operations are waiting for each other.

#### Zookeeper

To make the coordination between distributed environments easy, developers came up with an idea called zookeeper so that they don’t have to relieve distributed applications of the responsibility of implementing coordination services from scratch.

### Why is coordination in a distributed system challenging?

- Coordination or configuration management for a distributed application has many components that constantly change and scale.
- Synchronization is not easy between multiple servers and nodes.
- Careful design and implementation are needed.

## Zookeeper architecture

ZooKeeper allows distributed processes to coordinate with each other through a shared hierarchical namespace organized similarly to a standard file system. The namespace consists of data registers – called znodes, in ZooKeeper parlance – and these are similar to files and directories.

Unlike a typical file system designed for storage, ZooKeeper data is kept in memory, which means ZooKeeper can achieve high throughput and low latency numbers.

The ZooKeeper architecture consists of a hierarchy of nodes called znodes, organized in a tree-like structure. Each znode can store data and has a set of permissions that control access to the znode. The znodes are organized in a hierarchical namespace, similar to a file system. At the root of the hierarchy is the root znode, and all other znodes are children of the root znode. The hierarchy is similar to a file system hierarchy, where each znode can have children and grandchildren, and so on.

![image](https://github.com/user-attachments/assets/c1bac846-318a-49e9-b791-f77f7b659a55)

The name space provided by ZooKeeper is much like that of a standard file system. A name is a sequence of path elements separated by a slash (/). Every node in ZooKeeper's name space is identified by a path.

The data within Zookeeper is divided across multiple collection of nodes and this is how it achieves its high availability and consistency. In case a node fails, Zookeeper can perform instant failover migration; e.g. if a leader node fails, a new one is selected in real-time by polling within an ensemble. A client connecting to the server can query a different node if the first one fails to respond.

ZooKeeper is ordered. ZooKeeper stamps each update with a number that reflects the order of all ZooKeeper transactions. Subsequent operations can use the order to implement higher-level abstractions, such as synchronization primitives.

ZooKeeper is fast. It is especially fast in "read-dominant" workloads. ZooKeeper applications run on thousands of machines, and it performs best where reads are more common than writes, at ratios of around 10:1.

### Leader and follower

Request processor:
- Active in Leader Node and is responsible for processing write requests. After processing, it sends changes to the follower nodes

Atomic broadcast:
- Present in both Leader Node and Follower Nodes. It is responsible for sending the changes to other Nodes.

In-memory databases (replicated databases):
- It is responsible for storing the data in the zookeeper. Every node contains its own databases. Data is also written to the file system providing recoverability in case of any problems with the cluster.

<br/>
<br/>

This below diagram represents the ZooKeeper request processing architecture. It illustrates how ZooKeeper handles write requests and read requests within its distributed system:

<img width="448" alt="image" src="https://github.com/user-attachments/assets/eab5fb87-4c63-46cb-893b-627fbde23464">

Client:
- A client in ZooKeeper is an application or service that connects to the ZooKeeper ensemble (the cluster of servers) to access its distributed coordination services. Application processes using ZooKeeper libraries (e.g., Kafka brokers, Hadoop NameNodes) are examples of clients.

Server:
- A server in ZooKeeper is a node in the ZooKeeper ensemble responsible for handling client requests, maintaining data consistency, and ensuring high availability.

Ensemble:
- Group of Zookeeper servers. The minimum number of nodes that are required to form an ensemble is 3.

The replicated database is an in-memory database containing the entire data tree. Updates are logged to disk for recoverability, and writes are serialized to disk before they are applied to the in-memory database.

Every ZooKeeper server services clients. Clients connect to exactly one server to submit requests. Read requests are serviced from the local replica of each server database. Requests that change the state of the service, write requests, are processed by an agreement protocol.

As part of the agreement protocol all write requests from clients are forwarded to a single server, called the leader. The rest of the ZooKeeper servers, called followers, receive message proposals from the leader and agree upon message delivery. The messaging layer takes care of replacing leaders on failures and syncing followers with leaders.

ZooKeeper uses a custom atomic messaging protocol. Since the messaging layer is atomic, ZooKeeper can guarantee that the local replicas never diverge. When the leader receives a write request, it calculates what the state of the system is when the write is to be applied and transforms this into a transaction that captures this new state.

### Znodes

In Zookeeper, data is stored in a hierarchical namespace, similar to a file system. Each node in the namespace is called a Znode, and it can store data and have children. Znodes are similar to files and directories in a file system. Zookeeper provides a simple API for creating, reading, writing, and deleting Znodes. It also provides mechanisms for detecting changes to the data stored in Znodes, such as watches and triggers. 

Znodes maintain a stat structure that includes version numbers for data changes, ACL changes, and timestamps, to allow cache validations and coordinated updates. Each time a znode's data changes, the version number increases. For instance, whenever a client retrieves data it also receives the version of the data.

The data stored at each znode in a namespace is read and written atomically. Reads get all the data bytes associated with a znode and a write replaces all the data. Each node has an Access Control List (ACL) that restricts who can do what.

ZooKeeper supports the concept of watches. Clients can set a watch on a znodes. A watch will be triggered and removed when the znode changes. When a watch is triggered the client receives a packet saying that the znode has changed. And if the connection between the client and one of the Zoo Keeper servers is broken, the client will receive a local notification.

Types of Znodes:

- Persistence: Alive until they’re explicitly deleted.
- Ephemeral: Active until the client connection is alive.
- Sequential: Either persistent or ephemeral.

## Use cases

### Naming service

Identifying the nodes in a cluster by name. It is similar to DNS but for nodes.

### Configuration management

Manage latest and up-to-date configuration information of the system for a joining node.

### Cluster management

Manage joining/leaving a node in a cluster and node status in real-time.

### Leader election

Electing a node as a leader for coordination purpose.

### Locking and synchronization service

Locking the data while modifying it.

### Highly reliable data registry

Availability of data even when one or a few nodes are down.

## Advantages

### Guarantees Zookeeper provides

ZooKeeper is very fast and very simple. Since its goal, though, is to be a basis for the construction of more complicated services, such as synchronization, it provides a set of guarantees. These are:

- Sequential Consistency - Updates from a client will be applied in the order that they were sent.

- Atomicity - Updates either succeed or fail. No partial results.

- Single System Image - A client will see the same view of the service regardless of the server that it connects to.

- Reliability - Once an update has been applied, it will persist from that time forward until a client overwrites the update.

- Timeliness - The clients view of the system is guaranteed to be up-to-date within a certain time bound.

### Replication

Like the distributed processes it coordinates, ZooKeeper itself is intended to be replicated over a set of hosts called an ensemble.

The servers that make up the ZooKeeper service must all know about each other. They maintain an in-memory image of the state, along with a transaction logs and snapshots in a persistent store. As long as a majority of the servers are available, the ZooKeeper service will be available.

Clients connect to a single ZooKeeper server. The client maintains a connection through which it sends and gets responses. If the TCP connection to the server breaks, the client will connect to a different server.

### Simple coordination service

Apache Zookeeper is a simple distributed coordination process

### MapReduce jobs

Encode the data according to specific rules. Ensure your application runs consistently. This approach can be used in MapReduce to coordinate queue to execute running threads.

## Disadvantages

1. Write Scalability
- Problem: ZooKeeper is designed with a strong consistency model, which means every write operation must be replicated to a majority of nodes in the cluster. This replication creates a bottleneck for write-intensive workloads.
- Impact: It struggles to handle high-throughput write-heavy operations effectively.

2. Latency for Writes
- Problem: Due to the consistency guarantees (e.g., Paxos/ZAB protocol), write operations can exhibit higher latency compared to read operations.
- Impact: Applications requiring ultra-low-latency writes may find ZooKeeper unsuitable.

3. Dependency on Network Stability
- Problem: ZooKeeper relies heavily on reliable and low-latency network communication between nodes. Network partitions or instability can disrupt operations and even lead to split-brain scenarios.
- Impact: Network issues can result in delays, errors, or unavailability of services dependent on ZooKeeper.

4. Complexity in Setup and Management
- Problem: ZooKeeper requires careful setup, configuration, and tuning to ensure proper functioning and fault tolerance. Cluster management, including setting up quorum, monitoring, and maintaining data consistency, can be challenging.
- Impact: Teams need expertise to deploy and manage ZooKeeper effectively, which can increase operational overhead.

5. High Resource Usage
- Problem: ZooKeeper can be resource-intensive, requiring significant memory and CPU to handle larger datasets and high request volumes.
- Impact: Resource usage scales with the number of nodes, increasing the cost of running and maintaining the system.

6. Not a General Database
- Problem: ZooKeeper is designed for small, critical configuration data and metadata storage but is not meant to be a general-purpose database.
- Impact: Attempting to use ZooKeeper for large datasets or complex queries can result in performance degradation and operational issues.

7. Failure of Majority Nodes
- Problem: ZooKeeper requires a quorum (a majority of nodes in the cluster) to function. If more than half of the nodes fail, the cluster becomes unavailable.
- Impact: This can lead to service downtime in highly volatile environments where node failures are frequent.

8. Limited Programming Model
- Problem: The ZooKeeper API is relatively low-level and requires developers to build their own abstractions for features like leader election or distributed locks.
- Impact: This increases the development effort and complexity of applications that depend on ZooKeeper.

9. Not Cloud-Native
- Problem: ZooKeeper was designed before the cloud-native era and lacks features like elastic scaling and seamless integration with cloud platforms.
- Impact: Deploying ZooKeeper in containerized environments like Kubernetes can require additional tools or wrappers (e.g., Operators), adding complexity.

10. Single Point of Bottleneck
- Problem: In large-scale systems, the ZooKeeper leader node can become a bottleneck since it handles write requests.
- Impact: Overloading the leader node can degrade cluster performance.

11. Manual Scaling
- Problem: Scaling a ZooKeeper cluster is not straightforward and often requires careful coordination to add or remove nodes without disrupting the quorum.
- Impact: This can make scaling operations error-prone and time-consuming.

12. Potential for Overhead in Small Systems
- Problem: For small-scale systems, ZooKeeper's complexity and resource requirements may outweigh the benefits it provides.
- Impact: Using ZooKeeper for lightweight use cases can lead to unnecessary operational overhead.

13. Leader Election Overhead
- Problem: When a leader node fails, a new leader must be elected, which introduces latency and potential unavailability during the election process.
- Impact: Applications relying on ZooKeeper may experience downtime or degraded performance during leader transitions.

14. Evolving Ecosystem
- Problem: With the rise of alternatives like etcd, Consul, and cloud-native solutions, ZooKeeper is no longer the de facto choice for distributed coordination.
- Impact: Organizations may find more modern solutions better aligned with their architecture needs, reducing the appeal of ZooKeeper.

<br/>
<br/>

### When not to use Zookeeper

High Write Workloads: 
- Systems requiring high-throughput writes may be better served by alternatives like etcd or Kafka's internal metadata storage.

Cloud-Native Environments:
- Use solutions like etcd or Consul, which are designed for containerized, dynamic environments like Kubernetes.

Simple Use Cases: 
- For lightweight use cases, simpler solutions like Redis or even S3 for config storage might suffice.

## Using Zookeeper

One of the design goals of ZooKeeper is provide a very simple programming interface. As a result, it supports only these operations:

create:
- creates a node at a location in the tree

delete:
- deletes a node

exists:
- tests if a node exists at a location

get data:
- reads the data from a node

set data:
- writes data to a node

get children:
- retrieves a list of children of a node

sync:
- waits for data to be propagated

ZooKeeper provides a simple and reliable interface for reading and writing data. The data is stored in a hierarchical namespace, similar to a file system, with nodes called znodes. Each znode can store data and have children znodes. ZooKeeper clients can read and write data to these znodes by using the getData() and setData() methods, respectively. Here is an example of reading and writing data using the ZooKeeper Java API:

```java
// Connect to the ZooKeeper ensemble
ZooKeeper zk = new ZooKeeper("localhost:2181", 3000, null);
 
// Write data to the znode "/myZnode"
String path = "/myZnode";
String data = "hello world";
zk.create(path, data.getBytes(), Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
 
// Read data from the znode "/myZnode"
byte[] bytes = zk.getData(path, false, null);
String readData = new String(bytes);
 
// Prints "hello world"
System.out.println(readData);  
 
// Closing the connection 
// to the ZooKeeper ensemble
zk.close();
```

```py

from kazoo.client import KazooClient
 
# Connect to ZooKeeper
zk = KazooClient(hosts='localhost:2181')
zk.start()
 
# Create a node with some data
zk.ensure_path('/gfg_node')
zk.set('/gfg_node', b'some_data')
 
# Read the data from the node
data, stat = zk.get('/gfg_node')
print(data)
 
# Stop the connection to ZooKeeper
zk.stop()
```

Session:
- Requests in a session are executed in FIFO order.
- Once the session is established then the session id is assigned to the client.
- Client sends heartbeats to keep the session valid
- session timeout is usually represented in milliseconds

Watches:
- Watches are mechanisms for clients to get notifications about the changes in the Zookeeper
- Client can watch while reading a particular znode.
- Znodes changes are modifications of data associated with the znodes or changes in the znode’s children.
- Watches are triggered only once.
- If the session is expired, watches are also removed.

