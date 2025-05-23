# Recommendation engine for food delivery

## Requirements

### Questions

- A recommendation system uses multiple components, such as a data warehouse / data lake, real-time / batch processes, job scheduler and a analytics engine. Should we design all of this?
  - Let’s only focus on designing the real-time and batch processes

- What will this recommendation engine be used for?
  - Let’s assume it is a generic recommendation engine. But you could say it’s for a food delivery service if it	helps.

- Will the data from the real-time and batch process be sent to a ML model for generating predictions?
  - Yes, we can assume this

### Functional

- Support both real-time and batch process (lambda architecture)
- Data should be sent to a ML model

### Non-functional

- Throughput:
  - Throughput should be managed properly when moving data throughput the system
- Durability:
  - Input for the recommendation data should be persisted

## Recommendation engine 101

### Data warehouses
  
- A data warehouse is a store where all the data generated by services are collected and used by multiple other	services. The data could be used by the analytics team, alerts / monitoring systems, dashboards, etc. Data		warehouses store clean and processed data in a structured format with a fixed schema. Data warehouses are		usually used for analytical or reporting purposes used by a data analyst - mainly used for OLAP workloads.

- From multiple sources, the data could also be queried and joined, then put into a data lake. We pull from multiple	sources because we can’t directly query the data from the individual microservices. Individual microservices will likely maintain the data in an unstructured format, and not optimize the data for complex queries.

### Data lakes

- Data lakes store data from various sources, which can be structured or unstructured and has no defined purpose - mainly used for transactional based OLTP workloads, where real-time transactions take place within the data lakes.	Data lakes can be directly queried by data scientists, and are more cost effective than a data warehouse since		there is no fixed schema. However, data lakes are more complex to query around and require data scientists or	data engineers usually.

- To link the data from all the different sources into a data lake, we can find a common identifier in all the different	sources, such as for a food delivery service, it may be deliveryID. For the food delivery service, deliveryID may be	in a restaurants / payments / trips table.

- Using the deliveryID from above, we can run complex queries, for example to find how many deliveries had to be	refunded. Also, if we had a ML model, we could use the inputs from the restaurants / payments / trips table, and try	to predict the outputs, which is if the deliveryID had to be refunded or was successful. From the ML predictions, if a	specific restaurant had more failed trips or refunds, then the overall food delivery service may promote that		restaurant less, and vice versa. This is shown in ‘ML prediction using data lake’

- Data is fed into a data lake at different intervals, and this is usually done with a batch process via a cron job as	shown in ‘Data lake loading’. The loading into the downstream services, such as alerts, dashboards, operations will	also happen on different intervals, ie the Alerting service (let’s say for the number of trips going down) will want low latency for the data in-take, but the Dashboards service could wait a bit.

- A data lake is also usually immutable, where the entries can be added but not updated. Usually a data lake is		implemented via a file system like HDFS.

ML prediction using data lake:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/f3bdfda0-9956-43cb-b601-15904798d656" />

<br/>
<br/>

Data lake loading:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/75e92b62-a121-489a-9ff7-8ce7ba4bd831" />

### MapReduce

- Using MapReduce, the data within the data lake will likely be sharded, so that each shard can be processed		individually and in parallel via multiple nodes. After parallel processing is done by multiple nodes, the data will	be aggregated down to a single dataset. The parallel processing could include filtering the data, mapping the data to nodes, sorting the data, performing business logic on the data, then aggregating and reducing the data to a final dataset. This final dataset will be sent to a ML model for training,			predictions, evaluations, etc.

- Using MapReduce, horizontal scaling is very easy, since multiple nodes (which are usually stateless) can be added.	Also if any of the nodes crash, another node will be able to resume the operation.

- In MapReduce, the operations could also be broken into different layers, for example in ‘MapReduce layers’, there	is a filter / map / sort / reduce layer.

- A MapReduce process could also fall into a larger ETL process, where the data is first extracted from the data	lake, then transformed via the MapReduce process, and then loaded into different downstream destinations.

MapReduce layers:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/a6612031-4460-4108-80c2-590b4340d2f4" />

### Fault tolerance in MapReduce

