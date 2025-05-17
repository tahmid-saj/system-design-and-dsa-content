# Metrics monitoring and alerting system

## Requirements

We'll explore the design of a scalable metrics monitoring and alerting system. A well-designed monitoring and alerting system plays a key role in providing clear visibility into the health of the infrastructure to ensure high availability and reliability.

Below are some of the most popular metrics monitoring and alerting services in the marketplace.

<img width="450" alt="image" src="https://github.com/user-attachments/assets/04a80ff6-802f-4eca-9efb-035bfbf643a4" />

### Questions

A metrics monitoring and alerting system can mean many different things to different companies, so it is essential to nail down the exact requirements first with the interviewer. For example, you do not want to design a system that focuses on logs such as web server error or access logs if the interviewer has only infrastructure metrics in mind.

- Who are we building the system for? Are we building an in-house system for a large corporation like Facebook or Google, or are we designing a SaaS service like Datadog, Splunk, etc?
  - We'll build it for internal use only
 
- What metrics do we want to collect?
  - We'll collect operational system metrics. These can be low-level usage data of the OS, such as CPU load, memory usage, and disk space consumption. They can also be high-level concepts such as requests per second of a service or the running server count of a web pool. Business metrics are not in-scope.

- What is the scale of the infrastructure we're monitoring with this system?
  - 100M DAU, 1000 server pools and 100 machines per pool 

- How long should we keep the data?
  - Let's assume a 1-year retention
 
- Can we reduce the resolution of the metrics data for long-term storage?
  - Yes, we would like to be able to keep newly received data for 7 days. After 7 days, you may roll them up to a 1-minute resolution for 30 days. After 30 days, you may further roll them up at a 1-hour resolution.

- What are supported alert channels?
  - Email, phone, PagerDuty, or webhooks (HTTP endpoints)
 
- Do we need to collect logs, such as error logs or access logs?
  - No, just metrics only
 
- Do we need to support distributed system tracing?
  - No

### Functional

- The infrastructure being monitored is large-scale:
  - 100M DAU
  - Assume we have 1000 server pools, 100 machines per pool, 100 metrics per machine -> ~10 million metrics
  - 1-year data retention
  - Data retention policy: raw form for 7 days, 1-minute resolution for 30 days, 1-hour resolution for 1 year
 
- A variety of metrics can be monitored, ie:
  - CPU usage
  - Request count
  - Memory usage
  - Message count in message queues

### Non-functional

- Low latency for queries on metrics:
  - The system needs to have low query latency for dashboards and alerts
- Scaling to metrics and alert volume:
  - The system should be scalable to accommodate growing metrics and alert volume
- Accuracy in not missing critical metrics or alerts:
  - The system should be highly reliable to avoid missing critical alerts
- Adapting to new technologies:
  - Technology keeps changing, so the pipeline should be flexible enough to easily integrate new technologies in the future
 
#### Out of scope

- Log monitoring:
  - The Elasticsearch, Logstash, Kibana (ELK) stack is very popular for collecting and monitoring logs

- Distributed system tracing:
  - Distributed tracing refers to a tracing solution that tracks service requests as they flow through distributed systems. It collects data as requests go from one service to another

## Metrics monitoring 101

- A metrics monitoring and alerting system generally contains 5 components as shown below:

<img width="350" alt="image" src="https://github.com/user-attachments/assets/30938e1e-6fc9-46d7-b4ef-f5ecee5d7276" />

- **Data collection**: collect metric data from different sources.

- **Data transmission**: transfer data from sources to the metrics monitoring system.

- **Data storage**: organize and store incoming data.

- **Alerting**: analyze incoming data, detect anomalies, and generate alerts. The system must be able to send alerts to different communication channels.

- **Visualization**: present data in graphs, charts, etc. Engineers are better at identifying patterns, trends, or problems when data is presented visually, so we need visualization functionality.

### Metrics monitoring data model

Metrics data is usually recorded as a time series that contains a set of values with their associated timestamps. The series itself can be uniquely identified by its name, and optionally by a set of labels.

<br/>
<br/>

For example, if we want to find the CPU load on production server instance i631 at 20:00, we'll use the following graph:

<img width="443" alt="image" src="https://github.com/user-attachments/assets/fce963b6-435d-4133-ba1f-3fd5798e038f" />

The data point in the graph can be represented below:

