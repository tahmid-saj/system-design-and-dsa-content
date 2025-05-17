# Elasticsearch

## What is Elasticsearch?

Over the years, Elasticsearch and the ecosystem of components that’s grown around it called the “Elastic Stack” has been used for a growing number of use cases, from simple search on a website or document, collecting and analyzing log data, to a business intelligence tool for data analysis and visualization. So how did a simple search engine created by Elastic co-founder Shay Bannon for his wife’s cooking recipes grow to become today’s most popular enterprise search engine and one of the 10 most popular DBMS? We’ll answer that in this post by understanding what Elasticsearch is, how it works, and how it’s used.

At its core, you can think of Elasticsearch as a server that can process JSON requests and give you back JSON data.

Elasticsearch is a distributed, open-source search and analytics engine built on Apache Lucene and developed in Java. It started as a scalable version of the Lucene open-source search framework then added the ability to horizontally scale Lucene indices. Elasticsearch allows you to store, search, and analyze huge volumes of data quickly and in near real-time and give back answers in milliseconds. It’s able to achieve fast search responses because instead of searching the text directly, it searches an index. It uses a structure based on documents instead of tables and schemas and comes with extensive REST APIs for storing and searching the data. At its core, you can think of Elasticsearch as a server that can process JSON requests and give you back JSON data.

### How does Elasticsearch work?

Fundamentally, Elasticsearch organizes data into documents, which are JSON-based units of information representing entities. Documents are grouped into indices, similar to databases, based on their characteristics. Elasticsearch uses inverted indices, a data structure that maps words to their document locations, for an efficient search. Elasticsearch’s distributed architecture enables the rapid search and analysis of massive amounts of data with almost real-time performance.

You can send data in the form of JSON documents to Elasticsearch using the API or ingestion tools such as Logstash and Amazon Data Firehose. Elasticsearch automatically stores the original document and adds a searchable reference to the document in the cluster’s index. You can then search and retrieve the document using the Elasticsearch API. You can also use Kibana, a visualization tool, with Elasticsearch to visualize your data and build interactive dashboards.

Let's first cover some components of a search system and Elasticsearch first:

#### Documents

Documents are the basic unit of information that can be indexed in Elasticsearch expressed in JSON, which is the global internet data interchange format. You can think of a document like a row in a relational database, representing a given entity — the thing you’re searching for. In Elasticsearch, a document can be more than just text, it can be any structured data encoded in JSON. That data can be things like numbers, strings, and dates. Each document has a unique ID and a given data type, which describes what kind of entity the document is. For example, a document can represent an encyclopedia article or log entries from a web server.   

#### Indices

An index is a collection of documents that have similar characteristics. An index is the highest level entity that you can query against in Elasticsearch. You can think of the index as being similar to a database in a relational database schema. Any documents in an index are typically logically related. In the context of an e-commerce website, for example, you can have an index for Customers, one for Products, one for Orders, and so on. An index is identified by a name that is used to refer to the index while performing indexing, search, update, and delete operations against the documents in it.

#### Inverted index

An index in Elasticsearch is actually what’s called an inverted index, which is the mechanism by which all search engines work. It is a data structure that stores a mapping from content, such as words or numbers, to its locations in a document or a set of documents. Basically, it is a hashmap-like data structure that directs you from a word to a document. An inverted index doesn’t store strings directly and instead splits each document up to individual search terms (i.e. each word) then maps each search term to the documents those search terms occur within. For example, in the image below, the term “best” occurs in document 2, so it is mapped to that document. This serves as a quick look-up of where to find search terms in a given document. By using distributed inverted indices, Elasticsearch quickly finds the best matches for full-text searches from even very large data sets.

#### Cluster

An Elasticsearch cluster is a group of one or more node instances that are connected together. The power of an Elasticsearch cluster lies in the distribution of tasks, searching, and indexing, across all the nodes in the cluster.

#### Node

A node is a single server that is a part of a cluster. A node stores data and participates in the cluster’s indexing and search capabilities. An Elasticsearch node can be configured in different ways:

Master Node — Controls the Elasticsearch cluster and is responsible for all cluster-wide operations like creating/deleting an index and adding/removing nodes.

Data Node — Stores data and executes data-related operations such as search and aggregation.

Client Node — Forwards cluster requests to the master node and data-related requests to data nodes.

Each node in the cluster can discover each other by cluster name.

#### Shards

Elasticsearch provides the ability to subdivide the index into multiple pieces called shards. Each shard is in itself a fully-functional and independent “index” that can be hosted on any node within a cluster. By distributing the documents in an index across multiple shards, and distributing those shards across multiple nodes, Elasticsearch can ensure redundancy, which both protects against hardware failures and increases query capacity as nodes are added to a cluster.

#### Replicas

Elasticsearch allows you to make one or more copies of your index’s shards which are called “replica shards” or just “replicas”. Basically, a replica shard is a copy of a primary shard. Each document in an index belongs to one primary shard. Replicas provide redundant copies of your data to protect against hardware failure and increase capacity to serve read requests like searching or retrieving a document.

<img width="566" alt="image" src="https://github.com/user-attachments/assets/3a1e6267-a678-48c9-a113-42848a417f54">

### What is Elastic stack (Formerly ELK Stack)?

Elastic stack comprises of logstash, elasticsearch, and kibana. Logstash is responsible for gathering all the raw data and process the data before indexing and storing it in elasticsearch. Once indexed we can run complex queries against their data and use aggregations to retrieve complex summaries of their data. From Kibana, users can create powerful visualizations of their data, share dashboards, and manage the Elastic Stack.

<img width="566" alt="image" src="https://github.com/user-attachments/assets/6449a276-de80-4fe2-b81c-c8fafe60090d">


#### Kibana

Kibana is a data visualization and management tool for Elasticsearch that provides real-time histograms, line graphs, pie charts, and maps. It lets you visualize your Elasticsearch data and navigate the Elastic Stack. You can select the way you give shape to your data by starting with one question to find out where the interactive visualization will lead you. For example, since Kibana is often used for log analysis, it allows you to answer questions about where your web hits are coming from, your distribution URLs, and so on.

If you’re not building your own application on top of Elasticsearch, Kibana is a great way to search and visualize your index with a powerful and flexible UI. However, a major drawback is that every visualization can only work against a single index/index pattern. So if you have indices with strictly different data, you’ll have to create separate visualizations for each.

#### Logstash

Logstash is used to aggregate and process data and send it to Elasticsearch. It is an open-source, server-side data processing pipeline that ingests data from a multitude of sources simultaneously, transforms it, and then sends it to collect. It also transforms and prepares data regardless of format by identifying named fields to build structure, and transform them to converge on a common format. For example, since data is often scattered across different systems in various formats, Logstash allows you to tie different systems together like web servers, databases, Amazon services, etc. and publish data to wherever it needs to go in a continuous streaming fashion.

#### Beats

Beats is a collection of lightweight, single-purpose data shipping agents used to send data from hundreds or thousands of machines and systems to Logstash or Elasticsearch. Beats are great for gathering data as they can sit on your servers, with your containers, or deploy as functions then centralize data in Elasticsearch. For example, Filebeat can sit on your server, monitor log files as they come in, parses them, and import into Elasticsearch in near-real-time.

### Why use Elasticsearch?

Search: The main advantage of using Elasticsearch is it’s rapid and accurate search functionality. For large datasets, relational databases takes a lot more time for search queries because of the number of joins the query has to go through.

Scaling: Distributed architecture of Elasticsearch allows you to scale a lot of servers and data. We can scale the clusters to hundreds of nodes and also we can replicate data to prevent data loss in case of a node failure.

Analytical engine: Elasticsearch analytical use case has become more popular than the search use case. Elasticsearch is specifically used for log analysis

Elasticsearch has client libraries for many programming languages such as Java, JavaScript, PHP, C#, Ruby, Python, Go, and many more.

