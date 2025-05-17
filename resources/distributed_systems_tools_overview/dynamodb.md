# DynamoDB

## What is DynamoDB

Amazon DynamoDB is a serverless, NoSQL, fully managed database with single-digit millisecond performance at any scale.

DynamoDB addresses your needs to overcome scaling and operational complexities of relational databases. DynamoDB is purpose-built and optimized for operational workloads that require consistent performance at any scale. For example, DynamoDB delivers consistent single-digit millisecond performance for a shopping cart use case, whether you've 10 or 100 million users. Launched in 2012, DynamoDB continues to help you move away from relational databases while reducing cost and improving performance at scale.

Serverless database with no server provisioning, patching, or management required. There's no software to install, maintain, or operate, with zero downtime maintenance.

Global tables provide a multi-Region, multi-active database with up to 99.999% availability SLA, providing you with fast local reads and writes with increased application resilience.

Features include DynamoDB streams for building serverless event-driven applications and zero-ETL integration with Amazon OpenSearch Service for powerful search capabilities without the need to design, build, or maintain complex data pipelines.

Reliability is supported with managed backups, point-in-time recovery, and a broad set of security controls and compliance standards.

For events, such as Amazon Prime Day, DynamoDB powers multiple high-traffic Amazon properties and systems, including Alexa, Amazon.com sites, and all Amazon fulfillment centers. For such events, DynamoDB APIs have handled trillions of calls from Amazon properties and systems. DynamoDB continuously serves hundreds of customers with tables that have peak traffic of over half a million requests per second. It also serves hundreds of customers whose table sizes exceed 200 TB, and processes over one billion requests per hour.

As mentioned before, DynamoDB is a key-value store database that uses a documented-oriented JSON data model. Data is indexed using a primary key composed of a partition key and a sort key. There is no set schema to data in the same table; each partition can be very different from others. Unlike traditional SQL systems where data models can be created long before needing to know how the data will be analyzed, with DynamoDB, like many other NoSQL databases, data should be modeled based on the types of queries you seek to run.

We'll not further discuss the characteristics of DynamoDB

### Serverless

With DynamoDB, you don't need to provision any servers, or patch, manage, install, maintain, or operate any software. DynamoDB provides zero downtime maintenance. It has no versions (major, minor, or patch), has no version upgrades, and there are no downtime from maintenance.

DynamoDB's on-demand capacity mode offers pay-as-you-go pricing for read and write requests so you only pay for what you use. With on-demand, DynamoDB instantly scales up or down your tables to adjust for capacity and maintains performance with zero administration. It also scales down to zero so you don't pay for throughput when your table doesn't have traffic and there are no cold starts.

### NoSQL

To support a wide variety of use cases, DynamoDB supports both key-value and document data models.

Unlike relational databases, DynamoDB doesn't support a JOIN operator. We recommend that you denormalize your data model to reduce database round trips and processing power needed to answer queries.

### Fully managed

As a fully managed database service, DynamoDB handles the undifferentiated heavy lifting of managing a database so that you can focus on building value for your customers. It handles setup, configurations, maintenance, high availability, hardware provisioning, security, backups, monitoring, and more. This ensures that when you create a DynamoDB table, it's instantly ready for production workloads. DynamoDB constantly improves its availability, reliability, performance, security, and functionality without requiring upgrades or downtime.

On the back end, DynamoDB “automatically spreads the data and traffic for a table over a sufficient number of servers to meet the request capacity specified by the customer.” Furthermore, DynamoDB would replicate data across multiple AWS Availability Zones to provide high availability and durability.

### Single-digit millisecond performance at any scale

DynamoDB was purpose-built to improve upon the performance and scalability of relational databases to deliver single-digit millisecond performance at any scale. To achieve this scale and performance, DynamoDB is optimized for high-performance workloads and provides APIs that encourage efficient database usage. It omits features that are inefficient and non-performing at scale, for example, JOIN operations.

### Storage format

Storage for DynamoDB is in SSD.

To manage data, DynamoDB uses hashing and b-trees. While DynamoDB supports JSON, it only uses it as a transport format; JSON is not used as a storage format. Much of the exact implementation of DynamoDB’s data storage format remains proprietary. Generally a user would not need to know about it. Data in DynamoDB is generally exported through streaming technologies or bulk downloaded into CSV files through ETL-type tools like AWS Glue. As a managed service, the exact nature of data on disk, much like the rest of the system specification (hardware, operating system, etc.), remains hidden from end users of DynamoDB.

In DynamoDB you would redesign the data model so that everything was in a single table, denormalized, and without JOINs. This leads to the lack of deduplication you get with a normalized database, but it also makes a far simpler query.

