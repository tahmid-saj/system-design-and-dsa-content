# Cassandra

## What is Cassandra

Apache Cassandra is an open source NoSQL distributed database trusted by thousands of companies for scalability and high availability without compromising performance. Linear scalability and proven fault-tolerance on commodity hardware or cloud infrastructure make it the perfect platform for mission-critical data.

Cassandra is an open-source NoSQL distributed database that manages large amounts of data across commodity servers. It is a decentralized, scalable storage system designed to handle vast volumes of data across multiple commodity servers, providing high availability without a single point of failure.

Apache Cassandra® is the only distributed NoSQL database that delivers the always-on availability, blisteringly fast read-write performance, and unlimited linear scalability needed to meet the demands of successful modern applications.

It can handle petabytes of information and thousands of concurrent operations per second, enabling organizations to manage large amounts of structured data across hybrid and multi-cloud environments.

### Reliability

Masterless architecture and low latency means Cassandra will withstand an entire data center outage with no data loss—across public or private clouds and on-premises.

Cassandra’s support for replicating across multiple datacenters is best-in-class, providing lower latency for your users and the peace of mind of knowing that you can survive regional outages. Failed nodes can be replaced with no downtime.

To ensure reliability and stability, Cassandra is tested on clusters as large as 1,000 nodes and with hundreds of real world use cases and schemas tested with replay, fuzz, property-based, fault-injection, and performance tests.

Cassandra is suitable for applications that can’t afford to lose data, even when an entire data center goes down. There are no single points of failure. There are no network bottlenecks. Every node in the cluster is identical.

### Flexibility

Choose between synchronous or asynchronous replication for each update. Highly available asynchronous operations are optimized with features like Hinted Handoff and Read Repair.

It is also flexible in the structure (can accept structured, semi-structured, and unstructured data).

### Monitoring

The audit logging feature for operators tracks the DML, DDL, and DCL activity with minimal impact to normal workload performance, while the fqltool allows the capture and replay of production workloads for analysis.

### Scability

Cassandra streams data between nodes during scaling operations such as adding a new node or datacenter during peak traffic times. Zero Copy Streaming makes this up to 5x faster without vnodes for a more elastic architecture particularly in cloud and Kubernetes environments.

## How does Cassandra work?

One important Cassandra attribute is that its databases are distributed. That yields both technical and business advantages. Cassandra databases easily scale when an application is under high stress, and the distribution also prevents data loss from any given datacenter’s hardware failure. A distributed architecture also brings technical power; for example, a developer can tweak the throughput of read queries or write queries in isolation.

"Distributed" means that Cassandra can run on multiple machines while appearing to users as a unified whole. There is little point in running Cassandsra as a single node, although it is very helpful to do so to help you get up to speed on how it works. But to get the maximum benefit out of Cassandra, you would run it on multiple machines.

Since it is a distributed database, Cassandra can (and usually does) have multiple nodes. A node represents a single instance of Cassandra. These nodes communicate with one another through a protocol called gossip, which is a process of computer peer-to-peer communication. Cassandra also has a masterless architecture – any node in the database can provide the exact same functionality as any other node – contributing to Cassandra’s robustness and resilience. Multiple nodes can be organized logically into a cluster, or "ring". You can also have multiple datacenters.

<img width="551" alt="image" src="https://github.com/user-attachments/assets/14e02dc4-cce3-4ff6-b832-523c44dd1703">

### Nodes

One reason for Cassandra’s popularity is that it enables developers to scale their databases dynamically, using off-the-shelf hardware, with no downtime. You can expand when you need to – and also shrink, if the application requirements suggest that path.

Perhaps you are used to Oracle or MySQL databases. If so, you know that extending them to support more users or storage capacity requires you to add more CPU power, RAM, or faster disks. Each of those costs a significant amount of money. And yet: Eventually you still encounter some ceilings and constraints.

In contrast, Cassandra makes it easy to increase the amount of data it can manage. Because it’s based on nodes, Cassandra scales horizontally (aka scale-out), using lower commodity hardware. To double your capacity or double your throughput, double the number of nodes. That’s all it takes. Need more power? Add more nodes – whether that’s 8 more or 8,000 – with no downtime. You also have the flexibility to scale back if you wish.

This linear scalability applies essentially indefinitely. This capability has become one of Cassandra’s key strengths.

<img width="550" alt="image" src="https://github.com/user-attachments/assets/ffb8b3e9-1122-4cc6-a3e7-3dde9121752e">

### Partitions

In Cassandra, the data itself is automatically distributed, with (positive) performance consequences. It accomplishes this using partitions. Each node owns a particular set of tokens, and Cassandra distributes data based on the ranges of these tokens across the cluster. The partition key is responsible for distributing data among nodes and is important for determining data locality. When data is inserted into the cluster, the first step is to apply a hash function to the partition key. The output is used to determine what node (based on the token range) will get the data.

<img width="550" alt="image" src="https://github.com/user-attachments/assets/589a1ced-e596-4730-a4c0-b9ac638300f3">

When data comes in, the database’s coordinator takes on the job of assigning to a given partition – let’s call it partition 59. Remember that any node in the cluster can take on the role as the coordinator. As we mentioned earlier, nodes gossip to one another; during which they communicate about which node is responsible for what ranges. So in our example, the coordinator does a lookup: Which node has the token 59? When it finds the right one, it forwards that data to that node. The node that owns the data for that range is called a replica node. One piece of data can be replicated to multiple (replica) nodes, ensuring reliability and fault tolerance. So far, our data has only been replicated to one replica. This represents a replication factor of one, or RF = 1.

The coordinator node isn’t a single location; the system would be fragile if it were. It’s simply the node that gets the request at that particular moment. Any node can act as the coordinator.

### Replication

One piece of data can be replicated to multiple (replica) nodes, ensuring reliability and fault tolerance. Cassandra supports the notion of a replication factor (RF), which describes how many copies of your data should exist in the database. So far, our data has only been replicated to one replica (RF = 1). If we up this to a replication factor of two (RF = 2), the data needs to be stored on a second replica as well – and hence each node becomes responsible for a secondary range of tokens, in addition to its primary range. A replication factor of three ensures that there are three nodes (replicas) covering that particular token range, and the data is stored on yet another one.

<img width="551" alt="image" src="https://github.com/user-attachments/assets/e7744d0c-5c39-45f8-84eb-ce888d80f3de">

