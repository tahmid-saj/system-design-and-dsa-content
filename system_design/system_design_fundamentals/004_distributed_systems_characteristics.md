# Distributed systems characteristics

## Scalability

Scalability is the ability of a system to handle an increasing workload, either by adding more resources (scaling out) or by upgrading the capacity of existing resources (scaling up). In distributed systems, scalability is essential to ensure that the system can effectively manage the growing demands of users, data, and processing power.

Scalability is the capability of a system, process, or a network to grow and manage increased demand. Any distributed system that can continuously evolve in order to support the growing amount of work is considered to be scalable.

A system may have to scale because of many reasons like increased data volume or increased amount of work, e.g., number of transactions. A scalable system would like to achieve this scaling without performance loss.

Generally, the performance of a system, although designed (or claimed) to be scalable, declines with the system size due to the management or environment cost. For instance, network speed may become slower because machines tend to be far apart from one another. More generally, some tasks may not be distributed, either because of their inherent atomic nature or because of some flaw in the system design. At some point, such tasks would limit the speed-up obtained by distribution. A scalable architecture avoids this situation and attempts to balance the load on all the participating nodes evenly.

### Horizontal scaling

Horizontal scaling, also known as scaling out, involves adding more machines or nodes to a system to distribute the workload evenly. This approach allows the system to handle an increased number of requests without overloading individual nodes. Horizontal scaling is particularly useful in distributed systems because it provides a cost-effective way to manage fluctuating workloads and maintain high availability.

### Vertical scaling

Vertical scaling, or scaling up, refers to increasing the capacity of individual nodes within a system. This can be achieved by upgrading the hardware, such as adding more CPU, memory, or storage. Vertical scaling can help improve the performance of a system by allowing it to handle more workloads on a single node. However, this approach has limitations, as there is a physical limit to the amount of resources that can be added to a single machine, and it can also lead to single points of failure.

### Horizontal vs vertical scaling

With horizontal-scaling it is often easier to scale dynamically by adding more machines into the existing pool; Vertical-scaling is usually limited to the capacity of a single server and scaling beyond that capacity often involves downtime and comes with an upper limit.

Good examples of horizontal scaling are Cassandra and MongoDB as they both provide an easy way to scale horizontally by adding more machines to meet growing needs. Similarly, a good example of vertical scaling is MySQL as it allows for an easy way to scale vertically by switching from smaller to bigger machines. However, this process often involves downtime.