It is important to remember that DynamoDB does not use SQL at all. Nor does it use the NoSQL equivalent made popular by Apache Cassandra, Cassandra Query Language (CQL). Instead, it uses JSON to encapsulate queries.

```bash
{
    TableName: "Table_X"
    KeyConditionExpression: "LastName = :a",
    ExpressionAttributeValues: {
        :a = "smith"
    }
}
```

### Consistency

DynamoDB is a distributed database that offers two consistency models for reading data: eventually consistent and strongly consistent. Eventual consistency is the default option, and it maximizes read throughput.

Because of its availability in three geographically data centres, It consists of two different types of consistency models:

<img width="312" alt="image" src="https://github.com/user-attachments/assets/35523307-a571-410f-a84f-13eae62678f3">


Eventual consistency means that responses to a read request may not reflect the most recent write operation. However, if you repeat the read request after a short time, the response should eventually return the more recent item

A strongly consistent read returns a result that reflects all writes that received a successful response prior to the read.

Note: If your application wants the data from DynamoDB table immediately, then choose the Strongly Consistent Read model. If you can wait for a second, then choose the Eventual Consistent Model.

### Throughput

DynamoDB throughput capacity depends on the read/write capacity modes for performing read/write operation on tables:

<img width="316" alt="image" src="https://github.com/user-attachments/assets/57249ba6-58be-4fe2-8d87-2cff77bf8e66">

#### Provisioned mode

- It defines the maximum amount of capacity that an application can use from a specified table.
- In a provisioned mode, you need to specify the number of reads and writes per second required by the application.
- If the limit of Provisioned mode throughput capacity is exceeded, then this leads to the request throttling.
- A provisioned mode is good for applications that have predictable and consistent traffic.

The Provisioned mode consists of two capacity units:
- Read Capacity unit
- Write Capacity unit

##### Read capacity unit

- The total number of read capacity units depends on the item size, and read consistency model.

- Read Capacity unit represents two types of consistency models:

- Strongly Consistent model: Read Capacity Unit represents one strong consistent read per second for an item up to 4KB in size.

- Eventually Consistent model: Read Capacity Unit represents two eventually consistent reads per second for an item up to 4KB in size.

- DynamoDB will require additional read capacity units when an item size is greater than 4KB. For example, if the size of an item is 8KB, 2 read capacity units are required for strongly consistent read while 1 read capacity unit is required for eventually consistent read.

##### Write capacity unit

The total number of write capacity unit depends on the item size.
Only 1 write capacity unit is required for an item up to size 1KB.
DynamoDB will require additional write capacity units when size is greater than 1KB. For example, if an item size is 2KB, two write capacity units are required to perform 1 write per second.
For example, if you create a table with 20 write capacity units, then you can perform 20 writes per second for an item up to 1KB in size.

#### On-demand mode

- DynamoDB on-demand mode has a flexible new billing option which is capable of serving thousands of requests per second without any capacity planning.

- On-Demand mode offers pay-per-request pricing for read and write requests so that you need to pay only for what you use, thus, making it easy to balance costs and performance.

- In On-Demand mode, DynamoDb accommodates the customer's workload instantly as the traffic level increases or decreases.

- On-Demand mode supports all the DynamoDB features such as encryption, point-in-time recovery, etc except auto-scaling

- If you do not perform any read/write, then you just need to pay for data storage only.

- On-Demand mode is useful for those applications that have unpredictable traffic and database is very complex to forecast.

### TTL

Time-to-Live (TTL). The Time-to-Live (TTL) process allows users to set timestamps for automatic deletion of expired table data. This reduces manual deletion costs and DynamoDB storage size.

## How does DynamoDB work?

### Short answer

• They do consistent hashing to partition data

• They use virtual nodes to avoid hot shards

• They replicate data across many servers for durability

• They use sloppy quorum for data consistency

• They use vector clocks to find the latest data version

• They allow the client logic to resolve data conflicts

• They use hinted handoff to handle temporary failures

• They use Merkle trees to synchronize servers and handle permanent failures

• They use gossip protocol for service discovery and failure detection

### Long answer

AWS DynamoDB automatically scales throughput capacity to meet workload demands and partitions and re-partitions your data as your table size grows. Here is how it’s done:

Monitoring: CloudWatch is the central pane for monitoring the performance, resource utilization, and operational health of DynamoDB. CloudWatch keeps an eye on the various metrics and triggers an alarm when a threshold is breached. This can further initiate the auto-scaling of resources per the system’s configuration. (See  Figure 2.)

<img width="581" alt="image" src="https://github.com/user-attachments/assets/225b6a0e-4b94-4093-bb57-ff8a9942e85e">

Throughput: Throughput capacity is the maximum rate at which something can be produced or processed. It can be managed by DynamoDB’s auto-scaling, provisional throughput, or reserved capacity. Throughput is specified in terms of read capacity units and write capacity units: One read capacity unit represents one strongly consistent read per second, or two eventually consistent reads per second, for an item up to 4 KB in size. One write capacity unit represents one write per second for an item up to 1 KB in size.

