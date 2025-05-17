# Databases

## Databases introduction

### DBMS (Database management systems)

A Database Management System (DBMS) is software that interacts with users, applications, and the database itself to capture, store, and manage data. It provides an interface for performing various operations on the data, such as inserting, updating, deleting, and retrieving data. The primary goal of a DBMS is to ensure that data remains consistent, secure, and easily accessible.

There are two main types of DBMSs:

- Relational Database Management Systems (RDBMS)
  - These systems store data in tables with predefined relationships between them. The most common query language for RDBMSs is SQL (Structured Query Language).

- Non-Relational Database Management Systems (NoSQL)
  - These systems store data in various formats, such as key-value, document, column-family, or graph. NoSQL databases are known for their ability to scale horizontally and handle unstructured or semi-structured data.

## SQL and NoSQL databases

Databases can be broadly classified into two categories: SQL (Structured Query Language) and NoSQL (Not only SQL) databases. SQL databases, also known as relational databases, are based on the relational model, where data is stored in tables with predefined schema and relationships between them. Some popular SQL databases include MySQL, PostgreSQL, Microsoft SQL Server, and Oracle. SQL databases are known for their consistency, reliability, and powerful query capabilities.

On the other hand, NoSQL databases are a diverse group of non-relational databases that prioritize flexibility, scalability, and performance under specific workloads. NoSQL databases can be further categorized into document databases, key-value stores, column-family stores, and graph databases, each with their unique data models and use cases. Some widely-used NoSQL databases are MongoDB, Redis, Apache Cassandra, and Neo4j.

### SQL vs NoSQL

#### Storage

SQL stores data in tables where each row represents an entity and each column represents a data point about that entity; for example, if we are storing a car entity in a table, different columns could be ‘Color’, ‘Make’, ‘Model’, and so on.

NoSQL databases have different data storage models. The main ones are key-value, document, graph, and columnar. We will discuss differences between these databases below.

#### Schema

In SQL, each record conforms to a fixed schema, meaning the columns must be decided and chosen before data entry and each row must have data for each column. The schema can be altered later, but it involves modifying the whole database and going offline.

In NoSQL, schemas are dynamic. Columns can be added on the fly and each ‘row’ (or equivalent) doesn’t have to contain data for each ‘column.'

#### Querying

SQL databases use SQL (structured query language) for defining and manipulating the data, which is very powerful. In a NoSQL database, queries are focused on a collection of documents. Sometimes it is also called UnQL (Unstructured Query Language). Different databases have different syntax for using UnQL.

#### Scalability

In most common situations, SQL databases are vertically scalable, i.e., by increasing the horsepower (higher Memory, CPU, etc.) of the hardware, which can get very expensive. It is possible to scale a relational database across multiple servers, but this is a challenging and time-consuming process.

On the other hand, NoSQL databases are horizontally scalable, meaning we can add more servers easily in our NoSQL database infrastructure to handle a lot of traffic. Any cheap commodity hardware or cloud instances can host NoSQL databases, thus making it a lot more cost-effective than vertical scaling. A lot of NoSQL technologies also distribute data across servers automatically.

#### Reliability or ACID Compliancy (Atomicity, Consistency, Isolation, Durability)

The vast majority of relational databases are ACID compliant. So, when it comes to data reliability and safe guarantee of performing transactions, SQL databases are still the better bet.

Most of the NoSQL solutions sacrifice ACID compliance for availability, performance, and scalability.

## SQL databases

SQL (Structured Query Language) databases, also known as relational databases, are the most commonly used type of databases in software applications. They store data in tables, where each table consists of rows and columns. Relationships between tables are established using primary and foreign keys. SQL databases follow the ACID properties (Atomicity, Consistency, Isolation, Durability) to ensure reliable data transactions.

Relational databases store data in rows and columns. Each row contains all the information about one entity and each column contains all the separate data points. Some of the most popular relational databases are MySQL, Oracle, MS SQL Server, SQLite, Postgres, and MariaDB.

### RDMS concepts

- Tables
  - The fundamental building blocks of relational databases, tables represent the structure of the data. Each table contains rows (records) and columns (fields) that store individual pieces of data.

- Primary Key
  - A unique identifier for each row in a table. A primary key enforces uniqueness and ensures that no two rows share the same identifier.

- Foreign Key
  - A column (or a set of columns) in a table that refers to the primary key of another table. Foreign keys are used to establish relationships between tables and enforce referential integrity.

- Indexes
  - Database indexes are data structures that help to speed up data retrieval operations. They work similarly to the index in a book, allowing for faster lookups and searches.

- Normalization
  - The process of organizing a database into tables, columns, and relationships to reduce data redundancy and improve data integrity.

### SQL language

SQL is a standardized language for managing and querying relational databases. It provides a powerful and flexible way to interact with the data. The language consists of several components, including:

- Data Definition Language (DDL)
  - Allows for the creation, modification, and deletion of database structures, such as tables, indexes, and constraints.

- Data Manipulation Language (DML)
  - Enables data insertion, updating, deletion, and retrieval operations on database tables.

- Data Control Language (DCL)
  - Deals with user permissions and access control for database objects.

- Transaction Control Language (TCL)
  - Manages database transactions and ensures ACID compliance.

### SQL databases

Several well-known SQL databases are available, each with its own features and use cases. Some popular SQL databases include:

- MySQL
  - An open-source, widely used RDBMS, MySQL is popular for web applications and is a component of the LAMP (Linux, Apache, MySQL, PHP/Perl/Python) stack.

- PostgreSQL
  - Another open-source RDBMS that focuses on extensibility, standards compliance, and performance. PostgreSQL is well-regarded for its advanced features, such as support for custom data types, full-text search, and spatial data operations.

- Microsoft SQL Server
  - A commercial RDBMS developed by Microsoft, featuring a comprehensive set of tools and features for enterprise-level applications. SQL Server is known for its tight integration with other Microsoft products, security features, and business intelligence capabilities.

- Oracle Database
  - A widely-used commercial RDBMS that offers high performance, advanced features, and scalability. Oracle is popular in large organizations and mission-critical applications due to its robustness, reliability, and comprehensive toolset.

### SQL databases pros and cons

- ACID properties and consistency
  - SQL databases adhere to the ACID (Atomicity, Consistency, Isolation, Durability) properties, which ensure the reliability of transactions and the consistency of the data. These properties guarantee that any operation on the data will either be completed in its entirety or not at all, and that the data will always remain in a consistent state.

- Structured schema
  - SQL databases enforce a predefined schema for the data, which ensures that the data is structured, consistent, and follows specific rules. This structured schema can make it easier to understand and maintain the data model, as well as optimize queries for performance.

- Query language and optimization
  - SQL is a powerful and expressive query language that allows developers to perform complex operations on the data, such as filtering, sorting, grouping, and joining multiple tables based on specified conditions. SQL databases also include query optimizers, which analyze and optimize queries for improved performance.

- Scalability and performance
  - SQL databases can be scaled vertically by adding more resources (such as CPU, memory, and storage) to a single server. However, horizontal scaling, or distributing the data across multiple servers, can be more challenging due to the relational nature of the data and the constraints imposed by the ACID properties. This can lead to performance bottlenecks and difficulties in scaling for large-scale applications with high write loads or massive amounts of data.

## NoSQL databases

NoSQL databases, also known as "Not Only SQL" databases, are a diverse group of non-relational databases designed to address the limitations of traditional SQL databases, particularly in terms of scalability, flexibility, and performance under specific workloads. NoSQL databases do not adhere to the relational model and typically do not use SQL as their primary query language. Instead, they employ various data models and query languages, depending on the specific type of NoSQL database being used.

The key characteristics of NoSQL databases include their schema-less design, which allows for greater flexibility in handling data; horizontal scalability, which makes it easier to distribute data across multiple servers; and their ability to perform well under specific workloads, such as high write loads or large-scale data storage and retrieval.

### NoSQL databases

