# Distributed messaging system

## Distributed messaging system introduction

A messaging system is responsible for transferring data among services, applications, processes, or servers. Such a system helps decouple different parts of a distributed system by providing an asynchronous way of transferring messaging between the sender and the receiver. Hence, all senders (or producers) and receivers (or consumers) focus on the data/message without worrying about the mechanism used to share the data.

![image](https://github.com/user-attachments/assets/e015556e-7b83-4f0a-98fb-660a7a48b48a)

There are two common ways to handle messages: Queuing and Publish-Subscribe.

### Queuing

In the queuing model, messages are stored sequentially in a queue. Producers push messages to the rear of the queue, and consumers extract the messages from the front of the queue.

![image](https://github.com/user-attachments/assets/b250aa79-07d9-4402-8684-516280e9d303)

A particular message can be consumed by a maximum of one consumer only. Once a consumer grabs a message, it is removed from the queue such that the next consumer will get the next message. This is a great model for distributing message-processing among multiple consumers. But this also limits the system as multiple consumers cannot read the same message from the queue.

![image](https://github.com/user-attachments/assets/f8541c63-31f3-4276-b03f-5b53b8cccd3f)

### Publish-subscribe

In the pub-sub (short for publish-subscribe) model, messages are divided into topics. A publisher (or a producer) sends a message to a topic that gets stored in the messaging system under that topic. Subscribers (or the consumer) subscribe to a topic to receive every message published to that topic. Unlike the Queuing model, the pub-sub model allows multiple consumers to get the same message; if two consumers subscribe to the same topic, they will receive all messages published to that topic.

![image](https://github.com/user-attachments/assets/5331da39-a1a1-42d1-855b-f849dcd9c9b4)

The messaging system that stores and maintains the messages is commonly known as the message broker. It provides a loose coupling between publishers and subscribers, or producers and consumers of data.

![image](https://github.com/user-attachments/assets/f1260b70-4084-400d-894c-efb122517fb2)

The message broker stores published messages in a queue, and subscribers read them from the queue. Hence, subscribers and publishers do not have to be synchronized. This loose coupling enables subscribers and publishers to read and write messages at different rates.

The messaging system's ability to store messages provides fault-tolerance, so messages do not get lost between the time they are produced and the time they are consumed.

To summarize, a message system is deployed in an application stack for the following reasons:

- Messaging buffering
  - To provide a buffering mechanism in front of processing (i.e., to deal with temporary incoming message spikes that are greater than what the processing app can deal with). This enables the system to safely deal with spikes in workloads by temporarily storing data until it is ready for processing.

- Guarantee of message delivery
  - Allows producers to publish messages with assurance that the message will eventually be delivered if the consuming application is unable to receive the message when it is published.

- Providing abstraction
  - Distributed messaging systems enable decoupling of sender and receiver components in a system, allowing them to evolve independently. This architectural pattern promotes modularity, making it easier to maintain and update individual components without affecting the entire system.

- Scalability
  - Distributed messaging systems can handle a large number of messages and can scale horizontally to accommodate increasing workloads. This allows applications to grow and manage higher loads without significant performance degradation.

- Fault Tolerance
  - By distributing messages across multiple nodes or servers, these systems can continue to operate even if a single node fails. This redundancy provides increased reliability and ensures that messages are not lost during system failures.

- Asynchronous Communication
  - These systems enable asynchronous communication between components, allowing them to process messages at their own pace without waiting for immediate responses. This can improve overall system performance and responsiveness, particularly in scenarios with high latency or variable processing times.

- Load Balancing
  - Distributed messaging systems can automatically distribute messages across multiple nodes, ensuring that no single node becomes a bottleneck. This allows for better resource utilization and improved overall performance.

- Message Persistence
  - Many distributed messaging systems provide message persistence, ensuring that messages are not lost if a receiver is temporarily unavailable or slow to process messages. This feature helps maintain data consistency and reliability across the system.

- Security
  - Distributed messaging systems often support various security mechanisms, such as encryption and authentication, to protect sensitive data and prevent unauthorized access.

- Interoperability
  - These systems often support multiple messaging protocols and can integrate with various platforms and technologies, making it easier to connect different components within a complex system.

## Kafka

Apache Kafka is an open-source publish-subscribe-based messaging system. It is distributed, durable, fault-tolerant, and highly scalable by design. Fundamentally, it is a system that takes streams of messages from applications known as producers, stores them reliably on a central cluster (containing a set of brokers), and allows those messages to be received by applications (known as consumers) that process the messages.

![image](https://github.com/user-attachments/assets/f838858b-c66a-47ef-85c5-6d6c46b9dec8)

Kafka was created at LinkedIn around 2010 to track various events, such as page views, messages from the messaging system, and logs from various services. Later, it was made open-source and developed into a comprehensive system which is used for:

1. Reliably storing a huge amount of data.
2. Enabling high throughput of message transfer between different entities.
3. Streaming real-time data.

At a high level, we can call Kafka a distributed Commit Log. A Commit Log (also known as a Write-Ahead log or a Transactions log) is an append-only data structure that can persistently store a sequence of records. Records are always appended to the end of the log, and once added, records cannot be deleted or modified. Reading from a commit log always happens from left to right (or old to new).

![image](https://github.com/user-attachments/assets/de4d01ea-31a1-4c52-adbf-6f5fd2021fdc)

Kafka stores all of its messages on disk. Since all reads and writes happen in sequence, Kafka takes advantage of sequential disk reads (more on this later).

### Kafka use cases

Kafka can be used for collecting big data and real-time analysis. Here are some of its top use cases:

- Metrics
  - Kafka can be used to collect and aggregate monitoring data. Distributed services can push different operational metrics to Kafka servers. These metrics can then be pulled from Kafka to produce aggregated statistics.

- Log Aggregation
  - Kafka can be used to collect logs from multiple sources and make them available in a standard format to multiple consumers.

- Stream processing
  - Kafka is quite useful for use cases where the collected data undergoes processing at multiple stages. For example, the raw data consumed from a topic is transformed, enriched, or aggregated and pushed to a new topic for further consumption. This way of data processing is known as stream processing.

- Commit Log
  - Kafka can be used as an external commit log for any distributed system. Distributed services can log their transactions to Kafka to keep track of what is happening. This transaction data can be used for replication between nodes and also becomes very useful for disaster recovery, for example, to help failed nodes to recover their states.

- Website activity tracking
  - One of Kafka's original use cases was to build a user activity tracking pipeline. User activities like page clicks, searches, etc., are published to Kafka into separate topics. These topics are available for subscription for a range of use cases, including real-time processing, real-time monitoring, or loading into Hadoop or data warehousing systems for offline processing and reporting.

- Product suggestions
  - Imagine an online shopping site like amazon.com, which offers a feature of 'similar products' to suggest lookalike products that a customer could be interested in buying. To make this work, we can track every consumer action, like search queries, product clicks, time spent on any product, etc., and record these activities in Kafka. Then, a consumer application can read these messages to find correlated products that can be shown to the customer in real-time. Alternatively, since all data is persistent in Kafka, a batch job can run overnight on the 'similar product' information gathered by the system, generating an email for the customer with product suggestions.
 
### Kafka terminology

#### Brokers

A Kafka server is also called a broker. Brokers are responsible for reliably storing data provided by the producers and making it available to the consumers.

#### Records

A record is a message or an event that gets stored in Kafka. Essentially, it is the data that travels from producer to consumer through Kafka. A record contains a key, a value, a timestamp, and optional metadata headers.

![image](https://github.com/user-attachments/assets/0ffe5ed9-5b7a-48f7-b35d-7e024f6ddfe5)

#### Topics

Kafka divides its messages into categories called Topics. In simple terms, a topic is like a table in a database, and the messages are the rows in that table.

- Each message that Kafka receives from a producer is associated with a topic.
- Consumers can subscribe to a topic to get notified when new messages are added to that topic.
- A topic can have multiple subscribers that read messages from it.
- In a Kafka cluster, a topic is identified by its name and must be unique.

Messages in a topic can be read as often as needed — unlike traditional messaging systems, messages are not deleted after consumption. Instead, Kafka retains messages for a configurable amount of time or until a storage size is exceeded. Kafka's performance is effectively constant with respect to data size, so storing data for a long time is perfectly fine.

![image](https://github.com/user-attachments/assets/c5c0ba1f-0ea4-4f80-adb9-f7cfb015aa7a)

#### Producers

Producers are applications that publish (or write) records to Kafka.

#### Consumers

Consumers are the applications that subscribe to (read and process) data from Kafka topics. Consumers subscribe to one or more topics and consume published messages by pulling data from the brokers.

In Kafka, producers and consumers are fully decoupled and agnostic of each other, which is a key design element to achieve the high scalability that Kafka is known for. For example, producers never need to wait for consumers.

### Kafka architecture

At a high level, applications (producers) send messages to a Kafka broker, and these messages are read by other applications called consumers. Messages get stored in a topic, and consumers subscribe to the topic to receive new messages.

#### Kafka cluster

Kafka is deployed as a cluster of one or more servers, where each server is responsible for running one Kafka broker.

#### ZooKeeper

ZooKeeper is a distributed key-value store and is used for coordination and storing configurations. It is highly optimized for reads. Kafka uses ZooKeeper to coordinate between Kafka brokers; ZooKeeper maintains metadata information about the Kafka cluster. We will be looking into this in detail later.

![image](https://github.com/user-attachments/assets/531532e2-9b34-43e7-a6f0-1a2638132c4c)

## Messaging patterns

In the realm of distributed systems, effective communication between various components is crucial for achieving seamless integration and efficient data flow. Messaging patterns play a vital role in enabling this communication by defining standardized approaches to exchanging information between components. These patterns address various scenarios and requirements, such as ensuring message delivery, broadcasting information, and enabling synchronous or asynchronous communication. By understanding and applying these messaging patterns, developers can create robust, scalable, and maintainable distributed systems capable of meeting diverse business needs.

Here are some of the most common messaging patterns, their use cases, and real-life examples to help illustrate their significance and implementation in distributed systems.

### Point-to-point (Direct messaging)

In point-to-point messaging, messages are sent from a single producer to a single consumer. Queues are often used to implement this pattern, ensuring that messages are delivered in a first-in-first-out (FIFO) order. Point-to-point messaging is well-suited for applications where each message must be processed by a single consumer. Key characteristics of point-to-point messaging include:

- Simplicity
  - This pattern is straightforward, making it easy to understand and implement.
- Direct communication
  - Messages are sent directly between the producer and the consumer, without intermediaries.
- Limited scalability
  - Point-to-point messaging may not scale well for large systems with many producers and consumers.

Example: 

An order processing system where an order is placed by a customer, and a single consumer processes the order. The order messages are stored in a queue, and each consumer picks up one order at a time for processing.

### Publish-Subscribe (Pub/Sub)

In the publish-subscribe pattern, messages are sent from a producer (publisher) to multiple consumers (subscribers). The messages are sent to a topic, and all subscribers that have expressed interest in that topic receive the messages. This pattern is ideal for applications requiring the dissemination of information to multiple recipients or when the sender doesn't need to know who the recipients are. Key characteristics of publish-subscribe messaging include:

- Decoupling
  - Producers and consumers are decoupled, improving modularity and flexibility.
- Scalability
  - The pattern can scale to handle many producers and consumers.
- Dynamic subscriptions
  - Consumers can dynamically subscribe and unsubscribe from message topics.

Example: 

A stock market ticker application where stock price updates are sent to a topic. Multiple subscribers, such as trading applications, financial news services, or individual investors, receive these updates in real time.

### Request-reply (Request-response)

In the request-reply pattern, a producer (requester) sends a message to a consumer (responder) and waits for a response. This pattern is often used for synchronous communication between two parties, where the sender requires a response before continuing its operation.

Example: 

An e-commerce application where a user submits a payment request. The payment gateway processes the request and sends back a response indicating whether the payment was successful or not. The e-commerce application waits for the response before proceeding with the order confirmation. Key characteristics of request-reply messaging include:

- Synchronous communication
  - This pattern is often used for synchronous communication between components, where the consumer waits for the reply before proceeding.
- Coupling
  - The pattern can introduce tighter coupling between producers and consumers since the consumer must wait for a reply.
- Latency
  - Request-reply messaging can introduce latency as the consumer must wait for the reply to arrive.
 
### Fan-out/fan-in (Scatter-gather)

In the fan-out/fan-in pattern, a message is sent to multiple consumers (fan-out), and the responses from these consumers are aggregated before being sent back to the original sender (fan-in). This pattern is useful when a task needs to be distributed across multiple workers, and the results must be collected and combined. Key characteristics of fan-out / fan-in messaging include:

- Parallelism
  - The pattern enables parallel processing, improving throughput and performance.
- Load balancing
  - The pattern can be used to distribute workload evenly among consumers.
- Aggregation
  - The fan-in phase allows for aggregation of processed messages, enabling further processing or analysis.

Example: 

A search engine that sends a search query to multiple index servers. Each server returns relevant results, which are then combined and ranked before being sent back to the user as a single, unified set of search results.

### Dead letter queue (DLQ)

The dead letter queue pattern is used to handle erroneous or invalid messages that cannot be processed by consumers. These messages are sent to a dedicated queue called the dead letter queue, where they can be monitored, analyzed, or reprocessed. This pattern helps to ensure that problematic messages do not block the processing of other messages in the system. Key characteristics of Dead Letter Queue messaging include:

- Error handling
  - Unprocessable messages are redirected to the DLQ, preventing them from blocking the primary message queue.
- Monitoring and debugging
  - DLQs can be monitored to detect issues with message processing and help identify the root cause of problems.
- Retention
  - Messages in the DLQ can be retained for a specific period, allowing for the possibility of retries or manual intervention.
- Fault isolation
  - DLQs help isolate problematic messages, reducing the impact of errors on the rest of the system.

Example: 

An email delivery system where messages that fail to be delivered (due to invalid addresses, full mailboxes, etc.) are sent to a dead letter queue. Administrators can then inspect the messages, fix any issues, and attempt to redeliver them.

## Popular message queue systems

In this section, we will discuss some popular messaging queue systems and provide a brief overview of their key features and use cases.

### RabbitMQ

RabbitMQ is an open-source message broker that provides support for various messaging patterns, including publish-subscribe, request-reply, and point-to-point communication. Key features of RabbitMQ include:

- Flexibility
  - RabbitMQ supports various messaging patterns and protocols.
- Clustering and high availability
  - RabbitMQ can be deployed in clustered configurations for fault tolerance and load balancing.
- Extensibility
  - RabbitMQ provides a plugin system to extend its functionality, such as adding support for additional protocols.
- Monitoring and management
  - RabbitMQ includes built-in tools for monitoring and managing the message broker.

### Kafka

Apache Kafka is a distributed streaming platform designed for high-throughput, fault-tolerant, and scalable messaging. Kafka is widely used for stream processing, log aggregation, and event-driven architectures. Key features of Apache Kafka include:

- Distributed architecture
  - Kafka scales horizontally, allowing it to handle high-throughput and provide fault tolerance.
- Durability
  - Kafka stores messages persistently on disk, ensuring data durability and allowing for message replay.
- Low latency
  - Kafka is designed for real-time processing and provides low-latency messaging.
- Stream processing
  - Kafka includes a stream processing API for building real-time data processing applications.

### SQS

Amazon SQS is a fully managed message queuing service provided by Amazon Web Services (AWS). It enables decoupling of components in a distributed system, ensuring reliable and scalable communication. Key features of Amazon SQS include:

- Scalability
  - SQS automatically scales with the number of messages and the number of consumers.
- Reliability
  - SQS guarantees at-least-once message delivery and provides visibility timeouts for message processing.
- Security
  - SQS integrates with AWS Identity and Access Management (IAM) to control access to queues and messages.
- Cost-effective
  - SQS operates on a pay-as-you-go pricing model, making it cost-effective for various workloads.

### ActiveMQ

Apache ActiveMQ is an open-source, multi-protocol message broker that supports a variety of messaging patterns. Key features of Apache ActiveMQ include:

- High availability
  - ActiveMQ provides support for primary-replica replication and network of brokers for increased availability and load balancing.
- Message persistence
  - ActiveMQ supports various persistence options, such as file-based, in-memory, and JDBC-based storage.
- Integration
  - ActiveMQ can be easily integrated with various platforms, such as Java EE and Spring.

## RabbitMQ vs Kafka vs ActiveMQ

### Performance and Scalability

Kafka is designed for high throughput and horizontal scalability, making it well-suited for handling large volumes of data. RabbitMQ and ActiveMQ both offer high performance, but Kafka generally outperforms them in terms of throughput, particularly in scenarios with high data volume.

### Message Ordering

RabbitMQ and ActiveMQ guarantee message ordering within a single queue or topic, respectively. Kafka ensures message ordering within a partition but not across partitions within a topic.

### Message Priority

RabbitMQ and ActiveMQ support message prioritization, allowing messages with higher priority to be processed before those with lower priority. Kafka does not have built-in message priority support.

### Message Model

RabbitMQ uses a queue-based message model following the Advanced Message Queuing Protocol (AMQP), while Kafka utilizes a distributed log-based model. ActiveMQ is built on the Java Message Service (JMS) standard and also uses a queue-based message model.

### Durability

All three message brokers support durable messaging, ensuring that messages are not lost in case of failures. However, the mechanisms for achieving durability differ among the three, with RabbitMQ and ActiveMQ offering configurable durability options and Kafka providing built-in durability through log replication.

### Message Routing

RabbitMQ provides advanced message routing capabilities through exchanges and bindings, while ActiveMQ uses selectors and topics for more advanced routing. Kafka's message routing is relatively basic and relies on topic-based partitioning.

### Replication

RabbitMQ supports replication through Mirrored Queues, while Kafka features built-in partition replication. ActiveMQ uses a Master-Slave replication mechanism.

### Stream Processing

Kafka provides native stream processing capabilities through Kafka Streams, similarly RabbitMQ offers stream processing too, while ActiveMQ relies on third-party libraries for stream processing.

### Latency

RabbitMQ is designed for low-latency messaging, making it suitable for use cases requiring near-real-time processing.

### License

RabbitMQ is licensed under the Mozilla Public License, while both Kafka and ActiveMQ are licensed under the Apache 2.0 License.

## Scalability and performance

Scalability and performance are critical aspects of designing messaging systems in distributed environments. Ensuring that a messaging system can handle a growing number of messages and maintain an acceptable level of performance is crucial for its success.

### Partitioning

Partitioning is the process of dividing a data set into smaller, manageable pieces called partitions. This approach is used in messaging systems to distribute messages evenly among multiple nodes, ensuring that the system can scale horizontally. For example, Apache Kafka uses partitions to divide a topic's messages across multiple brokers, allowing the system to handle large amounts of data and maintain high throughput.

### Consumer groups

Consumer groups are a way to manage multiple consumers of a messaging system that work together to process messages from one or more topics. Each consumer group ensures that all messages in the topic are processed, and each message is processed by only one consumer within the group. This approach allows for parallel processing and load balancing among consumers. For example, in Apache Kafka, a consumer group can have multiple consumers that subscribe to the same topic, allowing the system to process messages in parallel and distribute the workload evenly.

### Load balancing and parallel processing

Load balancing refers to distributing incoming messages evenly among multiple consumers or processing units, while parallel processing involves processing multiple messages simultaneously. In messaging systems, load balancing and parallel processing are achieved through techniques like partitioning, sharding, and consumer groups. For instance, RabbitMQ uses a round-robin algorithm to distribute messages among available consumers, ensuring that the workload is balanced and messages are processed in parallel.

### Message batching and compression

Message batching is the process of combining multiple messages into a single batch before processing or transmitting them. This approach can improve throughput and reduce the overhead of processing individual messages. Compression, on the other hand, reduces the size of the messages, leading to less network bandwidth usage and faster transmission. For example, Apache Kafka supports both batching and compression: Producers can batch messages together, and the system can compress these batches using various compression algorithms like Snappy or Gzip, reducing the amount of data transmitted and improving overall performance.