The creation of any table or global index in DynamoDB requires specifying the object’s read and write capacity requirements. This lays the foundation for delivering high performance at a consistent pace by reserving required resources for your application.

Data Read Consistency: As mentioned earlier, as AWS DynamoDB is a NoSQL database it may not support ACID properties of a relational database. However, it still provides a degree of flexibility by supporting what are called eventually consistent reads—when a read request from a DynamoDB table does not immediately reflect the last committed transaction but does after waiting and trying again—and strongly consistent reads—when a read request returns the last saved data from the successful write transaction.

Key DynamoDB metrics and performance capabilities include:

- Tables replicate data across AWS regions automatically so globally distributed applications can access data locally for rapid read and write performance
- Scales tables up and down automatically to maintain performance and adjust for capacity
- DynamoDB performance tests reveal monthly uptime of 99.999% SLA per AWS region
- Fully managed in-memory caching dramatically reduces read time
- Backups affect neither application performance or availability—even for hundreds of terabytes
- Application performance monitoring scales up and down automatically with application traffic

## DynamoDB use cases

### Financial service applications

Suppose you're a financial services company building applications, such as live trading and routing, loan management, token generation, and transaction ledgers. With DynamoDB global tables, your applications can respond to events and serve traffic from your chosen AWS Regions with fast, local read and write performance.

DynamoDB is suitable for applications with the most stringent availability requirements. It removes the operational burden of manually scaling instances for increased storage or throughput, versioning, and licensing.

You can use DynamoDB transactions to achieve atomicity, consistency, isolation, and durability (ACID) across one or more tables with a single request. (ACID) transactions suit workloads that include processing financial transactions or fulfilling orders. DynamoDB instantly accommodates your workloads as they ramp up or down, enabling you to efficiently scale your database for market conditions, such as trading hours.

### Develop software applications

Build internet-scale applications supporting user-content metadata and caches that require high concurrency and connections for millions of users and millions of requests per second.

### Create media metadata stores

Scale throughput and concurrency for media and entertainment workloads such as real-time video streaming and interactive content, and deliver lower latency with multi-Region
replication across AWS Regions.

Media and entertainment companies use DynamoDB as a metadata index for content, content management service, or to serve near real-time sports statistics. They also use DynamoDB to run user watchlist and bookmarking services and process billions of daily customer events for generating recommendations. These customers benefit from DynamoDB's scalability, performance, and resiliency. DynamoDB scales to workload changes as they ramp up or down, enabling streaming media use cases that can support any levels of demand.

### Deliver seamless retail experiences

Use design patterns for deploying shopping carts, workflow engines, inventory tracking, and customer profiles. DynamoDB supports high-traffic, extreme-scaled events and can handle millions of queries per second.

### Scale gaming platforms

Focus on driving innovation with no operational overhead. Build out your game platform with player data, session history, and leaderboards for millions of concurrent users.

As a gaming company, you can use DynamoDB for all parts of game platforms, for example, game state, player data, session history, and leaderboards. Choose DynamoDB for its scale, consistent performance, and the ease of operations provided by its serverless architecture. DynamoDB is well suited for scale-out architectures needed to support successful games. It quickly scales your game’s throughput both in and out (scale to zero with no cold start). This scalability optimizes your architecture's efficiency whether you’re scaling out for peak traffic or scaling back when gameplay usage is low.

## Comparing DynamoDB to other databases

<img width="523" alt="image" src="https://github.com/user-attachments/assets/139e78ca-0473-4aeb-9671-3ae4abfa7b1c">

Distributed systems designed for fault tolerance are not much use if they cannot operate in a partitioned state (a state where one or more nodes are unreachable). Thus, partition-tolerance is always a requirement, so the two basic modes that most systems use are either Availability-Partition-tolerant (“AP”) or Consistency-Partition-tolerant (“CP”).

An “AP”-oriented database remains available even if it was partitioned in some way. For instance, if one or more nodes went down, or two or more parts of the cluster were separated by a network outage (a so-called “split-brain” situation), the remaining database nodes would remain available and continue to respond to requests for data (reads) or even accept new data (writes). However, its data would become inconsistent across the cluster during the partitioned state. Transactions (reads and writes) in an “AP”-mode database are considered to be “eventually consistent” because they are allowed to write to some portion of nodes; inconsistencies across nodes are settled over time using various anti-entropy methods.

A “CP”-oriented database would instead err on the side of consistency in the case of a partition, even if it meant that the database became unavailable in order to maintain its consistency. For example, a database for a bank might disallow transactions to prevent it from becoming inconsistent and allowing withdrawals of more money than were actually available in an account. Transactions on such systems are referred to as “strongly consistent” because all nodes on a system need to reflect the change before the transaction is considered complete or successful.

