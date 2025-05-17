# PostgreSQL

## What is PostgreSQL?

Unlike other RDMBS (Relational Database Management Systems), PostgreSQL supports both non-relational and relational data types. This makes it one of the most compliant, stable, and mature relational databases available today.

PostgreSQL is completely free from licensing restrictions, vendor lock-in potential, or the risk of over-deployment. Expert developers and commercial enterprises who understand the limitations of traditional database systems heavily support PostgreSQL. They work diligently to provide a battle-tested, best-of-breed relational database management system.

PostgreSQL is a powerful, open source object-relational database management system (ORDBMS) known for its reliability, data integrity, and extensive feature set. It can handle advanced data types, complex queries, foreign keys, triggers, and views, as well as procedural languages for stored procedures. PostgreSQL is highly expandable, allowing users to add new functions, data types, and other features. Its strong compliance with SQL standards, combined with support for ACID (Atomicity, Consistency, Isolation, Durability) properties, make it an ideal choice for developers and enterprises looking for a scalable, efficient, and secure database.

Choosing PostgreSQL as your database solution offers a unique blend of advantages that cater to a wide array of data management needs. One of the primary reasons to consider PostgreSQL is its exceptional support for advanced data types and sophisticated functionality. This includes native support for JSON, geometric data, and custom types, allowing for flexible and efficient data storage and retrieval that can adapt to the most complex and varied data models. PostgreSQL’s ability to easily handle complex queries, transactions, and extensive data warehousing operations makes it perfect for applications requiring detailed analytics, real-time processing, and high data integrity.

It also supports a wide range of data types, including custom user-created ones, and offers multiple procedural languages for writing stored procedures.

### PostgreSQL features

PostgreSQL possesses robust feature sets, including tablespaces, asynchronous replication, nested transactions, online/hot backups, and a refined query planner/optimizer. The PostgreSQL community has also developed extensions that extend the functionality of PostgreSQL database. PostgreSQL supports:

International character sets, multi-byte character encodings, and Unicode. 

Most SQL:2008 data types, including INTEGER, NUMERIC, BOOLEAN, CHAR, VARCHAR, DATE, INTER-VAL, and TIMESTAMP.

Storage of large binary objects, including pictures, sounds, video, and maps.

Foreign keys, joins, views, triggers, and stored procedures.

Leading programming languages and protocols, including Python, Java, Perl, .Net, Go, Ruby, C/C++, Tcl, and ODBC.

It is locale-aware for sorting, case sensitivity, and formatting. The PostgreSQL database server is highly scalable both in the quantity of data it can manage and in the number of concurrent users it can accommodate.

#### Point-in-time recovery

PostgreSQL enables developers to use PITR (Point-In-Time Recovery) to restore databases to a specific moment in time when running data recovery initiatives. Because PostgreSQL maintains a write ahead log (WAL) at all times, it logs every database change. This makes it easy to restore file systems back to a stable starting point. 

#### Stored procedures

PostgreSQL features built-in support for multiple procedural languages, giving developers the ability to create custom subroutines called stored procedures. These procedures can be created and called on a given database. With the use of extensions, procedural languages can also be used for development in many other programming languages, including Perl, Python, JavaScript, and Ruby.

#### Postgres is an ORDBMS

Postgres is often categorized as an ORDBMS (Object-Relational Database Management System) due to its ability to handle complex data types and store and retrieve objects. In comparison to traditional RDBMS (Relational Database Management System), ORDBMSs are better suited to handling complex data structures and have more advanced query capabilities.

In the context of NoSQL databases, which are designed to handle large amounts of unstructured or semi-structured data, ORDBMSs like Postgres have some advantages over traditional RDBMSs. NoSQL databases often prioritize scalability, availability, and high-speed data access over data consistency, whereas ORDBMSs are designed to prioritize data consistency while still providing some flexibility in data modeling.

The Postgres support for JSON and other semi-structured data types make it a viable option for applications that require some NoSQL capabilities. Additionally, Postgres's extensibility allows developers to add custom data types, functions, and operators, providing flexibility in data modeling and query capabilities. Postgres also has strong support for indexing, allowing for efficient retrieval of data even when dealing with large and complex data structures.

#### Foreign Data Wrappers

Foreign Data Wrappers (FDWs) in Postgres are beneficial for several reasons:

Data integration: FDWs allow you to integrate data from multiple sources into a single database, without having to physically move the data or create duplicate copies of it. This makes it easier to access and analyze data from disparate sources.

Performance: With FDWs, you can query data from external sources directly from within Postgres, without having to first extract and load the data. This can significantly improve query performance, especially when dealing with large datasets.

Data federation: FDWs allow you to create a unified view of data from multiple sources, even if the data is stored in different formats or on different platforms. This can simplify data analysis and reporting, and can also help to avoid data silos.

Data virtualization: FDWs allow you to create virtual tables in Postgres that are backed by data in external sources. This means that you can query external data as if it were stored locally in Postgres, without having to first load it into Postgres. This can simplify application development and reduce data redundancy.