The distributed nature of Cassandra makes it more resilient and performant. This really comes into play when we have multiple replicas for the same data. Doing so helps the system to be self-healing if something goes wrong, such as if a node goes down, a hard drive fails, or AWS resets an instance. Replication ensures that data isn’t lost. If a request comes in for data, even if one of our replicas has gone down, the other two are still available to fulfill the request. The coordinator stores a “hint” for that data as well, and when the downed replica comes back up, it will find out what it missed, and catch up to speed with the other two replicas. No manual action is required, this is done completely automatically.

<img width="550" alt="image" src="https://github.com/user-attachments/assets/41c732d1-4305-47b9-ba84-43776e5ff77f">

The use of multiple replicas also has performance advantages. Because we aren’t limited to a single instance We have three nodes (replicas) that can be accessed to provide data for our operations, which we can load balance amongst to achieve the best performance.

Cassandra automatically replicates that data around your different data centers. Your application can write data to a Cassandra node on the U.S. west coast, and that data is automatically available in data centers at nodes in Asia and Europe. That has positive performance advantages – especially if you support a worldwide user base. In a world dependent on cloud computing and fast data access, no user suffers from latency due to distance

<img width="551" alt="image" src="https://github.com/user-attachments/assets/355ade5d-1d6d-4652-81dc-42a5cddd216b">

### Consistency

We’ve been talking a lot about distributed systems and availability. If you are familiar with CAP theorem, Cassandra is by default an AP (Available Partition-tolerant) database, hence it is “always on”. But you can indeed configure the consistency on a per-query basis. In this context, the consistency level represents the minimum number of Cassandra nodes that must acknowledge a read or write operation to the coordinator before the operation is considered successful. As a general rule, you will select your consistency level (CL) based on your replication factor. 

<img width="551" alt="image" src="https://github.com/user-attachments/assets/449e66c1-8d9f-4f10-85df-2a581108ed84">

For the example below, our data is replicated out to three nodes. We have a CL=QUORUM (Quorum referring to majority, 2 replicas in this case or RF/2 +1) therefore the coordinator will need to get acknowledgement back from two of the replicas in order for the query to be considered a success.

As with other computing tasks, it can take some skill to learn to tune this feature for ideal performance, availability, and data integrity – but the fact that you can control it with such granularity means you can control deployments in great detail.

<img width="551" alt="image" src="https://github.com/user-attachments/assets/7d67dd9c-a636-4a19-98c6-bb01a28a17af">

### ACID and BASE

Cassandra is not a fully ACID-style database, since it does not support strict consistency in the ACID-sense such as two-phase commits, rollbacks or locking mechanisms. While it does support other ACID-like features, such as strong consistency (using CL=ALL), compare-and-set updates with Lightweight Transactions, atomicity and isolation on the row-level, and has a durable writes option, it is inaccurate to describe Cassandra as an ACID-compliant database.

Instead, furthering the analogy of comparative pH levels, Cassandra has been described as a BASE database, since it offers Basic Availability, Soft state, and Eventual consistency. 

### CAP theorem

Apache Cassandra is a highly scalable, distributed database that strictly follows the principle of the CAP (Consistency Availability and Partition tolerance) theorem. It adheres to high availability and partition tolerance, and also has tunable consistency.

In Apache Cassandra, there is no master-client architecture. It has a peer-to-peer architecture. In Apache Cassandra, we can create multiple copies of data at the time of keyspace creation. We can simply define replication strategy and RF (Replication Factor) to create multiple copies of data.

In this example, we define RF (Replication Factor) as 3 which simply means that we are creating here 3 copies of data across multiple nodes in a clockwise direction.

```cql
CREATE KEYSPACE Example
WITH replication = {'class': 'NetworkTopologyStrategy', 
                             'replication_factor': '3'}; 
```

<img width="275" alt="image" src="https://github.com/user-attachments/assets/14c55aa9-fc5c-4d11-b9ac-e1eeda02826d">

- cqlsh: CQL shell cqlsh is a command-line shell for interacting with Cassandra through CQL (Cassandra Query Language).
  
To create keyspace use the following CQL query.

```cql
CREATE KEYSPACE Emp
WITH replication = {'class': 'SimpleStrategy', 
                             'replication_factor': '1'}; 
```

## Cassandra architecture

The primary architecture of Cassandra is made up of a cluster of nodes. Apache Cassandra is structured as a peer-to-peer system and closely resembles DynamoDB and Google Bigtable. 

Every node in Cassandra is equal and carries the same level of importance, which is fundamental to the structure of Cassandra. Each node is the exact point where specific data is stored. A group of nodes that are related to each other makes up a data center. The complete set of data centers capable of storing data for processing is what makes up a cluster. 

The beautiful thing about Cassandra’s architecture is that it can easily be expanded to house more data. By adding more nodes, you can double the amount of data the system carries without overwhelming it. This dynamic scaling ability goes both ways. By reducing the number of nodes, developers can shrink the database system if necessary. Compared to previous structured query language (SQL) databases and the complexity of increasing their data-carrying capacity, Cassandra’s architecture gives it a considerable advantage.

Cassandra’s architecture is fundamentally designed to achieve scalability, fault tolerance, and high availability, making it an excellent choice for applications requiring distributed data across many nodes with no single point of failure. Here’s a breakdown of its core architectural components and how they contribute to its robustness.

<img width="579" alt="image" src="https://github.com/user-attachments/assets/419605e7-1573-4b3e-9a56-42d3688f2438">

- Node is the basic component in Cassandra. It is the place where data is stored. For Example: As shown in the diagram, node which has IP address 11.0.0.5 contain data (keyspace which contain one or more tables).

- Keyspace: The top-level database object that contains all data in Cassandra. Keyspaces control replication for the objects they contain, and are analogous to SQL databases. 

- Tables: Contain the key value data in Cassandra. Each table should have a primary key, which identifies the location and order of stored data. 

- Columns: Contain the data in Cassandra.

<img width="578" alt="image" src="https://github.com/user-attachments/assets/818a4d99-5aad-4fb7-b71e-879d702648e8">

- Data Center is a collection of nodes.

<img width="579" alt="image" src="https://github.com/user-attachments/assets/f77cdd68-ae6c-4097-8269-673cbbda94e0">

- Cluster: It is the collection of many data centers.

<img width="578" alt="image" src="https://github.com/user-attachments/assets/25b023b4-f831-47a5-8ba9-e7d400f91728">

### Data storage