It was initially designed to operate primarily as an “AP”-mode database. However later Amazon introduced DynamoDB Transactions to allow the database to act in a manner similar to a “CP”-mode database. These sorts of transactions are important to perform conditional updates — for example, ensuring a record meets a certain condition before setting it to a new value. (Such as having sufficient money in an account before making a withdrawal.) If the condition is not met, then the transaction does not proceed. This type of transaction requires a read-before-write (to check for existing values), and also a subsequent check to ensure the update went through properly. While providing this level of “all-or-nothing” operational guarantee transaction performance will naturally be slower, and may in fact fail at times. For example, users may notice DynamoDB system errors such as returning HTTP 500 server errors.

However, without the use of transactions, DynamoDB is usually considered to display BASE properties:

- Basically Available
- Soft-state
- Eventually consistent

Compared to other transactional databases, like Oracle, MSSQL, or PostgreSQL, AWS DynamoDB is schemaless, meaning it does not require conformation to a rigid schema of data types, tables, etc. This, though, also comes with a tradeoff: key advantages, like consistently high performance and millisecond latency, are compromised with ACID (atomicity, consistency, isolation, and durability) properties supported by a relational database.

Compared to other NoSQL databases, AWS DynamoDB supports data models like key-value pair (see figure below), and document data structures such as JSON, XML and HTML. But DynamoDB lacks support for columnar data sets, like Cassandra and HBase, and graph models such as Orient DB.

### DynamoDB vs Cassandra

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

### DynamoDB vs MySQL

MySQL is an open source SQL server widely adopted by web and application developers. In 2008 it was acquired by Oracle; now available as both open source and proprietary enterprise editions.

MySQL and DynamoDB are distinctly different database technologies. In contrast to the DynamoDB NoSQL database, MySQL is a relational (SQL) database. [learn about the differences between SQL and NoSQL]

Relational databases like MySQL store data in tables connected with relations. Structured Query Language (SQL) is used to query the database. SQL databases are comprised of records organized into tables. In a single table, data is organized into rows, labeled with a primary key, and with many columns (columnar databases) to hold values for different kinds of data – typically large data sets. These tables are related to each other through the use of foreign keys, which join together the different tables in the database.

In contrast, the DynamoDB database type (key-value NoSQL) associates named keys to values of any type, including complex types. A key value store is useful for storing simple collections of mixed types where the data being stored would not logically contain the same columns.

### DynamoDB vs PostgreSQL

The main difference between PostgreSQL and DynamoDB is that DynamoDB is a NoSQL database engine that can support tables of any size, whereas PostgreSQL can store structured and unstructured data in a single product.

### DynamoDB vs MongoDB

#### Environment

One important difference between DynamoDB vs MongoDB is deployment environment and strategy. MongoDB is platform-agnostic and one of the leading DynamoDB alternatives.
DynamoDB is limited to Amazon Web Services (AWS).

MongoDB can be configured to run virtually anywhere from a container, a local machine, or through any cloud provider. In contrast, you can only configure and use DynamoDB and DynamoDB tools through AWS. DynamoDB is a native AWS application, with much tighter integration with other AWS tools and services.

DynamoDB is fully managed, which means DynamoDB provisioning only takes a few clicks, even for multiple regions, dramatically reducing the need for dedicated management of infrastructure.

MongoDB requires users to configure and manage infrastructure for MongoDB deployments, although MongoDB Atlas offers a fully managed multi-cloud, multi-region NoSQL solution and cloud database service that can be deployed across Google Cloud, Microsoft Azure, and AWS.

#### Data model

The MongoDB data model and schema are different in that MongoDB stores data in documents using the BSON format with support for more data types and document sizes. In contrast, DynamoDB data types and document sizes are more limited. It does, however, support document data models using JSON.

MongoDB is a schema-free database, yet its built-in schema validation allows users to enforce a schema as needed, including for document structure, data types, fields, and more. In contrast, DynamoDB is schema-free and lacks the ability to enforce schemas. With both MongoDB and DynamoDB ACID compliance is possible.

#### Flexibility

MongoDB is more flexible in querying data and indexes, allowing users to aggregate data natively in multiple ways: graph traversals, JOINs, ranges, single keys, and more.

DynamoDB is less flexible, natively supporting only key-value queries. However, by enabling other AWS services such as Elastic MapReduce, it allows users to carry out complex aggregations. There is a per retrieval DynamoDB query limit of 1MB of data. However, all of these services increase complexity, cost, and latency.

MongoDB supports creating indexes and different indexing types such as array, compound, hash, TTL, text, wildcard, etc. The indexes and underlying data are strongly consistent.

