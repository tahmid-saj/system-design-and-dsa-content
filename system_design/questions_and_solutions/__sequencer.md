# Sequencer

## Requirements

### Questions

- What are the characteristics of unique IDs?
	- IDs must be unique and sortable

- Should the IDs increment by 1 for each new record?
	- IDs increment by time, not necessarily by 1

- Should the IDs only contain numeric values?
	- Yes

- What is the ID length?
	- IDs should fit into a 64 bit

- How many IDs should the system generate per second?
	- The system should generate 10k IDs per second

### Functional

- The IDs contain only numerical values
- The ID should fit into 64 bit
- The system should be able to generate 10k IDs per second
- The IDs grow with time

### Nonfunctional

- Availability / scalability
- Consistency (no duplicates)

## Sequencer 101

Multiple approaches can be used to generate unique IDs in distributed systems such as:

### Multimaster database approach

- In a multimaster database approach we increase the ID by K instead of 1 where K is the number of servers

- This approach does not scale well when a server is added or removed
- Also, the IDs do not go up with time

### UUID

- A UUID (universally unique identifier) is a 128-bit string which has a very low probability of getting a collision.		UUIDs can also be generated independently without coordination between servers.

- A UUID is simple to implement
- A UUID is 128 bits not 64 bits
- The IDs do not go up with time
- Also, the IDs are strings and not numerical

### Ticket server

- Ticket servers are another way to generate unique IDs. Flicker developed ticket servers.

- In this approach, there is a centralized auto_increment feature in a single database server known as the ticket	server. The ticket server performs the auto increments for multiple other web servers as shown in		‘Ticket server’

- A ticket server approach is simple to implement for small to medium scale applications

- The ticket server is a SPOF, and if the ticket server goes down, all services dependent on it will face issues. If we	also have multiple ticket servers, we will introduce a new challenge such as data synchronization

### Twitter snowflake
  
- In a twitter snowflake approach, we divide the 64 bits into different parts as follows and shown in 		‘Twitter snowflake’:
  - 1 bit for sign | 41 bits for timestamp | 5 bits for datacenter ID | 5 bits for machine ID | 12 bits for sequence 		number (4096 sequence IDs per millisecond)

- The sign bit is reserved for future uses, and will always be 0. It can be used to distinguish between signed and	unsigned numbers. The 0 for the sign bit always makes the overall number positive.

- The timestamp will be a UNIX based timestamp down to the millisecond

- The datacenter ID will identify the data center for the data record, and it will be allocated 5 bits which will give us	32 datacenters (2 ^ 5 = 32)

- The machine ID will identify the machine in the data center for the data record, and it will be allocated 5 bits		which will give us 32 machines per data center (2 ^ 5 = 32)

- The sequence ID is 12 bits. For every ID generated on the machine or process, the sequence number is		incremented by 1. The number is reset to 0 every millisecond. The sequence ID adds another layer to avoid 		duplication.

- The bits in Twitter snowflake could also be reduced or increased depending on the use case.

- Using this approach, it’s important to use UTC for the unix based timestamps so that all the timestamps refer to	the same timezone. When generating an ID, the clock in the machine of the datacenter will generate a UNIX		timestamp and a sequence number for the ID that is being generated (the sequencer number will increase by 1 for	every ID generated on the machine or process within that millisecond). The machine or process will use the UNIX	timestamp and sequence number, along with the sign bit, data center ID and machine ID to produce the twitter		snowflake unique ID.

- A twitter snowflake approach is scalable and is unique. Additionally, it fits in 64-bit and contains only numerical	values. Using twitter snowflake is reliable in a distributed system, however the clocks in the individual servers will	need to be synchronized, which will have some error, but this error is still insignificant because of how granular		twitter snowflake is.

### Range handler

- In a range handler approach, different databases handle different ranges of numbers, and a database can		produce unique values in it’s assigned range

- This approach is capable of scaling by adding a new range for a new server, or when removing a server, we can	migrate tha ranges to the new server. 

- We can also use a microservice which can keep track of which ranges are	handled by which server. As this 		microservice can be a SPOF, we can have a backup server for the microservice which recovers the crashed		microservice’s state via checkpointing the modifications to the ranges for the servers.

- A single server can also handle multiple ranges, but a single range cannot be handled by two different servers
	
- A range handler approach is scalable and produces unique IDs, however if a server dies, we lose the range the	server supports. Also, if there is a burst of IDs being generated for a specific range, it could cause a hotspot on a	server

### Logical clocks

We can utilize different logical clocks such as lamport clocks and vector clocks. The combination of the node ID	and the logical timestamps can be used to generate a unique ID that considers causality:

#### Lamport clocks

- Lamport clocks are a mechanism used in distributed systems to assign a sequence of events in a way that		reflects the causality between them. Lamport clocks were introduced to address the ordering of events in			distributed systems where there is no global clock.

- Instead of a real-time timestamp, lamport clocks use a logical timestamp to represent the sequence of			events.

- If one event can potentially affect another, then they are causally related. Lamport clocks ensure that if an		event A happens before an event B, then the logical timestamp of A is less than that of B.
		
- Each node in a distributed system maintains a counter which is the logical timestamp initially set to 0.			When a node processes an event, it includes the node’s counter value in the event’s message. When			another node processes that same event afterwards, the node will update it’s own counter to the max 			between the event’s counter and the node’s counter, + 1 ( max (eventCounter, nodeCounter) + 1 ). This			node will then send the event with the updated counter to any other nodes.
		
- Example of lamport clocks:
  - node_1 performs an event and increments it’s counter to 1
  - node_1 sends the event to node_2 with a counter of 1
  - node_2 has a counter of 0. Node_2 receives the event from node_1 and updates it’s own counter and the		node’s counter to	 max(1, 0) + 1 = 2. 
  - node_2 will send this event to any other nodes with the updated counter.

- Lamport clocks only ensures a partial ordering of the events. Two events which are not causally related		may still have the same counter values. Also, lamport clocks do not scale well when there are multiple		concurrent events happening in a distributed system. Vector clocks addresses the limitation of lamport		clocks by maintaining a vector of counters for each event, and provides a more precise representation of		causality.

#### Vector clocks

- Vector clocks maintain a causality history about all the happened-before relationships for an event.
	
- A vector clock uses a vector of elements, where each element in the vector represents an event in a node.
	The element can be an integer or a tuple such as (node_1, 1) to signify that node_1 processed the event		and increased the counter for the event to 1.

- A full vector clock will look like: event_A[(node_1, 0), (node_2, 1), (node_1, 2)] which shows the causality and which nodes performed operations for which counter values

- Vector clocks show causality for events, but will take up a lot of space if the system or event contains			multiple nodes.

- Vector clocks with twitter snowflake:
  - We could also generate an ID similar to twitter snowflake and use it as an element. We could do the		following:
    - sign bit (1 bit) | vector clock bits for the counters of each node (53 bits) | sequence bits (10 bits)

Ticket server:

<img width="537" alt="image" src="https://github.com/user-attachments/assets/1b152009-0fbe-4274-9d57-b01389959c73" />

<br/>
<br/>

Twitter snowflake:

<img width="578" alt="image" src="https://github.com/user-attachments/assets/e42807e7-0dfc-4aeb-991e-6aafdfeff20e" />

## Wrap up

- Clock synchronization is important in generating unique IDs by time
- More bits for timestamp beyond milliseconds may help for high concurrency and long-term applications if using twitter snowflake