A key Cassandra feature also involved how it stored data. Rather than constantly altering large monolithic, mutable (alterable) data files, the system relied upon writing files to disk in an immutable (unalterable) state. If data changed for a particular entry in the database, the change would be written to a new immutable file instead. Automatic system processes triggered by periodic, size or modification rate of the files, would gather a number of these immutable files together (each of which may have redundant or obsolete data) and write out a new single composite table file of the most current data — a process known as compaction. The format of these immutable data files are known as a Sorted Strings Tables, or SSTables.

Since Cassandra spreads out data across multiple nodes, and multiple SSTable files per node, the system would need to understand where a particular record could be found. To do so, it used a theoretical ring architecture to distribute ranges of data across nodes. And, within a node, it used Bloom filters to determine which SSTable in particular held the specific data being queried.

- Commit Log: Every write operation in Cassandra is first written to a commit log, a durable write-ahead log on disk. This mechanism ensures data durability and provides a recovery point in case of a crash.

- Memtable: After writing to the commit log, data is stored in a memtable, an in-memory data structure. Once the memtable reaches a certain size or after a specific time, it is flushed to disk.

- SSTables: When data from a memtable is flushed to disk, it is stored in an SSTable (Sorted String Table), an immutable data file. Cassandra merges and compacts SSTables periodically to optimize storage and query efficiency.

### Peer-to-peer model

Unlike traditional databases that use a master-slave architecture, Cassandra operates on a peer-to-peer model. This setup means that all nodes in a Cassandra cluster are identical, with no master nodes. Each node communicates with the other nodes directly, which ensures there are no bottlenecks or single points of failure.

### Reads and writes

- Writes: Cassandra’s write path is designed for high performance. Writes are first logged in the commit log for durability and then written to the memtable. This process ensures rapid write operations with minimal latency.

- Reads: Reading data in Cassandra involves checking both the memtable and SSTables. To optimize read performance, Cassandra uses bloom filters to quickly determine if an SSTable contains the requested data, minimizing unnecessary disk reads.

### Gossip protocol

Node Discovery and Communication: Cassandra uses the Gossip protocol for inter-node communication. This protocol ensures nodes within the cluster exchange information about themselves and other nodes, maintaining a consistent and updated view of the cluster’s state. Gossip allows Cassandra to monitor the health of nodes and manage the cluster’s topology dynamically.

### Partitioning

In Cassandra, data is stored and retrieved via a partitioning system. A partitioner is what determines where the primary copy of a data set is stored. This works with nodal tokens in a direct format. Every node owns or is responsible for a set of tokens based on a partition key. The partition key is responsible for determining where data is stored. 

Immediately as data enters a cluster, a hash function is added to the partition key. The coordinator node (the node a client connects to with a request) is responsible for sending the data to the node with the same token under that partition. 

### Replication

Another way Cassandra works is by replicating data across nodes. These secondary nodes are called replica nodes, and the number of replica nodes for a given data set is based on the replication factor (RF). A replication factor of 3 means three nodes cover the same token range, storing the same data. Multiple replicas are key to the reliability of Cassandra.

Even when one node stops functioning, temporarily or permanently, other nodes hold the same data, meaning that data is hardly ever wholly lost. Better still, if a temporarily disrupted node is back on track, it receives an update on the data actions it may have missed and then catches up to speed to continue functioning.

- Partitioning: Cassandra distributes data across the cluster using partitioning. It hashes the partition key of a row with a consistent hashing algorithm to determine which node will store that row. Each node is responsible for a range of data determined by its position on the hash ring.

- Replication: To ensure data availability and fault tolerance, Cassandra replicates partitions across multiple nodes. The replication factor, which can be configured per keyspace, defines how many copies of the data exist across the cluster. This replication strategy ensures that even in the event of node failures, the data is still accessible from replica nodes.

### Data model

Cassandra, by itself, natively focuses upon two different NoSQL data models:

- Wide Column Store – Cassandra is primarily identified as a “wide column store.” This sort of database is particularly adept at handling aggregate functions quickly and is more efficient when dealing with sparse data (where the database may have only a few values set for many possible rows and columns).

- Key Value – Cassandra also readily serves as a key-value store.

- Cassandra can support additional data models with extensions:

- Graph – Cassandra can use various extensions or additional packages, such as through the Linux Foundation’s JanusGraph, to serve as a graph database, which keeps track of interrelationships between entities through edges and vertices.
Time series – Cassandra can work as a passable time series database (TSDB) by itself, but it can also be made more robust for this use case with open source packages such as KairosDB.

### Clusters

Given that Apache Cassandra features were architected with scalability foremost in mind, Cassandra is capable to scale to a theoretically unlimited number of nodes in a cluster, and clusters can be geographically dispersed, with data exchanged between clusters using multi-datacenter replication.

In Cassandra a node is either a whole physical server, or an allocated portion of a physical server in a virtualized or containerized environment. Each node will have requisite processing power (CPUs), memory (RAM), and storage (usually, in current servers, in the form of solid-state drives, known as SSDs).

These nodes are organized into clusters. Clusters can be in physical proximity (such as in the same datacenter), or can be disbursed over great geographical distances. To organize clusters into datacenters, and then also across different racks (to ensure high availability), Cassandra uses a snitch monitor.

Once deployed Cassandra uses a mechanism called multi-datacenter replication to ensure data is transferred and eventually synchronized between clusters. Note that two clusters could be installed side-by-side in the same datacenter yet employ this mechanism to transfer data between the clusters. 

Within a Cassandra cluster, there is no central primary (or master) node. All nodes are peers. There are mechanisms, such as the Gossip protocol to determine when the cluster is first started for nodes to discover each other. Once the topology is established, however, it is not static. This same Gossip mechanism helps to determine when additional nodes are added, or when nodes are removed (either through purposeful decommissioning or through temporary unavailability or catastrophic outages). (Read more here about Cassandra’s use of Gossip.)

During such topology changes, Cassandra uses a mechanism to redistribute data across the cluster. Let’s look more into how Cassandra distributes data across the cluster.

### Keyspaces, Columns, Rows, Partitions, Tokens

Within a Cassandra cluster, you can have one or more keyspaces. The keyspace is the largest “container” for data within Cassandra. Creating a keyspace in Cassandra CQL is roughly equivalent to CREATE DATABASE in SQL. You can have multiple keyspaces inside the same Cassandra cluster, but creating too many separate keyspaces can make the cluster less performant. Also be careful about naming your keyspaces, because the names cannot be altered thereafter (you would need to migrate all your data into a differently-named keyspace).

