# Redis

## What is Redis?

Redis (REmote DIctionary Server) is an open source, in-memory, NoSQL key/value store that is used primarily as an application cache or quick-response database.

Redis stores data in memory, rather than on a disk or solid-state drive (SSD), which helps deliver unparalleled speed, reliability, and performance.

When an application relies on external data sources, the latency and throughput of those sources can create a performance bottleneck, especially as traffic increases or the application scales. One way to improve performance in these cases is to store and manipulate data in-memory, physically closer to the application. Redis is built to this task: It stores all data in-memory—delivering the fastest possible performance when reading or writing data—and offers built-in replication capabilities that let you place data physically closer to the user for the lowest latency.

The answer lies in how Redis does the job. Redis is designed specifically for speed. It’s an “in-memory” database, storing data right in your computer’s active memory (RAM). This makes retrieving data lightning-fast because it’s already in the workspace where your computer actively operates.

Redis is an open source (BSD licensed), in-memory data structure store used as a database, cache, message broker, and streaming engine. Redis provides data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes, and streams. Redis has built-in replication, Lua scripting, LRU eviction, transactions, and different levels of on-disk persistence, and provides high availability via Redis Sentinel and automatic partitioning with Redis Cluster.

### In-memory database

An in-memory database is a type of database that stores data entirely in main memory (RAM) rather than on disk. In-memory databases are designed to provide fast access to data by leveraging the high speed of main memory, which is several orders of magnitude faster than disk storage.

One of the main drawbacks of in-memory databases is that they are more sensitive to data loss in the event of a crash or shutdown, as the data is stored entirely in memory and is not persisted to disk. To address this issue, many in-memory databases, including Redis, provide features such as persistence and replication, which allow data to be saved to disk and replicated across multiple servers to ensure data durability and availability.

## Single-threaded Redis

Redis is designed to be extremely fast, even though it is primarily single-threaded. Its speed comes from careful design choices and the use of efficient techniques like I/O multiplexing.

You might be wondering: why would Redis, opt for a single-threaded design? Wouldn’t it be more efficient to utilise multiple threads and tap into all available CPU cores for parallel computation?

While many helpers might sound good, for Redis, it prefers a single thread for precision, avoiding chaos and ensuring each task is flawlessly executed.

While many applications benefit from parallel processing, Redis primarily focuses on quick data access and minimal latency. A single-threaded approach simplifies the design, ensuring that commands are executed sequentially without the complexities of managing multiple threads and potential synchronisation issues.

In Redis, each command is executed atomically, guaranteeing consistency. This simplicity contributes to faster execution, as the single thread can fully utilise the CPU optimising performance.

In a multi-threaded environment, threads share certain resources, including the CPU cache. When one thread updates data, it may cause the cache to be updated or invalidated. If another thread was using the same data or related data, it might experience what is known as a “cache miss” because the data it needs is no longer in the cache or has been modified.

This situation creates what we call cache contention or cache thrashing, where threads are competing for access to the same limited cache space. Instead of a smooth flow of data, you get interruptions and inefficiencies as threads contend for access, leading to potential performance bottlenecks.

How does a single thread manage many thousands of incoming requests and outgoing responses simultaneously? Wont the thread get blocked in completing each request individually?

However, its single-threaded nature doesn't make it a bottleneck because:

In-Memory Storage: Redis stores all data in memory, making operations extremely fast compared to disk-based databases.

Efficient Data Structures: Redis uses highly optimized data structures like hash tables, sorted sets, and lists that are engineered for fast access.

Minimal System Calls: Redis minimizes blocking I/O operations by keeping most interactions in memory.

### I/O multiplexing in Redis

Redis uses I/O multiplexing to handle multiple client connections concurrently, despite being single-threaded. Here's how it works:

#### What is I/O Multiplexing? 

I/O multiplexing is a technique that enables Redis to monitor multiple file descriptors (network sockets) simultaneously. When one or more of these file descriptors are ready (e.g., data is available to read or write), Redis processes them. This allows Redis to handle multiple client connections simultaneously using a single thread. It uses system-level calls such as epoll, kqueue, select and poll.