Overall, FDWs in Postgres provide a powerful and flexible mechanism for integrating, analyzing, and reporting on data from multiple sources.

#### Advanced indexing

Postgres supports various index types, including B-trees, Hash, GiST, SP-GiST, and GIN.

#### Replication and high availability

Postgres supports both synchronous and asynchronous replication and provides several tools for achieving high availability.

Replication involves copying data from one PostgreSQL database server (primary) to others (replicas). It is commonly used for high availability, load balancing, and disaster recovery.

There are different types of replication:

Streaming Replication: Real-time replication of WAL (Write-Ahead Logging) data to replica servers.

Logical Replication: Row-level replication that allows selective and fine-grained replication between databases.

File-based Replication: Involves copying WAL files to replicas; typically used in backup setups.

#### Sharding

Sharding is used to horizontally partition data across multiple PostgreSQL instances, distributing tables or data subsets to improve performance and scalability.

There are different approaches to sharding in PostgreSQL:

Foreign Data Wrappers (FDW): 
- PostgreSQL's postgres_fdw allows federated querying across multiple databases.

Table Partitioning:
- Manually partition data across nodes based on specific column values.
- Use triggers or application logic to route queries to the appropriate shard.

Citus Extension: 
- Citus (an open-source PostgreSQL extension) simplifies sharding and distributed processing.

## PostgreSQL vs other databases

A relational database is a collection of data items with pre-defined relationships. These items are organized as a set of tables with columns and rows. A relational database management system is software that lets you read, write, and modify the relational database. PostgreSQL is an object-relational database management system (ORDMBS), which means that it has relational capabilities and an object-oriented design.

Using object-oriented features of PostgreSQL, programmers can:

Communicate with the database servers using objects in their code.

Define complex custom data types.

Define functions that work with their own data types.

Define inheritance, or parent-child relationships, between tables.

Thus, PostgreSQL design is more flexible than other relational database servers. You can model different relationships and types within the existing database system instead of externally in your application code. You can maintain consistency and improve database performance by enforcing intended behavior closer to the actual data.

### PostgreSQL vs MySQL

PostgreSQL and MySQL differ in licensing, SQL standards, and performance. Both support ACID properties and are open-source.

- PostgreSQL offers advanced SQL features, including support for complex queries, window functions, common table expressions (CTEs), and more.
- PostgreSQL has more advanced data integrity features and constraints, allowing for finer control over data validation and enforcement of business rules.
- PostgreSQL has superior support for JSON data types, making it a good choice for applications requiring structured and semistructured data.
- PostgreSQL has advanced support for geospatial data and geographic information system (GIS) functionality, making it a preferred choice for applications that deal with location-based data.
- PostgreSQL is released under the PostgreSQL License, which is more permissive than MySQL’s dual licensing (GPL or commercial).

Ff you need to scale faster to a very large volume, PostgreSQL is a better choice. However, you can choose MySQL if you want a lightweight server than integrates quickly with third-party tools.

#### Similarities

Both are Relational Database Management Systems (RDBMS): Both PostgreSQL and MySQL fall under the category of relational database systems, organizing data into structured tables of rows and columns, and leveraging SQL for data manipulation and queries.

ACID compliance: Each database system upholds ACID (Atomicity, Consistency, Isolation, Durability) principles, providing a foundation for secure and reliable transaction processing.

Cross-platform compatibility: PostgreSQL and MySQL are designed to operate across multiple operating systems, including Linux, Windows, and macOS, offering flexibility in deployment environments.

Community support: Both databases benefit from active, supportive communities that contribute to ongoing development, provide support, and offer resources for users.

Support for replication and high availability: To ensure continuous operation and data safety, both PostgreSQL and MySQL incorporate mechanisms for data replication and high availability to ensure data redundancy and fault tolerance in distributed systems.

#### DIfferences

Licensing: PostgreSQL is distributed under the PostgreSQL License, a permissive open source license. In contrast, MySQL offers dual licensing options: the GNU General Public License (GPL) for open-source projects and a proprietary commercial license for other uses.

Data types: PostgreSQL provides a more extensive selection of data types than MySQL, encompassing complex types such as arrays, JSON, XML, and user-defined types, allowing for more flexibility in data storage and manipulation.

SQL syntax and features: Although both databases utilize SQL for querying, there are notable distinctions in their SQL syntax and capabilities. PostgreSQL, for instance, includes support for window functions, Common Table Expressions (CTEs), and recursive queries, areas where MySQL might offer limited functionality.

Transaction isolation levels: PostgreSQL offers a broader array of transaction isolation levels, including the highly stringent Serializable level, providing more options for controlling concurrency and data integrity.

Performance and scaling:PostgreSQL stands out for its strong performance and scalability, especially with complex queries and large datasets. While MySQL has traditionally excelled in simple, read-heavy operations, both systems have evolved to enhance their performance capabilities over time.

### Oracle vs Postgres