Data is then defined based on the different APIs used to access Cassandra. Under the older Thrift API, data was defined as a column family. However, given that Thrift was deprecated in Cassandra 4.0, it is more important to consider how data is defined as tables in CQL.

Tables in CQL are somewhat similar to those in ANSI SQL, with columns and rows. They can be modified (adding or removing columns, for instance), but like keyspaces, tables cannot be renamed. You can have multiple tables per keyspace.

Unlike SQL, though, not every row will appear in every column. For example, for a user, you may or may not have their first and last name. You may or may not have their mobile phone number, their email address, their date of birth, or other specific elements of data. For example, for a user, you might just have their first name, “Bob,” and their phone number. The Cassandra data model is therefore more efficient to handle sparse data. 

While some people might say this means Cassandra is schemaless, or only supports unstructured data, these assertions are technically imprecise and incorrect. Apache Cassandra does have a schema and structure within each table in a keyspace.

Within a table, you organize data into various partitions. Partitions should be defined based on the query patterns expected against the data (writes, reads and updates), to even balance transactions as evenly as possible. Otherwise, frequently-requested data would make for “hot partitions” since they might be queried (written to or read from) so often. Frequently-written-to partitions can also turn into “large partitions,” potentially growing to a gigabyte or more of data, which can make the database less performant.

Finally, once a partitioning scheme is determined for the database, the Murmur 3 hashing function is used by default to turn the primary keys into partition keys represented as tokens. These tokens are distributed to the different nodes in the cluster using Cassandra’s data distribution and replication mechanisms across its ring architecture.

### Ring architecture

For the Cassandra database model to be a highly-available distributed database, it needs mechanisms to distribute data, queries and transactions across its constituent nodes. As noted, it uses the Murmur 3 partitioning function to distribute data as evenly as possible across the nodes. Say you had three nodes and 30,000 partitions of data. Each node would be assigned 10,000 partitions.

<img width="573" alt="image" src="https://github.com/user-attachments/assets/0f00e966-e027-4c86-a6a5-7949821873ea">

However, to be fault tolerant, there are multiple nodes where data can be found. The number of times a piece of data will be copied within a Cassandra cluster is based on the Replication Factor (RF) assigned to the keyspace. If you set RF to 2, there would be two copies of every piece of data in the database. Many Cassandra clusters are set up with an RF of 3, where each piece of data was written to three different nodes, to ensure that if you can get a quorum, or majority, query across the nodes to agree for better and more reliable data consistency.

<img width="524" alt="image" src="https://github.com/user-attachments/assets/04ad355d-b92b-4e3b-b237-88198027451f">

For more granular and finely balanced data distribution, a Cassandra node is further abstracted into Virtual Nodes (vNodes). This mechanism is designed to ensure that data is more evenly distributed across and within nodes. For example, our three node cluster could be split into 12 vNodes. Each physical node would have a number of vNodes, each responsible for a different range of partitions, as well as keeping replicas of other partitions from two other vNodes.

The Cassandra partitioning scheme is also topology aware, so that no single physical node contains all replica copies of a particular piece of data. The system will try to ensure that the partition range replicas in vNodes are all distributed to be stored on different machines. This high availability feature is to maximize the likelihood that even if there are a few nodes down the data remains available in the database.

<img width="419" alt="image" src="https://github.com/user-attachments/assets/dda4aecf-3ff8-45b9-8aaa-027fdeb4addc">

### Memory and bloom filter

The write path in Cassandra goes first goes to an in-memory structure called the memtable and is also committed to a persistent commit log.

Once committed, that data will continue to be held in the memtable. Periodically a collection of updates in the memtable will be flushed and written to a Sorted Strings Table (SSTable). The SSTable is usually written to persistent storage, but for fastest performance it can also reside in-memory (in RAM).

Whereas many databases have files that are constantly changing with each new write (“mutable” files), Cassandra SSTable files are immutable — they do not change once written. Apache Cassandra writes these immutable files in a Log Structured Merge tree (LSM tree) format. If a record needs to be updated, it is written to a new file instead. If a record needs to be deleted, the immutable tables are not altered, but instead an artifact called a tombstone is written to a new SSTable, a marker that the original record is to be deleted, and also, if a query comes in for that data, it should not appear in any returned result.

Over time a number of separate SSTable files are merged together through a process known as compaction, where only the latest version of each data record is written to the new SSTable. Any data associated with a tombstone is not written to the new SSTable. Compaction can either be automatic (the system will periodically compact files), or it can be triggered by a user operator.

The read path for Cassandra goes through the memtable first, then to a row cache (if it was enabled), a Bloom filter (which tells the system if the data will be found in storage), a partition key cache, and only then does it check for the data on disk.

Since the memtable and caches are stored in RAM, these reads happen very quickly. SSTable lookups can vary in time, depending on whether the SSTable is stored in-memory, on solid state drives (SSDs), or on traditional spinning hard disk drives (HDDs). In-memory storage is fastest, but also the most-expensive option. Hard disk drives are the slowest, but also the least-expensive option. Solid state drives provide a middle-ground in terms of performance and affordability.

The role of the Bloom Filter in the read path is to avoid having to check every SSTable on the node to figure out in which file particular data exists. A Bloom Filter is a probabilistic mechanism to say that either the data does not exist in that file, or that it probably does exist in a file; false positives are possible, but false negatives are not. The Bloom Filter resides in memory, like the memtable and caches, but it exists offheap.

### Garbage collection

Apache Cassandra is built on Java, and runs in the Java Virtual Machine (JVM). Summarily, Cassandra relies on JVM Garbage Collection, or JVM GC, in order to occasionally identify and reclaim unused memory so there is always enough space to allocate new objects. Java GC performance is, however, contingent on the accuracy of tuning based on your specific Apache Cassandra application node cluster architecture.

Cassandra GC tuning is essential to maintain low latency and high throughput. Engineers want the JVM garbage collector to run often enough so there is always space in RAM to allocate new objects to, but not so often that the JVM heap size affects node performance. Specific tuning varies greatly depending on the types of queries and transactional loads running in a Cassandra database. According to The Last Pickle, properly tuned clusters can exhibit a 5-10x improvement in latency and throughput when correctly tuning the JVM, reducing costs dramatically. Conversely, a modern NoSQL database architecture built on C++ like ScyllaDB is designed to be self-tuning while avoiding the wasteful garbage collection in Cassandra.

## Cassandra query language