#### How Redis Implements I/O Multiplexing? 

Redis uses system calls like epoll (Linux), kqueue (macOS and BSD), or select (older systems) to achieve I/O multiplexing. These system calls allow Redis to handle thousands of connections efficiently by:
- Monitoring readiness of sockets for reading/writing.
- Responding only to sockets that are ready, without blocking on others.

#### Event Loop Mechanism: 

Redis uses a custom event loop. The loop waits for events to occur from the network sockets, such as reading items, writing items, etc. This loop:
- Waits for I/O events using multiplexing.
- Processes events (e.g., read commands, execute them, and send responses).
- Returns to waiting for more events.

#### Avoiding Context Switching Overhead

By handling all commands in a single thread and leveraging I/O multiplexing, Redis avoids the overhead associated with thread or process context switching where the CPU stops executing one thread or process, and starts executing another. This means the CPU will also save the current thread's state and restore the state of another thread when switching threads. The single-threaded approach ensures that no time is wasted on synchronization or race conditions.

#### High Throughput with Non-Blocking Design

Redis achieves high throughput because:
- Network I/O and command execution are non-blocking.
- Commands are small and lightweight, with responses returned immediately.
- Pipelining allows multiple commands to be sent together, reducing round-trip latency.

#### When Multi-Threading is Used

Although Redis core operations are single-threaded, it uses background threads for:
- Disk persistence (e.g., saving snapshots or appending to logs).
- Asynchronous data loading.
- Some blocking operations (e.g., keys command) in Redis 6+ for better scalability.

### I/O monitoring in Redis

Redis also uses I/O monitoring system calls to different connections:

I/O monitoring system calls are functions provided by the operating system that allow your program to keep an eye on multiple input/output sources, like file descriptors or network sockets, at the same time.

Think of I/O monitoring as setting up a watchman for your program. You tell the watchman what you’re interested in (readiness to read, write, etc.), and then your program takes a break, letting the watchman keep an eye on things. When an event happens, the watchman signals your program, saying, “Hey, something’s ready!” Your program then jumps back in to handle the specific event.

### Why is Redis's Design Optimal?

- The single-threaded model simplifies the codebase and reduces complexity while achieving exceptional performance for most use cases.
- By combining in-memory data storage, efficient algorithms, and I/O multiplexing, Redis achieves remarkable speed even under heavy workloads.

This design ensures Redis is fast and scalable for real-time applications.

## Redis features

Redis provides a built-in replication mechanism, automatic failover, and different levels of persistence. Apart from that, Redis understands Memcached protocols, and therefore, solutions using Memcached can translate to Redis. A particularly good aspect of Redis is that it separates data access from cluster management. It decouples the control plane from the data plane. This results in increased reliability and performance. Finally, Redis doesn’t provide strong consistency due to the use of asynchronous replication.

### Redis key-value pairs

In Redis, a key-value pair is a data structure that consists of a unique key, which is used to identify the data, and a value, which is the data itself. Key-value pairs are the most basic data structure in Redis, and they are used to store and manage data in the database.

Redis supports a wide range of data types for keys and values, including strings, hashes, lists, sets, and sorted sets. This allows developers to store and manipulate a variety of data types in Redis, such as text, numbers, arrays, and complex data structures.

Redis provides a rich set of commands for working with key-value pairs, such as SET, GET, and DEL for strings, HSET, HGET, and HDEL for hashes, and LPUSH, LGET, and LREM for lists. These commands enable developers to store, retrieve, and manipulate data in Redis efficiently and easily.

### Redis data structures

Data structures in Redis are collections of data that are organized and managed in a specific way to support efficient operations. For example, the string data type in Redis is a sequence of bytes that can be used to store and manipulate text or binary data. The hash data type, on the other hand, is a mapping of field-value pairs that can be used to store and manipulate complex data structures.