<img width="422" alt="image" src="https://github.com/user-attachments/assets/a6c563dd-44d3-47c3-aa12-790f70ebbc02" />

In the above example, the time series is represented by the metric name (cpu.load), the labels (host:i631,env:prod), and a single point value at a specific time.

<br/>
<br/>

Let's consider another example: what is the average CPU load across all web servers in the us-west region for the last 10 minutes? Conceptually, we would pull up something like this from storage where the metric name is “CPU.load” and the region label is “us-west”:

```bash
CPU.load host=webserver01,region=us-west 1613707265 50
CPU.load host=webserver01,region=us-west 1613707265 62
CPU.load host=webserver02,region=us-west 1613707265 43
CPU.load host=webserver02,region=us-west 1613707265 53
...
CPU.load host=webserver01,region=us-west 1613707265 76
CPU.load host=webserver01,region=us-west 1613707265 83
```

The average CPU load could be computed by averaging the values at the end of each line. The format of the lines in the above example is called the line protocol. It is a common input format for many monitoring software in the market.

Every time series based metric usually consists of the following:

<img width="500" alt="image" src="https://github.com/user-attachments/assets/54401e05-6421-482a-beef-8b6acc43ad0e" />

### Data access pattern

In the graph below, each label on the y-axis represents a time series (uniquely identified by the names and labels) while the x-axis represents time.

<img width="500" alt="image" src="https://github.com/user-attachments/assets/5544667b-760b-4d5c-88f2-fdb544ad965a" />

The write load is heavy, there can be many time-series data points written at any moment. As mentioned in the requirements, about 10M metrics are written per day at high frequency.

The read load is also spiky, where both visualization and alerting services send queries to the database, and depending on the access patterns of the graphs and alerts, the read volume could be bursty.

In other words, the system is under constant heavy write load, while the read load is spiky.

### Data storage system

For the data storage, a SQL DB is not optimized for operations we would normally perform against time-series data. A SQL DB doesn't perform well under constant heavy write load, and we'll likely be expecting 50k - 100k writes per second or so. If we did use a SQL DB, we would need to spend significant effort in tuning the DB, and even then, it might not perform well.

A NoSQL DB will handle time-series data more effectively. Both Cassandra and Bigtable can be used as opposed to specific time-series DBs. A lot of the times, time-series DBs such as InfluxDB requires SME knowledge, which makes it not always the first choice for storing time-series data. Many NoSQL DBs are alternatives for storing time-series data, and quite a lot of SQL technacalities could be transferred to these NoSQL DBs. For this design, we'll use Cassandra as our DB.

#### Note:

There are many storage systems available that are optimized for time-series data. The optimization lets us use far fewer servers to handle the same volume of data. Many of these databases also have custom query interfaces specially designed for the analysis of time-series data that are much easier to use than SQL. Some even provide features to manage data retention and data aggregation. Here are a few examples of time-series databases.

OpenTSDB is a distributed time-series database, but since it is based on Hadoop and HBase, running a Hadoop/HBase cluster adds complexity. Twitter uses MetricsDB, and Amazon offers Timestream as a time-series database. According to DB-engines, the two most popular time-series databases are InfluxDB and Prometheus, which are designed to store large volumes of time-series data and quickly perform real-time analysis on that data. Both of them primarily rely on an in-memory cache and on-disk storage. And they both handle durability and performance quite well. As shown below, an InfluxDB with 8 cores and 32GB RAM can handle over 250,000 writes per second.

<img width="650" alt="image" src="https://github.com/user-attachments/assets/056d2da4-feaf-4a1b-8a56-288302d23cd5" />

Since a time-series database is a specialized database, you are not expected to understand the internals in an interview unless you explicitly mentioned it in your resume.

Another feature of a strong time-series database is efficient aggregation and analysis of a large amount of time-series data by labels, also known as tags in some databases. For example, InfluxDB builds indexes on labels to facilitate the fast lookup of time-series by labels. It provides clear best-practice guidelines on how to use labels, without overloading the database. The key is to make sure each label is of low cardinality (having a small set of possible values). This feature is critical for visualization, and it would take a lot of effort to build this with a general-purpose database.

### Monitoring types

