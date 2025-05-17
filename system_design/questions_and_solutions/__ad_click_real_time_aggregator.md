# Ad click event aggregator - real-time

An Ad Click Aggregator is a system that collects and aggregates data on ad clicks. It is used by advertisers to track the performance of their ads and optimize their campaigns. For our purposes, we will assume these are ads displayed on a website or app, like Facebook.

## Requirements

### Questions

- In the system, users can click on ads placed on websites and get redirected, and we can query the ad click event aggregations which are registered. Are we designing this?
  - Yes

- Does the system require real-time aggregations, ie it needs to query data which just got registered in the past few minutes or so?
  - Yes, we require real-time aggregations

- What is the format of the input data?
  - It’s a log file located in different servers, and the latest click events are appended to	the end of the log file. The event has the following attributes:
    - adID, clickedAt, userID, IP, country

- The scale is very important for this design, how many ads does the system have, and what is the number of ad clicks happening per second?
  - Let's assume there's 10M active ads, and 1B ad clicks happening per day.
  - The number of ad click events also grows 30% year over year

- What are some of the most important queries to support?
  - Return the number of click events for a particular ad in the last M minutes
  - Return the top N most clicked ads in the last M minutes
    - Both parameters of M minutes and N most clicked ads should	be	configurable. Aggregation also occurs every minute
    - The above 2 queries should support filtering by IP address, userID or country

- What are some edge cases to consider?
  - There might be ad click events that arrive into the servers much later than when the ad was clicked
  - There might be duplicated ad click events

- What is the latency requirement?
  - Latency for RTB (real-time bidding discussed in 'Ad click event aggregation 101') and ad click aggregation are very different. The aggregation for RTB usually happens in less 	than a second, while the aggregation for ad click event aggregation usually occurs in a few		minutes because it is primarily used for ad billing and reporting

### Functional

- Users can click on an ad and be redirected to the advertiser's website
- Advertisers can query ad click metrics over time with a minimum granularity of 1 minute. The queries include:
  - Aggregate the number of clicks of adID in the last M minutes
  - Return the top N most clicked adIDs in the last M minutes
    - Both parameters of M minutes and N most clicked ads should	be	configurable. Aggregation also occurs every minute
    - Support aggregation filtering by different fields such as IP address, userID or country for the above 2 queries

- There's 10M active ads, and 1B ad clicks per day

### Non-functional

- Throughput:
  - The system should support roughly 10K ad clicks per second (1B ad clicks per day means 10K ad clicks per second)
- Latency:
  - Query results should be returned quickly (<1 s)
  - Advertisers should be able to query the same ad click data as soon as possible right after the ad click is registered
- Data accuracy:
  - The data stored and aggregation result should be correct and not have duplicated events or lost click data

## Ad click event aggregation 101

- Digital advertising has a core process called Real-Time Bidding (RTB), in which digital advertising inventory is bought and sold. The RTB process usually occurs in less than a second. The key metrics used in online advertising include click-through rate (CTR) and conversion rate (CVR)

## Data model / entities

### Ads
- This entity will represent an ad that is placed in a website, and which users will click on. If we're only designing the querying feature of the system, then we don't necessarily need this entity. We only need this entity if we're designing the redirection logic as well.
  - adID
  - redirectURL
  - website

<br/>
<br/>

There are mainly two types of data the system will collect:
  - Raw data:
    - The raw data contains the full dataset and supports filtering and recalculation. It requires a large storage and direct queries on it are very slow.
  - Aggregated data:
    - The aggregated data is an aggregation of the raw data, and is a smaller dataset than the raw data and supports faster queries.
    - The aggregated data contains aggregates so there is some data loss, ie 10 entries from the raw data can be aggregated into 1 entry

We should store both the raw and aggregated data for the reasons below:
  - If the aggregated data is lost, the aggregated data could still be derived from the raw data
  - The aggregated data should be stored for fast querying
  - If the aggregated data is invalid, aggregations can be recalculated on the raw data to	get new aggregated data
  - When a worker processing the raw data crashes, the raw data should still be persisted so that another worker can retry processing the raw data again