Each data structure in Redis has its own unique set of operations that can be performed on it, such as GET, SET, and DELETE for strings, HGET, HSET, and HDEL for hashes, and LPUSH, LPOP, and LRANGE for lists. These operations enable developers to efficiently store, retrieve, and manipulate data in Redis.

Overall, data structures in Redis are an important aspect of the framework, as they provide the underlying foundation for efficient data management and manipulation.

### Session store

Session store is a mechanism for storing user session data in a web application. In a Redis session store, session data is stored in a Redis database, which is a fast, in-memory data structure store that can be used as a cache, database, and message broker.

In a Redis session store, session data is stored in a Redis database as key-value pairs, where the key is a unique identifier for the session and the value is the session data itself, which may include information such as the user’s login status, preferences, and shopping cart contents.

The benefits of using a Redis session store include improved performance and scalability, as Redis can store and retrieve session data quickly and efficiently, even when dealing with large amounts of data. Additionally, Redis allows session data to be shared across multiple servers, which can be useful in a load-balanced environment.

### Redis Sentinel

Redis Sentinel is a stand-alone distributed system that helps developers calibrate their instances to be highly available for clients. Sentinel uses a series of monitoring processes, notifications, and automatic failovers to inform users when there is something wrong with master and slave instances, while automatically reconfiguring new connections for applications when necessary.

### Redis Cluster

Redis Cluster is a distributed implementation of Redis that automatically splits datasets among multiple nodes. This supports higher performance and scalability of database deployments, while ensuring continuous operations in the event that node subsets are unable to communicate with the rest of the cluster.

Redis has built-in cluster support that provides high availability. This is called Redis Sentinel. A cluster has one or more Redis databases that are queried using multithreaded proxies. Redis clusters perform automatic sharding where each shard has primary and secondary nodes. However, the number of shards in a database or node is configurable to meet the expectations and requirements of an application.

Each Redis cluster is maintained by a cluster manager whose job is to detect failures and perform automatic failovers. The management layer consists of monitoring and configuration software components.

In a Redis Cluster, a cluster manager is a tool or component that assists with managing the lifecycle, configuration, and operations of the Redis cluster. While Redis itself provides native support for clustering, certain tasks—like creating, managing, monitoring, or reconfiguring clusters—can be streamlined with the help of a cluster manager.

Redis does not have an official, built-in "Redis Cluster Manager," but community tools and Redis CLI commands fill this role. These tools facilitate the administrative overhead of setting up and maintaining a Redis Cluster.

<img width="557" alt="image" src="https://github.com/user-attachments/assets/45a4d1a4-f544-49e3-b3fb-ec8a34330b45">

Architecture of Redis clusters:

<img width="454" alt="image" src="https://github.com/user-attachments/assets/eb920262-54b7-440a-bf17-16b8ff6f5461">

### Pipelining in Redis

Since Redis uses a client-server model, each request blocks the client until the server receives the result. A Redis client looking to send subsequent requests will have to wait for the server to respond to the first request. So, the overall latency will be higher.

Redis uses pipelining to speed up the process. Pipelining is the process of combining multiple requests from the client side without waiting for a response from the server. As a result, it reduces the number of RTT spans for multiple requests.

Note: The round-trip-time (RTT) is the latency for a request to travel from the client to the server and back.

<img width="557" alt="image" src="https://github.com/user-attachments/assets/239cee7f-6a43-48d4-8cc6-1aaba143666a">

The process of pipelining reduces the latency through RTT and the time to do socket level I/O. Also, mode switching through system calls in the operating system is an expensive operation that’s reduced significantly via pipelining. Pipelining the commands from the client side has no impact on how the server processes these requests.

For example, two requests pipelined by the client reach the server, and the server can’t entertain the second. The server provides a result for the first and returns an error for the second. The client is independent in batching similar commands together to achieve maximum throughput.

Note: Pipelining improves the latency to a minimum of five folds if both the client and server are on the same machine. The request is sent on a loopback address (127.0.0.1). The true power of pipelining is highlighted in systems where requests are sent to distant machines.

### Redis Pub/Sub