Oracle is a well-known enterprise-level RDBMS with a reputation for scalability and dependability. While Postgres adopted a procedural language name echoing Oracle’s (PL/SQL for Oracle and PL/pgSQL for Postgres), Postgres sets itself apart in terms of functionality, scalability, and licensing. For most use cases, Postgres is a capable and cost-effective alternative to Oracle, thanks to its reliability, flexibility, security, and active community support. Postgres is great for cost avoidance because it is open-source and has a lower total cost of ownership compared to Oracle.

### MongoDB vs Postgres

MongoDB is a NoSQL database management system designed to handle massive volumes of data in a flexible, JSON-like manner. It is generally easier to set up and use than Postgres but is not as feature-rich or powerful. It is also not as good at handling complex queries or transactions as Postgres.

### Microsoft SQL Server vs Postgres

SQL Server, developed by Microsoft, supports a wide range of transaction processing, business intelligence, and analytics applications. It offers extensive integration with other Microsoft products, making it a preferred choice for many enterprises already invested in the Microsoft ecosystem (Microsoft Stack). While both SQL Server and Postgres are popular RDBMS options, SQL Server often has an edge in enterprise environments due to its comprehensive toolset, deep integration capabilities, and longstanding market presence, leading to its higher popularity in certain sectors.

## PostgreSQL use cases

### Website applications

Because PostgreSQL can handle high volumes of data and concurrent users efficiently, it’s suitable for applications that require scalability and performance. This makes it an excellent choice for dynamic website applications, from e-commerce platforms to content management systems, where uptime and data integrity are critical.

### Data warehousing

PostgreSQL enables businesses to store and analyze large amounts of data for reporting and business intelligence. Its capability to handle massive datasets and complex queries and its support for advanced data types make it ideal for integrating and consolidating data from various sources for comprehensive analysis.

### OLTP and analytics

PostgreSQL is great for managing OLTP (Online Transaction Processing) protocols. As a general purpose OLTP database, PostgreSQL works well for a variety of use cases like e-commerce, CRMs, and financial ledgers. PostgreSQL’s SQL compliance and query optimizer also make it useful for general purpose analytics on your data.

### Geographic information systems

PostGIS is an Open Geospatial Consortium (OGC) software offered as an extender to PostgreSQL. It allows PostgreSQL to support geospatial data types and functions to further enhance data analysis. By supporting geographic objects, PostgreSQL can refine sales and marketing efforts by augmenting situational awareness and intelligence behind stored data as well as help improve fraud detection and prevention.

## PostgreSQL advantages

### Concurrency support

When multiple users access data at the same time, traditional database systems typically lock out access to records to avoid read/write conflicts. PostgreSQL manages concurrency efficiently through its use of MVCC (Multiversion Concurrency Control). In practice, this means that reads don’t block writes and writes don’t block reads.

### Deep language support

PostgreSQL is one of the most flexible databases for developers due to its compatibility and support of multiple programming languages. Popular coding languages such as Python, JavaScript, C/C++, Ruby, and others offer mature support for PostgreSQL, letting developers perform database tasks in whichever language they are proficient in without generating system conflicts.

### Replication

PostgreSQL can be configured to ensure high availability of services through either Asyncronous or Synchronous replication methods across multiple servers.

### 100% open source

Deploying open source database management technology offers unique benefits to enterprises, including better costs, higher flexibility, and innovation not always available with proprietary database solutions. Developed by a diverse group of contributors, PostgreSQL builds on a strong foundation of knowledge, expertise, and open source values, making it the world’s most advanced database.

### DevOps and cloud-native

Postgres is well-suited for cloud-native deployment and DevOps, integrating smoothly with modern CI/CD pipelines and cloud services. In the context of service-oriented architectures like microservices, Postgres becomes even more relevant. With containerization, especially using platforms like Kubernetes, Postgres can be efficiently managed, making it a strong choice for microservices in cloud-native environments.

## PostgreSQL disadvantages

### Scalability

While Postgres can scale well, it can be challenging to manage for large-scale applications. Database administrators need to have experience with advanced database administration tasks such as replication, clustering, and partitioning.

### Performance

Postgres can be slower compared to some other database systems, especially for write-intensive applications. However, it has many features and configuration options that can be tuned to improve performance.

### Lack of built-in tools for backups

Compared to some other database systems, Postgres does not have built-in tools for backups, monitoring and management. However, there are many third-party tools available that can provide these features.

## PostgreSQL deployment and setup

The following steps can be taken to deploy and setup a PostgreSQL database:

1. Install and configure PostgreSQL on the local environment, either on Windows, Mac, Linux. Docker can also be used to run a PostgreSQL instance locally.
2. Connecting to PostgreSQL either via psql in the command line or using a GUI like pgAdmin or DBeaver could be done to access the PostgreSQL DBMS and create databases and tables.
3. The PostgreSQL database could be deployed using a cloud offering such as AWS RDS or Azure Database for PostgreSQL. Kubernetes can also help in scaling the PostgreSQL instances and deployment.
