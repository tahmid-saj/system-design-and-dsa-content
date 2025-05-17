# MySQL

## What is MySQL?

MySQL is an open-source Relational Database Management System (RDBMS) that enables users to store, manage, and retrieve structured data efficiently. It is widely used for various applications, from small-scale projects to large-scale websites and enterprise-level solutions.

Computers that install and run RDBMS software are called clients. Whenever they need to access data, they connect to the RDBMS server.

MySQL is one of many RDBMS software options. RDBMS and MySQL are often thought to be the same because of MySQL’s popularity. A few big web applications like Facebook, Twitter, YouTube, Google, and Yahoo! all use MySQL for data storage purposes. Even though it was initially created for limited usage, it is now compatible with many important computing platforms like Linux, macOS, Microsoft Windows, and Ubuntu.

MySQL and SQL are not the same. Be aware that MySQL is one of the most popular RDBMS software’s brand names, which implements a client-server model.

The client and server use a domain-specific language – Structured Query Language (SQL) to communicate in an RDBMS environment. If you ever encounter other names that have SQL in them, like PostgreSQL and Microsoft SQL server, they are most likely brands which also use Structured Query Language syntax. RDBMS software is often written in other programming languages but always uses SQL as its primary language to interact with the database. MySQL itself is written in C and C++.

SQL tells the server what to do with the data. In this case, SQL statements can instruct the server to perform certain operations:

Data query – requesting specific information from the existing database.

Data manipulation – adding, deleting, changing, sorting, and other operations to modify the data, the values or the visuals.

Data identity – defining data types, e.g. changing numerical data to integers. This also includes defining a schema or the relationship of each table in the database

Data access control – providing security techniques to protect data. This includes deciding who can view or use any information stored in the database

Is there a cloud version of MySQL?

HeatWave MySQL is a fully managed database service, and the only cloud service built on MySQL Enterprise Edition. It provides advanced security features for encryption, data masking, authentication, and a database firewall. HeatWave improves MySQL query performance by orders of magnitude and enables real-time analytics on transactional data in MySQL without the complexity, latency, risks, and cost of ETL duplication to a separate analytics database. It’s available on OCI, AWS, and Microsoft Azure.

### MySQL Heatwave

HeatWave is an in-memory query accelerator for MySQL Database. HeatWave MySQL is the only MySQL cloud database service that offers such acceleration and that combines transactions with real-time analytics, eliminating the complexity, latency, cost, and risk of extract, transform, and load (ETL) duplication.

As a result, users can see orders-of-magnitude increases in MySQL performance for analytics and mixed workloads. In addition, HeatWave AutoML lets developers and data analysts build, train, deploy, and explain the outputs of machine learning models within HeatWave MySQL in a fully automated way. They can also benefit from integrated and automated generative AI using HeatWave GenAI.

HeatWave MySQL can help improve MySQL query performance significantly and enables organizations to access real-time analytics on their transactional data without moving it to a separate analytics database. You can enhance data security and deploy HeatWave MySQL-powered applications in Oracle Cloud Infrastructure (OCI), Amazon Web Services (AWS), or Microsoft Azure.

HeatWave MySQL is the only MySQL cloud service integrating HeatWave, an in-memory, massively parallel, hybrid columnar query-processing engine. It’s also the only MySQL cloud service built on MySQL Enterprise Edition. Advanced features provide additional security measures to help companies protect data throughout its lifecycle and address regulatory requirements. Additionally, the built-in HeatWave Autopilot automatically helps improve MySQL performance and reduce costs with machine learning-powered automation, without requiring database tuning expertise. Autopilot can help increase the productivity of developers and DBAs and help reduce human error.

HeatWave MySQL also enables you to take advantage of a wider set of integrated HeatWave capabilities, including:

HeatWave Lakehouse - Query data in object storage in various file formats, including CSV, Parquet, Avro, and JSON. Export files from other databases using standard SQL syntax and optionally combine it with transactional data in MySQL databases.