DynamoDB, in contrast, supports two types of secondary indexes: DynamoDB Global Secondary Index (GSI) or DynamoDB GSI encompasses all base table data across all partitions and can be scaled and stored apart from the underlying data table. DynamoDB Local Secondary Index (LSI) or DynamoDB LSI matches the value of the table partition key to the LSI partition key, limiting the scope to the base table.

Both LSI and GSI in DynamoDB support multi-document transactions, but DynamoDB lacks support for multiple operations within a single transaction. MongoDB supports reads and writes to the same fields and documents in a single transaction.

MongoDB is more flexible than DynamoDB. It is better-suited for applications without strict latency requirements, larger documents, geospatial data, and bursty workloads. There are more available data types, and users can run MongoDB anywhere.

While it delivers impressively consistent performance, design and data modeling in DynamoDB can be more difficult—particularly for people used to working with relational databases. It’s also essential to understand global and local secondary indexes as part of DynamoDB data modeling.

#### Security

DynamoDB best practices for security are based on AWS Identity and Access Management (IAM) and managed by AWS so it is secure by default. This model offers users fine-grained control over DynamoDB roles, users, and policies.

MongoDB Atlas offers enhanced security practices, such as encryption and network solutions for authorization and authentication. In other words, you can securely manage MongoDB, but the default configuration is still more difficult to secure.

#### Backups

DynamoDB is a serverless, maintenance-free, distributed system that scales, provisions, and heals itself automatically. DynamoDB continuous backup is part of on-demand, automated, point-in-time recovery.

MongoDB Atlas requires more configurations than DynamoDB, but also supports continuous and on-demand cloud backups and allows users to provision and manage MongoDB clusters across various multi-cloud environments.

#### Latency

MongoDB Atlas delivers significantly better query performance than what you would find with DynamoDB because it stores query data in RAM. MongoDB Atlas may be the best choice if speed is a concern and the data set fits in RAM.

#### Vendor lock-in

A major downside to using DynamoDB is vendor lock-in, which can leave users without the ability to easily change the deployment environment. This makes it harder to focus on a multi-cloud strategy.

#### Cost

DynamoDB pricing is lower for those who have heavily invested in the AWS ecosystem, in the form of seamless integration with services and tools. It’s less complex and simpler to manage a multi-tiered DynamoDB architecture that supports all organizational cloud services consolidated into one cloud provider.

However, capacity management can be a serious challenge for DynamoDB users. DynamoDB autoscaling provisioned capacity is best suited for large, relatively predictable tables. Smaller tables or more unpredictable traffic can cause higher costs. Most workloads hosted on MongoDB clusters do not scale as well with a single API call but are cheaper overall with respect to data storage than DynamoDB.

Both DynamoDB and MongoDB Atlas support encryption of data at rest.

### DynamoDB vs DocumentDB

The DynamoDB DocumentDB comparison starts with both being non-relational databases, but with different purposes. Amazon DynamoDB is a serverless key-value database that delivers scalable, rapid performance, while Amazon DocumentDB is a fully managed, JSON NoSQL document database service that supports MongoDB workloads.

Amazon DocumentDB is partly compatible with MongoDB. DocumentDB runs atop the Amazon Aurora backend platform and mimics the MongoDB API. It is meant to serve as an alternative to and compete with MongoDB.

### DynamoDB vs Redis

Redis (Remote Dictionary Server) is an open-source, fast, NoSQL database and among the leading alternatives to DynamoDB. Written in the ANSI C language, Redis works in most of the POSIX systems such as Linux, BSD, and OS X without external dependencies. Delivering sub-millisecond response times, Redis enables real-time applications in ad tech, financial services, gaming, healthcare, IoT, and social networking. It supports data structures such as bitmaps, hashes, hyperloglogs, lists, strings, sets, geospatial indexes with radius queries, and sorted sets with range queries.

The primary strength in this DynamoDB comparison is persistent storage, but Amazon DynamoDB Accelerator (DAX or DynamoDB DAX) is a highly available, fully managed, in-memory DynamoDB cache that keeps Redis and DynamoDB in about the same position and lets users retain the advantages of DynamoDB.

DAX DynamoDB accelerates DynamoDB table design without requiring management of data population, cache invalidation, or cluster management. It is easy to enable DAX in the AWS Management Console with a few clicks or by using the AWS DynamoDB SDK. DAX is also compatible with existing DynamoDB API calls.

### DynamoDB vs Aurora

Amazon Aurora is a relational database solution that is compatible with MySQL and PostgreSQL. Among its basic design principles is writing in the foreground to minimize the problem seen in DynamoDB latency.