Cassandra is not a relational database and does not use the standard query language or SQL. It uses the Cassandra query language (CQL). This would have posed a problem for admins as they would have to master a whole new language – but the good thing about Cassandra Query language is that it is very similar to SQL. It is structured to operate with rows and columns, i.e., table-based data. 

However, it does lack the flexibility that comes with the fixed schema of SQL. CQL combines the tabular database management system and the key value. It operates using the data type operations, definition operation, data definition operation, triggers operation, security operations, arithmetic operations, etc. Developers use CQL commands to write and read data from the database.

CQL’s simple API provides an abstraction layer that keeps Cassandra’s internal storage structure and implementation details hidden. Native syntaxes for collections and other common encodings are also included.

Developers can interact with Cassandra using the CQL shell interface, cqlsh, on the command line of a node. The cqlsh prompt can be used to create and modify keyspaces and tables, make changes to data, insert and query tables, and more.

If you prefer a command line tool and use Astra DB, definitely take a look at the Astra CLI. It will install and configure CQLSH for you to work with your cloud-managed database service instance. You can also use it to manage, operate and configure your Astra DB instance via scripts or commands in a terminal.

If you prefer a graphical tool, definitely take a look at DataStax Studio. And language drivers are available for Java (JDBC), Python (DBAPI2), Node.JS (Datastax), Go (gocql), and C++. Take a look at all the drivers DataStax provides allowing CQL statements to be passed from client to cluster and back.

### CQL vs SQL

Data access in Cassandra also required an API. The original API consisted of only three methods: insert, get and delete. Over time, these basic queries were expanded upon. The resultant API was, in time, called Cassandra Query Language (CQL). CQL appears in many ways like the ANSI Structured Query Language (SQL) used for Relational Database Management Systems (RDBMS), but CQL lacks several SQL’s specific features, such as being able to do JOINs across multiple tables. There are some commands that would be equally valid across CQL and SQL. On the other hand, there are dissimilar capabilities between the two query languages. Thus, even though CQL and SQL bear a great deal of similarity, Cassandra is formally classified as a NoSQL database.

As mentioned earlier, because of their many similarities, developers with SQL experience should be able to get to work fast in CQL.

Just like SQL, CQL stores data in tables containing rows and columns. Many interactions and implementations are the same, such as retrieving all the rows in a table, and how permissions and resources of entities are controlled. If you have a handle on SQL statements like SELECT, INSERT, UPDATE, and DELETE, CQL should be a snap.

That said, there are some differences. For example, in SQL any column can be included in the WHERE clause, whereas in CQL only columns that are strictly declared in the primary key can be used as a restricting column. Also, each query must have a partition key defined at a minimum in CQL.

### CQL major data types

CQL comes with many built-in data types. Let’s review some of the key ones.

#### String types

Two data types are included to represent text. Either of the data types, text or varchar, can be used to create an UTF-8-character string—the more recent, commonly used text standard that supports interna. To handle legacy data in ASCII format, CQL also includes the ascii type.

#### Numeric types

Numeric types in CQL are similar to those found in Java and other languages. They include integers, decimals, and floating-point numbers.

#### Date and time types

CQL provides data types for dates, date ranges, time, timestamps, and duration (in months, days, and nanoseconds).

#### Geo-spatial types

Data types to handle spatial and geospatial searches are provided. They can be used to index and query latitude and longitude location data, as well as point and shape data.

#### Collection types

CQL supports collections — storing multiple values in a single column. Use collections to store or denormalize small amounts of data, such as phone numbers, tags, or addresses. Collections are not appropriate for data that is expected to grow unbounded, such as all events for a particular user. In those cases, use a table with clustering columns.

#### Other CQL data types

Several other data types are available to handle special situations. For example, CQL includes the blob type for storing binary data, boolean for true or false values, and counter to define counter columns. It also includes unique identifier types.

## Cassandra use cases

### E-commerce

E-commerce is an extremely sensitive field that cuts across every region and country. The nature of financial markets means anticipated peak times as well as downtimes. For a finance operation, no customer would want to experience downtime or lack of access when there is revenue to be earned and lots of opportunities to hold on to. E-commerce companies can avoid these downtimes or potential blackouts by using a highly reliable system like Cassandra. Its fault tolerance allows it to keep running even if a whole center is damaged with little or no hitch in the system. 

Due to its easy scalability, especially in peak seasons, E-commerce and inventory management is also a significant application of Cassandra. When there is a market rush, the company has to increase the ability of the database to carry and store more data. The seasonal, rapid E-commerce growth that is affordable and does not cause system restart is simply a perfect fit for companies. 

E-commerce websites also benefit from Cassandra as it stores and records visitors’ activities. It then allows analytical tools to modulate the visitor’s action and, for instance, tempts them to stay on the website. 

### Entertainment websites

With the aid of Cassandra, websites for movies, games and music can keep track of customer behavior and preferences. The database records for each visitor, including what was clicked, downloaded, time spent, etc. This information is analyzed and used to recommend further entertainment options to the end-user. 

This application of Cassandra falls under the personalization, recommendation and customer experience use cases. It is not just limited to entertainment sites, but also online shopping platforms and social media recommendations. This is why users would receive notifications of similar goods to what they spent time browsing. 

### IoT

Today’s world is seeing the rise of the Internet of Things (IoT). We are steadily bombarded with thousands of new information points or datasets. Every wearable device, weather sensor, traffic sensor, or mobile device keeps track of and sends data on weather, traffic, energy usage, soil conditions, etc. This flood of information can be overwhelming and easily lost. 

However, storing and analyzing information from IoT devices, no matter how large, has become much more effective on Cassandra technology. This is due to (but not limited to) the following reasons: 

- Cassandra allows every individual node to carry out read and write operations.
- It can handle and store a large amount of data.
- Cassandra supports the analysis of data in real-time.

### Messaging

There are currently several messaging applications in use, and an ever-growing number of individuals are using them. This creates the need for a stable database system to store ever-flowing information volumes. Cassandra provides both stability and storage capacity for companies that offer messaging services. 

### Asset management

Cassandra is used in logistics and asset management to track the movement of any item to get transported. From the purchase to the final delivery, applications can rely on Cassandra to log each transaction. This is especially applicable to large logistic companies regularly processing vast amounts of data. Cassandra had found a robust use case in backend development for such applications. It stores and analyzes data flowing through without impacting application performance. 

## Comparing Cassandra to other databases

### Cassandra vs relational databases

Below are the differences between Cassandra and relational databases

<img width="494" alt="image" src="https://github.com/user-attachments/assets/45d46974-1fac-4235-9800-a5b33fa675e2">

