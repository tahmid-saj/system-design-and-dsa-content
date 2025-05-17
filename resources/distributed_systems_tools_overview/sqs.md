# SQS

## What is SQS

Amazon Simple Queue Service (Amazon SQS) offers a secure, durable, and available hosted queue that lets you integrate and decouple distributed software systems and components. Amazon SQS offers common constructs such as dead-letter queues and cost allocation tags. It provides a generic web services API that you can access using any programming language that the AWS SDK supports.

Messages can contain up to 256 KB of text in any format such as json, xml, etc. Any component of an application can later retrieve the messages programmatically using the Amazon SQS API.

## SQS architecture

### Distributed queues

There are three main parts in a distributed messaging system: the components of your distributed system, your queue (distributed on Amazon SQS servers), and the messages in the queue.

In the following scenario, your system has several producers (components that send messages to the queue) and consumers (components that receive messages from the queue). The queue (which holds messages A through E) redundantly stores the messages across multiple Amazon SQS servers.

<img width="562" alt="image" src="https://github.com/user-attachments/assets/62b8c5e4-c180-40d8-a2a0-5332ab566d99">

The queue acts as a buffer between the component producing and saving data, and the component receives the data for processing. This means that the queue resolves issues that arise if the producer is producing work faster than the consumer can process it, or if the producer or consumer is only intermittently connected to the network.

If you got two EC2 instances which are pulling the SQS Queue. You can configure the autoscaling group if a number of messages go over a certain limit. Suppose the number of messages exceeds 10, then you can add additional EC2 instance to process the job faster. In this way, SQS provides elasticity.

### Message lifecycle

The following scenario describes the lifecycle of an Amazon SQS message in a queue, from creation to deletion.

<img width="485" alt="image" src="https://github.com/user-attachments/assets/1af34e41-2553-48d4-bb22-29b0eaab0792">

1. A producer (component 1) sends message A to a queue, and the message is distributed across the Amazon SQS servers redundantly.

2. When a consumer (component 2) is ready to process messages, it consumes messages from the queue, and message A is returned. While message A is being processed, it remains in the queue and isn't returned to subsequent receive requests for the duration of the visibility timeout.

3. The consumer (component 2) deletes message A from the queue to prevent the message from being received and processed again when the visibility timeout expires.

Note: Amazon SQS automatically deletes messages that have been in a queue for more than the maximum message retention period. The default message retention period is 4 days. However, you can set the message retention period to a value from 60 seconds to 1,209,600 seconds (14 days) using the SetQueueAttributes action.

### Queue types

There are two types of queues:
- Standard queues (default)
- FIFO queues

<img width="308" alt="image" src="https://github.com/user-attachments/assets/1e194af2-3d7d-4682-aa4e-7871c6a82156">

#### Standard queues

You can use standard message queues in many scenarios, as long as your application can process messages that arrive more than once and out of order.

<img width="320" alt="image" src="https://github.com/user-attachments/assets/6fb23cdf-41fd-45ce-86c9-174c56d596fc">

- SQS offers a standard queue as the default queue type.
- Throughput - It allows you to have an unlimited number of transactions per second.
- It guarantees that a message is delivered at least once. However, sometime, more than one copy of a message might be delivered out of order. So it’s essential to have idempotent message processing logic.
- It provides best-effort ordering which ensures that messages are generally delivered in the same order as they are sent but it does not provide a guarantee.
- Standard queues attempt to keep message strings in the same order in which the messages were originally sent, but processing requirements may change the original order or sequence of messages. For example, standard queues can be used to batch messages for future processing or allocate tasks to multiple worker nodes.

#### FIFO queues

FIFO queues are designed to enhance messaging between applications when the order of operations and events is critical, or where duplicates can't be tolerated.

<img width="319" alt="image" src="https://github.com/user-attachments/assets/a75e0e4a-f057-48d8-b5f4-c9ec2781bef9">