Because Redis supports the use of publish and subscribe (Pub/Sub) commands, users can design high-performance chat and messaging services across all their applications and services. This includes the ability to use list data structures to run atomic operations and blocking capabilities.

Redis implements the Pub/Sub pattern by providing a simple and efficient messaging system between clients. In Redis, clients can “publish” messages to a named channel, and other clients can “subscribe” to that channel to receive the messages.

When a client publishes a message to a channel, Redis delivers that message to all clients that are subscribed to that channel. This allows for real-time communication and the exchange of information between separate components of an application.

Redis Pub/Sub provides a lightweight, fast, and scalable messaging solution that can be used for various use cases, such as implementing real-time notifications, sending messages between microservices, or communicating between different parts of a single application.

#### Redis Pub/Sub is synchronous

Redis Pub/Sub is synchronous. Subscribers and publishers must be connected at the same time in order for the message to be delivered.

Think of it as a radio station. You are able to listen to a station while you’re tuned into it. However, you’re incapable of listening to any message broadcast while your radio was off. Redis Pub/Sub will only deliver messages to connected subscribers.

This means that if one subscriber loses connection and this connection is restored later on, it won’t receive any missed messages or be notified about them. Therefore, it limits use cases to those that can tolerate potential message loss.

#### Redis Pub/Sub has a fire & forget model

Fire & Forget is a messaging pattern where the sender sends a message without expecting an explicit acknowledgment from the receiver that the message was received. The sender simply sends the message and moves on to the next task, regardless of whether or not the message was actually received by the receiver.

Redis Pub/Sub is considered a “Fire & Forget” messaging system because it does not provide an explicit acknowledgment mechanism for confirming that a message was received by the receiver. Instead, messages are broadcast to all active subscribers, and it is the responsibility of the subscribers to receive and process the messages.

#### Redis Pub/Sub is fan-out only

Redis Pub/Sub is fan-out only, meaning that when a publisher sends a message, it is broadcast to all active subscribers. All subscribers receive a copy of the message, regardless of whether they are specifically interested in the message or not.

#### Implementation

Redis message brokering is implemented through the PUBLISH and SUBSCRIBE commands. The PUBLISH command allows the user to send a message to a specific channel, and the SUBSCRIBE command allows the user to listen to messages on a specific channel. This makes it easy to implement a publish-subscribe pattern in your application.

### Redis persistence

Redis uses persistent disk storage designed to survive process outages and network bottlenecks. Redis can persist datasets by taking regular snapshots of data and appending them with changes as they become available. Redis can then be configured to generate these database backups on demand or at automatic intervals to ensure database durability and integrity.

Redis persistence enables data to be saved to disk and restored when the Redis server starts up again, ensuring that data is not lost in the event of a crash or shutdown.

Redis persistence can be configured in several ways, depending on the needs of the application. The simplest form of persistence is snapshotting, which involves periodically saving the entire Redis dataset to disk. This approach is fast and efficient, but it can result in data loss if the Redis server crashes between snapshots.

<img width="792" alt="image" src="https://github.com/user-attachments/assets/a4c808a8-c26e-49ec-b471-f99c0f7ab56d">

Another form of persistence is append-only file (AOF) persistence, which involves saving each write operation to a log file on disk. This approach provides better durability than snapshotting, as it allows the Redis server to recreate the dataset by replaying the log file in the event of a crash. However, it can be slower and more resource-intensive than snapshotting.

Overall, Redis persistence is a valuable feature that allows data to be saved to disk and restored in the event of a crash or shutdown, ensuring data durability and availability.

### Lua scripting

Lua scripting is a technique for writing and executing scripts in the Lua programming language within a host application. Lua is a lightweight, versatile, and embeddable scripting language that is widely used for writing scripts that can be run within other applications.

In the context of Redis, Lua scripting allows developers to write and execute scripts that manipulate data stored in a Redis database. Redis provides a built-in scripting engine that supports Lua, which allows developers to write scripts that can be executed within the Redis server.

