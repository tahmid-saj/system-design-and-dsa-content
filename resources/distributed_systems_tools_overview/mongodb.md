# MongoDB

## What is MongoDB?

MongoDB is an open source, nonrelational database management system (DBMS) that uses flexible documents instead of tables and rows to process and store various forms of data.

As a NoSQL database solution, MongoDB does not require a relational database management system (RDBMS), so it provides an elastic data storage model that enables users to store and query multivariate data types with ease. This not only simplifies database management for developers but also creates a highly scalable environment for cross-platform applications and services.

MongoDB is used for high-volume data storage, helping organizations store large amounts of data while still performing rapidly. Organizations also use MongoDB for its ad-hoc queries, indexing, load balancing, aggregation, server-side JavaScript execution and other features.

MongoDB documents or collections of documents are the basic units of data. Formatted as Binary JSON (Java Script Object Notation), these documents can store various types of data and be distributed across multiple systems. Since MongoDB employs a dynamic schema design, users have unparalleled flexibility when creating data records, querying document collections through MongoDB aggregation and analyzing large amounts of information.

### How does MongoDB work?

MongoDB environments provide users with a server to create databases with MongoDB. MongoDB stores data as records that are made up of collections and documents.

Documents contain the data the user wants to store in the MongoDB database. Documents are composed of field and value pairs. They are the basic unit of data in MongoDB. The documents are similar to JavaScript Object Notation (JSON) but use a variant called Binary JSON (BSON). The benefit of using BSON is that it accommodates more data types. The fields in these documents are like the columns in a relational database. Values contained can be a variety of data types, including other documents, arrays and arrays of documents, according to the MongoDB user manual. Documents will also incorporate a primary key as a unique identifier. A document's structure is changed by adding or deleting new or existing fields.

Sets of documents are called collections, which function as the equivalent of relational database tables. Collections can contain any type of data, but the restriction is the data in a collection cannot be spread across different databases. Users of MongoDB can create multiple databases with multiple collections.

The mongo shell is a standard component of the open-source distributions of MongoDB. Once MongoDB is installed, users connect the mongo shell to their running MongoDB instances. The mongo shell acts as an interactive JavaScript interface to MongoDB, which allows users to query or update data and conduct administrative operations.

A binary representation of JSON-like documents is provided by the BSON document storage and data interchange format. Automatic sharding is another key feature that enables data in a MongoDB collection to be distributed across multiple systems for horizontal scalability, as data volumes and throughput requirements increase.

### Workings of MongoDB

MongoDB is a database server and the data is stored in these databases. Or in other words, MongoDB environment gives you a server that you can start and then create multiple databases on it using MongoDB. 

Because of its NoSQL database, the data is stored in the collections and documents. Hence the database, collection, and documents are related to each other as shown below.

The documents are created using the fields. Fields are key-value pairs in the documents, it is just like columns in the relation database. The value of the fields can be of any BSON data types like double, string, boolean, etc.

<img width="432" alt="image" src="https://github.com/user-attachments/assets/e9ced217-46d2-4036-afb3-3bd0abbc7607">

NOTE: In MongoDB server, you are allowed to run multiple databases.

### MongoDB features

#### Replication

A replica set is two or more MongoDB instances used to provide high availability. Replica sets are made of primary and secondary servers. The primary MongoDB server performs all the read and write operations, while the secondary replica keeps a copy of the data. If a primary replica fails, the secondary replica is then used.

MongoDB provides high availability and redundancy with the help of replication, it creates multiple copies of the data and sends these copies to a different server so that if one server fails, then the data is retrieved from another server.

To configure a replica set, we can start multiple MongoDB instances on different MongoDB servers or ports. Then we can connect to one of the instances using the mongo shell to specify the replica set, such as how many replicas do we need and which are the primary and secondary nodes.

Writes are performed on the primary node, and changes are replicated to secondary nodes.

In case the primary node fails, an election is held, and one of the secondaries becomes the new primary.

#### Scalability

MongoDB supports vertical and horizontal scaling. Vertical scaling works by adding more power to an existing machine, while horizontal scaling works by adding more machines to a user's resources.

#### Sharding

MongoDB provides horizontal scalability with the help of sharding. Sharding means to distribute data on multiple servers, here a large amount of data is partitioned into data chunks using the shard key, and these data chunks are evenly distributed across shards that reside across many physical servers. It will also add new machines to a running database.

