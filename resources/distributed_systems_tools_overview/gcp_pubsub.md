# GCP Pub/Sub

## What is GCP Pub/Sub

Google Cloud Pub/Sub (Publish/Subscribe) is a fully-managed, scalable, and asynchronous messaging service offered by Google Cloud Platform (GCP). It is designed to enable reliable communication between decoupled systems through message publishing and subscribing. It supports real-time event-driven architectures, where producers send messages to topics and subscribers receive those messages asynchronously.

Pub/Sub decouples producers and consumers, allowing them to operate independently. Producers do not need to know the details of the subscribers, and subscribers can process messages at their own pace. This model is particularly useful in distributed systems and microservices architectures.

## How does it work

Topics:
- A topic is a named resource that represents a stream of messages. Publishers send messages to topics.

Messages:
- A message consists of data (payload) and optional attributes (key-value pairs). Messages are sent to topics and stored temporarily until they are delivered to all subscribers.

Subscriptions:
- Subscriptions are linked to topics. When a subscription is created, Pub/Sub delivers messages from the associated topic to the subscriber. Subscriptions can be push-based (Pub/Sub sends HTTP POST requests to an endpoint) or pull-based (subscribers explicitly pull messages from Pub/Sub).

Ack/Nack Mechanism:
- Subscribers acknowledge (ack) messages upon successful processing. If a message is not acknowledged within a certain period (ack deadline), it is redelivered to ensure reliability.

Message Ordering and Deduplication:
- Pub/Sub guarantees at-least-once delivery by default. Optional features like message ordering (FIFO) and exactly-once delivery are available in specific configurations.

Scalability and Durability:
- Messages are replicated across multiple zones to ensure high availability. Pub/Sub automatically scales to handle large volumes of messages without requiring user intervention.

## Architecture

The architecture of Google Cloud Pub/Sub revolves around three key components: publishers, topics, and subscribers, with a robust underlying infrastructure to ensure reliability, scalability, and availability.

Publisher:
- The publisher is the producer of messages. It sends messages to a specific topic. Publishers are decoupled from subscribers and do not need to know who is consuming the messages.
- Message Format: Each message contains a payload (binary data or text) and optional attributes (key-value metadata).

Topics:
- A topic is a named resource where messages are sent by publishers. It acts as the central point for the message flow.
- Topics are independent of subscribers, enabling a decoupled and distributed system.

Subscribers:
- Subscribers consume messages from a subscription linked to a topic. There are two types of subscribers:
- Pull Subscribers: The subscriber explicitly pulls messages from the subscription.
- Push Subscribers: Pub/Sub pushes messages to an HTTP(S) endpoint provided by the subscriber.

Subscriptions:
- A subscription is a named resource linked to a topic. Each subscription has its own message queue that receives messages from the topic.
- Multiple subscriptions can be associated with a single topic, enabling multiple independent processing pipelines.

Message Delivery:
- At-least-once delivery: Messages are delivered at least once to each subscription. Deduplication logic may be required for idempotent processing.
- Ack/Nack Mechanism: Subscribers acknowledge (ACK) successfully processed messages. If a message is not acknowledged within a configurable acknowledgment deadline, it is redelivered.

Retention and Dead Letter Queues (DLQ):
- Unacknowledged messages are retained for up to 7 days (extendable to 31 days).
- Dead Letter Queues (DLQ) store undeliverable messages after a configured number of delivery attempts.

Ordering:
- By default, Pub/Sub does not guarantee message ordering. However, ordering keys can be used to ensure ordered delivery within the same key.

<br/>
<br/>

Scalability:
- Pub/Sub automatically partitions topics across Google’s global infrastructure to handle large-scale message traffic.
- It uses dynamic load balancing to adapt to traffic spikes.

Storage and Replication:
- Messages are stored in a durable, highly available, and replicated storage system across multiple zones. This ensures data durability and resilience against failures.

Message Processing:
- Pub/Sub uses a fan-out model for distributing messages to multiple subscriptions linked to the same topic.
- The system uses checkpoints and acknowledgments to track message delivery.

Security:
- Pub/Sub supports Identity and Access Management (IAM) for fine-grained access control.
- Messages are encrypted in transit and at rest.

## Use cases

Event-Driven Microservices:
- Enables communication between loosely coupled microservices in real-time. For example, user registration events can trigger multiple downstream services like email notifications and logging.

Data Ingestion for Analytics:
- Collects and streams large volumes of data into analytics platforms like BigQuery or Dataflow. For instance, IoT devices can send telemetry data to Pub/Sub for processing.

Real-Time Notifications:
- Facilitates real-time notifications for applications such as live sports updates, stock price alerts, or user activity tracking.

Log Aggregation:
- Consolidates logs from distributed systems and forwards them to centralized logging platforms for analysis.

Video and Media Processing:
- Transcodes or processes video/audio files asynchronously by publishing media processing jobs to a topic.

## Advantages

Fully Managed Service:
- No need to provision or maintain servers; Pub/Sub automatically scales to handle fluctuating workloads.

Global Scalability:
- Capable of handling millions of messages per second across multiple regions, making it suitable for high-traffic use cases.

Durability and Availability:
- Messages are stored redundantly across multiple availability zones, ensuring reliability.

Decoupled Architecture:
- Allows independent scaling of producers and consumers, improving system flexibility and maintainability.

Integration with GCP Ecosystem:
- Seamlessly integrates with other Google Cloud services like BigQuery, Dataflow, Cloud Functions, and Cloud Run.