Aurora and DynamoDB encryption at rest are both supported using encryption keys. There are three ways to use Amazon DynamoDB keys to encrypt the table. The DynamoDB AWS-owned key is free and encrypted by default. KMS will also secure stored AWS-managed keys for a fee.
And KMS Customer Management Keys (CMKs) give total control over KMS keys to users.

DynamoDB and Amazon Aurora have similar permission schemes, but Aurora also offers MySQL and PostgreSQL-compatible connection interfaces.

### DynamoDB vs Redshift

Amazon DynamoDB is a fully-managed NoSQL database service that supports both key-value and document data models. Flexible and fast, DynamoDB is often selected for applications that need scalable, consistent low latency.

Amazon Redshift is a large-scale relational database management system (DBMS) and data warehouse service that is part of the Amazon Web Services cloud-computing platform. Amazon Redshift is intended for use with business intelligence tools.

While DynamoDB does not support SQL query language, Redshift does (although it does not fully support an SQL-standard).

DynamoDB has no foreign keys because it does not account for referential integrity. Redshift does accept foreign keys, accounting for referential integrity.

While DynamoDB does not support server-side scripting, Redshift supports user-defined functions for server-side scripting in Python. Finally, Redshift supports restricted secondary indexes, while DynamoDB simply supports secondary indexes.

### DynamoDB vs S3

Amazon Simple Storage Service (Amazon S3) is a scalable, high-speed, cloud storage service. It was developed for archiving and backing up data and applications on AWS. This object store holds large amounts of binary unstructured data grouped into buckets, each associated with a region.

DynamoDB was designed to store structured textual/JSON data, although it can also store binary objects. It stores items in tables, and DynamoDB global tables support multi-master replication.

Unlike DynamoDB which was designed for low latency and sustained usage patterns, Amazon S3 was designed not for predictable latency, but for throughput. It can handle many traffic requests, even for different items, without being overwhelmed.

With DynamoDB batch write you can write or delete massive quantities of data efficiently, or copy data into DynamoDB from another database. Amazon S3 supports automatic versioning, while DynamoDB version history doesn’t automatically support object versioning, although you can refer to the DynamoDB history table for the log of the past 24 hours.

## DynamoDB advantages

### Multi-active replication with global tables

Global tables provide multi-active replication of your data across your chosen AWS Regions with 99.999% availability. Global tables deliver a fully managed solution for deploying a multi-Region, multi-active database, without building and maintaining your own replication solution. With global tables, you can specify the AWS Regions where you want the tables to be available. DynamoDB replicates ongoing data changes to all of these tables.

Your globally distributed applications can access data locally in your selected Regions to achieve single-digit millisecond read and write performance. Because global tables are multi-active, you don't need a primary table. This means there are no complicated or delayed fail-overs, or database downtime when failing over an application between Regions.

### ACID transactions

DynamoDB is built for mission-critical workloads. It includes (ACID) transactions support for applications that require complex business logic. DynamoDB provides native, server-side support for transactions, simplifying the developer experience of making coordinated, all-or-nothing changes to multiple items within and across tables.

### Change data capture for event-driven architecture

DynamoDB supports streaming of item-level change data capture (CDC) records in near-real time. It offers two streaming models for CDC: DynamoDB Streams and Kinesis Data Streams for DynamoDB. Whenever an application creates, updates, or deletes items in a table, streams records a time-ordered sequence of every item-level change in near-real time. This makes DynamoDB Streams ideal for applications with event-driven architecture to consume and act upon the changes.

### Secondary indexes

DynamoDB offers the option to create both global and local secondary indexes, which let you query the table data using an alternate key. With these secondary indexes, you can access data with attributes other than the primary key, giving you maximum flexibility in accessing your data.

### AWS Integrations

DynamoDB broadly integrates with several AWS services to help you get more value from your data, eliminate undifferentiated heavy lifting, and operate your workloads at scale. Some examples are: AWS CloudFormation, Amazon CloudWatch, Amazon S3, AWS Identity and Access Management (IAM), and AWS Auto Scaling. The following sections describe some of the service integrations that you can perform using DynamoDB:

#### Serverless integrations

To build end-to-end serverless applications, DynamoDB integrates natively with a number of serverless AWS services. For example, you can integrate DynamoDB with AWS Lambda to create triggers, which are pieces of code that automatically respond to events in DynamoDB Streams. With triggers, you can build event-driven applications that react to data modifications in DynamoDB tables. For cost optimization, you can filter events that Lambda processes from a DynamoDB stream.

The following list presents some examples of serverless integrations with DynamoDB:

AWS AppSync for creating GraphQL APIs

Amazon API Gateway for creating REST APIs

Lambda for serverless compute

Amazon Kinesis Data Streams for change data capture (CDC)

#### S3 integration