Sharding distributes data across multiple servers (shards) to handle large datasets and high throughput.

When setting up sharding, we'll need the 3 components below:
Config Servers: Store metadata and configuration information for the cluster.
Shard Servers: Store the actual data.
Query Routers (mongos): Direct queries to the appropriate shards.

We'll need to start up the config servers, shard servers and query routers via the mongo shell. We'll then connect to a mongodb database and add shards, and enable sharding on the database. We'll also have to specify a shard key for a collection. To choose a shard key, we choose a field or combination of fields with high cardinality and even distribution to ensure balanced data placement. For sharding, it's also a best practice to use multiple config servers in a replica set for reliability. We'll also need to monitor the mongodb database health using tools like mongostat and mongotop, and periodically balance data across shards to avoid hotspots using the MongoDB balancer.

#### Load balancing

MongoDB handles load balancing without the need for a separate, dedicated load balancer, through either vertical or horizontal scaling.

#### Indexing

In MongoDB database, every field in the documents is indexed with primary and secondary indices this makes easier and takes less time to get or search data from the pool of the data. If the data is not indexed, then database search each document with the specified query which takes lots of time and not so efficient. 

MongoDB supports a number of different index types, including single field, compound (multiple fields), multikey (array), geospatial, text, and hashed.

## MongoDB use cases

### Mobile applications

MongoDB’s JSON document model lets you store back-end application data wherever you need it, including in Apple iOS and Android devices as well as cloud-based storage solutions. This flexibility lets you aggregate data across multiple environments with secondary and geospatial indexing, giving developers the ability to scale their mobile applications seamlessly.

### Real-time analytics
As companies scale their operations, gaining access to key metrics and business insights from large pools of data is critical. MongoDB handles the conversion of JSON and JSON-like documents, such as BSON, into Java objects effortlessly, making the reading and writing of data in MongoDB fast and incredibly efficient when analyzing real-time information across multiple development environments. This has proved beneficial for several business sectors, including government, financial services and retail.

### Content management systems

Content management systems (CMS) are powerful tools that play an important role in ensuring positive user experiences when accessing e-commerce sites, online publications, document management platforms and other applications and services. By using MongoDB, you can easily add new features and attributes to your online applications and websites using a single database and with high availability.

### Storage

MongoDB can store large structured and unstructured data volumes and is scalable vertically and horizontally. Indexes are used to improve search performance. Searches are also done by field, range and expression queries.

### Complex data structures descriptions

Document databases enable the embedding of documents to describe nested structures (a structure within a structure) and can tolerate variations in data.

## Comparing MongoDB to other databases

### MongoDB vs. MySQL

MySQL uses a structured query language to access stored data. In this format, schemas are used to create database structures, utilizing tables as a way to standardize data types so that values are searchable and can be queried properly. A mature solution, MySQL is useful for a variety of situations including website databases, applications and commercial product management.

Because of its rigid nature, MySQL is preferable to MongoDB when data integrity and isolation are essential, such as when managing transactional data. But MongoDB’s less-restrictive format and higher performance make it a better choice, particularly when availability and speed are primary concerns.

### MongoDB vs. Cassandra

While Cassandra and MongoDB are both considered NoSQL databases, they have different strengths. Cassandra uses a traditional table structure with rows and columns, which enables users to maintain uniformity and durability when formatting data before it’s compiled.

Cassandra can offer an easier transition for enterprises looking for a NoSQL solution because it has a syntax similar to SQL; it also reliably handles deployment and replication without a lot of configuration. However, it can’t match MongoDB’s flexibility for handling structured and unstructured data sets or its performance and reliability for mission-critical cloud applications.

## MongoDB advantages

### Load balancing

As enterprises' cloud applications scale and resource demands increase, problems can arise in securing the availability and reliability of services. MongoDB’s load balancing sharing process distributes large data sets across multiple virtual machines at once while still maintaining acceptable read and write throughputs. This horizontal scaling is called sharding and it helps organizations avoid the cost of vertical scaling of hardware while still expanding the capacity of cloud-based deployments.

### Ad hoc database queries

One of MongoDB’s biggest advantages over other databases is its ability to handle ad hoc queries that don’t require predefined schemas. MongoDB databases use a query language that’s similar to SQL databases and is extremely approachable for beginner and advanced developers alike. This accessibility makes it easy to push, query, sort, update and export your data with common help methods and simple shell commands.