Security:
- Offers features like IAM-based access control, message encryption, and secure endpoints.

## Disadvantages

At-Least-Once Delivery:
- By default, Pub/Sub guarantees at-least-once delivery, which may result in duplicate messages. Implementing deduplication requires additional effort.

Latency:
- While Pub/Sub is optimized for real-time processing, pull-based subscriptions may introduce latency if subscribers poll infrequently.

Ordering Constraints:
- Message ordering is not guaranteed by default. Enabling it comes with limitations (e.g., one publisher per region for a topic).

Cost Considerations:
- Costs can escalate for high-throughput applications, especially if messages are retained for long durations or if there are multiple subscriptions.

Feature Parity:
- Compared to some alternatives like Kafka, Pub/Sub lacks advanced features like message replay from specific offsets (though snapshots can provide similar functionality).

## GCP Pub/Sub vs other services

### GCP Pub/Sub vs Kafka

Architecture:
- Kafka is a distributed log-based messaging system, while Pub/Sub is a fully managed publish-subscribe service.
- Kafka requires a dedicated cluster and more operational management, whereas Pub/Sub is serverless.

Use Cases:
- Kafka excels in high-throughput, low-latency scenarios and offers fine-grained control over message offsets and retention.
- Pub/Sub is better for users who prefer a fully managed solution and need to integrate seamlessly with GCP.

Message Retention:
- Kafka allows long-term message retention with replay capabilities.
- Pub/Sub has limited retention (up to 7 days by default, extendable to 31 days).

Scaling:
- Kafka requires explicit scaling of brokers and partitions, whereas Pub/Sub scales automatically.

### GCP Pub/Sub vs SNS

Purpose:
- Pub/Sub and SNS are similar in their publish-subscribe models, but SNS focuses more on simple notification-based workflows.
- Pub/Sub offers richer features like pull subscriptions, message deduplication, and ordering.

Integration:
- SNS integrates seamlessly with AWS services, while Pub/Sub integrates with GCP services.

Subscriber Types:
- SNS supports multiple subscriber types (e.g., SMS, email, HTTP). Pub/Sub is optimized for application-to-application messaging.

### GCP Pub/Sub vs SQS

#### Message Model

GCP Pub/Sub:
- Supports a publish-subscribe model, allowing multiple subscribers to process the same message independently.
- Messages are distributed to subscriptions linked to a topic, with each subscription having its own message queue.

AWS SQS:
- Primarily a queue-based model designed for point-to-point communication.
- Messages are sent to an SQS queue and consumed by a single consumer (unless the queue is shared).

#### Message Retention

GCP Pub/Sub:
- Messages are retained for up to 7 days (extendable to 31 days).
- Unacknowledged messages are redelivered until acknowledged or the retention period expires.

AWS SQS:
- Default retention period is 4 days (extendable to 14 days).
- Once a message is read and acknowledged, it is deleted from the queue.

#### Message Delivery Semantics

GCP Pub/Sub:
- Guarantees at-least-once delivery. Duplicates may occur, requiring deduplication logic in the application layer.

AWS SQS:
- Offers at-least-once delivery by default but supports exactly-once delivery in FIFO queues.
- FIFO queues guarantee strict ordering, which is an optional feature.

#### Subscription Types

GCP Pub/Sub:
- Supports push and pull delivery models, offering flexibility for different use cases.

AWS SQS:
- Pull-only by default. Integration with SNS can enable a publish-subscribe pattern but lacks the flexibility of Pub/Sub’s built-in model.

<img width="548" alt="image" src="https://github.com/user-attachments/assets/cf0f8b60-9f01-4c58-9ec2-0b3934eaaff1">

<br/>
<br/>

#### Use Cases

GCP Pub/Sub:
- Event-driven systems.
- Real-time analytics pipelines.
- Global systems requiring high throughput and low latency.
- Scenarios with multiple subscribers processing the same event stream.

AWS SQS:
- Task queues for microservices.
- Decoupling producer/consumer systems.
- Scenarios requiring FIFO or deduplication (via FIFO queues).

<img width="550" alt="image" src="https://github.com/user-attachments/assets/9b0bb69c-61b4-46dc-8f8f-a704804d6c53">

- GCP Pub/Sub is ideal for real-time event-driven systems, global architectures, and use cases where multiple consumers need to process the same data stream.

- AWS SQS is better suited for point-to-point messaging, deduplication, and use cases requiring strict FIFO. However, for publish-subscribe use cases, SNS + SQS is required, which lacks the seamless integration provided by Pub/Sub.

- The choice between the two depends on workload patterns, system architecture, and the cloud ecosystem in use.

### GCP Pub/Sub vs RabbitMQ

Architecture:
- RabbitMQ is a broker-based messaging system that supports advanced queuing patterns like priority queues and message acknowledgments.
- Pub/Sub is designed for cloud-native, high-throughput use cases.

Deployment:
- RabbitMQ requires manual setup and maintenance, while Pub/Sub is fully managed.

Message Ordering:
- RabbitMQ offers strict FIFO by default. Pub/Sub requires explicit configuration for message ordering.

GCP Pub/Sub is a powerful, scalable, and managed messaging service ideal for modern cloud-native applications. While it has some limitations compared to other systems like Kafka, RabbitMQ, or SNS, its seamless integration with the GCP ecosystem and auto-scaling capabilities make it an attractive choice for organizations using Google Cloud. The choice between these services depends on specific use cases, workload patterns, and operational preferences.