One of the main advantages of Lua scripting in Redis is that it allows developers to write complex operations that can be executed atomically and in a single step. This means that the scripts can manipulate data in Redis without interference from other operations, ensuring data consistency and integrity.

Overall, Lua scripting is a powerful and flexible tool that can be used within Redis to write and execute complex operations on data stored in the database.

## Redis vs other data stores

### Redis vs Memcached

Both Redis and Memcached are open source, in-memory data stores, but they differ when it comes to their benefits and features. Memcached is often the preferred choice for simple applications requiring fewer memory resources, but it is limited when storing data in its serialized form. Redis' use of data structures provides much more power when working with large datasets and more ability to fine-tune cache contents and maintain greater efficiency in specific application scenarios.

Even though Memcached and Redis both belong to the NoSQL family, there are subtle aspects that set them apart:

Simplicity: Memcached is simple, but it leaves most of the effort for managing clusters left to the developers of the cluster. This, however, means finer control using Memcached. Redis, on the other hand, automates most of the scalability and data division tasks.

Persistence: Redis provides persistence by properties like append only file (AOF) and Redis database (RDB) snapshot. There’s no persistence support in Memcached. But this limitation can be catered to by using third-party tools.

Data types: Memcached stores objects in the form of key-value pairs that are both strings, whereas Redis supports strings, sorted sets, hash maps, bitmaps, and hyper logs. However, the maximum key or value size is configurable.

Memory usage: Both tools allow us to set a maximum memory size for caching. Memcached uses the slab allocation method for reducing fragmentation. However, when we update the existing entries’ size or store many small objects, there may be a wastage of memory. Nonetheless, there are configuration workarounds to resolve such issues.

Multithreading: Redis runs as a single process using one core, whereas Memcached can efficiently use multicore systems with multithreading technology. We could argue that Redis was designed to be a single-threaded process that reduces the complexity of multithreaded systems. Nonetheless, multiple Redis processes can be executed for concurrency. At the same time, Redis has improved over the years by tweaking its performance. Therefore, Redis can store small data items efficiently. Memcached can be the right choice for file sizes above 100 K.

Replication: As stated before, Redis automates the replication process via few commands, whereas replication in Memcached is again subject to the usage of third-party tools. Architecturally, Memcached can scale well horizontally due to its simplicity. Redis provides scalability through clustering that’s considerably complex.

<img width="625" alt="image" src="https://github.com/user-attachments/assets/7e88f05a-f546-42d2-ab5c-d358cc5b6182">

To summarize, Memcached is preferred for smaller, simpler read-heavy systems, whereas Redis is useful for systems that are complex and are both read- and write-heavy.

### Redis vs MongoDB

While Redis is an in-memory database store, MongoDB is known as an on-disk document store. Although both solutions are built for different purposes, they are often used together to maximize the speed and efficiency of a NoSQL database. Because of its caching ability, Redis can locate required data extremely quickly, serving as an ingestion buffer that makes MongoDB more efficient and able to manage larger frequencies of document updates in near real-time. With MongoDB’s ability to store significant amounts of data and Redis’ ability to process it faster, the pairing offers a powerful database management solution for a variety of use cases.

## How is Redis different from traditional NoSQL data stores?

Redis stands apart from ‘traditional’ NoSQL data stores as an auxiliary component designed specifically to improve application performance. Here are a few differentiating capabilities of Redis:

### Redis cache sessions

Again, unlike NoSQL databases such as MongoDB and PostreSQL, Redis stores data in the server's main memory rather than on hard disks and solid-state drives. This leads to significantly faster response times when performing read and write operations. It also helps ensure high availability (together with Redis Sentinel) and scalability of services and application workloads.

### Redis queues

Redis can queue tasks that may take web clients longer to process than usual. Multiprocess task queuing is commonplace in many of today's web-based applications, and Redis makes it easy to implement automated Python-written processes that run in the background of request/response cycles.

### Redis data types

While technically a key/value store, Redis is an actual data structure server that supports multiple data types and structures, including:

- Unique and unsorted string elements
- Binary-safe data
- HyperLogLogs
- Bit arrays
- Hashes
- Lists