Integrating DynamoDB with Amazon S3 enables you to easily export data to an Amazon S3 bucket for analytics and machine learning. DynamoDB supports full table exports and incremental exports to export changed, updated, or deleted data between a specified time period. You can also import data from Amazon S3 into a new DynamoDB table. Data is also backed up to Amazon Simple Storage Service (S3) in order to maintain high performance on a massive scale all while preserving durability and security.

#### ETL integration

DynamoDB supports zero-ETL integration with Amazon Redshift and Using an OpenSearch Ingestion pipeline with Amazon DynamoDB. These integrations enable you to run complex analytics and use advanced search capabilities on your DynamoDB table data. For example, you can perform full-text and vector search, and semantic search on your DynamoDB data. Zero-ETL integrations have no impact on production workloads running on DynamoDB.

#### Caching integration

DynamoDB Accelerator (DAX) is a fully managed, highly available caching service built for DynamoDB. DAX delivers up to 10 times performance improvement – from milliseconds to microseconds – even at millions of requests per second. DAX does all the heavy lifting required to add in-memory acceleration to your DynamoDB tables, without requiring you to manage cache invalidation, data population, or cluster management.

DAX is a fully managed, secure, and scalable DynamoDB cache service. It is suitable for read-intensive workloads and provides major improvements in DynamoDB’s response time. DAX clusters are hosted by and run in Amazon Virtual Private Cloud (Amazon VPC). A DAX client should be installed on the Amazon EC2 instance hosting your application in VPC. All requests are routed via the DAX client, which fetches data, if available, from the DAX cluster (a cache hit).

If data is not available in the cluster, it will be extracted from DynamoDB (a cache miss). Results will be provided to your application via the DAX cluster. Caching data in DAX clusters reduces overall read requests on DynamoDB tables, which can save you money. Companies such as Tinder, Expedia, and Genesys all use DAX to enhance the customer experience by providing sub-millisecond response times to customer queries.

### Security

DynamoDB utilizes IAM to help you securely control access to your DynamoDB resources. With IAM, you can centrally manage permissions that control which DynamoDB users can access resources. You use IAM to control who is authenticated (signed in) and authorized (has permissions) to use resources. Because DynamoDB utilizes IAM, there are no user names or passwords for accessing DynamoDB. Because you don't have any complicated password rotation policies to manage, it simplifies your security posture. With IAM, you can also enable fine-grained access control to provide authorization at the attribute level. You can also define resource-based policies with support for IAM Access Analyzer and Block Public Access (BPA) to simplify policy management.

By default, DynamoDB encrypts all customer data at rest. Encryption at rest enhances the security of your data by using encryption keys stored in AWS Key Management Service (AWS KMS). With encryption at rest, you can build security-sensitive applications that meet strict encryption compliance and regulatory requirements. When you access an encrypted table, DynamoDB decrypts the table data transparently. You don't have to change any code or applications to use or manage encrypted tables. DynamoDB continues to deliver the same single-digit millisecond latency that you've come to expect, and all DynamoDB queries work seamlessly on your encrypted data. It is important to note that encryption will not cause latency or performance issues while executing DML and DDL operations.

You can specify whether DynamoDB should use an AWS owned key (default encryption type), AWS managed key, or a Customer managed key to encrypt user data. The default encryption using AWS-owned KMS keys is available at no additional charge. For client-side encryption, you can use the AWS Database Encryption SDK.

### Resilience

By default, DynamoDB automatically replicates your data across three Availability Zones to provide high durability and a 99.99% availability SLA. DynamoDB also provides additional capabilities to help you achieve your business continuity and disaster recovery objectives.

DynamoDB includes the following features to help support your data resiliency and backup needs:

#### Global tables

DynamoDB global tables enable a 99.999% availability SLA and multi-Region resilience. This helps you build resilient applications and optimize them for the lowest recovery time objective (RTO) and recovery point objective (RPO). Global tables also integrates with AWS Fault Injection Service (AWS FIS) to perform fault injection experiments on your global table workloads. For example, pausing global table replication to any replica table.

#### Continuous backups and point-in-time recovery

Continuous backups provide you per-second granularity and the ability to initiate a point-in-time recovery. With point-in-time recovery, you can restore a table to any point in time up to the second during the last 35 days.

Continuous backups and initiating a point-in-time restore doesn't use provisioned capacity. They also don't have any impact on the performance or availability of your applications.

#### On-demand backup and restore

On-demand backup and restore let you create full backups of a table for long-term retention and archival for regulatory compliance needs. Backups don't impact the performance of your table and you can back up tables of any size. With AWS Backup integration, you can use AWS Backup to schedule, copy, tag, and manage the life cycle of your DynamoDB on-demand backups automatically. Using AWS Backup, you can copy on-demand backups across accounts and Regions, and transition older backups to cold storage for cost-optimization.

### DynamoDB Scalability and High Availability