### Multilanguage support

One of the great things about MongoDB is its multilanguage support. Several versions of MongoDB have been released and are in continuous development with driver support for popular programming languages, including Python, PHP, Ruby, Node.js, C++, Scala, JavaScript and many more.

### Schema-less

Like other NoSQL databases, MongoDB doesn't require predefined schemas. It stores any type of data. This gives users the flexibility to create any number of fields in a document, making it easier to scale MongoDB databases compared to relational databases.

### Scalability

A core function of MongoDB is its horizontal scalability, which makes it a useful database for companies running big data applications. In addition, sharding lets the database distribute data across a cluster of machines. MongoDB also supports the creation of zones of data based on a shard key.

### Aggregation

The DBMS also has built-in aggregation capabilities, which lets users run MapReduce code directly on the database rather than running MapReduce on Hadoop. MongoDB also includes its own file system called GridFS, akin to the Hadoop Distributed File System. The use of the file system is primarily for storing files larger than BSON's size limit of 16 MB per document. These similarities let MongoDB be used instead of Hadoop, though the database software does integrate with Hadoop, Spark and other data processing frameworks.

Note: MongoDB does not support join operation.
Note: MongoDB is easily integrated with Big Data Hadoop

## MongoDB disadvantages

### Continuity

With its automatic failover strategy, a user sets up just one master node in a MongoDB cluster. If the master fails, another node will automatically convert to the new master. This switch promises continuity, but it isn't instantaneous -- it can take up to a minute. By comparison, the Cassandra NoSQL database supports multiple master nodes. If one master goes down, another is standing by, creating a highly available database infrastructure.

### Write limits

MongoDB's single master node also limits how fast data can be written to the database. Data writes must be recorded on the master, and writing new information to the database is limited by the capacity of that master node.

### Data consistency

MongoDB doesn't provide full referential integrity through the use of foreign-key constraints, which could affect data consistency.

## MongoDB deployment and setup

Deployment involves two primary activities: installing MongoDB and creating a database.

### Installing MongoDB

Windows: To install MongoDB in a Windows environment (link resided outside ibm.com), run Windows Server 2008 R2, Windows Vista or later. Once you’ve decided on the type of database architecture you’ll be using, you can download the latest version of the platform on MongoDB’s download page (link resided outside ibm.com).
Mac: When you install MongoDB on macOS, there are two ways you can approach it. As with the install process for Windows-based environments, MongoDB can be installed directly from the developer website once you’ve decided on the type of build you’ll be using. However, the easier and more common method of installing and running MongoDB on a Mac is through the use of the Terminal app, running Homebrew (link resided outside ibm.com). Click here for more information on Homebrew installations of MongoDB (link resided outside ibm.com).

### Creating a database

After installing MongoDB, you’ll need to create a directory where your data will be stored. This can be done locally or through public or private cloud storage solutions. For more information about getting started with MongoDB, click here (link resided outside ibm.com) for comprehensive guides, tutorials and walk-throughs.

## MongoDB platforms

MongoDB is available in community and commercial versions through vendor MongoDB Inc. MongoDB Community Edition is the open source release, while MongoDB Enterprise Server brings added security features, an in-memory storage engine, administration and authentication features, and monitoring capabilities through Ops Manager.

A graphical user interface (GUI) named MongoDB Compass gives users a way to work with document structure, conduct queries, index data and more. The MongoDB Connector for BI lets users connect the NoSQL database to their business intelligence tools to visualize data and create reports using SQL queries.

Following in the footsteps of other NoSQL database providers, MongoDB Inc. launched a cloud database as a service named MongoDB Atlas in 2016. Atlas runs on AWS, Microsoft Azure and Google Cloud Platform. Later, MongoDB released a platform named Stitch for application development on MongoDB Atlas, with plans to extend it to on-premises databases.

### MongoDB Atlas

MongoDB Atlas is a fully managed cloud database service provided by MongoDB, Inc. It is designed to simplify the deployment, management, and scaling of MongoDB databases. Atlas runs on major cloud providers, including Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure.

It allows developers and businesses to leverage the capabilities of MongoDB without worrying about underlying infrastructure, maintenance, or operational complexities.