### Redis client handling

Redis features native client integration capabilities to help developers manipulate and interact with their data. There are currently well over 100 different open source clients available in the Redis client library, and developers can easily add new integrations to support additional features and programming languages.

## Redis advantages

One of the main advantages of using Redis for caching is its fast read and write speeds. Redis can handle millions of operations per second, which allows it to serve webpages faster than traditional databases. It also offers excellent support for transactions, allowing applications to perform multiple operations atomically. Additionally, Redis supports the use of pub/sub channels for fast data sharing between applications.

Redis is also highly scalable and can be deployed across multiple machines for high availability. This makes it ideal for distributed systems that need to quickly process large amounts of data.

For example, Redis can be used to store session information in a distributed system and provide quick access to that data across multiple servers. This makes Redis incredibly powerful gaming applications because it can quickly and efficiently share data across multiple nodes in near real time.

In addition to excellent performance, another advantage of Redis is that it offers a number of features that are not available in traditional databases. These include pub/sub, which allows you to publish messages and subscribe to them, as well as transactions and Lua scripting. These features can be used to build powerful applications that are not possible with traditional databases.

## Redis disadvantages

One of the main drawbacks of Redis is that it stores data entirely in memory, which means that it can be sensitive to data loss in the event of a crash or shutdown. To address this issue, Redis provides features such as persistence and replication, which allow data to be saved to disk and replicated across multiple servers. However, these features can add complexity and overhead, which may not be suitable for all applications.

Another drawback of Redis is that it is a single-threaded system, which means that it can only process one command at a time. This can limit the performance and scalability of Redis in applications that require high concurrency and parallelism. To address this issue, Redis provides clustering and sharding features that allow data to be distributed across multiple servers, but these features can be complex to set up and manage.

## Redis use cases

### Real-time analytics

Because Redis can process data with sub-millisecond latency, it is ideal for real-time analytics, online advertising campaigns, and AI-driven machine learning processes.

### Location-based applications

Redis simplifies the development of location-based applications and services by providing geospatial indexing, sets, and operations. Using sorted sets, Redis is able to offload time-consuming searching and sorting of location data while also using an intelligent geo-hashing implementation.

### Caching for databases

Redis is able to handle large amounts of real-time data, making use of its in-memory data storage capabilities to help support highly responsive database constructs. Caching with Redis allows for fewer database accesses, which helps to reduce the amount of traffic and instances required. By using Redis for caching, development teams can dramatically improve their application throughputs by achieving sub-millisecond latency. And since Redis’ caching layer can scale quickly and economically, organizations are able to develop these highly responsive applications while reducing their overall expenditures.

### Chat and messaging applications

To support chat and messaging applications, Redis can be used to store and manage data related to conversations, users, and messages. For example, Redis can be used to store information about individual conversations, such as the participants and the latest messages. It can also be used to store information about individual users, such as their profile details and their list of contacts. Finally, Redis can be used to store the actual messages themselves, along with metadata such as the sender, recipient, and timestamp.

In addition to storing data, Redis can also be used to manage messaging operations, such as delivering messages to recipients, broadcasting messages to multiple recipients, and storing messages for offline users. These capabilities make Redis a powerful tool for building chat and messaging applications that are fast, scalable, and reliable.

## Installing Redis

Getting started with Redis is a fairly seamless process, especially with the use of the Redis Desktop Manager (RDM) (link resides outside ibm.com). And since Redis and RDM are open source, active development communities are always working to improve their efficiency of operation and continuously evolve supported tools and integrations.

## Redis deployment and setup

1. We can first install Redis from online, the GitHub repository or via the Docker image
2. We can then run the redis servia using 'redis-server' and open the redis cli using 'redis-cli'
3. The redis instance will then need to be configured with the port, username and password
4. We can install additional libraries in JS/TS, Go, Java, Python, etc to communicate with the redis instance
5. Redis can be deployed to the cloud using AWS Elasticache, Azure cache for redis, GCP Memorystore for Redis, etc