Let’s say the second node in the Map layer in ‘MapReduce layers’ crashed, and it can’t send the outputs to the	Sort nodes in the Sort layer. To solve this problem when a node crashes, the previous Filter node for the crashed	Map node could either pull the data from the crashed node OR push the Filter node’s output data to another Map	node. This creates a pull vs push problem:

#### Pull approach

- A pull approach will require the Map node to still be responsive so that the Filter node could retrieve			the data from the crashed Map node and re-do the operation.

#### Push approach

- A push approach will require the Filter node to store it’s previous outputs, so that it could push the			output again to another Map node instead.

#### Hybrid approach - decoupled nodes

- A hybrid approach could also be used where a node is placed between the Filter and Map nodes that			will temporarily store the output from the Filter node - we'll call it the "decoupled node". This will ensure the layers are decoupled, and the			Filter node is not pushing the data to the Map node when the Map node is not ready. In the event a Map			node crashes, another Map node could retrieve the data from this decoupled node and re-try the Map			operation again.
			
- Because these decoupled nodes could contain data which will not be needed, a separate cron job	could be run which will delete any old data. This will reduce the storage on these decoupled nodes. We could also use a Redis cache as the decoupled nodes, and set up a TTL.

- Also, health checks are usually done in MapReduce to ensure fault tolerance, such that crashed nodes			determined by the health checks will not be fed any outputs.

- Within a MapReduce process, a job scheduler could also be used instead of the decoupled nodes, where the job	scheduler sends data from one stage to another in batches. Thus, It will decouple the system as shown in		‘MapReduce job scheduler’. However, the job scheduler can still be a SPOF.

MapReduce job scheduler:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/0893389a-7e99-4f4c-880d-7221b4cb989c" />

### Real-time streaming
  
- To produce real-time streaming, the events / data from the different upstream services could be fed into an event	bus which facilitates real-time communication. This event bus may be a PubSub service like Kafka, where there are	multiple topics for different downstream real-time analytics services (real-time ML predictor, recommendation		engine, etc), and the upstream services such as trips / payments / restaurants will send events to the event bus for	the downstream services to consume those events in real-time.

- Real-time streaming is also different from a MapReduce approach in that it operates with very low latency.		Additionally, a real-time streaming process doesn’t necessarily need to persist the data, as it is loaded from one	place to another very quickly. Also, real-time streaming will usually process smaller chunks of data as opposed to a	MapReduce process. Complex operations are also easier to do in a MapReduce or batch process as opposed to in	real-time streaming. In real-time streaming, availability is usually more important than consistency, thus a missing	event is not critical. 

- Note that an event bus usually provides real-time communication, as opposed to a message queue which		provides asynchronous communication.

### Lambda architecture

- The lambda architecture consists of both the batch (MapReduce) and real-time streaming architecture. A lambda	architecture can balance fault tolerance (batch / MapReduce), throughput (batch / MapReduce) and latency		(real-time streaming) by combining both of these architectures.

### Recommendation engine real-time and batch process

A recommendation engine can utilize both a real-time and batch process as follows:

#### Batch process

- Let’s say we want to find the number of deliveries which failed, the delivery time took over 30 mins and thus was	cancelled by the customer. We can do so using the query in ‘Failed delivery SQL query’. The different operations in	this query, such as filtering, counting, etc can be performed by the different MapReduce layers. Afterwards, the	MapReduce output could be fed into a ML model.

Failed delivery SQL query:
```sql
select count(deliveryID) 
where deliveryStatus = ‘FAILED’ and deliveryTime > 30 and cancelReason = ‘CUSTOMER_CANCELLED’
```

#### Real-time process

- The real-time process could also work with similar but smaller datasets, and use a similar query like the 'Failed delivery SQL query' (likely implemented using Spark streaming or Kinesis), and then send the final dataset to the ML model. Note that we'll want real-time streaming if the downstream services require real-time results, ie if the ML model needs to produce near real-time results.

#### ML model

- After the data is fed into the ML model, the ML model will discover correlations between the input / outputs, and	generate parameters and weights which will be used for future ML predictions. This is the overall process of how a	recommendation engine works as shown in ‘Recommendation engine real-time and batch process’.

Recommendation engine real-time and batch process:

<img width="1200" alt="image" src="https://github.com/user-attachments/assets/ba480a5b-0b11-42b6-b7d0-e34ae93b3c63" />

