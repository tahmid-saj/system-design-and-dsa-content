# Event driven vs polling architecture

Event-Driven and Polling architectures represent two different approaches to monitoring and responding to changes or new data in software systems. Each has its characteristics, benefits, and best use cases.

## Event driven

Event-Driven Architecture is a design pattern in which a component executes in response to receiving one or more event notifications. Events are emitted by a source (like user actions or system triggers), and event listeners or handlers react to these events.

### Characteristics

- Reactive
  - The system reacts to events as they occur.
- Asynchronous
  - Event handling is typically non-blocking and asynchronous.
- Loose Coupling
  - The event producers and consumers are loosely coupled, enhancing flexibility and scalability.
- Real-Time Processing
  - Ideal for scenarios requiring immediate action in response to changes.

### Use cases

- Real-time user interfaces, where user actions trigger immediate system responses.
- Complex event processing in distributed systems.
- Implementing microservices communication via message brokers like Kafka or RabbitMQ.

Example:

In a smart home system, a temperature sensor detects a change in room temperature and emits an event. The heating system subscribes to these events and reacts by adjusting the temperature.

## Polling

Polling Architecture involves a design where a component frequently checks (polls) a source to detect if any new data or change in state has occurred, and then acts on the change.

### Characteristics

- Active Checking
  - The system regularly queries or checks a source for changes.
- Synchronous
  - Polling is often a synchronous and blocking operation.
- Simple to Implement
  - Easier to implement than event-driven systems but can be less efficient.
- Predictable Load
  - The polling interval sets a predictable load on the system.

### Use cases

- Checking for new emails or updates in applications where real-time processing is not critical.
- Monitoring system status or performing routine checks where events are infrequent.

Example:

A backup software that checks every 24 hours to see if new files need to be backed up.

## Event driven vs polling architecture

### Response to Changes

- Event-Driven: Responds immediately to events as they occur.
- Polling: Checks for changes at regular intervals.

### Resource Utilization

- Event-Driven: Generally more efficient with system resources, as it only reacts to changes.
- Polling: Can be resource-intensive, especially with frequent polling intervals.

### Complexity

- Event-Driven: Can be more complex to implement, requiring robust event handling and management.
- Polling: Simpler to implement but may not be as responsive or efficient.

### Real-Time Capability

- Event-Driven: Suitable for real-time applications.
- Polling: More suitable for applications where real-time response is not critical.

### Scalability

- Event-Driven: Scales well, especially in distributed systems with many events.
- Polling: Scaling can be challenging, particularly if the polling frequency is high.

Choosing between event-driven and polling architectures depends on the specific requirements of the application. Event-driven architectures are ideal for systems where immediate responsiveness to changes is critical, and efficiency and scalability are important. Polling architectures, while simpler, are best suited for scenarios where events are less frequent or real-time responsiveness is not a necessity.