### Cassandra vs DynamoDB

Apache Cassandra and DynamoDB are both NoSQL databases that are often selected for geographically distributed applications that are growing fast and require low latency. DynamoDB is often selected for its simplified administration and maintenance vs Cassandra. Cassandra is often selected vs DynamoDB due to lower costs, its lower costs at scale than DynamoDB, as well as the additional control and flexibility associated with it being an open source database.

#### Replication

NoSQL data stores such as DynamoDB and Cassandra use multiple data copies to ensure durability and high availability. With Cassandra, the number of replicas per cluster is the replication factor and the user can control it.

In contrast, with DynamoDB, data is located in a single region by default and replicates to three availability zones there. For multi-region replication, Amazon streams must be enabled. However, DynamoDB limits the number of tables in an AWS region to 256, while in Cassandra the practical limit is about 500 tables.

The maximum item size in DynamoDB is 400KB. In Cassandra, the practical limit is a few megabytes although the hard limit is 2GB.

#### Keys and clustering

Because it is a schemaless database, only the primary key DynamoDB attributes need to be defined when the table is created. However, consider the costs of read and write throughput at the time of table and application design.

The DynamoDB primary key and sort key can each have only one attribute. Cassandra allows multiple clustering columns and composite partition keys. Cassandra supports different data types from DynamoDB types.

To set up clusters, both Cassandra and DynamoDB demand capacity planning, but their approaches are different. Creating capacity for a performant Cassandra cluster requires a good data model, a properly sized cluster, and the right hardware. With DynamoDB, the type of read/write capacity modes selected determines the nature of capacity planning.

The hashed value of both Cassandra and AWS DynamoDB partition keys form the basis for data grouping and distribution. These are called grouping partitions in both systems, but they are defined in very different ways based on size, partition key values, and limits.

#### Accessing data

Cassandra uses Cassandra Query Language (CQL) to access data, an SQL-like language. In DynamoDB JSON is the syntax.

#### TTL

The Time To Live (TTL) feature removes items from a table automatically after a specific period of time. In Cassandra TTL is the number of seconds from row creation or update, while TTL is a timestamp value that represents a specific expiration time and date in DynamoDB. Cassandra applies TTL to the column, while DynamoDB applies it at item level.

#### Consistency

Since both DynamoDB and Cassandra are distributed systems, they always face a tradeoff between consistency and availability, which leads to two possible consistency states:

Eventual consistency. Eventually consistent systems maintain speed, but reads may return stale data until all copies are consistent; updates reach all replicas, but eventually.
Strong consistency. Strongly consistent systems return up-to-date data for all prior successful writes but decrease availability and reduce response time.
The DynamoDB default is eventual consistency although it supports eventually consistent and strongly consistent reads on a per query basis.

Strongly consistent reads in DynamoDB may not be available in case of outage or delay, and the operation can have higher latency. Global secondary indexes (GSIs) do not support strongly consistent reads. Strongly consistent reads also cost more than eventually consistent reads as they use more throughput capacity.

Cassandra offers strong, tunable consistency for both reads and writes, but again, increasing latency is a tradeoff.

#### Encryption

Both Cassandra and DynamoDB use encryption for inter-node and client communication. DynamoDB encryption at rest also exists. The principle of “last write wins” applies only to strongly consistent reads and global tables for the sake of DynamoDB consistency.

#### Scans

Scans are costly for both Cassandra and DynamoDB. Cassandra must scan all nodes in the cluster, making the process slow. DynamoDB scans are faster, but also more expensive, because DynamoDB resource use is based on the data amounts returned. DynamoDB will generate errors if the scan exceeds your provisioned DynamoDB read capacity.

#### Advantages

DynamoDB advantages include an absence of database management burden; an easy start; plenty of availability, flexibility, and auto scaling; built-in monitoring metrics; and at-rest data encryption. DynamoDB is commonly selected by organizations making extensive use of AWS products.

Cassandra’s main advantages include constant availability; relatively fast read and write speeds; reliable cross data center replication; linear scalability; Cassandra Query Language which is familiar and SQL-like rather than DynamoDB’s complex API; and generally high performance. Cassandra is a better choice for applications that demand strong read consistency, teams that need open source tools such as Apache Spark, Apache Kafka, or ElasticSearch, or organizations that run their own data centers or use cloud providers other than AWS.

### Cassandra vs MongoDB

#### Cassandra

Cassandra is a distributed NoSQL database known for its scalability, high availability and fault tolerance. Some of its key features include:

- Distributed Architecture: Cassandra is designed to run on multiple nodes across multiple data centers, providing high availability and scalability by distributing data across the cluster.
- Linear Scalability: As new nodes are added to the cluster, Cassandra can easily scale out to handle increased load without downtime or application interruption.
- High Availability: Data is replicated across multiple nodes in the cluster, ensuring that if a node fails, data can still be accessed from other nodes, providing continuous availability.
- Fault Tolerance: Cassandra is fault-tolerant, meaning it can withstand node failures and network partitions without losing data or availability.
- Schema-Free: Unlike traditional relational databases, Cassandra is schema-free, allowing you to store different types of data in the same table without defining a rigid schema.

#### MongoDB

MongoDB is a well-liked NoSQL database that stores data as flexible, scalable documents. Some key features of MongoDB include:

- Document-Oriented: MongoDB stores data in flexible, JSON-like documents, making it easy to work with data in a natural and intuitive way.
- Schemaless: MongoDB does not require a predefined schema, allowing you to easily change the structure of your documents as your application evolves.
- Highly Scalable: MongoDB is designed to scale out horizontally, allowing you to easily scale your database across multiple servers to handle increasing amounts of data.
- Highly Available: MongoDB supports replica sets, which provide automatic failover and data redundancy to ensure high availability of your data.
- Flexible Query Language: MongoDB supports a rich query language that allows us to perform complex queries on your data, including queries that span multiple documents and collections.
- Indexes: MongoDB supports indexes to improve the performance of your queries, including single-field, compound, and geospatial indexes.

#### Querying

Cassandra:
- Query Language: Cassandra uses CQL (Cassandra Query Language) for querying data. CQL is similar to SQL in syntax but is designed specifically for Cassandra’s data model.
- Data Model: Cassandra is based on a wide-column store data model, which means that data is stored in rows and columns. It is optimized for write-heavy workloads and is designed to be highly scalable and fault-tolerant.