### Raw data

- Over time, older raw data could be moved to cold storage to reduce storage costs

  - adID
  - clickedAt
  - userID
  - IP
  - country

### Aggregated data

**The aggregated data is both read and write heavy, and will likely be written to every minute or so, which is the aggregation window**
  
- Ad click counts:
  - To support ad filtering, we can also add an additional field called the filterID to this "Ad click events" entity. For a single	adID and clickMinute, there will be multiple filterIDs for common filters made on the raw data. A separate filters entity will also be used to contain the actual filters made. The "Ad click events" entity / table (top table), and filters entity / table (bottom table) are shown in 'Filtering table logic', where the filterID is a foreign key that references a specific filter on the filters entity.

  - To support filtering, we can include fields such as country, region, device, etc in the aggregated data.	This format is known as a star schema, where the table contains filtering fields called		dimensions.

    - adID
    - advertiserID
    - clickMinute (this can be an integer value such as 202101010001 or a UNIX timestamp)
    - adClickCount
    - filterID

- Filters:
  - filterID
  - country, region, device, etc

<br/>

Filtering table logic:

<img width="600" alt="image" src="https://github.com/user-attachments/assets/a478d9a0-052a-40e3-a612-290979dc9f69" />

<br/>
<br/>
<br/>

- Top N most clicked ads for a specific clickMinute (we'll call this "Most clicked ads" entity):
  - This entity will contain the clickMinute as an integer value, and the most clicked ads for the clickMinute
  - Everytime a new click minute window appears with time, we'll find the mostClickedAds for the new click minute window using the raw data, and then add an entry with the clickMinute and mostClickedAds into this entity. We can limit the mostClickedAds list to, let's say 1000 or so.
  - Like the "Ad click counts" entity, this entity could also contain the filterID foreign key which references the filters entity, where there are different mostClickedAds values for different filterIDs.
    
    - clickMinute (this can be an integer value such as 202101010001 or a UNIX timestamp)
    - mostClickedAds: [ { adID, clickCount } ]
    - filterID

## API design

- Note: The client is the advertiser or admin who runs queries against the aggregation service

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

### User clicks on an adID on a website

- After the user clicks on a specific ad on a website, the user will also send a request to this endpoint such that the system can track the click and then redirect the user to the advertiser's website

Request:
```bash
POST /ads/:adID/click
```

Response:
```bash
HTTP/1.1 301 / 302 Redirection
Location: <AD_REDIRECT_URL>
```

### Query the number of clicks for a specific adID in the last M minutes

- This endpoint allows us to query the "Ad click counts" entity using an adID and M minutes, where we can request from AND/OR to clickMinute timestamps, and potentially any fields to filter on.
- This endpoint will return the sum of the adClickCounts from the adID entries where the clickMinute field in the entity falls between the from and to timestamps provided in the request. We'll also join on the filters table, and return the appropriate sum of the adClickCounts for the filters provided in the request.

**Note that the following SQL queries are only a POC and not what the querying will look like as these queries will be very slow**

- The SQL query for this endpoint might look as follows:
```sql
-- Without filtering:
select sum(adClickCount) from adClickCountsTable
where adID = ${adID} and clickMinute between ${from} and ${to}

-- With filtering:
select sum(adClickCount) from (
(select adClickCount, filterID from adClickCountsTable
where adID = ${adID} and clickMinute between ${from} and ${to}) as adClick
inner join
(select filterID from filtersTable
where country = ${country} and region = ${region} and device = ${device}) as filters
on adClick.filterID = filters.filterID)
```

Request:
```bash
GET /ads/:adID/adClickCount?from&to&filters={ COUNTRY=CANADA & DEVICE=MOBILE }
```

Response:
```bash
{
  adID
  adClickCount
}
```

### Query the top N most clicked adIDs in the last M minutes

- This endpoint returns the top N most clicked adIDs in the last M minutes using the "Most clicked ads" entity
- This endpoint queries the "Most clicked ads" entity using the from and to clickMinute timestamps provided in the request. It will then return the top N adIDs using the N value provided in the request. We could also potentially add any filters

- The SQL query for this endpoint might look as follows:
```sql
-- Without filtering:
select unnest(mostClickedAds) as mostClickedAdsList(adID, clickCount) from mostClickedAdsTable
where clickMinute between ${from} and ${to}
group by adID
order by clickCount
limit ${n}

-- With filtering:
select adID from (
(select unnest(mostClickedAds) as mostClickedAdsList(adID, clickCount), filterID from mostClickedAdsTable
where clickMinute between ${from} and ${to}) as mostClickedAds
inner join
(select filterID from filtersTable
where country = ${country} and region = ${region} and device = ${device}) as filters
on mostClickedAds.filterID = filters.filterID)
group by adID
order by clickCount
limit ${n}

-- Note that we'll use unnest(), which is supported in PostgreSQL, to split an array into separate rows.
-- Also mostClickedAdsList specifies the name we'll give to the unnested list
```

Request:
```bash
GET /ads/topNAds?n&from&to&filters={ COUNTRY=CANADA & DEVICE=MOBILE }
```

Response:
```bash
{
  mostClickedAds: [ adIDs ]
}
```

## Workflow / data flow

The workflow of the ad click aggregator will be:

1. User clicks on an adID on a website
2. The click is stored in the raw data using the userID, clickedAt, country, IP, etc fields
3. The user is redirected to the adversiter's website
4. The system will aggregate the clicks data
5. Adversiters or admins can query the system for aggregated click metrics

## High level design

### Real-time (Streaming) vs batch (MapAggregateReduce) processing

- This design will talk about using both approaches, but the final design is using real-time processing.

- Overall, if real-time aggregation is not a requirement, we could likely go with batch processing. But if real-time aggregation is required, we could go with stream processing. Since we need real-time aggregation / query for this design, we'll use stream processing.

#### Real-time processing

- Stream / real-time processing is about processing small chunks of data quickly. Stream processing is more suitable if the data intake has an even distribution and is consistent throughout, such as with ad click events. Stream processing also requires resources to be constantly available

- The real-time processing approach via a Kafka event stream and spark streaming workers is a synchronous processing approach, where it aggregates smaller datasets every minute or so, and pushes the output to an OLAP database.
- If there are sudden spikes in the ad click traffic, then this approach might cause some hotspots, but scaling the system should take care of these short-lived hotspots.

#### Batch processing

- Batch processing tends to have a higher processing time than stream processing because batch processing handles a larger sized data chunk. Also batch processing can handle complex operations such as aggregating the data since the data doesn't need to be processed in real-time. However, ad click aggregation is relatively simple.
- Batch processing is more appropriate for workloads with spikes or uneven distributed, and it doesn't require resources to be constantly available.

- A batch processing approach, with a MapAggregateReduce model is also a good option to process ad click events. This is because the raw data can be broken down into chunks to aggregate, then combined later. Also, we have 2 types of aggregated data, thus we can follow a DAG structure shown in ‘Aggregation DAG structure’.

Aggregation DAG structure:

<img width="600" alt="image" src="https://github.com/user-attachments/assets/59f3db32-2883-4752-8977-caca24f1aea2" />

<br/>
<br/>

The DAG structure will have the below components:

##### Map node

- The map node reads the raw data, and sends chunks of it to individual aggregator nodes. The aggregator nodes can either be a process within a server (container) or individual servers which communicate via TCP for faster communication. A single node could also store the aggregated data in memory for faster processing. Also, to ensure the output from each node is never lost, we can store it within a data lake such as S3. This way, if a node crashes mid-operation, another node can retrieve the saved output from S3 and resume the operation.
- The map node could also route an adID to an aggregator node using adID % 2, such as in 'Map operation'.

Map operation:

<img width="600" alt="image" src="https://github.com/user-attachments/assets/ddfbe208-73b2-4e0c-a360-26057d22775d" />

##### Aggregator node

- The aggregator node will count the ad click events by the adID using a minute as the window size.
- A single aggregator node will also maintain a heap data structure in memory to sort by the most clicked adIDs to generate the data for querying the top N most clicked adIDs.
- The ad click events by adID, and this heap data structure will then be sent to the reduce node to combine the other aggregated outputs.

##### Reduce node

- There will likely be one reduce node for N aggregator nodes. The reduce node combines the aggregated ad click counts by adID into a single dataset.
- It will also combine the outputs from the heap from the aggregator node into a single heap, such that there will be <1000 or so most clicked adIDs per clickMinute. This "most clicked counts reduce" operation is shown in 'Most clicked counts adID reduce operation':

Most clicked counts adID reduce operation:

<img width="519" alt="image" src="https://github.com/user-attachments/assets/f32b347a-2079-44b0-a044-b2cc43f0711b" />

<br/>
<br/>

The batch processing approach will consist of:

##### 0. Click processor

- The Click processor will push the raw data into the raw data message queue

##### 1. Raw data message queue

- We can use Kafka as the message queue to buffer and decouple the Click processor and the Aggregator service. Kafka is preferable over other message queue services because Kafka provides a higher retention and scalability of events as opposed to RabbitMQ and SQS. Also, the messages within Kafka could also be persisted for a configured time, let's say 7 days or so. Also, Kafka provides an exactly-once delivery of a single message such that there are no duplicate consumptions for the same message.

##### 2. Aggregator service (performing MapAggregatorReduce)

- The Aggregator service will consist of the map, aggregator and reduce nodes, which can likely be containers with the spark code to perform the mapping, aggregation and reduce logic. If a map node is free, it will pull a set of click events from the raw data message queue and route the adIDs to the aggregator nodes to perform the aggregation.
- Once the adIDs reach the reduce node, the reduce node will combine the aggregation results, and push the data to the aggregation data message queue.

##### 3. Aggregation data message queue

- The aggregation data message queue will buffer and decouple the Aggregator service from the OLAP database writers. When workers of the OLAP database writers are free, they will pull a message from this queue and write to the OLAP database.

##### 4. OLAP database writers

- When workers of the OLAP database writers are free, they will pull a message from the this queue and write the data into an appropriate format to the OLAP database. The OLAP database will contain the final aggregated data, which can be queried by the Analytics service.

### Ad placement service

- When a user clicks on an ad in their browser, they need to be redirected to the advertiser's website. The Ad placement service will be responsible for placing ads on the website and mapping them to the correct redirect URL. When a user clicks on an adID which was placed by the Ad placement service, the Ad placement service will redirect the user to the redirectURL for the adID.

- The Ad placement service will also use the ads entity in the ads database to perform the redirection when a user clicks an adID.

- We can handle the redirection in the two ways below, where the client-side redirect is simpler, and the server-side redirect is more robust, ('Handling redirects for clicked ads'):
  - Client side redirect
  - Server side redirect

### Ads database / cache

- The ads entity will be stored in the ads database, and will contain the mapping of adID : redirectURL, such that the Ad placement service can redirect the user. Also, because the data is fairly simple, and will likely require fast reads, we could use DynamoDB which provides an efficient way to retrieve entries using LSIs and GSIs. We can set a GSI, where the partition key could be adID, and the sort key could be the createdAt timestamp value within the ad entry's metadata.

#### Cache

- Because it's better if the redirection is implemented in the server-side, we could speed up the redirection by caching the frequently accessed adID : redirectURL mappings in both a database-side cache and the Ad placement service.
- We could also use Memcached for the cache, and benefit from it's multi-threaded approach.

### Click processor

- When a user clicks on an adID which was placed by the Ad placement service, they'll also send a request to the Click processor service, which will process the click event and write it to an event stream such as Kafka.

### Raw data lake - S3 / Azure Data Lake

- We will still need to store the raw data coming from the Click processor to perform validations and reconciliations by re-aggregating the raw data and comparing it with the outputs in our OLAP database

- The actual raw click event data coming from the Click processor is write heavy, and will not be queried as often - or even at all. The raw data itself can likely be stored within a data lake like S3 in the form of parquet, avro, orc, etc files which provides lossless compression of data and allows spark to aggregate and process the raw data. The older raw data could also be moved to colder storages over time.

- The raw data can also be stored in write heavy databases such as Cassandra, if queries via CQL are needed, since queries may be more difficult to perform within a data lake, since the files will need to be organized properly within folders.

- Depending on how frequently the raw data is queried, S3 (in-frequently queried) or Cassandra (frequently queried) could be used

**Storing the raw data in a SQL DB might not be optimal, since the raw data is very write heavy, 
 and a data lake or Cassandra will provide better support for writes**

### Analytics service

- Advertisers need to be able to quickly query the metrics on their ads to see how they're performing. The Analytics service will allow advertisers / admins to query the ad click events data on the OLAP database.
- We will need a separate Analytics service instead of querying the OLAP database directly because the Analytics service may still need to query multiple shards of the OLAP database or apply logic and return the results in a dashboard. Thus the querying implementation should be separately maintained within the Analytics service - likely within an IO optimized EC2 instance, since we'll be querying the OLAP very frequently.

- We can design the storage and querying logic of the ad click events data in the following ways, and in 'Storage and querying logic of the ad click events data':
  - Store and query from the same database
  - Separate analytics database with batch processing
  - Real-time analytics with stream processing

### Kafka event stream

- When a click event comes in, the Click processor service will immediately write the event to the Kafka event stream. This event stream will allow us to perform real-time analytics with stream processing.
- The spark event streaming processor will then read the events from this Kafka event stream and perform the aggregation on the events in real-time

### Spark event streaming processor

- The spark event streaming processor will read the events from the Kafka event stream and aggregate the events in real-time, then push the aggregated data to the OLAB database
- The spark event streaming processor will use spark streaming likely within memory optimized EC2 instance to perform the aggregation in real-time.
- The spark streaming code will keep a running count of click totals for adIDs for the current minute (clickMinute field), and also keep a list of most clicked adIDs for the current minute (clickMinute field) - it will keep this data in memory, and update the data as events come in. Once we reach the end of a time window (minute in this case), the spark streaming code will push the aggregated data to the OLAP database.

### OLAP database

- The OLAP database will store the different types of aggregated data from the Data model, and the Analytics service can directly query the OLAP database to view ad click metrics.

- For our analytics database, the database which will store frequently queried data, we want a service that is optimized for reads and aggregations. OLAP tends to work well in data warehouses like Redshift and Azure Data Warehouse. These services are optimized for complex queries and can handle parsing through a large volume of data efficiently using SQL. Redshift also supports heavy write loads from multiple sources via AWS Redshift Spark streaming.

**Data warehouses can contain multiple databases or one large database. A data warehouse is a system that stores data from multiple sources in a central location. It can include data from operational systems like sales or marketing.**

- AWS Redshift is essentially a RDBMS, where it stores data in tables, each with a primary key and is compatible with other RDBMS applications. Redshift is fully managed by AWS, and is built on the PostgreSQL engine. It is able to store and analyze large amounts of data, up to petabytes. Redshift also uses a columnar database design, which means that the data is stored in columns, similar to Cassandra, which provides fast querying for use cases like getting aggregations within a column, where a column could represent the past minute.

**Note that while Cassandra is write optimized, it is not read optimized for complex queries which include range based queries, as opposed to SQL DBs or Redshift. Therefore, we won't use Cassandra as the OLAP database**

## DD

### Querying metrics at low latency

- This was largely solved by the preprocessing of the data in real-time. Whether using the "good" solution with periodic batch processing or the "great" solution with real-time stream processing, the data is already aggregated and stored in the OLAP database making the queries fast.

- Where this query can still be slow is when we are aggregating over larger time windows, like days, weeks, or even years. In this case, we can pre-aggregate the data in the OLAP database. This can be done by creating a new table that stores the aggregated data at a higher level of granularity, like daily or weekly. This can be via a nighly cron job that runs a query to aggregate the data and store it in the new table. When an advertiser queries the data, they can query the pre-aggregated table for the higher level of granularity.

**Pre-aggregating the data in the OLAP database is a common technique to improve query performance. It can be thought of similar to a form of caching. We are trading off storage space for query performance for the most common queries.**

### Ensuring no click events are lost

- We're using Kafka as the event stream, and so it's very unlikely we'll lose click events since the data will be in log based storage, and can also be replicated. Kafka also allows us to enable persistent storage, so even if the data is consumed by the stream processor, it will still be stored in Kafka for a certain period of time, let's say 7 days or so.

- If the stream processor instance goes down, another instance can pick up the data from the Kafka event stream and perform the aggregation.

#### Checkpointing

- Stream processors like spark streaming also have a feature called checkpointing, where Spark periodically writes its state to a connected persistent storage like S3. If an instance of the spark stream processor goes down, another instance can read the last checkpoint and resume the processing. Checkpointing is useful when the aggregation window is large, like a day or a week.

**For our case, however, our aggregation windows are very small. Candidates often propose using checkpointing when I ask this question in interview, but I'll usually push back and ask if it really makes sense given the small aggregation windows. If a stream processor were to go down, we would have lost, at most, a minutes worth of aggregated data. Given persistence is enabled on the stream, we can just read the lost click events from the stream again and re-aggregate them.**

**These types of identifications that somewhat go against the grain are really effective ways to show seniority. A well-studied candidate may remember reading about checkpointing and propose it as a solution, but an experienced candidate will instead think critically about whether it's actually necessary given the context of the problem.**

#### Reconciliation

- Guaranteeing data accuracy (consistency) and low latency are often at odds. We can balance the two by doing the following:
  - Just after the raw click events are exiting the Kafka event stream, we can asynchronously dump the raw click events to the Raw data lake. Then we can run a batch job that reads all the raw click events from the data lake and re-aggregates them. This way, we can compare the results of the periodic batch job (let's call it "Reconcilliation worker" - which runs every hour or day and validates the data) to the results stored in the OLAP database and ensure that they match. If they don't, we can investigate the discrepancies and fix the root cause while updating the data in the OLAP database with the correct values.

<br/>

- This essentially combines our two solutions, real-time stream processing and periodic batch processing, to ensure that our data is not only fast but also accurate.

### Scaling to support 10K clicks per second

We'll walk through each bottleneck the system could face from the moment a click is captured:

#### Click processor service

- The Click processor service can easily be scaled horizontally by adding more instances. Most modern cloud providers like AWS, Azure, and GCP provide managed services that automatically scale services based on CPU or memory usage. We'll need a load balancer in front of the service to distribute the load across instances.

#### Kafka event stream

- Kafka can handle a large number of events per second but needs to be properly configured. Kafka, for example, can have a throughput of over 100 MB/s, but sharding will further support this throughput. Sharding by adID is a natural choice, this way, the stream processor can read from multiple shards in parallel since click events from different adIDs will be independent from each other.

#### Spark event streaming processor

- The stream processor, like Spark streaming or Flink, can also be scaled horizontally by adding more workers to handle the real-time aggregation. We'll have a seperate Spark / Flink job reading from each shard doing the aggregation for the adIDs in that shard.

#### OLAP database

- The OLAP database can be scaled horizontally by adding more nodes. While we could shard by adID, it may be more beneficial to shard by advertiserID instead. This way, all the data for a given advertiserID will be on the same shard, which will make queries for the advertiser's ads faster since we don't have have to query multiple shards.

#### Hotspots

- There are scenarios where an adID within a shard of the Kafka event stream and stream processor may become a hotspot, if let's say Adidas released an ad with Ronaldo which is getting a lot of clicks. The shard with the adID will be overwhelmed and become a hotspot.

- To prevent these hotspots for very popular adIDs, one popular approach is to append a random number between 0-N (where N is the number of shards of the Kafka event stream and stream processor) to the adID whenever click events come in from the Click processor for these popular adIDs. We'll only do this for popular adIDs determined by the click count. The adID will now look like adID:0-N where N is the number of shards of the Kafka event stream and stream processor. Therefore, when a popular adID comes in, it'll be routed to a random shard within both the Kafka event stream and stream processor each time by appending that 0-N random number.

### Preventing abuse from users clicking on the same ad multiple times

- If a user clicks on an adID multiple times, we still only want to count it as one click. We can implement this feature using the below ways, and in 'Preventing abuse from users clicking on the same ad multiple times':
  - Add userID to click event payload
  - Generate a unique impression ID

### Using click time sent by client OR processed time generated by Click processor

- There are mainly two types of timestamps generated: event time from when an ad click happens by the client, and the processed time when the click processor receives the ad click event. There could be a slight gap between the event time and processed time, let's say a few seconds or so.

- If we used the event time as the clickMinute for our aggregations, the time generated by the client may be modified. However, if we used the processed time, the time will not be as accurate due to network delays.
- To accurately process these delayed click events, we can use the event time instead of the processed time. A watermark can be used which extends the aggregation window by a few seconds so that delayed 		event times (from clients) are still captured in the correct aggregation window. Using a watermark	improves the accuracy but increases the latency since the aggregation window is extended.

- Since data accuracy is still a requirement, event time is preferrable, and the event time sent by the client could be validated as well within the Click processor to check if it seems valid.

### Aggregation window

- There are 2 relevant types of windows we can use below:
  - Tumbling window:
    - In a tumbling window, the time is split into fixed sized windows, which are non-overlapping. Tumbling windows are a good fit for aggregating the counts for ad click events every minute.
  - Sliding window:
    - In a sliding window, a window slides across time and events are processed within the sliding window. A sliding window can be overlapping. A sliding window can be used to get the top N most clicked ads in the last M minutes, since a window size of M can be used. Also, a sliding window can slide across the data stream by a specific interval, as opposed to a tumbling window which operates with a fixed window size.

### Delivery guarantees

- Kafka provides all 3 delivery guarantees: at-most-once, at-least-once and exactly-once. Since we require an entry to be 		processed exactly-once, and cannot allow any duplicates, Kafka can be configured to use exactly-once delivery.

### Data deduplication

#### Client side data deduplication

- Data duplication can come from both the client and server side. It can come from the client side, in which there is a malicious actor - thus, a deduplication layer or a rate limiter could be added between the client and the load balancer.

#### Server side data deduplication

- A duplication could also occur via the servers. Let's say there is an error during the aggregation before the stream processor updates the offset in the Kafka event stream but after the aggregated data is already saved in the OLAP database. Since there is an error, the stream processor could possibly retry the aggregation twice from the same offset and send the aggregated data twice to the OLAP database.

- Since the issue in the server side duplication will likely happen because the stream processor did not use a distributed transaction to save the aggregation data to the OLAP database, we could put the below operations the stream processor will perform within a distributed transaction via a Redis distributed lock:
  - Acquire a Redis distributed lock (with TTL) for the clickMinute entry in the OLAP database that will be updated
  - Read from offset at the Kafka event stream
  - Perform the aggregations
  - Save the aggregations data to the OLAP database
  - Update the offset at the Kafka event stream
  
  - If everything up until now was successful, then the lock will be released and the transaction is a success. However, if there were any errors, then the transaction will be rolled back, and the lock will be released.
  - Release the Redis distributed lock. If the lock was released before the transaction was completed, then the transaction itself will be rolled back, and will be considered unsuccessful

Additional deep dives:

### Monitoring

- We can monitor metrics such as latency and clickCounts for adIDs to detect sudden hotspots, such that new instances of the Click processor and stream processor could be allocated. Also, the system's resources such as CPU, available disk storage, memory in stream processors, etc could also be monitored, incase allocation may be needed.