HeatWave AutoML - Quickly and easily build, train, deploy, and explain machine learning models within HeatWave MySQL. There’s no need to move data to a separate machine learning cloud service, and no need to be a machine learning expert.

HeatWave GenAI - Gain integrated and automated generative AI with in-database large language models (LLMs); an automated, in-database vector store; scale-out vector processing; and the ability to have contextual conversations in natural language. Now companies can take advantage of generative AI without AI expertise, data movement, or additional costs.

### How does MySQL work?

The basic structure of the client-server structure involves one or more devices connected to a server through a specific network. Every client can make a request from the graphical user interface (GUI) on their screens, and the server will produce the desired output, as long as both ends understand the instruction. Without getting too technical, the main processes taking place in a MySQL environment are the same, which are:

MySQL creates a database for storing and manipulating data, defining the relationship of each table.
Clients can make requests by typing specific SQL statements on MySQL.
The server application will respond with the requested information, and it will appear on the client’s side.

Some of the most popular MySQL GUIs are MySQL WorkBench, SequelPro, DBVisualizer, and the Navicat DB Admin Tool. For web database management, including a WordPress site, the most obvious go-to is phpMyAdmin.

A schema defines how data is organized and stored and describes the relationship among various tables. With this format, developers can easily store, retrieve, and analyze many data types, including simple text, numbers, dates, times, and, more recently, JSON and vectors.

MySQL Database is a client/server system that consists of a multithreaded SQL server that supports different back ends, several client programs and libraries, a choice of administrative tools, and a wide variety of application programming interfaces (APIs). MySQL is available as an embedded multithreaded library that developers can link into applications to get a smaller, faster, easier-to-manage standalone product.

SQL is the most common standardized programming language used to access databases. Depending on the programming environment, a developer might enter SQL directly—for example, to generate reports. It’s also possible to embed SQL statements into code written in another programming language or use a language-specific API that hides the SQL syntax.

## MySQL use cases

MySQL is fast, reliable, scalable, and easy to use. It was originally developed to handle large databases quickly and has been used in highly demanding production environments for many years. MySQL offers a rich and useful set of functions, and it’s under constant development by Oracle, so it keeps up with new technological and business demands. MySQL’s connectivity, speed, and security make it highly suited for accessing databases on the internet.

MySQL use cases include managing customer and product data for ecommerce websites, helping content management systems serve web content, securely tracking transactions and financial data, and powering social networking sites by storing user profiles and interactions.

Ecommerce - Many of the world’s largest ecommerce applications—including Uber and Booking.com—run their transactional systems on MySQL. It’s a popular choice for managing user profiles, credentials, user content, and financial data, including payments, along with fraud detection.

Social platforms - Facebook, X (formerly Twitter), and LinkedIn are among the world’s largest social networks, and they all rely on MySQL.

On-premises applications with MySQL Enterprise Edition - MySQL Enterprise Edition includes the most comprehensive set of advanced features along with management tools and technical support, enabling organizations to achieve the highest levels of MySQL scalability, security, reliability, and uptime. It reduces the risk, cost, and complexity in developing, deploying, and managing business-critical MySQL applications. It provides security features, including MySQL Enterprise Backup, Monitor, Firewall, Audit, Transparent Data Encryption, and Authentication, to help customers protect data and achieve regulatory and industry compliance.

## Comparing MySQL to other databases

### MySQL vs PostgreSQL

### PostgreSQL

Both MySQL and PostgreSQL support JavaScript Object Notation (JSON) to store and transport data, although PostgreSQL also supports JSONB, the binary version of JSON which eliminates duplication of keys and extraneous whitespace.

Features of PostgreSQL include the following:

Point-in-time recovery (PITR) to restore databases to a specific moment in time.

Write ahead log (WAL) that logs all changes to the database using tools such as pgBackRest.

Stored procedures to create and retain custom subroutines.