MongoDB:
- Query Language: MongoDB uses a query language that is based on JSON-like documents. Queries are expressed using a rich and flexible syntax that allows for complex queries and aggregations.
- Data Model: MongoDB uses a document-oriented approach, storing data as JSON-like documents. It is designed to be flexible and scalable and making it suitable for a wide range of use cases.

#### Conclusion

Both Cassandra and MongoDB are popular NoSQL databases, but they have different use cases. If you’re focusing on MongoDB for full-stack development, the Full Stack Development with Node JS course provides in-depth lessons on building scalable applications with MongoDB.

<img width="740" alt="image" src="https://github.com/user-attachments/assets/3678d197-9e5f-4a4b-a615-5b0032e51f56">

##### How do Cassandra and MongoDB store data?

Cassandra: Cassandra uses a partitioned row store data model, distributing data across a cluster based on the primary key. Each part of the data is saved on a separate server.

MongoDB: MongoDB stores data in BSON documents within collections. Documents can contain nested structures and vary in structure within a collection.

##### How do Cassandra and MongoDB handle scalability?

Cassandra: Cassandra is highly scalable, allowing you to add more nodes to handle increased load. It spreads out the work across many servers so that if one server fails, the whole system doesn’t stop working.

MongoDB: MongoDB also scales horizontally, using sharding to distribute data across multiple nodes. It’s good at managing big amounts of data and handling a lot of writing at the same time.

##### What about the performance of Cassandra vs. MongoDB?

Cassandra: Cassandra is optimized for write-heavy workloads and provides high write throughput and low latency. It also offers good read performance, especially for linear scans.

MongoDB: MongoDB offers fast read and write operations, especially for simple queries. However, complex queries and aggregations can be slower compared to Cassandra.

##### Which database, Cassandra or MongoDB, is simpler to manage?

Cassandra: Managing Cassandra can be complex, requiring careful configuration and monitoring of the cluster. It may be more challenging for beginners.

MongoDB: MongoDB is generally considered easier to manage, especially for smaller deployments. It has a more flexible schema and requires less upfront configuration.

##### Is MongoDB good for reading or writing?

MongoDB is known for its fast read and write operations, making it suitable for applications that require high-performance reads and writes. However, performance can vary depending on the workload and configuration.

### Cassandra vs Redis

#### Data model

Cassandra uses a wide-column store as a primary database model, making it easy to store huge databases. The wide-column store acts as a two-dimensional key-value store as the record keys are not fixed in this model.

While on the other hand, Redis uses a key-value store as a primary database and that helps the tool to be more dynamic and handle varying datasets. It is also used as a message broker process, and queuing process.

#### Latency

Cassandra is more focussed on giving you stability, and hence like SQL, you can store huge data sets. But, it is slower in speed than that of Redis.

Redis is much faster than Cassandra, but it gets slower if you use it for huge data sets and is ideally suited for rapidly changing datasets.

#### Architecture

Cassandra focuses on CP (Consistency, Partition Tolerance) of CAP (Consistency, Availability, and Partition Tolerance) theorem. It makes it a more favorable alternative in the financial services domain.

On the other hand, Redis focuses on AP (Availability, and Partition Tolerance) part of CAP (Consistency, Availability, and Partition Tolerance) theorem. This makes the tool more useful in dynamically changing database solutions like real-time analytics or data analytics.

#### Use cases

Cassandra is more useful when you have distributed, linearly scalable, write-oriented, and democratic peer to peer database or data structure. Hence it is used more in transaction logging, health care data storage, telematics for automotive, and weather services.

Redis is more useful when you have in-memory data storage, vertically scalable, and read-oriented data structure and dynamic database.

Hence it is used more in session caching, queuing, counting, publish-subscribe pattern, and in full-page caching. Redis is more useful when you have in-memory data storage, vertically scalable database.

Also, it is useful when the database is read-oriented & dynamic. Hence it is used more in session caching, queuing, counting, publish-subscribe pattern, and in full-page caching.

MongoDB differs from Cassandra and Redis in terms of a primary database as it uses the document store. MongoDB is written in C++, while Cassandra is written java and Redis in C.

#### Conclusion

MongoDB stores data in JSON format while Redis stores in key-value stores and Cassandra in a wide-columns store. MongoDB scales lot easier than either Redis or Cassandra. MongoDB also allows more flexibility than Redis and Cassandra.

Key Takeaways:

From our comparison, we can say that both the tools have their pros and cons. Cassandra is more useful when you have huge but static data, while Redis is more useful when the data is dynamic and the data is not too large.

## Cassandra advantages

### Open-source availability

Nothing is more exciting than getting a handy product for free. This is probably one of the significant factors behind Cassandra’s far-reaching popularity and acceptance. Cassandra is among the open-source products hosted by Apache and is free for anyone who wants to utilize it. 

Open source technologies are attractive because of their affordability and extensibility, as well as the flexibility to avoid vendor lock-in. Organizations adopting open source report higher speed of innovation and faster adoption.

### Distributed footprint

Another feature of Cassandra is that it is well distributed and meant to run over multiple nodes as opposed to a central system. All the nodes are equal in significance, and without a master node, no bottleneck slows the process down. This is very important because the companies that utilize Cassandra need to constantly run on accurate data and can not tolerate data loss. The equal and wide distribution of Cassandra data across nodes means that losing one node does not significantly affect the system’s general performance. 

Since every Cassandra node is capable of performing read and write operations, data is quickly replicated across hybrid cloud environments and geographies. If a node fails, users will be automatically routed to the nearest healthy node, leaving no single point of failure. They won’t even notice that a node has been knocked offline because applications behave as designed even in the event of failure. As a result, applications are always available and data is always accessible and never lost. What’s more, Cassandra’s built-in repair services fix problems immediately when they occur — without any manual intervention. Productivity doesn’t need to take a hit if nodes fail.

### Scalability

Cassandra has elastic scalability. This means that it can be scaled up or down without much difficulty or resistance. Cassandra’s scalability once again is due to the nodal architecture. It is intended to grow horizontally as your needs as a developer or company grow. Scaling-up in Cassandra is very easy and not limited to location. Adding or removing extra nodes can adjust your database system to suit your dynamic needs. 

Another exciting point about scaling in Cassandra is that there is no slow down, pause or hitch in the system during the process. This means end-users would not feel the effect of whatever happened, ensuring smooth service to all individuals connected to the network.