DynamoDB scalability includes methods such as autosharding and load-balancing. Autosharding means that when load on a single Amazon server gets to a certain point, the database can select a certain amount of records and place that data on a new node. Traffic between the new and existing servers is load-balanced so that, ideally, no one node is impacted with more traffic than others. However, the exact methods of how the database supports autosharding and load-balancing are proprietary, part of its internal operational mechanics, and are not visible to nor controllable by users.

## DynamoDB disadvantages

The below list provides us with the limitations of DynamoDB: 

- It has a low read capacity unit of 4kB per second and a write capacity unit of 1KB per second.
All tables and global secondary indexes must have a minimum of one read and one write capacity unit.

- Table sizes have no limits, but accounts have a 256 table limit unless you request a higher cap.

- Only Five local and twenty global secondary (default quota) indexes per table are permitted.

- DynamoDB does not prevent the use of reserved words as names.

- Partition key length and value minimum length sits at 1 byte, and maximum at 2048 bytes, however, DynamoDB places no limit on values.

### Online analytical processing (OLAP)

Systems that undertake online analytical processing and data warehousing typically demand massive amounts of data aggregation, and a normalized or relational view of data via joined dimensional tables. Because DynamoDB is a non-relational database that works better with NoSQL formatted data tables, general data structures for analytics aren’t as well supported, and DynamoDB analytics are more challenging to run.

### Querying DynamoDB

Querying DynamoDB is also more difficult as DynamoDB does not interface with SQL. This is important because most developers are more familiar with SQL than DynamoDB queries.

### Cost

DynamoDB can be very expensive. Teams pay for read and write transactions and are charged by the hour – plus storage and optional services. Benchmarks find that DynamoDB is often up to 7x more expensive than compatible database-as-a-service options with similar or better performance. Companies spend a great deal of time and engineering effort in their attempts to reduce their DynamoDB costs. [Compare costs vs Astra, Keyspaces, and ScyllaDB Cloud with this cost calculator].

While indexing can help reduce the cost of analytics processing, indexing is more expensive with DynamoDB. This is because DynamoDB’s global secondary indexes must provision additional read and write capacity to function.

### DynamoDB for relational data

DynamoDB is inappropriate for extremely large data sets (petabytes) with high frequency transactions where the cost of operating DynamoDB may make it prohibitive. It is also important to remember DynamoDB is a NoSQL database that uses its own proprietary JSON-based query API, so it should be used when data models do not require normalized data with JOINs across tables which are more appropriate for SQL RDBMS systems.

### DynamoDB migration to another alternative

There are no other direct alternatives to DynamoDB. While different NoSQL databases can provide key-value or document data models, it would require re-architecting data models and redesigning queries to achieve a DynamoDB migration to another database.

For example, you could migrate from DynamoDB to ScyllaDB using its Cassandra Query Language (CQL) interface, but it would require redesign of your data model, as well as completely rewriting your existing queries from DynamoDB’s JSON format to CQL. While this may be advantageous to take advantage of various features of ScyllaDB currently available only through its CQL interface, this requires more of a reengineering effort than a simple “lift and shift” migration.

## DynamoDB deployment and setup

You can work with DynamoDB using the AWS Management Console, the AWS Command Line Interface, NoSQL Workbench for DynamoDB, or DynamoDB APIs.

Getting started with DynamoDB – Walks you through the process of setting up DynamoDB, creating sample tables, and uploading data. This topic also provides information about performing some basic database operations using the AWS Management Console, AWS CLI, NoSQL Workbench, and DynamoDB APIs.

DynamoDB core components – Describes the basic DynamoDB concepts.

Best practices for designing and architecting with DynamoDB – Provides recommendations about NoSQL design, DynamoDB Well-Architected Lens, table design and several other DynamoDB features. These best practices help you maximize performance and minimize throughput costs when working with DynamoDB.

DynamoDB can be developed using Software Development Kits (SDKs) available from Amazon in a number of programming languages.

There are also a number of integrations for DynamoDB to connect with other AWS services and open source big data technologies, such as Apache Kafka, and Apache Hive or Apache Spark via Amazon EMR.

When you set up DynamoDB on AWS, you do not provision specific servers or allocate set amounts of disk. Instead, you provision throughput — you define the database based on provisioned capacity — how many transactions and how many kilobytes of traffic you wish to support per second. Users specify a service level of read capacity units (RCUs) and write capacity units (WCUs).

As stated above, users generally do not directly make DynamoDB API calls. Instead, they will integrate an AWS SDK into their application, which will handle the back-end communications with the server.

### DynamoDB local

DynamoDB local enables teams to develop and test applications in a dev/test environment. It is not intended or suitable for running DynamoDB on-premises in production. Since DynamoDB local is not designed for production, it does not provide high availability.