PostgreSQL is a “one-size-fits-all” solution for many enterprises looking for cost-effective and efficient ways to improve their Database Management Systems (DBMS). It is expandable and versatile enough to quickly support a variety of specialized use cases with a powerful extension ecosystem, covering efforts like time-series data types and geospatial analytics.

PostgreSQL offers the ideal solution for enterprise database administrators responsible for managing online transaction processing (OLTP) protocols for business activities, including e-commerce, customer relationship management systems (CRMs) and financial ledgers. It is also ideal for managing the analytics of the data received, created and generated.

These are some of the main benefits of PostgreSQL:

Performance and scalability — including geospatial support and unrestricted concurrency — and deep, extensive data analysis across multiple data types.

Concurrency support through the use of multiversion concurrency control (MVCC), which enables the simultaneous occurrence of write operations and reads.

Deep language support due to its compatibility and support for multiple programming languages, including Python, Java, JavaScript, C/C++ and Ruby.

Business continuity, with high availability of services through asynchronous or synchronous replication methods across servers.

Greater flexibility and cost-effective innovation through open-source database management technology.

### MySQL

MySQL Workbench is a single, integrated visual SQL platform used for the creation, development, design and management of MySQL databases.

MySQL provides many benefits to the market, including the following:

Unmatched data security — as compared to other database management platforms — due to its use of 
Secure Socket Layer (SSL). This helps to ensure data integrity, which makes it a popular database for web applications.

High performance, because MySQL’s storage-engine framework supports demanding applications with high-speed partial indexes, full-text indexes and unique memory caches for superior database performance.

Scalability and support for unlimited storage growth in a small footprint.

Flexible open-source framework with support for transactional processing, although not as flexible as non-relational databases such as NoSQL.

### PostgreSQL vs MySQL

Database type
- MySQL: Relational
- PostgreSQL: Object-relational

Programming language
- MySQL: C/C++
- PostgreSQL: C

User interface
- MySQL: Workbench GUI
- PostgreSQL: PgAdmin

Encryption between client and server
- MySQL: Transport Layer Security (TLS) protocol
- PostgreSQL: SSL

XML data type support
- MySQL: No
- PostgreSQL: Yes

Support for materialized view and table inheritance
- MySQL: No
- PostgreSQL: Yes

Support for advance data types
- MySQL: No
- PostgreSQL: Yes – hstore and user-defined tdtaa

Support for multiversion concurrency control (MVCC)
- MySQL: No
- PostgreSQL: Yes

In summary, there are distinct uses for both PostgreSQL and MySQL, and the choice between them depends upon enterprise objectives and resources. In general, PostgreSQL is a more robust, advanced database management system, well-suited for an organization that needs to perform complex queries in a large environment quickly. However, MySQL is an ideal solution for a company more constrained by budget and space.

## MySQL advantages

### Flexible and Easy To Use

As open-source software, you can modify the source code to suit your need and don’t need to pay anything. It includes the option for upgrading to the advanced commercial version. The installation process is relatively simple, and shouldn’t take longer than 30 minutes.

MySQL is often praised for being easy to use and for offering broad compatibility with technology platforms and programming languages, including Java, Python, PHP, and JavaScript. MySQL also supports replication from one release to the next, so an application running MySQL 5.7 can easily replicate to MySQL 8.0.

In addition, MySQL offers flexibility in developing both traditional SQL and NoSQL schema-free database applications. This means developers can mix and match relational data and JSON documents in the same database and application.

### High Performance

A wide array of cluster servers backs MySQL. Whether you are storing massive amounts of big eCommerce data or doing heavy business intelligence activities, MySQL can assist you smoothly with optimum speed.

The open source RDBMS can handle high volumes of data and concurrent connections and provide uninterrupted operations under demanding circumstances. This is partly due to MySQL’s robust replication and failover mechanisms, which help minimize the risk of data loss.

Because MySQL is open source, it’s freely available to use at no cost, beyond the on-premises hardware it runs on and training on how to use it. For the latter, a global community of MySQL users provide cost-effective access to learning resources and troubleshooting expertise. Oracle also offers a wide range of training courses.