The majority of traditional relational databases feature a primary / secondary architecture. In these configurations, a single primary replica performs read and write operations, while secondary replicas are only able to perform read operations. Downsides to this architecture include increased latency, higher costs, and lower availability at scale. With Cassandra, no single node is in charge of replicating data across a cluster. Instead, every node is capable of performing all read and write operations. This improves performance and adds resiliency to the database.

Today’s leading enterprises are increasingly moving to multi-data center, hybrid cloud, and even multi-cloud deployments to take advantage of the strengths of each, without getting locked into any single provider’s ecosystem. By placing data on different machines, it proves easy data distribution with no single point of failure. Getting the most out of multi-cloud environments, however, starts with having an underlying cloud database that offers scalability, security, performance, and availability.

### Fault tolerance

Cassandra is fault-tolerant primarily because of its data replicative ability. Data replication denotes the ability of the system to store the same information at multiple locations or nodes. This makes it highly available and tolerant of faults in the system. Failure of a single node or data center does not bring the system to a halt as data has been replicated and stored across other nodes in the cluster. Data replication leads to a high level of backup and recovery. 

### Schema free

SQL is a fixed schema database language making it rigid and fixed. However, Cassandra is a schema-optional data model and allows the operator to create as many rows and columns as is deemed necessary. 

### Tunable consistency

Cassandra has two types of consistency – the eventual consistency and the setting consistency. The string consistency is a type that broadcasts any update or information to every node where the concerned data is located. In eventual consistency, the client has to approve immediately after a cluster receives a write. 

Cassandra’s tunable consistency is a feature that allows the developer to decide to use any of the two types depending on the function being carried out. The developer can use either or both kinds of consistency at any time. 

Cassandra was designed to operate originally as an “AP”-mode database. However, it is not as simple as that. Cassandra supports “tunable” consistency, meaning that each different database transaction can have a different consistency level, including requiring quorum (where a majority, or n/2+1 of the nodes agree) or for all replicas to return the same data.

Cassandra also supports Paxos, a consensus algorithm that utilizes lightweight transactions (LWT). With this feature, Cassandra added a serial consensus, both for the local cluster as well as for cross-datacenter transactions. This allows linearizability of writes.

With lightweight transactions and a consensus protocol like Paxos, Cassandra can operate somewhat similar to a “CP”-mode database. However, even with these “CP”-oriented features for consistency, it remains classified as an “AP”-mode database.

### Fast writes

Cassandra is known to have a very high throughput, not hindered by its size. Its ability to write quickly is a function of its data handling process. The initial step taken is to write to the commit log. This is for durability to preserve data in case of damage or node downtime. Writing to the commit log is a speedy and efficient process using this tool. 

The next step is to write to the “Memtable” or memory. After writing to Memtable, a node acknowledges the successful writing of data. The Memtable is found in the database memory, and writing to in-memory is much faster than writing to a disk. All of these account for the speed Cassandra writes. 

### Peer-to-peer architecture

Cassandra is built on a peer-to-peer architectural model where all nodes are equal. This is unlike some database models with a “slave to master” relationship. That is where one unit directs the functioning of the other units, and the other unit only communicates with the central unit or master. In Cassandra, different units can communicate with each other as peers in a process called gossiping. This peer-to-peer communication eliminates a single point of failure and is a prominent defining feature of Cassandra.

## Cassandra disadvantages

- Firstly, there is no official documentation from Apache, which makes it necessary to take the risk of sourcing the tool from third-party platforms.

- Cassandra does not provide support for relational and ACID database properties.

- While Cassandra provides superior performance in write operations, read operations are sub-optimal.

- Latency issues are a common problem when managing large amounts of data and requests.

- Cassandra also does not provide support for aggregates and subqueries.

- Cassandra stores the same data multiple times as it is based on queries, which in turn results in Java Memory Model (JVM) issues.

- Complexity in Data Modeling: Requires careful planning of data models to ensure efficient queries.

- Consistency Trade-Off: While consistency can be tuned, achieving strong consistency across all operations can be challenging.

- Operational Complexity: Managing and tuning a Cassandra cluster for optimal performance requires expertise.

Apache Cassandra is inappropriate for small data sets (smaller than, say, dozens of gigabytes), when database scalability or availability are not vital issues, or when there are relatively low amounts of transactions.

It is also important to remember Apache Cassandra is an open source NoSQL database that uses its own CQL query language, so it should be used when data models do not require normalized data with JOINs across tables which are more appropriate for SQL RDBMS systems.

## Cassandra deployment and setup

Ultimately, Cassandra is deployment agnostic. It doesn’t care where you put it – on prem, a cloud provider, multiple cloud providers. You can use a combination of those for a single database. That gives software developers the maximum amount of flexibility.

<img width="548" alt="image" src="https://github.com/user-attachments/assets/06d7162a-d70e-49c8-932b-1134b5619f75">

Because Cassandra is currently one of the most popular databases in the world, there are many integrations made for it to interoperate with other open source and commercial big data projects.

Some of these include the above-mentioned integrations to adapt Cassandra to support new data models and use cases, such as time series data (KairosDB) or graph database models (JanusGraph). Others are for integration with streaming data solutions like Apache Kafka, or Lightbend’s Akka toolkit.

There are also Cassandra integrations with big data analytics systems. Some good examples of this include pairing Cassandra with Apache Spark, Hadoop (Pig/Hive), search engines (such as Solr or Elasticsearch), and fast in-memory deployment solutions (Apache Ignite).

As well, there are various tools and technologies to virtualize, deploy and manage Cassandra, with implementations for Docker, Kubernetes, and Mesosphere DC/OS among others.

Apache Cassandra, being open source, has also been implemented within many products and services as an underlying database. For example, VMWare’s vCloud Director.

For application developers, the broad popularity of Cassandra has meant that there are clients written to connect to it from many different programming languages including:

<img width="561" alt="image" src="https://github.com/user-attachments/assets/681e0a80-b5b1-4403-93cf-d0570ecbc82b">

Cassandra has spawned a number of databases that extend Cassandra capabilities, or work using its APIs.

- Datastax Enterprise — a commercialized variant of Cassandra that provides additional features. Also supports a commercial cloud-hosted version.

- Microsoft Cosmos DB — a commercialized, cloud-hosted database that supports a Cassandra CQL-compatible API.

- Amazon Keyspaces (for Apache Cassandra) — a hybrid of Apache Cassandra for its CQL interface and DynamoDB for scalability. Formerly known as Amazon Managed Cassandra Service. (Read more.)

- Yugabyte — an open-source database that supports a Cassandra CQL-compatible API. Also has a commercial cloud-hosted version.