## Elasticsearch use cases

Application search —- For applications that rely heavily on a search platform for the access, retrieval, and reporting of data.

Website search —- Websites which store a lot of content find Elasticsearch a very useful tool for effective and accurate searches. It’s no surprise that Elasticsearch is steadily gaining ground in the site search domain sphere. 

Enterprise search —- Elasticsearch allows enterprise-wide search that includes document search, E-commerce product search, blog search, people search, and any form of search you can think of. In fact, it has steadily penetrated and replaced the search solutions of most of the popular websites we use on a daily basis. From a more enterprise-specific perspective, Elasticsearch is used to great success in company intranets.

Logging and log analytics —- As we’ve discussed, Elasticsearch is commonly used for ingesting and analyzing log data in near-real-time and in a scalable manner. It also provides important operational insights on log metrics to drive actions. 

Infrastructure metrics and container monitoring —- Many companies use the ELK stack to analyze various metrics. This may involve gathering data across several performance parameters that vary by use case.

## Elasticsearch advantages

### Fast time-to-value

Elasticsearch offers simple REST-based APIs, a simple HTTP interface, and uses schema-free JSON documents, making it easy to get started and quickly build applications for various use cases.

### High performance

The distributed nature of Elasticsearch enables it to process large volumes of data in parallel, quickly finding the best matches for your queries.

### Complimentary tooling and plugins

Elasticsearch comes integrated with Kibana, a popular visualization and reporting tool. It also offers integration with Beats and Logstash, helping you easily transform source data and load it into your Elasticsearch cluster. You can also use various open-source Elasticsearch plugins such as language analyzers and suggesters to add rich functionality to your applications.

### Near real-time operations

Elasticsearch operations such as reading or writing data usually take less than a second to complete. This lets you use Elasticsearch for near real-time use cases such as application monitoring and anomaly detection.

### Easy application development

Elasticsearch provides support for various languages including Java, Python, PHP, JavaScript, Node.js, Ruby, and many more.

## Elasticsearch internals

### Elasticsearch memory requirements

Elasticsearch is run on Java. Hence it requires JVM runtime engine. Each Java process requires a specific amount of heap memory. Similarly Elasticsearch also requires heap memory to run the process. Allocating correct heap size for the elasticsearch process plays a crucial role. In general, we set the max heap size(-Xmx) to 50% of the total RAM.

What happens if too much heap size is allocated?

If too much memory is allocated to the heap for elasticsearch, then more memory can be used for indexing and search operations. But, this may leave less RAM for all other processes. This may lead to more swapping (disk operations) which is known as thrashing.

Besides JVM heap, elasticsearch may use additional memory for various purposes such as caching, field data, and other internal data structures.

What happens if less heap size is allocated?

If less heap memory is allocated then this may lead to OutOfMemory error which is quite common issue in elasticsearch. When the heap size is constrained, Elasticsearch may need to write more frequently to disk to free up memory. This increased disk I/O can put extra strain on the storage system and slow down data read and write operations.

Factors to decide heap memory?

In general, ensure that the heap size is set to a maximum of 50% of the available RAM, but may vary depending on the use case.

JVM garbage collection settings must be optimized based on the specific use case.

The available physical RAM on the system and other memory requirements of your applications.

The size of your dataset and the expected growth rate.

Monitor the heap size and garbage collection metrics to ensure that the cluster is running optimally.

We have seen how important deciding heap size is, now we’ll understand what elasticsearch cache types are and why are they important. Elasticsearch also uses memory for caching. The caches in Elasticsearch can play an important role when it comes to performance. Field data cache, Node query cache, and Shard request cache are few types. We can have caching strategies adjusted based on the nature of the data and the specific requirements of the Elasticsearch cluster.

## Elasticsearch deployment and setup

1. Elasticsearch can be installed from online in Windows, Mac or Linux, or from Docker
2. Elasticsearch can then be configured to run on a specific port
3. It can then be integrated to an application