- The FIFO Queue complements the standard Queue.
- It guarantees ordering, i.e., the order in which they are sent is also received in the same order.
- The most important features of a queue are FIFO Queue and exactly-once processing, i.e., a message is delivered once and remains available until consumer processes and deletes it.
- FIFO Queue does not allow duplicates to be introduced into the Queue.
- It also supports message groups that allow multiple ordered message groups within a single Queue.
- FIFO Queues are limited to 300 transactions per second but have all the capabilities of standard queues.
- If you require higher throughput, you can enable high throughput mode for FIFO on the Amazon SQS console, which will support up to 70,000 messages per second without batching and even higher with batching.

### Visibility timeout

The visibility timeout is the amount of time that the message is invisible in the SQS Queue after a reader picks up that message.

If the provided job is processed before the visibility time out expires, the message will then be deleted from the Queue. If the job is not processed within that time, the message will become visible again and another reader will process it. This could result in the same message being delivered twice.

The Default Visibility Timeout is 30 seconds. Visibility Timeout can be increased if your task takes more than 30 seconds. The maximum Visibility Timeout is 12 hours.

### Dead letter queues

Dead-letter queues (DLQ) are used to capture messages that cannot be processed successfully after a certain number of attempts, helping to isolate problematic messages for later analysis.

### Long polling

Amazon SQS offers short and long polling options for receiving messages from a queue. Long polling is a feature that allows the Amazon SQS queue to wait for a message to arrive instead of returning an empty response when the queue is empty. This reduces the cost of polling and improves performance