Once you've designed your system, some interviewers will ask you to discuss how you'll monitor it. The idea here is simple: candidates who understand monitoring are more likely to have experience with actual systems in production. Monitoring real systems is also a great way to learn about how systems actually scale (and break). Monitoring generally occurs at 3 levels, and it's useful to name them.

#### Infrastructure Monitoring

Infrastructure monitoring is the process of monitoring the health and performance of your infrastructure. This includes things like CPU usage, memory usage, disk usage, and network usage. This is often done with a tool like Datadog or New Relic. While a disk usage alarm may not break down your service, it's usually a leading indicator of problems that need to be addressed.

#### Service-Level Monitoring

Service-level monitoring is the process of monitoring the health and performance of your services. This includes things like request latency, error rates, and throughput. If your service is taking too long to respond to requests, it's likely that your users are having a bad time. If throughput is spiking, it may be that you're handling more traffic or your system may be misbehaving.

#### Application-Level Monitoring

Application-level monitoring is the process of monitoring the health and performance of your application. This includes things like the number of users, the number of active sessions, and the number of active connections. This could also include key business metrics for the business. This is often done with a tool like Google Analytics or Mixpanel. This is often the most important level of monitoring for product design interviews.

<br/>

## Data model / entities

- Metric:
  - This entity will be used to feed metric data from machines into the system 
    - metricID
    - metricName
    - value
    - timestamp
    - tags: Map(key:value) pairs

- Alerts:
  - If the SDI involves alerting, we might also have this entity to manage the data in alerts
    - alertID
    - metricID
    - alertStatus: PENDING / SUBMITTED

## API design

### Feed metric values

- Machines will use this endpoint to feed metric data into the system

Request:
```bash
PATCH /metrics/:metricID
{
  metricName,
  value, timestamp
  tags
}
```

### Query metric values

- Query visualizers or dashboards will use this endpoint to query the metric data stored in the system

Request:
```bash
GET /metrics/:metricID?tags&startTimestamp&endTimestamp&nextCursor={ current paginated result's oldest metricID's timestamp }&limit -> Metric[]
```

Response:
```bash
{
  metrics: [{ metricID, metricName, tags, value, timestamp }],
  nextCursor, limit
}
```

## HLD

### Message source

- The Metrics source will be the external application servers, SQL DBs, message queues, etc, which will send the metrics data to the Metrics collector

### Metrics collector

- The Metrics collector will be internal servers which will gather metrics data and write the data into the Metrics database. The Metrics collector is stateless and will also experience a high write load, thus it can be easily horizontally scaled.
- The Metrics collector will also handle the endpoint 'PATCH /metrics/:metricID', which will allow Metrics sources to send metric data to the system.

### Metrics database

- The Metrics database will store the metrics data in Cassandra across multiple nodes to handle a high write load. The Cassandra table will maintain a partition key on the metricID, metricName and date part of the timestamp, while there will be clustering key for the timestamp itself. We'll set the timestamp of the metric value as the clustering key because there may be multiple metrics logged for the same date, and we'll want to sort the metric values in a specific partition by this timestamp, similar to the below example:

![image](https://github.com/user-attachments/assets/26859eca-16a8-4af8-8f85-aeef45c2bb45)

Our CQL create-table statement will then look like:

```cql
create table metrics (
  metricID UUID,
  metricName text,
  createdDate date
  createdTime timestamp,
  tags map<text, text>,
  value int,
  primary key ((metricID, metricName, date), timestamp)
with clustering order by (timestamp asc))
```

### Query service

- The Query service will allow users to query and retrieve data from the Metrics DB. This could be an internal / external service which is essentially a wrapper to the Metrics DB, and provides date-range based queries, or queries to visualize the metrics over time for specific metricID, metricName, tags, etc.
- The Query service will handle the endpoint 'GET /metrics/:metricID' and likely additional querying endpoints for viewing different views of the metric data.

### Alerting system

- The Alerting system will send alert notifications to various alerting destinations after using the Query service to query metric data. Note that for high risk alerts, such as crashes, increasing cpu load, etc, the Metrics collector could directly send the high risk alerts to the Alerting system, instead of allowing the Alerting system to query the metric data itself via the Query service.

### Visualization system

- The Visualization system will show metrics in the form of various graphs / charts.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/6205a829-aa95-48fa-93ae-b26bcd0ad311" />

## DD

### Metrics collection

For metrics collection like counters or CPU usage, occasional data loss is not the end of the world. It’s acceptable for clients to fire and forget. The Metrics collection part of the system is inside the dashed box below.

<img width="637" alt="image" src="https://github.com/user-attachments/assets/23b2836f-8eb8-4fca-9176-a3249c3c57e7" />

#### Pull vs push models

There are two ways metrics data can be collected, pull or push. It is a routine debate as to which one is better and there is no clear answer.

##### Pull model

Below shows data collection with a pull model over HTTP. We have dedicated Metric collector servers which pull metrics values from the running applications periodically.

<img width="512" alt="image" src="https://github.com/user-attachments/assets/2cbc6f90-19c4-4068-9697-f8ea619d1fe9" />

In this approach, the Metrics collector needs to know the complete list of Metric source endpoints to pull data from. One naive approach is to use a file to hold DNS/IP information for every service endpoint on the “metric collector” servers. While the idea is simple, this approach is hard to maintain in a large-scale environment where servers are added or removed frequently, and we want to ensure that metric collectors don’t miss out on collecting metrics from any new servers. The good news is that we have a reliable, scalable, and maintainable solution available through Service Discovery, provided by ZooKeeper, etcd, etc, where services register their availability and the Metrics collector can be notified by the service discovery component whenever the list of service endpoints changes.

The service discovery component contains configuration rules about when and where to collect metrics as shown below:

<img width="436" alt="image" src="https://github.com/user-attachments/assets/fb49c990-72ba-4fca-9db3-27fffb2786b4" />

As shown below, the Metrics collector will then:

1. Discover metric source endpoints using the service discovery component. Service discovery can store data such as pulling interval, IP addresses, timeout and retry parameters, etc.
2. The Metrics collector will then pull metric data via a pre-defined HTTP endpoint like '/metrics/:metricID' on the metric sources - the metric source servers will be responsible for exposing this endpoint.
3. Optionally, the Metrics collector registers a change event notification with service discovery to receive an update whenever the service endpoints change. Alternatively, the metrics collector can poll for endpoint changes periodically.

<img width="454" alt="image" src="https://github.com/user-attachments/assets/7f143ae7-65da-4623-8778-5a642ce812d1" />

At our scale, a single Metrics collector server will not be able to handle thousands of servers. We must use a pool of Metrics collectors to handle the demand. One common problem when there are multiple collectors is that multiple instances might try to pull data from the same resource and produce duplicate data. There must exist some coordination scheme among the instances to avoid this.

One potential approach is to designate each collector to a range in a consistent hash ring, and then map every single server being monitored by its unique name in the hash ring. This ensures one metrics source server is handled by one collector only. Let’s take a look at an example.

As shown below, there are four collectors and 6 metrics source servers. Each collector is responsible for collecting metrics from a distinct set of servers. Collector 2 is responsible for collecting metrics from server 1 and 5.

<img width="652" alt="image" src="https://github.com/user-attachments/assets/88599db8-4487-4761-9833-39da5f71c50a" />

##### Push model

As shown below, in a push model, various metrics sources such as web servers, database servers, etc, directly send metrics to the Metrics collector.

<img width="427" alt="image" src="https://github.com/user-attachments/assets/d3d2cbd5-2c4a-4cb3-bc35-c4167f2f82ee" />

In a push model, a collection job (cron job) might also be installed on every server being monitored. A collection job is a piece of long-running software that collects metrics from the services running on the server and pushes those metrics periodically to the Metrics collector. The collection job may also aggregate metrics (especially a simple counter) locally, before sending them to Metric collectors.

Aggregation is an effective way to reduce the volume of data sent to the Metrics collector. If the push traffic is high and the Metrics collector rejects the push with an error, the collection job could keep a small buffer of data locally (possibly by storing them locally on disk in the metric sources), and resend them later. However, if the metric sources are in an auto-scaling group where they are rotated out frequently, then holding data locally (even temporarily) might result in data loss if the stored local data has not been sent out yet to the Metrics collector (thus the Metrics collector could fall behind).

To prevent the Metrics collector from falling behind in a push model, the Metrics collector should be in an auto-scaling cluster with a load balancer in front of it as shown below. The cluster should scale up and down based on the CPU load of the Metric collector servers so that it doesn't fall behind frequently.

<img width="637" alt="image" src="https://github.com/user-attachments/assets/f2660ff5-75d1-4877-93e0-7dc6f24b25c6" />

##### Pull or push?

So, which one is the better choice for us? Just like many things in life, there is no clear answer. Both sides have widely adopted real-world use cases:

- Examples of pull architectures include Prometheus
- Examples of push architectures include Amazon CloudWatch and Graphite

Knowing the advantages and disadvantages of each approach is more important than picking a winner during an interview. The below table compares the pros and cons of push and pull architectures:

<img width="900" alt="image" src="https://github.com/user-attachments/assets/f63634e5-b399-4007-8a84-87fd5e44f57c" />

As mentioned above, pull vs push is a routine debate topic and there is no clear answer. A large organization probably needs to support both, especially with the popularity of serverless these days - there might not be a way to install a collection job from which to push data in the first place if using a push model.

### Scale the metrics transmission pipeline

We'll now focus on the Metrics collector and Metrics DB (time-series DB). Whether you use the push or pull model, the Metrics collector is a cluster of servers, and the cluster receives enormous amounts of data. For either push or pull, the Metrics collector cluster is set up for auto-scaling, to ensure that there are an adequate number of collector instances to handle the demand.

However, there may be a risk of data loss if the write load is too high where the write requests to the Metrics DB might be throttled. There could also be a data loss if nodes of the Metrics DB crashes (however, this is very unlikely if using Cassandra). To mitigate data loss and handle the write load, we can introduce a queue between the Metrics collector and Metrics DB.

<img width="592" alt="image" src="https://github.com/user-attachments/assets/261cee58-4e12-4cfb-a158-75b97e57b821" />

In this approach, the Metrics collector sends metrics data to the Kafka queue. The Metrics collector will essentially contain the code logic and act as a Kafka producer. There will also be a Kafka sink connector for Cassandra using Kafka Connect, which will consume the data from Kafka, then push the metrics into Cassandra.

#### Scale through kafka

There are a couple of ways that we can leverage Kafka’s built-in partition mechanism to scale our system:

- Configure the number of partitions based on throughput requirements
- Partition metrics data by metricID or metricName, so consumers can aggregate data by a specific metric since messages with the same key (metricID or metricName) will be sent to the same partition - this is shown bellow
- Further partition metrics data by their tags / labels

<img width="450" alt="image" src="https://github.com/user-attachments/assets/d41830d8-43a8-4d16-aad5-d2aab798dcb7" />

#### Where aggregations can happen

Metrics can be aggregated in different places; in the collection job (on the client-side if using a push model), the ingestion pipeline (on the Metrics collector), and the query side (after writing to storage). Let’s take a closer look at each of them:

- **Collection agent**:
  - The collection job installed on the client-side only supports simple aggregation logic. For example, aggregate a counter every minute before it is sent to the Metrics collector.
- **Ingestion pipeline**:
  - To aggregate data before writing to the storage, we usually need stream processing engines such as Spark or Kafka Streams. The write volume will be significantly reduced since only the calculated result is written to the database. However, handling late-arriving events could be a challenge and another downside is that we lose data precision and some flexibility because we no longer store the raw data in the Metrics DB.
- **Query side**:
  - Raw data can be aggregated over a given time period at query time. There is no data loss with this approach, but the query speed might be slower because the query result is computed at query time and is run against the whole raw metrics data.

### Query service

The Query service comprises a cluster of Query servers, which access the Metrics DB and handle requests from the visualization or alerting systems. Having a dedicated set of Query servers decouples the Metrics DB from the downstream clients (Visualization and Alerting systems). And this gives us the flexibility to change the Metrics DB or the Visualization and Alerting systems, whenever needed.

#### Cache servers for Query service

To reduce the load of the Metrics DB and make the Query service more performant, cache servers can be added to store query results as shown below:

<img width="631" alt="image" src="https://github.com/user-attachments/assets/8527ae9e-cabe-44a3-be29-7c4e33822679" />

#### We might not need a Query service

There might not be a need to introduce our own abstraction (a Query service) because most Visualization and Alerting systems have powerful plugins and connectors to interface with well-known databases like Cassandra. For example, instead of implementing the below CQL query in our Query service, different existing Cassandra connectors might already provide the ability to perform the query on Cassandra:

```cql
select metricID, metricName, createdDate, createdDate, tags, value
from metrics
where metricID = :metricID and metricName = :metricName and createdDate = :createdDate
```

### Metrics DB

#### Space optimization

As explained in high-level requirements, the amount of metric data to store is enormous. Here are a few strategies for tackling this:

##### Data encoding and compression

Data encoding and compression can significantly reduce the size of data. Those features are usually built into a good time-series database. Here is a simple example.

<img width="500" alt="image" src="https://github.com/user-attachments/assets/d3c35deb-2a4b-45f2-b8bd-8b0007d8e4a4" />

As you can see in the image above, 1610087371 and 1610087381 differ by only 10 seconds, which takes only 4 bits to represent, instead of the full timestamp of 32 bits. So, rather than storing absolute values, the delta of the values can be stored along with one base value like: 1610087371, 10, 10, 9, 11

##### Downsampling

Downsampling is the process of converting high-resolution data to low-resolution to reduce overall disk usage. Since our data retention is 1 year, we can downsample old data. For example, we can let engineers and data scientists define rules for different metrics. Here is an example:

- If the retention is 7 days, then don't sample
- Retention: 30 days, downsample to 1-minute resolution
- Retention: 1 year, downsample to 1-hour resolution

Let’s take a look at another concrete example. It aggregates 10-second resolution data to 30-second resolution data:

<img width="660" alt="image" src="https://github.com/user-attachments/assets/5d4f1eac-6baa-43f1-ac90-bda758d1b348" />

##### Cold storage

Cold storage is the storage of inactive data that is rarely used. The financial cost for cold storage is much lower.

### Alerting system

For the purpose of the SDI, let’s look at the Alerting system shown below:

<img width="800" alt="image" src="https://github.com/user-attachments/assets/5354e07e-bc9c-4c31-aad8-5608e0d10ec9" />

<br/>

The alert flow works as follows:

1. Load config files to cache servers. Rules are defined as config files on the disk. YAML is a commonly used format to define rules. Here is an example of alert rules:

```yml
- name: instance_down
  rules:

  # Alert for any instance that is unreachable for >5 minutes.
  - alert: instance_down
    expr: up == 0
    for: 5m
    labels:
      severity: page
```

2. The Alert manager fetches alert configs from the cache.

3. Based on config rules, the Alert manager calls the query service at a predefined interval - or it could also directly receive an alert from the Metrics collector is the alert is urgent. If the value violates the threshold, an alert event is created. The Alert manager is responsible for the following:
    - **Filter, merge, and dedupe alerts**. Below is an example of merging alerts that are triggered within one instance within a short amount of time (instance1):
    - **Access control**. To avoid human error and keep the system secure, it is essential to restrict access to certain alert management operations to authorized individuals only.
    - **Retry**. The alert manager checks alert states and ensures a notification is sent at least once.

<img width="450" alt="image" src="https://github.com/user-attachments/assets/add4edfc-a52c-4455-89c4-313074c6ebfe" />

4. The Alert store is a KV store or SQL DB, such as DynamoDB or PostgreSQL, that stores the Alerts entity. It also allows us to ensure via the alertStatus, that the alerts are sent at least once.

5. Eligible alerts are inserted into Kafka.

6. Alert consumers pull alert events from Kafka.

7. Alert consumers process alert events from Kafka and send notifications over to different channels such as email, text message, PagerDuty, or HTTP endpoints.

Note: There are many industrial-scale alerting systems available off-the-shelf, and most provide tight integration with the popular time-series databases. Many of these alerting systems integrate well with existing notification channels, such as email and PagerDuty. In the real world, it is a tough call to justify building your own alerting system. In SDI settings, especially for a senior position, be ready to justify your decision.

### Visualization system

Visualization is built on top of the data layer. Metrics can be shown on the metrics dashboard over various time scales and alerts can be shown on the alerts dashboard. The image below shows a dashboard that displays some of the metrics like the current server requests, memory/CPU utilization, page load time, traffic, and login information.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/f35b8b57-0175-4e60-b488-5523367bae59" />

A high-quality visualization system is hard to build. The argument for using an off-the-shelf system is very strong. For example, Grafana can be a very good system for this purpose. It integrates well with many popular time-series databases which you can buy.

The final design of our system looks as follows:

<img width="900" alt="image" src="https://github.com/user-attachments/assets/a1002f72-5bd5-4ca6-af5b-59d8d665bb54" />