When it’s time to scale out, MySQL supports multithreading to handle large amounts of data efficiently. Automated failover features help reduce the potential costs of unplanned downtime.

MySQL Enterprise Edition provides advanced security features, including authentication/authorization, transparent data encryption, auditing, data masking, and a database firewall.

### An Industry Standard

Industries have been using MySQL for years, which means that there are abundant resources for skilled developers. MySQL users can expect rapid development of the software and freelance experts willing to work for a smaller wage if they ever need them.

### Secure

Your data should be your primary concern when choosing the right RDBMS software. With its Access Privilege System and User Account Management, MySQL sets the security bar high. Host-based verification and password encryption are both available.

## MySQL disadvantages

1. Limited Scalability for Large-Scale Applications

While MySQL can handle moderate levels of traffic and data, it may struggle with very large-scale applications, especially when compared to other databases like PostgreSQL or NoSQL solutions designed for high scalability.

2. Lack of Advanced Features

MySQL lacks some advanced features that are available in competitors like PostgreSQL, such as:
Advanced indexing techniques (e.g., partial and functional indexes).
Support for more complex SQL queries and features like window functions (though newer versions have improved in this area).
Native JSONB storage and indexing for JSON data.

3. Replication Challenges
   
MySQL's replication mechanism (e.g., master-slave replication) can be complex to set up and maintain. It often requires manual intervention and is less robust compared to modern solutions like PostgreSQL's logical replication or distributed systems like Cassandra.

4. Transaction Handling Limitations

MySQL historically used the MyISAM storage engine, which does not support transactions. While InnoDB resolves this by providing transactional support, it still may not match the advanced transaction handling capabilities of other RDBMS.

5. Less Extensible
   
MySQL is less extensible than PostgreSQL, which allows developers to create custom functions, data types, and operators more easily.

6. Limited Community-Driven Development
   
Since MySQL is now owned by Oracle, some developers perceive a slower pace of innovation compared to open-source community-driven projects like PostgreSQL.

7. Lack of Built-In Full-Text Search (Advanced Needs)

While MySQL offers full-text search capabilities, it is not as powerful as dedicated search engines like Elasticsearch or the full-text capabilities in PostgreSQL.

8. Limited NoSQL Features

MySQL offers support for JSON data types, but it is not designed to be a NoSQL database. Applications requiring extensive NoSQL-like flexibility may find MySQL insufficient.

## MySQL deployment and setup

To deploy and setup a MySQL databases:

1. Plan Your Deployment

- Determine the server environment (local, cloud, or on-premises).
- Choose an appropriate version of MySQL.
- Decide on a storage engine (e.g., InnoDB is recommended for most use cases).

2. Install MySQL on the development environment, ie on Windows, Mac, Linux

3. Configure the security and credentials of the MySQL server and GUI. GUI can be the GUI of the RDBMS, such as MySQL workbench.

4. We can then create a MySQL database and table such as the below:

```sql
CREATE DATABASE my_database;

CREATE USER 'my_user'@'%' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON my_database.* TO 'my_user'@'%';
FLUSH PRIVILEGES;

-- creating the users table
CREATE TABLE users (
    userID INT AUTO_INCREMENT PRIMARY KEY,
    userFullName VARCHAR(100) NOT NULL,
    userEmail VARCHAR(100) UNIQUE NOT NULL
);

SHOW TABLES; -- shows the tables

DESCRIBE users; -- describes and outputs the users table

-- inserting into the users table
INSERT INTO users (userFullName, userEmail)
VALUES 
('John Doe', 'john.doe@example.com'),
('Jane Smith', 'jane.smith@example.com');
```

5. A cloud offering of MySQL can be used to deploy the database to the cloud and on a development, staging or production, such as MySQL heatwave or AWS RDS. The database could then be connected to via other services or clients.

6. For performing backups, cron jobs could be run on a periodic basis. Additionally, updates could be made to the database when new patches or versions come out.