![image](https://github.com/user-attachments/assets/3b5aebb8-6987-4245-9407-fa84285975ed)

#### Key-value databases

Key-value databases store data as key-value pairs, where the key is a unique identifier and the value is the associated data. These databases excel in scenarios requiring high write and read performance for simple data models, such as session management and real-time analytics.

Use cases: Session management, user preferences, and product recommendations.

Examples: Amazon DynamoDB, Azure Cosmos DB, Riak.

#### In-memory key-value databases

The data is primarily stored in memory, unlike disk-based databases. By eliminating disk access, these databases enable minimal response times. Because all data is stored in main memory, in-memory databases risk losing data upon a process or server failure. In-memory databases can persist data on disks by storing each operation in a log or by taking snapshots.

Examples: Redis, Memcached, Amazon Elasticache.

#### Document databases

Document databases are structured similarly to key-value databases except that keys and values are stored in documents written in a markup language like JSON, BSON, XML, or YAML. Each document can contain nested fields, arrays, and other complex data structures, providing a high degree of flexibility in representing hierarchical and related data.

Use cases: User profiles, product catalogs, and content management.

Examples: MongoDB, Amazon DocumentDB, CouchDB.

#### Wide-column databases

Instead of ‘tables,' in columnar databases we have column families, which are containers for rows. Unlike relational databases, we don’t need to know all the columns up front and each row doesn’t have to have the same number of columns. Columnar databases are best suited for analyzing large datasets - big names include Cassandra and HBase.

Wide column databases are based on tables but without a strict column format. Rows do not need a value in every column, and segments of rows and columns containing different data formats can be combined.

Use cases: Telemetry, analytics data, messaging, and time-series data.

Examples: Cassandra, Accumulo, Azure Table Storage, HBase.

#### Graph databases

These databases are used to store data whose relations are best represented in a graph. Data is saved in graph structures with nodes (entities), properties (information about the entities), and lines (connections between the entities). Examples of graph database include Neo4J and InfiniteGraph.

Graph databases map the relationships between data using nodes and edges. Nodes are the individual data values, and edges are the relationships between those values.

Use cases: Social graphs, recommendation engines, and fraud detection.

Examples: Neo4j, Amazon Neptune, Cosmos DB through Azure Gremlin.

#### Time series databases

These databases store data in time-ordered streams. Data is not sorted by value or id but by the time of collection, ingestion, or other timestamps included in the metadata.

Use cases: Industrial telemetry, DevOps, and Internet of Things (IOT) applications.

Examples: Graphite, Prometheus, Amazon Timestream.

#### Ledger databases

Ledger databases are based on logs that record events related to data values. These databases store data changes that are used to verify the integrity of data.

Use cases: Banking systems, registrations, supply chains, and systems of record.

Examples: Amazon Quantum Ledger Database (QLDB).

### NoSQL databases

Here are some well-known NoSQL databases:

- MongoDB
  - A document-oriented database that uses the BSON format for data storage and supports horizontal scaling through sharding.

- Redis
  - An in-memory, key-value store that supports various data structures and offers fast performance for caching, message queues, and real-time analytics.

- Apache Cassandra
  - A highly scalable, distributed column-family store that provides high availability and fault tolerance, designed for handling large-scale data across many commodity servers.

- Neo4j
  - A graph database that offers powerful query capabilities for traversing complex relationships and analyzing connected data.

### NoSQL databases pros and cons

- Flexibility and schema-less design
  - One of the primary advantages of NoSQL databases is their schema-less design, which allows for greater flexibility in handling diverse and dynamic data models. This makes it easier to adapt to changing requirements and accommodate new data types without the need for extensive schema modifications, as is often the case with SQL databases.

- Horizontal scalability
  - NoSQL databases are designed to scale horizontally, enabling the distribution of data across multiple servers, often with built-in support for data replication, sharding, and partitioning. This makes NoSQL databases well-suited for large-scale applications with high write loads or massive amounts of data, where traditional SQL databases may struggle to maintain performance and consistency.

- Performance under specific workloads
  - NoSQL databases can offer superior performance under specific workloads, such as high write loads, large-scale data storage and retrieval, and complex relationships. By choosing a NoSQL database tailored to the needs of a particular application, developers can optimize performance and resource utilization while maintaining an appropriate level of data consistency and reliability.

- CAP theorem and trade-offs
  - The CAP theorem states that a distributed data store can provide only two of the following three guarantees: Consistency, Availability, and Partition Tolerance. NoSQL databases often prioritize Availability and Partition Tolerance over Consistency, resulting in a trade-off known as “eventual consistency.” While this may be acceptable in some applications, it can lead to challenges in maintaining data integrity and reconciling conflicting updates in scenarios where strong consistency is required.

- Query complexity and expressiveness
  - While some NoSQL databases offer powerful query languages and capabilities, they may not be as expressive or versatile as SQL when it comes to complex data manipulation and analysis. This can be a limiting factor in applications that require sophisticated querying, joining, or aggregation of data. Additionally, developers may need to learn multiple query languages and paradigms when working with different types of NoSQL databases.

## SQL vs NoSQL

When it comes to database technology, there’s no one-size-fits-all solution. That’s why many businesses rely on both relational and non-relational databases for different needs. Even as NoSQL databases are gaining popularity for their speed and scalability, there are still situations where a highly structured SQL database may perform better; choosing the right technology hinges on the use case.

### When to use SQL

Here are a few reasons to choose a SQL database:

- We need to ensure ACID compliance. ACID compliance reduces anomalies and protects the integrity of your database by prescribing exactly how transactions interact with the database. Generally, NoSQL databases sacrifice ACID compliance for scalability and processing speed, but for many e-commerce and financial applications, an ACID-compliant database remains the preferred option.

- Your data is structured and unchanging. If your business is not experiencing massive growth that would require more servers and if you're only working with data that is consistent, then there may be no reason to use a system designed to support a variety of data types and high traffic volume.

### When to use NoSQL

When all the other components of our application are fast and seamless, NoSQL databases prevent data from being the bottleneck. Big data is contributing to a large success for NoSQL databases, mainly because it handles data differently than the traditional relational databases. A few popular examples of NoSQL databases are MongoDB, CouchDB, Cassandra, and HBase.

- Storing large volumes of data that often have little to no structure. A NoSQL database sets no limits on the types of data we can store together and allows us to add new types as the need changes. With document-based databases, you can store data in one place without having to define what “types” of data those are in advance.

- Making the most of cloud computing and storage. Cloud-based storage is an excellent cost-saving solution but requires data to be easily spread across multiple servers to scale up. Using commodity (affordable, smaller) hardware on-site or in the cloud saves you the hassle of additional software and NoSQL databases like Cassandra are designed to be scaled across multiple data centers out of the box, without a lot of headaches.

- Rapid development. NoSQL is extremely useful for rapid development as it doesn’t need to be prepped ahead of time. If you’re working on quick iterations of your system which require making frequent updates to the data structure without a lot of downtime between versions, a relational database will slow you down.

### Data model and schema

One of the primary factors to consider when selecting a database is the data model and structure of the information you plan to store. Understanding the complexity, diversity, and relationships within the data will help you determine the most appropriate database type.

- SQL databases
  - SQL databases are best suited for structured data with a well-defined schema that can be represented in tables with rows and columns. The schema is enforced, and any changes to the schema require modifications to the entire database structure. This works well for applications with a well-defined, predictable data model, such as inventory management systems, where each product has a specific set of attributes (name, price, quantity, etc.).

- NoSQL databases
  - NoSQL databases are designed for unstructured or semi-structured data, and they generally do not require a fixed schema. This allows for greater flexibility in handling data model changes or when working with varied data types. This is beneficial for applications with evolving data models or diverse datasets, such as social networks, where user-generated content can vary greatly in format and structure. If your application needs to store and manage data that does not fit neatly into a table structure, NoSQL databases are a better fit.

### Scalability

Evaluating your application’s scalability needs, both in terms of data volume and read/write load, is crucial in choosing the right database.

- SQL databases
  - SQL databases are known for their vertical scalability, which means adding more resources (CPU, RAM, storage) to a single server to handle increased workload. This can be suitable for applications with moderate scaling requirements, such as small to medium-sized web applications or internal company tools. However, this approach can be expensive and has limitations as the server's capacity is finite.

- NoSQL databases
  - NoSQL databases provide horizontal scalability, allowing you to distribute data across multiple servers, making it easier to handle large volumes of data or high traffic loads. This is advantageous for large-scale applications with high throughput and data volume requirements, such as big data analytics, real-time data processing, or Internet of Things (IoT) applications. If your application requires easy scaling to accommodate growing data or user bases, NoSQL databases are a better choice.

### Consistency

The level of consistency and reliability required by your application plays a significant role in determining the most suitable database type.

- SQL databases
  - SQL databases provide strong consistency and full ACID (Atomicity, Consistency, Isolation, Durability) compliance for transactions. If your application requires strict data consistency and transactional guarantees, such as banking or e-commerce systems, an SQL database is a better fit.

- NoSQL databases
  - NoSQL databases often sacrifice consistency for availability and partition tolerance, following the CAP theorem. Most NoSQL databases provide eventual consistency and partial ACID compliance. For applications where data consistency can be relaxed in favor of availability and performance, such as social networks, analytics, or recommendation engines, NoSQL databases are a better choice.

### Query complexity and frequency

Assessing the complexity and frequency of queries your application will perform is essential in selecting the right database.

- SQL databases
  - SQL databases offer powerful and expressive querying capabilities with the SQL language, which allows for complex filtering, joining, and aggregation operations. This makes them a suitable choice for applications that rely heavily on analytics, reporting, or data warehousing, where complex data retrieval and filtering are necessary. If your application requires advanced querying and reporting features, SQL databases are a better fit.

- NoSQL databases
  - NoSQL databases have diverse querying capabilities depending on the database type, but generally, they lack the full range of features provided by SQL databases. NoSQL databases are better suited for simple or specialized queries that match the underlying data model, such as key-value lookups, graph traversals, or document searches.

### Latency

Considering the performance and latency requirements of your application is critical when choosing a database.

- SQL databases
  - SQL databases can provide robust, general-purpose performance for a wide range of applications. While they may not be optimized for specific workloads or access patterns, they offer a consistent and reliable performance profile for most use cases.

- NoSQL databases
  - If you need high performance and low latency for specific workloads or data access patterns, choose a NoSQL database that is optimized for those scenarios. NoSQL databases can offer superior performance under certain workloads, such as high write loads, large-scale data storage, and complex relationships.

### Maintenance

Finally, take into account the operational complexity and maintenance requirements of your chosen database. This includes factors such as deployment, monitoring, backup, and recovery. Choose a database that aligns with your team’s expertise, tools, and processes.

- Deployment
  - Consider the ease of deployment and integration with your existing infrastructure. Some databases may require more complex setup and configuration, while others offer streamlined deployment processes or managed services that handle the operational aspects for you.

- Monitoring
  - Evaluate the monitoring capabilities of the database, including performance metrics, error tracking, and log analysis. A database with comprehensive monitoring tools can help you identify and address issues proactively, ensuring the smooth operation of your application.

- Backup and recovery
  - Assess the backup and recovery features of the database, including the ease of creating and restoring backups, as well as the ability to handle disaster recovery scenarios. A robust backup and recovery strategy is essential to protect your data and maintain business continuity in case of unforeseen events.

- Security
  - Investigate the security features of the database, such as encryption, access control, and auditing. A secure database can help protect your sensitive data from unauthorized access and mitigate potential risks associated with data breaches.

- Community and support
  - Consider the community and support ecosystem surrounding the database. A vibrant community can provide valuable resources, such as documentation, tutorials, and forums, while a strong support ecosystem can offer professional assistance and guidance when needed.

- Cost
  - Finally, take into account the cost of using the chosen database, including licensing, hardware, and operational expenses. Depending on your budget and requirements, you may need to weigh the benefits of various databases against their associated costs to make an informed decision.

## ACID vs BASE

ACID and BASE are two sets of properties that represent different approaches to handling transactions in database systems. They reflect trade-offs between consistency, availability, and partition tolerance, especially in distributed databases.

### ACID

ACID stands for Atomicity, Consistency, Isolation, and Durability. It's a set of properties that guarantee reliable processing of database transactions.

![image](https://github.com/user-attachments/assets/9a94dc94-ea0c-4afa-953b-e2f503b221da)

#### Components

- Atomicity
  - Ensures that a transaction is either fully completed or not executed at all.
- Consistency
  - Guarantees that a transaction brings the database from one valid state to another.
- Isolation
  - Ensures that concurrent transactions do not interfere with each other.
- Durability
  - Once a transaction is committed, it remains so, even in the event of a system failure.

Example: 

Consider a bank transfer from one account to another. The transfer operation (debit from one account and credit to another) must be atomic, maintain the consistency of total funds, be isolated from other transactions, and changes must be permanent.

#### Use Cases

- Ideal for systems requiring high reliability and data integrity, like banking or financial systems.

### BASE

BASE stands for Basically Available, Soft state, and Eventual consistency. It's an alternative to ACID in distributed systems, favoring availability over consistency.

![image](https://github.com/user-attachments/assets/ece1819f-7b7c-4469-b3b0-2116174c31fe)

#### Components

- Basically Available
  - Indicates that the system is available most of the time.
- Soft State
  - The state of the system may change over time, even without input.
- Eventual Consistency
  - The system will eventually become consistent, given enough time.

Example: 

A social media platform using a BASE model may show different users different counts of likes on a post for a short period but eventually, all users will see the correct count.

#### Use Cases

Suitable for distributed systems where availability and partition tolerance are more critical than immediate consistency, like social networks or e-commerce product catalogs.

### Summary

- Consistency and Availability
  - ACID prioritizes consistency and reliability of each transaction, while BASE prioritizes system availability and partition tolerance, allowing for some level of data inconsistency.

- System Design
  - ACID is generally used in traditional relational databases, while BASE is often associated with NoSQL and distributed databases.

- Use Case Alignment
  - ACID is well-suited for applications requiring strong data integrity, whereas BASE is better for large-scale applications needing high availability and scalability.

ACID is critical for systems where transactions must be reliable and consistent, while BASE is beneficial in environments where high availability and scalability are necessary, and some degree of data inconsistency is acceptable.

## SQL and NoSQL use cases

### SQL use cases

- E-commerce platforms
  - SQL databases are widely used in e-commerce platforms, where structured data and well-defined relationships are the norm. For example, an online store’s database may have tables for customers, products, orders, and shipping details, all with established relationships. SQL databases enable efficient querying and data manipulation, making it easier for e-commerce platforms to manage inventory, customer data, and order processing.

- Financial systems
  - Financial applications, such as banking and trading platforms, rely on SQL databases to maintain transactional consistency, ensure data integrity, and support complex queries. The ACID properties of SQL databases are crucial in this context, as they guarantee the correct processing of transactions and safeguard against data corruption.

- Content Management Systems (CMS)
  - Many popular CMS platforms, such as WordPress and Joomla, use SQL databases to store content, user data, and configuration information. The structured nature of the data and the powerful query capabilities of SQL databases make them well-suited for managing content and serving dynamic web pages.

### NoSQL use cases

- Social media platforms
  - NoSQL databases, particularly graph databases, are ideal for managing complex relationships and interconnected data found in social media platforms. For example, Facebook uses a custom graph database called TAO to store user profiles, friend connections, and other social graph data. This allows Facebook to efficiently query and traverse the massive social graph, providing features like friend recommendations and newsfeed personalization.

- Big data analytics
  - NoSQL databases, such as Hadoop’s HBase and Apache Cassandra, are commonly used for big data analytics, where large-scale data storage and processing are required. These databases are designed to scale horizontally, enabling them to handle vast amounts of data and high write loads. For example, Netflix uses Apache Cassandra to manage its customer data and viewing history, which helps the streaming service to provide personalized content recommendations to its users.

- Internet of Things (IoT)
  - IoT applications generate massive volumes of data from various devices and sensors, often with varying data structures and formats. NoSQL databases like MongoDB and Amazon DynamoDB are suitable for handling this diverse and dynamic data, providing flexible data modeling and high-performance storage capabilities. For example, Philips Hue, a smart lighting system, uses Amazon DynamoDB to store and manage data generated by its connected light bulbs and devices.

### Hybrid use cases

- Gaming industry
  - In the gaming industry, developers often use a combination of SQL and NoSQL databases to support different aspects of their applications. For instance, an SQL database may be employed to manage user accounts, in-game purchases, and other transactional data, while a NoSQL database like Redis can be used to store real-time game state information and leaderboards.

- E-commerce with personalized recommendations
  - Some e-commerce platforms combine SQL databases for transactional data and inventory management with NoSQL databases for personalized recommendations. This hybrid approach allows the platform to leverage the strengths of both database types, ensuring efficient data storage, querying, and analysis for various aspects of the application.

## SQL normalization and denormalization

### SQL normalization

Normalization in SQL is a database design technique that organizes tables in a manner that reduces redundancy and dependency. It involves dividing a database into two or more tables and defining relationships between them to achieve a more efficient database structure.

#### Characteristics

- Reduces Redundancy
  - Avoids duplication of data.
- Improves Data Integrity
  - Ensures data accuracy and consistency.
- Database Design
  - Involves creating tables and establishing relationships through primary and foreign keys.

Example: 

Customer orders database

<img width="732" alt="image" src="https://github.com/user-attachments/assets/436b6f8c-cbe6-4009-af50-72aec5ec2c68" />

<img width="740" alt="image" src="https://github.com/user-attachments/assets/8a55e63e-deaf-4432-a2e4-ac592e7c099e" />

#### Levels (Normal forms)

- 1NF (First Normal Form)
  - Data is stored in atomic form with no repeating groups.
- 2NF (Second Normal Form)
  - Meets 1NF and has no partial dependency on any candidate key.
- 3NF (Third Normal Form)
  - Meets 2NF and has no transitive dependency.

#### Use cases

Ideal for complex systems where data integrity is critical, like financial or enterprise applications.

### SQL denormalization

Denormalization, on the other hand, is the process of combining tables to reduce the complexity of database queries. This can introduce redundancy but may lead to improved performance by reducing the number of joins required.

#### Characteristics

- Increases Redundancy
  - May involve some data duplication.
- Improves Query Performance
  - Reduces the complexity of queries by reducing the number of joins.
- Data Retrieval
  - Optimized for read-heavy operations.

Example:

Denormalization would involve combining these tables back into a single table to optimize read performance. Taking the above table:

<img width="740" alt="image" src="https://github.com/user-attachments/assets/9ab0d277-e95d-4ccc-817f-b4baba49ada1" />

#### Use cases

- In read-heavy database systems where query performance is a priority.
- In systems where data changes are infrequent and a slightly less normalized structure doesn't compromise data integrity.

### Normalization vs denormalization

#### Purpose

- Normalization aims to minimize data redundancy and improve data integrity.
- Denormalization aims to improve query performance.

#### Data Redundancy

- Normalization reduces redundancy.
- Denormalization may introduce redundancy.

#### Performance

- Normalization can lead to a larger number of tables and more complex queries, potentially affecting read performance.
- Denormalization can improve read performance but may affect write performance due to data redundancy.

#### Complexity

- Normalization makes writes faster but reads slower whereas denormalization makes writes slower but reads faster. Lets understand this with an example.

#### Normalization

Imagine you run a bookstore, and you store all the info about customers and orders in a neat way. Instead of writing a customer's name, address, and phone number every time they order something, you just save it once in a "customer" list. When someone orders a book, you only link to their entry in the customer list.

- Effect on Write Operations
  - When you write data (like adding a new order), you only store the order info, not all the customer info. This makes writing faster and easier because there’s no duplicate info.

- Effect on Read Operations
  - But when you read the data, it takes more work. If you want to see everything about an order and the customer who made it, you have to look in multiple places (one for the order, one for the customer details). So, reads can be slower because the database has to gather info from different tables.

#### Denormalization

Now, imagine you’re tired of looking in different places to find info about an order. You decide to save everything in one place: each order will have the customer's name, address, and phone number. No more linking back to a customer list!

- Effect on Write Operations
  - Writing gets more complicated and slower. If a customer changes their address, you now have to update every single order that includes the old address. There’s a lot of duplicate data, and changes require updating multiple records.

- Effect on Read Operations
  - But reading becomes much faster! Since all the information is in one place, you don’t have to jump around to gather it. You get everything you need in one go, so reads are quick and easy.

### Summary

- Normalization is about reducing redundancy and improving data integrity but can lead to more complex queries.
- Denormalization simplifies queries but at the cost of increased data redundancy and potential maintenance challenges.

The choice between the two depends on the specific requirements of your database system, considering factors like the frequency of read vs. write operations, and the importance of query performance vs. data integrity.

## In-memory database vs on-disk database

In-memory databases and on-disk databases are two types of database systems designed for storing and managing data, but they fundamentally differ in how and where they store their data. Understanding these differences is key to choosing the right type of database for a specific application or workload.

### In-memory database (IMDB)

#### Storage

- Data Storage
  - Primarily stores data in the main memory (RAM) of the server.
- Persistence
  - Some in-memory databases can persist data on disk, but the primary data access and manipulation happen in memory.

#### Performance

- Speed
  - Offers high performance and low latency, as accessing data in RAM is significantly faster than disk access.
- Efficiency
  - Especially efficient for read-heavy operations and complex, real-time computations.

#### Use cases

- Real-Time Analytics
  - Ideal for applications that require real-time analysis and reporting.
- Caching
  - Commonly used for caching where quick data retrieval is crucial.
- Session Storage
  - Used in web applications for session management.

#### Limitations

- Cost
  - Generally more expensive due to the high cost of RAM.
- Scalability
  - Scaling large volumes of data can be challenging and costly.
- Data Volatility
  - In the event of power loss or system crash, data stored only in memory can be lost unless the database is designed with persistence mechanisms.

#### Examples

- Redis
  - A widely used in-memory data store, often employed as a distributed cache, message broker, and for quick read/write operations. Redis supports various data structures such as strings, hashes, lists, sets, and sorted sets.

- Memcached
  - A high-performance, distributed memory caching system, originally intended for speeding up dynamic web applications by alleviating database load.

- SAP HANA
  - An in-memory, column-oriented, relational database management system. HANA is known for advanced analytics processing, such as OLAP and OLTP processing on the same platform.

- Apache Ignite
  - A memory-centric distributed database, caching, and processing platform for transactional, analytical, and streaming workloads.

- Hazelcast IMDG
  - An in-memory data grid that offers distributed data structures and computing utilities. It's often used for scalable caching and in-memory data storage.

### On-disk database

#### Storage

- Data Storage
  - Stores data on persistent disk storage (HDD or SSD).
- Persistence
  - Data is inherently persistent and does not require additional mechanisms to survive system restarts.

#### Performance

- Speed
  - Generally slower compared to in-memory databases due to the time required for disk I/O operations.
- Suitability
  - More suited for applications where the speed of data access is less critical.

#### Use cases

- Transactional Systems
  - Widely used in transactional applications (OLTP systems), where data persistence is key.
- Large Data Sets
  - Ideal for applications with large data sets that cannot be cost-effectively stored in memory.
- General-Purpose Databases
  - Most traditional databases (like MySQL, PostgreSQL) are on-disk and cater to a wide range of applications.

#### Limitations

- Speed
  - The speed can be a limiting factor, especially for applications requiring real-time response.
- I/O Bottlenecks
  - Performance can be bottlenecked by disk I/O, particularly in high-throughput scenarios.

#### Examples

- MySQL
  - One of the most popular open-source relational database management systems. MySQL is widely used for web applications and supports a broad array of features.

- PostgreSQL
  - An advanced open-source relational database. PostgreSQL is known for its robustness, scalability, and support for advanced data types and features.

- MongoDB
  - A leading NoSQL database that stores data in JSON-like documents. It is designed for ease of development and scaling.

- Oracle Database
  - A multi-model database management system known for its feature-rich, enterprise-grade capabilities, widely used in large organizations.

- Microsoft SQL Server
  - A relational database management system developed by Microsoft, offering a wide range of data analytics, business intelligence, and transaction processing capabilities.

- SQLite
  - A C-language library that implements a small, fast, self-contained, high-reliability SQL database engine. It's widely used in applications where an embedded, lightweight database is needed.

### In-memory vs on-disk databases summary

#### Data Storage Location

- IMDB: Main memory (RAM).
- On-Disk Database: Persistent disk storage.

#### Performance

- IMDB: Faster read/write operations.
- On-Disk Database: Slower, depending on disk I/O.

#### Cost and Scalability

- IMDB: Higher cost, scaling large data sets is more challenging.
- On-Disk Database: More cost-effective for large data volumes.

#### Data Persistence

- IMDB: Requires mechanisms for data durability.
- On-Disk Database: Inherently persistent.

#### Use Cases

- IMDB: Real-time processing, caching, session storage.
- On-Disk Database: Transactional systems, large data storage, general-purpose usage.

Each type of database serves different needs: in-memory databases are optimal for scenarios requiring rapid data access and processing, while on-disk databases are better suited for applications needing reliable data persistence and management of large data volumes. The choice depends on specific application requirements, including performance needs, data size, and persistence considerations.

## Data replication vs data mirroring

Data replication and data mirroring are both methods used in managing and safeguarding data, particularly in the context of databases and storage systems. While they share similarities in creating copies of data, they serve different purposes and have distinct operational characteristics.

### Data replication

Data Replication involves copying data from one location to another. The replication can be synchronous or asynchronous.

#### Characteristics

- Asynchronous/Synchronous
  - Data replication can be done in real-time (synchronous) or with some delay (asynchronous).
- Multiple Copies
  - Often creates multiple copies of data, which can be stored across different servers or locations.
- Purpose
  - Enhances data availability and accessibility, used for load balancing, and enables data analysis without impacting the primary data source.
- Use Cases
  - In distributed databases, backup systems, and data warehouses.

#### Example

A company might replicate its database across multiple data centers to ensure that if one data center goes down, the others can still serve the data.

### Data mirroring

Data Mirroring refers to the process of creating an exact replica of a database or storage system, usually in real-time.

#### Characteristics

- Synchronous
  - Mirroring is typically synchronous, meaning the data in the primary and mirror locations are always in sync.
- Redundancy for High Availability
  - Primarily used for redundancy and high availability.
- Mirror Copy
  - Usually involves a one-to-one relationship between the original and the mirror. If data changes in the original location, it is immediately written to the mirror.
- Use Cases
  - In critical applications requiring high availability and data integrity, such as financial transaction systems.

#### Example

A financial services firm may use data mirroring to ensure that all transactional data is instantly copied to a secondary server, which can take over with no data loss in case the primary server fails.

### Data replication vs data mirroring

#### Real-Time Synchronization

- Replication
  - Can be either synchronous or asynchronous.
- Mirroring
  - Typically synchronous.

#### Purpose and Use

- Replication
  - Used for load balancing, data localization, and reporting.
- Mirroring
  - Primarily for disaster recovery and high availability.

#### Number of Copies

- Replication
  - Can create multiple copies of data in different locations.
- Mirroring
  - Usually involves a single mirror copy.

#### Performance Impact

- Replication
  - Can be designed to minimize performance impact.
- Mirroring
  - Since it’s synchronous, it might have a more significant impact on performance.

#### Flexibility

- Replication
  - More flexible in terms of configuration and use cases.
- Mirroring
  - More rigid, focused on creating a real-time exact copy for redundancy.

Choosing between data replication and data mirroring depends on the specific requirements of the system in terms of availability, performance, and the nature of the data being managed. In many systems, both techniques are used in conjunction to achieve both scalability and high availability.

## Database federation

Database Federation, often referred to as Federated Database Systems, is a concept in database management where multiple database systems are coordinated to function as a single entity. This approach allows for the integration and unified management of data from various sources without the need to physically consolidate it into a single location.

### Characteristics

#### Data Integration

- Federated databases integrate data from different sources, which can include both traditional databases and other forms of data repositories.

#### Logical Unification

- The data remains in its original location but is logically unified. This means users can query and manipulate the data as if it were all contained in a single database.

#### Heterogeneity Support

- Federated databases can combine data from different types of databases (such as SQL, NoSQL, XML databases) and other data sources.

#### Distributed Query Processing

- They allow queries to span across multiple databases, handling the complexity of retrieving and combining data from these varied sources.

#### Autonomy of Individual Databases

- Each database in the federation maintains its autonomy in terms of operation, schema, and administration.

### Use cases

- Enterprise Data Access
  - In large organizations with data spread across various systems and departments, database federation allows for comprehensive data access without data consolidation.

- Business Intelligence and Analytics
  - Enables complex analytics by aggregating data from various sources, providing a comprehensive view for decision-making.

- Data Warehousing
  - Enhances data warehousing strategies by allowing access to a wider range of data sources.

- Mergers and Acquisitions
  - Useful in corporate scenarios where newly merged companies need to access each other's data without undergoing a full data integration.

### Advantages

- Reduced Complexity
  - No need to physically move or replicate data, simplifying management and reducing storage costs.
- Flexibility
  - Easy to add or remove databases from the federation.
- Real-Time Access
  - Offers real-time access to data across the organization.

### Challenges

- Performance
  - Query performance can be a challenge, especially when dealing with large datasets across networks.
- Security and Compliance
  - Ensuring data security and compliance across different systems can be complex.
- Complex Queries
  - Managing and optimizing queries across heterogeneous systems require advanced techniques.

### Summary

Database Federation is a powerful approach for organizations needing to integrate and access data from multiple, disparate sources. It offers the benefits of data integration without the overhead and complexity of physically consolidating data. However, it requires careful planning and management to address challenges in performance, security, and query optimization.