![image](https://github.com/user-attachments/assets/70ab13f2-1fd4-4794-8dc5-71c6aad00fb1)

## Reliability

Reliability refers to the ability of a system to continue operating correctly and effectively in the presence of faults, errors, or failures. In simple terms, a distributed system is considered reliable if it keeps delivering its services even when one or several of its software or hardware components fail. Reliability represents one of the main characteristics of any distributed system, since in such systems any failing machine can always be replaced by another healthy one, ensuring the completion of the requested task.

Take the example of a large electronic commerce store (like Amazon), where one of the primary requirement is that any user transaction should never be canceled due to a failure of the machine that is running that transaction. For instance, if a user has added an item to their shopping cart, the system is expected not to lose it. A reliable distributed system achieves this through redundancy of both the software components and data. If the server carrying the user's shopping cart fails, another server that has the exact replica of the shopping cart should replace it.

Obviously, redundancy has a cost and a reliable system has to pay that to achieve such resilience for services by eliminating every single point of failure.

## Availability

By definition, availability is the time a system remains operational to perform its required function in a specific period. It is a simple measure of the percentage of time that a system, service, or a machine remains operational under normal conditions. An aircraft that can be flown for many hours a month without much downtime can be said to have a high availability. Availability takes into account maintainability, repair time, spares availability, and other logistics considerations. If an aircraft is down for maintenance, it is considered not available during that time.

Reliability is availability over time considering the full range of possible real-world conditions that can occur. An aircraft that can make it through any possible weather safely is more reliable than one that has vulnerabilities to possible conditions.

Availability is a measure of how accessible and reliable a system is to its users. In distributed systems, high availability is crucial to ensure that the system remains operational even in the face of failures or increased demand. It is the backbone that enables businesses to provide uninterrupted services to their users, regardless of any unforeseen circumstances.

High availability is often measured in terms of uptime, which is the ratio of time that a system is operational to the total time it is supposed to be operational. Achieving high availability involves minimizing planned and unplanned downtime, eliminating single points of failure, and implementing redundant systems and processes.

When it comes to distributed systems, high availability goes beyond simply ensuring that the system is up and running. It also involves guaranteeing that the system can handle increased load and traffic without compromising its performance. This scalability aspect is crucial, especially in scenarios where the user base grows rapidly or experiences sudden spikes in demand.

### Reliability vs availability

If a system is reliable, it is available. However, if it is available, it is not necessarily reliable. In other words, high reliability contributes to high availability, but it is possible to achieve a high availability even with an unreliable product by minimizing repair time and ensuring that spares are always available when they are needed. Let's take the example of an online retail store that has 99.99% availability for the first two years after its launch. However, the system was launched without any information security testing. The customers are happy with the system, but they don't realize that it isn't very reliable as it is vulnerable to likely risks. In the third year, the system experiences a series of information security incidents that suddenly result in extremely low availability for extended periods of time. This results in reputational and financial damage to the customers.

### High availability strategies

To achieve high availability, organizations implement various strategies that focus on redundancy, replication, load balancing, distributed data storage, health monitoring, regular system maintenance, and geographic distribution.

#### Redundancy and replication

One of the most effective strategies for achieving high availability is redundancy and replication. By duplicating critical components or entire systems, organizations can ensure that if one fails, the redundant system takes over seamlessly, avoiding any interruption in service. Replication involves creating multiple copies of data, ensuring that it is available even if one copy becomes inaccessible.

Redundancy and replication are commonly used in mission-critical systems such as data centers, where multiple servers are deployed to handle the workload. In the event of a hardware failure or system crash, the redundant server takes over, ensuring uninterrupted service for users.

#### Load balancing

Load balancing involves distributing workloads across multiple servers, ensuring that no single server is overwhelmed. Through intelligent load-balancing algorithms, organizations can optimize resource utilization, prevent bottlenecks, and enhance high availability by evenly distributing traffic.

#### Distributed data storage

Storing data across multiple locations or data centers enhances high availability by reducing the risk of data loss or corruption. Distributed data storage systems replicate data across geographically diverse locations, ensuring that even if one site experiences an outage, data remains accessible from other locations.

#### Consistency models (Eventual, Weak, Strong)

Consistency models define how a distributed system maintains a coherent and up-to-date view of its data across all replicas. Different consistency models provide different trade-offs between availability, performance, and data correctness. Strong consistency ensures that all replicas have the same data at all times, at the cost of reduced availability and performance. Weak consistency allows for temporary inconsistencies between replicas, with the advantage of improved availability and performance. Eventual consistency guarantees that all replicas will eventually converge to the same data, providing a balance between consistency, availability, and performance.

#### Monitoring and alerts

Implementing robust health monitoring systems ensures that organizations can proactively identify and address potential issues before they impact system availability. Real-time monitoring and automated alerts enable timely response and rapid resolution of problems, minimizing downtime.

Health monitoring involves continuously monitoring system performance, resource utilization, and various metrics to detect any anomalies or potential issues. Alerts are triggered when predefined thresholds are exceeded, allowing IT teams to take immediate action and prevent service disruptions.

#### Maintenance and system updates

Regular system maintenance and updates are crucial for achieving high availability. By keeping systems up to date with the latest patches, security enhancements, and bug fixes, organizations can mitigate the risk of failures and vulnerabilities that could compromise system availability.

System maintenance involves tasks such as hardware inspections, software updates, and routine checks to ensure that all components are functioning correctly. By staying proactive and addressing any potential issues promptly, organizations can maintain high availability and minimize the impact of system failures.

#### Geographic distribution

Geographic distribution is a strategy that involves deploying system components across multiple locations or data centers. This ensures that even if one region or data center experiences an outage, users can still access the system from other geographically dispersed locations.

Geographic distribution is particularly important for organizations with a global presence or those that rely heavily on cloud infrastructure. By strategically placing system components in different geographical areas, organizations can ensure that users from various locations can access the system without any interruptions, regardless of localized incidents or natural disasters.

## Latency and performance

### Data locality

Data locality refers to the organization and distribution of data within a distributed system to minimize the amount of data that needs to be transferred between nodes. By storing related data close together or near the nodes that access it most frequently, you can reduce the latency associated with data retrieval and improve overall performance. Techniques to achieve data locality include data partitioning, sharding, and data replication.

### Load balancing

Load balancing is the process of distributing incoming network traffic or computational workload across multiple nodes or resources to ensure that no single node is overwhelmed. This helps to optimize resource utilization, minimize response times, and prevent system overloads. Various load balancing algorithms, such as round-robin, least connections, and consistent hashing, can be employed to achieve efficient load distribution and improved system performance.

### Caching

Caching is a technique used to store frequently accessed data or computed results temporarily, allowing the system to quickly retrieve the data from cache instead of recalculating or fetching it from the primary data source. By implementing effective caching strategies, you can significantly reduce latency and improve the performance of your distributed system. Common caching strategies include in-memory caching, distributed caching, and content delivery networks (CDNs).

## Concurrency and coordination

In distributed systems, multiple processes or components often need to work together concurrently, which can introduce challenges related to coordination, synchronization, and data consistency.

### Concurrency control

Concurrency control is the process of managing simultaneous access to shared resources or data in a distributed system. It ensures that multiple processes can work together efficiently while avoiding conflicts or inconsistencies. Techniques for implementing concurrency control include:

- Locking
  - Locks are used to restrict access to shared resources or data, ensuring that only one process can access them at a time.
- Optimistic concurrency control
  - This approach assumes that conflicts are rare and allows multiple processes to work simultaneously. Conflicts are detected and resolved later, usually through a validation and rollback mechanism.
- Transactional memory
  - This technique uses transactions to group together multiple operations that should be executed atomically, ensuring data consistency and isolation.

### Synchronization

Synchronization is the process of coordinating the execution of multiple processes or threads in a distributed system to ensure correct operation. Synchronization can be achieved using various mechanisms, such as:

- Barriers
  - Barriers are used to synchronize the execution of multiple processes or threads, ensuring that they all reach a specific point before proceeding.
- Semaphores
  - Semaphores are signaling mechanisms that control access to shared resources and maintain synchronization among multiple processes or threads.
- Condition variables
  - Condition variables allow processes or threads to wait for specific conditions to be met before proceeding with their execution.

#### Concurrency control vs synchronization

##### Concurrency control

- Primary Goal
  - The main objective of concurrency control is to manage access to shared resources (like data or hardware resources) in an environment where multiple processes or threads are executing simultaneously.
Focus: It is concerned with how to handle situations where multiple processes need to access or modify shared data at the same time.

##### Synchronization

- Primary Goal
  - The purpose of synchronization is to coordinate the timing of multiple concurrent processes or threads. It's about managing the execution order and timing of processes to ensure correct operation.
- Focus
  - It ensures that concurrent processes execute in a way that respects certain timing constraints, like making sure certain operations happen before others or that operations do not interfere destructively with one another.

### Coordination services

Coordination services are specialized components or tools that help manage distributed systems' complexity by providing a set of abstractions and primitives for tasks like configuration management, service discovery, leader election, and distributed locking. Examples of coordination services include Apache ZooKeeper, etcd, and Consul.

### Consistency models

In distributed systems, consistency models define the rules for maintaining data consistency across multiple nodes or components. Various consistency models, such as strict consistency, sequential consistency, eventual consistency, and causal consistency, provide different levels of guarantees for data consistency and can impact the overall system performance, availability, and complexity.

Consistency models are fundamental in distributed systems, defining the rules for how and when changes made by one operation (like a write) become visible to other operations (like reads). Different models offer various trade-offs between consistency, availability, and partition tolerance.

#### Strong consistency

- Definition
  - After a write operation completes, any subsequent read operation will immediately see the new value.
- Example
  - Traditional relational databases (RDBMS) like MySQL or PostgreSQL typically offer strong consistency. If a record is updated in one transaction, any subsequent transaction will see that update.

#### Eventual consistency

- Definition
  - Over time, all accesses to a particular data item will eventually return the last updated value. The time it takes to achieve consistency after a write is not guaranteed.
- Example
  - Amazon's DynamoDB uses eventual consistency. If you update a data item, the change might not be immediately visible to all users, but it will eventually propagate to all nodes.

#### Causal consistency

- Definition
  - Operations that are causally related are seen by all processes in the same order. Concurrent operations might be seen in a different order on different nodes.
- Example
  - In a social media app, if a user posts a message and then comments on that post, any user who sees the comment must also see the original post.

#### Read-your-writes consistency

- Definition
  - Guarantees that once a write operation completes, any subsequent reads (by the same client) will see that write or its effects.
- Example
  - A user profile update in a web application. Once the user updates their profile, they immediately see the updated profile data.

#### Session consistency

- Definition
  - A stronger version of read-your-writes consistency. It extends this guarantee to a session of interactions, ensuring consistency within the context of a single user session.
- Example
  - In an e-commerce site's shopping cart, items added to the cart in a session will be consistently visible throughout that session.

#### Sequential consistency

- Definition
  - Operations from all nodes or processes are seen in the same order. There is a global order of operations, but it doesn't have to be real-time.
- Example
  - A distributed logging system where logs from different servers are merged into a single, sequentially consistent log.

#### Monotonic read consistency

- Definition
  - Ensures that if a read operation reads a value of a data item, any subsequent read operations will never see an older value.
- Example
  - A user checking a flight status on an airline app will not see a departure time that goes back in time; it will only move forward.

#### Linearizability (Strong consistency)

- Definition
  - A stronger version of sequential consistency, it ensures that all operations are atomic and instantly visible to all nodes.
- Example
  - In a distributed key-value store, once a new value is written to a key, any read operation on any node immediately reflects this change.

## Monitoring and observability

### Metrics collection

Metrics are quantitative measurements that provide insights into the performance, health, and behavior of a distributed system. Collecting and analyzing metrics, such as latency, throughput, error rates, and resource utilization, can help identify performance bottlenecks, potential issues, and areas for improvement. Tools like Prometheus, Graphite, or InfluxDB can be used to collect, store, and query metrics in distributed systems.

### Distributed tracing

Distributed tracing is a technique for tracking and analyzing requests as they flow through a distributed system, allowing you to understand the end-to-end performance and identify issues in specific components or services. Implementing distributed tracing using tools like Jaeger, Zipkin, or OpenTelemetry can provide valuable insights into the behavior of your system, making it easier to debug and optimize.

### Logging

Logs are records of events or messages generated by components of a distributed system, providing a detailed view of system activity and helping identify issues or anomalies. Collecting, centralizing, and analyzing logs from all services and nodes in a distributed system can provide valuable insights into system behavior and help with debugging and troubleshooting. Tools like Elasticsearch, Logstash, and Kibana (ELK Stack) or Graylog can be used for log aggregation and analysis.

### Alerting and anomaly detection

Alerting and anomaly detection involve monitoring the distributed system for unusual behavior or performance issues and notifying the appropriate teams when such events occur. By setting up alerts based on predefined thresholds or detecting anomalies using machine learning algorithms, you can proactively identify issues and take corrective actions before they impact users or system performance. Tools like Grafana, PagerDuty, or Sensu can help you set up alerting and anomaly detection for your distributed system.

### Visualization

Visualizing metrics, traces, and logs in an easy-to-understand format can help you better comprehend the state of your distributed system and make data-driven decisions. Dashboards are an effective way to aggregate and display this information, providing a unified view of your system's performance and health. Tools like Grafana, Kibana, or Datadog can be used to create customizable dashboards for monitoring and observability purposes.

## Resilience and error handling

Resilience and error handling help minimize the impact of failures and ensure that the system can recover gracefully from unexpected events.

### Fault tolerance

Fault tolerance is the ability of a system to continue functioning correctly in the presence of faults or failures. Designing a fault-tolerant system involves incorporating redundancy at various levels (data, services, nodes) and implementing strategies like replication, sharding, and load balancing to ensure that the system can withstand failures without impacting users or overall performance.

### Graceful degradation

Graceful degradation refers to the ability of a system to continue providing limited functionality when certain components or services fail. Instead of completely shutting down or becoming unavailable, a gracefully degrading system can continue serving user requests, albeit with reduced functionality or performance. Techniques like circuit breakers, timeouts, and fallbacks can be employed to implement graceful degradation in distributed systems.

### Retry abd backoff

In distributed systems, transient failures like network issues, timeouts, or service unavailability are common. Implementing retry and backoff strategies can help improve resilience by automatically reattempting failed operations with an increasing delay between retries. This can increase the likelihood of successful operation completion while preventing excessive load on the system during failure scenarios.

### Error handling and reporting

Proper error handling and reporting are crucial for understanding and addressing issues in distributed systems. By consistently logging errors, categorizing them, and generating alerts when necessary, you can quickly identify and diagnose problems in the system. Additionally, exposing error information through monitoring and observability tools can help provide insights into system health and behavior.

### Chaos engineering

Chaos engineering is the practice of intentionally injecting failures into a distributed system to test its resilience and identify weaknesses. By simulating real-world failure scenarios, you can evaluate the system's ability to recover and adapt, ensuring that it can withstand various types of failures. Tools like Chaos Monkey or Gremlin can be used to implement chaos engineering in your distributed system.

## Fault tolerance vs high availability

### Fault tolerance

Fault Tolerance refers to a system's ability to continue operating without interruption when one or more of its components fail. Fault-tolerant systems are designed to handle hardware, software, and network failures seamlessly.

#### Characteristics

- Redundancy
  - Incorporates redundancy in system components (like servers, networks, storage) to ensure no single point of failure.
- Automatic Failover
  - Automatically switches to a redundant or standby system upon the failure of a system component.
- No Data Loss
  - Ensures that no data is lost in the event of a failure.
- Cost
  - Generally more expensive due to the need for redundant components.

#### Use cases

Critical applications in sectors like finance, healthcare, and aviation, where system downtime can have severe consequences.

### High availability

High Availability refers to a system's ability to remain operational and accessible for a very high percentage of the time, minimizing downtime as much as possible.

#### Characteristics

- Uptime Guarantee
  - Designed to ensure a high level of operational performance and uptime (often quantified in terms of “nines” – for example, 99.999% availability).
- Load Balancing and Redundancy
  - Achieved through techniques like load balancing, redundant systems, and clustering.
- Rapid Recovery
  - Focuses on quickly restoring service after a failure, though a brief disruption is acceptable.
- Cost-Effectiveness
  - Balances cost against the desired level of availability.

#### Use cases

Online services, e-commerce platforms, and enterprise applications where availability is critical for customer satisfaction and business continuity.

### Fault tolerance vs high availability

- Objective

  - Fault Tolerance is about continuous operation without failure being noticeable to the end-user. It is about designing the system to handle failures as they occur.
  - High Availability is about ensuring that the system is operational and accessible over a specified period, with minimal downtime. It focuses on quick recovery from failures.

- Approach

  - Fault Tolerance: Involves redundancy and automatic failover mechanisms.
  - High Availability: Focuses on preventing downtime through redundant resources and rapid recovery strategies.

- Downtime

  - Fault Tolerance: No downtime even during failure.
  - High Availability: Minimal downtime, but brief interruptions are acceptable.

- Cost and Complexity

  - Fault Tolerance: More expensive and complex due to the need for exact replicas and seamless failover.
  - High Availability: More cost-effective, balancing the level of availability with associated costs.

- Data Integrity

  - Fault Tolerance: Maintains data integrity even in failure scenarios.
  - High Availability: Prioritizes system uptime, with potential for minimal data loss in certain failure conditions.

While both fault tolerance and high availability are about ensuring reliable system operations, they address different levels of resilience and operational continuity. Fault tolerance is about uninterrupted operation even in the face of component failures, while high availability is about keeping the overall system operational as much as possible. The choice between them depends on the specific requirements, criticality, and budget constraints of the business or application in question.

## Efficiency

To understand how to measure the efficiency of a distributed system, let's assume we have an operation that runs in a distributed manner and delivers a set of items as result. Two standard measures of its efficiency are the response time (or latency) that denotes the delay to obtain the first item and the throughput (or bandwidth) which denotes the number of items delivered in a given time unit (e.g., a second). The two measures correspond to the following unit costs:

- Number of messages globally sent by the nodes of the system regardless of the message size.
- Size of messages representing the volume of data exchanges.

The complexity of operations supported by distributed data structures (e.g., searching for a specific key in a distributed index) can be characterized as a function of one of these cost units. Generally speaking, the analysis of a distributed structure in terms of 'number of messages' is over-simplistic. It ignores the impact of many aspects, including the network topology, the network load, and its variation, the possible heterogeneity of the software and hardware components involved in data processing and routing, etc. However, it is quite difficult to develop a precise cost model that would accurately take into account all these performance factors; therefore, we have to live with rough but robust estimates of the system behavior.

## Serviceability or manageability

Another important consideration while designing a distributed system is how easy it is to operate and maintain. Serviceability or manageability is the simplicity and speed with which a system can be repaired or maintained; if the time to fix a failed system increases, then availability will decrease. Things to consider for manageability are the ease of diagnosing and understanding problems when they occur, ease of making updates or modifications, and how simple the system is to operate (i.e., does it routinely operate without failure or exceptions?).

Early detection of faults can decrease or avoid system downtime. For example, some enterprise systems can automatically call a service center (without human intervention) when the system experiences a system fault.