When the wait time for the ReceiveMessage API action is greater than 0, long polling is in effect. The maximum long polling wait time is 20 seconds. Long polling helps reduce the cost of using Amazon SQS by eliminating the number of empty responses (when there are no messages available for a ReceiveMessage request) and false empty responses (when messages are available but aren't included in a response).

### Deduplication

In FIFO queues, Amazon SQS automatically deduplicates messages within a 5-minute window to prevent the same message from being processed more than once.

### SQS features

- SQS is pull-based, not push-based.
- Messages are 256 KB in size.
- Messages are kept in a queue from 1 minute to 14 days.
- The default retention period is 4 days.
- It guarantees that your messages will be processed at least once.

## Use cases

### Batch processing

SQS is typically used to manage workloads that require data processing. The queue can be used for scenarios like data transfer, image processing, and report production since producers can add tasks to it, and consumers can retrieve and process them concurrently.

### Decoupling microservices

In micro-services architectures, services need to communicate with each other asynchronously. SQS allows services to send messages to each other without needing to know the details of the recipient, enabling loose coupling between services.

### Order processing

For e-commerce platforms, SQS can be used to manage order processing. When an order is placed, it can be added to a queue, and multiple workers can process orders in parallel, ensuring timely order fulfillment.

### Notifications

SQS can be used to send notifications or alerts to various parts of an application. For example, an event occurring in one component can publish a message to an SQS queue, which can then be processed by other components for notifications, logging, or real-time updates.

### Asynchronous tasks

Asynchronous processing involves components pushing tasks to an SQS queue and proceeding without waiting to complete the tasks. The tasks are processed later, either by the same system or a different one, which retrieves the messages from the queue.

Asynchronous processing enables tasks requiring significant processing time without stalling the primary application processes. It helps ensure application responsiveness.

## SQS vs message services

### SQS vs AWS MQ vs AWS SNS

Amazon SQS decouples and scales distributed software systems and components as a queue service. It processes messages through a single subscriber typically, ideal for workflows where order and loss prevention are critical. For wider distribution, integrating Amazon SQS with Amazon SNS enables a fanout messaging pattern, effectively pushing messages to multiple subscribers at once.

Amazon SNS allows publishers to send messages to multiple subscribers through topics, which serve as communication channels. Subscribers receive published messages using a supported endpoint type, such as Amazon Data Firehose, Amazon SQS, Lambda, HTTP, email, mobile push notifications, and mobile text messages (SMS). This service is ideal for scenarios requiring immediate notifications, such as real-time user engagement or alarm systems. To prevent message loss when subscribers are offline, integrating Amazon SNS with Amazon SQS queue messages ensures consistent delivery.

Amazon MQ fits best with enterprises looking to migrate from traditional message brokers, supporting standard messaging protocols like AMQP and MQTT, along with Apache ActiveMQ and RabbitMQ. It offers compatibility with legacy systems needing stable, reliable messaging without significant reconfiguration.

The following chart provides an overview of each services' resource type:

<img width="484" alt="image" src="https://github.com/user-attachments/assets/18dd9576-006e-47f4-8222-297031f3cfae">

Both Amazon SQS and Amazon SNS are recommended for new applications that can benefit from nearly unlimited scalability and simple APIs. They generally offer more cost-effective solutions for high-volume applications with their pay-as-you-go pricing. We recommend Amazon MQ for migrating applications from existing message brokers that rely on compatibility with APIs such as JMS or protocols such as Advanced Message Queuing Protocol (AMQP), MQTT, OpenWire, and Simple Text Oriented Message Protocol (STOMP).

### SQS vs Kafka

<img width="433" alt="image" src="https://github.com/user-attachments/assets/501aaa64-31c7-4790-a0c7-e2a7cf9f6241">

When to choose SQS?

When you need a simple, managed, scalable queue for decoupling components or background task processing.

When to choose Kafka?

When you need a high-throughput, distributed event-streaming platform for real-time analytics, data pipelines, or event-driven architectures.

### SQS vs RabbitMQ

<img width="385" alt="image" src="https://github.com/user-attachments/assets/f62b6c56-9541-4160-82a8-cc28c0eb6a68">

When to choose SQS?

When you want a simple, managed service with automatic scaling and minimal setup for decoupling systems or task processing.

When to choose RabbitMQ?

When you need complex routing and protocol support or are looking for an open-source solution for on-premises or cloud deployments.

### SQS vs Kafka vs RabbitMQ

Use Case:
- SQS: Simple message queuing for tasks and decoupling.
- Kafka: High-throughput, distributed event streaming and log storage.
- RabbitMQ: General-purpose messaging with advanced routing and protocol support.

Complexity:
- SQS: Minimal setup and no maintenance (fully managed).
- Kafka: Requires significant expertise to manage clusters and partitions.
- RabbitMQ: Easier than Kafka but requires management of nodes and queues.

Message Replay:
- SQS: Not supported.
- Kafka: Fully supported (messages stored indefinitely or for a defined period).
- RabbitMQ: Limited replay via dead-letter or persistent queues.

Performance:
- SQS: Scales automatically but prioritizes simplicity.
- Kafka: Optimized for high-throughput and real-time processing.
- RabbitMQ: Balanced performance, good for smaller-scale use cases.

Routing Flexibility:
- SQS: Basic (FIFO and delay queues).
- Kafka: Partition-based routing.
- RabbitMQ: Highly flexible routing via exchanges.

<br/>
<br/>
<br/>

SQS:
- Best for simple, serverless queueing with minimal maintenance.
- Suitable for applications running in AWS needing easy integration.

Kafka:
- Ideal for large-scale event-driven systems and real-time data pipelines.
- Best when data replay and high throughput are critical.

RabbitMQ:
- Great for complex message patterns and flexible protocol support.
- Ideal for microservices communication and task-based systems.

## Advantages

### Cloud service

Building software to manage message queues requires advanced development skills. Although there are prepackaged options available, they may require upfront development and configuration. These alternatives also require a continual investment in hardware maintenance and system administration resources, as well as redundant storage in the event of hardware failure. Amazon SQS enables users to sidestep such issues, as it eliminates the additional time and resource requirements.

Amazon SQS queues do not have to be the same. For example, a user can set a default delay on a particular queue. There are also options that enable users to store the contents of messages above a certain size using Amazon Simple Storage Service or Amazon DynamoDB. Larger messages can also be split into a series of smaller ones.

### Security

You control who can send messages to and receive messages from an Amazon SQS queue. You can choose to transmit sensitive data by protecting the contents of messages in queues by using default Amazon SQS managed server-side encryption (SSE), or by using custom SSE keys managed in AWS Key Management Service (AWS KMS). The messages are stored in encrypted form and Amazon SQS decrypts messages only when they are sent to an authorized consumer.

### Durability

For the safety of your messages, Amazon SQS stores them on multiple servers. Standard queues support at-least-once message delivery, and FIFO queues support exactly-once message processing and high-throughput mode.

SQS replicates messages across multiple servers and data centers to ensure low latency and high throughput. This redundancy enables reliable queuing for critical systems that require continuous uptime and robust performance.

### Reliability

Amazon SQS locks your messages during processing, so that multiple producers can send and multiple consumers can receive messages at the same time.

When a message is received, it becomes “locked” while being processed. This keeps other computers from processing the message simultaneously. If the message processing fails, the lock will expire and the message will be available again.

### Customization

Your queues don't have to be exactly alike—for example, you can set a default delay on a queue. You can store the contents of messages larger than 256 KB using Amazon Simple Storage Service (Amazon S3) or Amazon DynamoDB, with Amazon SQS holding a pointer to the Amazon S3 object, or you can split a large message into smaller messages.

## Disadvantages

### Message ordering for standard queues

AWS SQS only guarantees that the message order will be retained in FIFO queues. For standard queues, the order of message delivery is not guaranteed, meaning that messages can be delivered in any order. This makes standard queues unsuitable for applications where the order is critical.

### Throughput limits for FIFO queues

While SQS enables almost unlimited transactions per second for standard queues, it enforces throughput limits for FIFO queues. With batching, the limit is 3,000 messages per second. Without batching, it is 300 messages per second. For some applications, these limits can create a bottleneck.

### No dead letter handling for FIFO queues

In SQS, a dead letter queue (DLQ) can sideline messages that failed to be processed even after multiple attempts. This feature is available for standard queues, but FIFO queues do not support dead letter handling by default. If a message in a FIFO queue consistently fails to be processed, developers must handle it manually.

## Using SQS

### SQS API and SDK

AWS SQS API allows developers to programmatically interact with Amazon Simple Queue Service to create, manage, send, and receive messages from queues. It supports both standard and FIFO queues, offering flexibility for various use cases. With the API, you can automate tasks like sending and receiving messages, batch processing, and setting queue attributes.

Some Key API Functions:
- CreateQueue: To Set up a new queue.
- SendMessage: To Send a message to the queue.
- ReceiveMessage: To Retrieve messages from the queue.
- DeleteMessage: To Remove processed messages.
- Batch Operations: To Perform multiple actions (send, delete) in a single call.

### SQS CLI

AWS SQS CLI Allows you to interact with the Amazon Simple Queue Service (SQS) directly from the command line. This is useful for automating tasks, managing queues, sending and receiving messages, and controlling access, all without needing to use the AWS Management Console.

### Best practices

#### Ensure efficient polling

AWS provides two types of polling: short and long. Short polling responds immediately, sometimes even when messages are available in the queue. Long polling waits for a message to arrive or the timeout to lapse, reducing the number of empty responses and lowering costs. Implementing long polling with proper timeout settings can enhance the efficiency and cost-effectiveness of message processing in SQS.

#### Manage visibility timeouts

Visibility timeouts control the period a message remains invisible in SQS after a reader picks it up. If processing isn’t completed before the timeout expires, the message becomes visible again and might be reprocessed, leading to duplicates. Properly configuring the visibility timeout minimizes this risk and improves the processing reliability of transactions.

#### Implement retry mechanisms

If a message cannot be processed after several attempts, SQS can redirect it to a dead letter queue (DLQ). A DLQ is a collector for problematic messages, which can be examined and reprocessed manually or programmatically. Configuring retry policies and dead letter queues ensures that messages are not lost and errors are properly managed.

#### Use dead letter queues (DLQ)

DLQs help manage messages that fail to process multiple times. By storing these messages aside, developers can later analyze why they weren’t processed and decide corrective measures without affecting the overall system performance. Implementing DLQs ensures that even if a message consistently fails, it does not disappear.

When a message's maximum receive count is exceeded, Amazon SQS moves the message to the DLQ associated with the original queue. DLQs must be of the same type as the source queue (standard or FIFO). You can inspect the messages in DLQs to understand why your consumer has not successfully received them. Once you have remediated the issues, you can move the messages from the DLQ to their respective source queues.

#### Ensure idempotency

Idempotency mechanisms guarantee that a particular operation yields the same result no matter how often it is performed. This is important in environments where message duplication might occur, ensuring consistency and reliability while reducing duplicates and potential conflicts within applications. It is particularly useful for financial transactions and operations that alter system state.


