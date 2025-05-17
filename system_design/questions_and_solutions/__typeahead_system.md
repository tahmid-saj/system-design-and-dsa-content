# Typeahead system

Typeahead suggestions enable users to search for known and frequently searched terms. As the user types into the search box, it tries to predict the query based on the characters the user has entered and gives a list of suggestions to complete the query. Typeahead suggestions help the user to articulate their search queries better. It’s not about speeding up the search process but rather about guiding the users and lending them a helping hand in constructing their search query.

## Requirements

### Questions

- Are we designing the query gathering part, as well as the search functionality?
  - Yes both

- Is the matching only at the prefix of a search query or in the middle as well?
  - Only at the beginning of a search query

- How many autocomplete suggestions should the system return?
  - 5

- How does the system rank which 5 suggestions to return?
  - This is determined by popularity, decided by the historical query frequency.

- Do we convert all the text to lowercase?
  - Yes

- What is the DAU?
  - 10 million DAU

### Functional

- Matching is only supported for the prefix
- Should return N (5) results max with sorting
- All search queries have lowercase alphabetic characters

- Should take <200 ms to return search results
  
### Non-functional

- Low latency:
  - Low latency in typeahead suggestions should be provided - should take <200 ms to return search results
- Throughput:
  - The system should handle a high traffic volume
- Search suggestion accuracy:
  - There should be accuracy in the search suggestions
- The search results should also be sorted by the query frequency

## Trie 101

Below are some operations which could be done in a trie:

- We'll first assume the following parameters:
  - **p**:
    - Length of a prefix
  - **n**:
    - Total number of nodes in a trie		
  - **c**:
    - Number of child nodes in a given prefix node

**Note that within the trie, we'll likely only store letters, numbers, spaces, and punctuation to save storage space**

### Search in trie - unoptimized

The steps to get the top K most searched queries for a given query is as follows:

1. Find the prefix. **Time complexity: O(p)**
2. Traverse the subtree from the prefix node to get the searched queries and their frequencies from all the child nodes. Child nodes will likely have an endOfWord boolean value which specifies if the child node contains a full search query (not a prefix). **Time complexity: O(c)**
3. Sort the child node's search queries by their frequency, and return the top K searched queries. **Time complexity: O(clogc)**

The time complexity for the unoptimized search operation is: **O(p) + O(c) + O(clogc)**

### Search in trie - optimized

The above unoptimized search algorithm is simple, but will take too long because we need to traverse the entire trie to get the top K searched queries. We can make the below optimizations:

#### Limit the max length of a prefix

- Users will rarely type a long search query, thus it is safe to limit p to a small number, like 50. If we limit p, then the time complexity for finding the prefix of the search query input can be reduced from **O(p) to O(50)**.

#### Cache top K frequently searched queries at nodes

- To avoid traversing all the child nodes after we've found the prefix, we can cache the top K frequently searched queries at each node. K will be a small number, like 5, since typeahead systems will usually return the 5-10 or so searched queries.
- By caching the top searched queries at the nodes, we'll significantly reduce the time complexity of traversing the child nodes after we've found the prefix node, from **O(c) to O(5)**. We'll also reduce the time complexity for sorting the child node's search queries by their frequency, since we don't need to sort the top K any more - we'll reduce it from **O(clogc) to O(1)**.
- However, storing the searched queries at all the nodes require a lot of space, but because we have low latency as a strict requirement, this optimization will be suitable.

**Note that these cached queries will be the full search query and the trie node will represent only the prefix of the full search query. Therefore, the child nodes are not directly dependent on their parent nodes - the child nodes' frequentQueries field won't cache any prefixes of the parent nodes**

#### Merge trie nodes which have only one branch

- We could also merge trie nodes which have only one branch to save storage space, since the Trie could become large very quickly. This optimization will also improve both the time and space complexity.

<br/>

- The finalized time complexity with all the optimizations will be **O(50) + O(5) + O(1)**, which is **O(1)**. The finalized trie data structure is shown in 'Finalized trie data structure'.

Finalized trie data structure:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/6af3e97c-614a-44e0-acdc-184f48b8d19d" />

<br/>

### Insert into trie

- To insert a word into the trie, we will take **O(length of word)** time to go down the trie and checking if the prefixes (node) of the word exists, or needs to be created. Also, because we're inserting a new node into the trie for a new word, it is assumed the word we're inserting has a default prefixFrequency of 1 OR a prefixFrequency from the aggregated analytics logs. However, if the word is in any parent nodes' frequentQueries leading up to the prefix node for the new word, then the parent node's frequentQueries will need this new word's frequency value to be updated according to the prefixFrequency from the aggregated analytics logs.

### Update in trie

Updating a word in the trie will take **O(length of word)**, since we will do the following:

1. First update the frequency values in the frequentQueries field	of the parent nodes leading up to the prefix node if the word we're updating for is in the frequentQueries field. For every parent node, we'll check if the word is part of the top 5. If so, we'll update the corresponding frequency. If not, we check if the word’s frequency is high enough to be a part of the top 5. If so, we'll insert this new word and remove the word with the lowest frequency.
2. Then we'll update the prefixFrequency, and the frequentQueries in the node containing the full word using this same logic.

- Also, when updating the trie nodes, if the frequency exceeds a threshold, let's say 1000, then we can also stop any further increments to the		frequency to reduce the number of updates we need to perform on the trie.

Updating a trie:

- In here, on the left side, the search query “beer” has the original value 10. On the right side, it is updated to 30. As you can see, the node and its ancestors have the “beer” value updated to 30.
<img width="800" alt="image" src="https://github.com/user-attachments/assets/ba3338bd-88ee-4f74-8aa6-e338c91e5011" />

<br/>

### Delete from trie

- To delete a word from the trie, it will take **O(length of word) + O(number of child nodes)** since we'll first delete / update	all the nodes for the word, and then delete / update the child nodes for the word. We also delete / update the child nodes	because they could contain the word to be deleted in the frequentQueries field as well.

### Building the trie

- We can efficiently build the trie by traversing through all the queries in the analytics logs, and inserting the queries into the trie one at a time. After we insert a query into the trie, we will traverse through every parent node leading up to the query, then we'll recursively call all the child nodes and get the child node's top 5 frequentQueries. The parent nodes will combine these top 5 frequentQueries from all their child nodes to determine their own frequentQueries field.
- The total time complexity for building a trie is: **O(number of queries to add * average length of query * c)** where c is the average number of child nodes we're recursively calling for every node containing the full query

## Data model / entities

### Analytics logs

- We'll likely have an entity storing the query strings, their frequency and query time. We'll add to this entity when users type in new queries. Afterwards we'll later update the Trie database / cache via an offline job using this entity

  - query
  - frequency
  - queryTime

### Trie node

- Below are the entries of a trie node:

```bash
{
	prefix: a
	prefixFrequency: 3 (note we'll use prefixFrequency as the GSI's sort key discussed later in the Trie database part of the HLD)
	frequentQueries: [ { abc: 5 } ]
	childNodes: [ b ]
	endOfWord: false
},
{
	prefix: b
	prefixFrequency: 5
	frequentQueries: [ { abc: 5 } ]
	childNodes: [ c ]
	endOfWord: false
},
{
	prefix: c
	prefixFrequency: 2
	frequentQueries: [ { abc: 5 } ]
	childNodes: [ c ]
	endOfWord: true
}
```

## API design

- For many applications, autocomplete search suggestions may not change much within a short time. Thus, autocomplete suggestions can be saved in browser cache to allow subsequent requests to get results from the cache directly.
- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
  - Cache-Control: no-cache max-age Private/Public

### Get suggestions

- Note that we'll likely use websockets and rely on it's low latency / lightweight connection to get back suggestions.

#### Eatablish a websocket connection

- This endpoint will be used to establish the websocket connection. The			Sec-WebSocket-Key header will be a value that the server will use to generate a		response key to send websocket requests. The Sec-WebSocket-Version will be the	websocket protocol version, usually 13.

Request:
```bash
GET /query
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: xyz
Sec-WebSocket-Version: 13
```

- In the response, the Sec-WebSocket-Accept header will usually be generated by	combining the Sec-WebSocket-Key from the client with another hashed value. This	resulting value will be returned to the client

Response:
```bash
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: xyz + hash value
```

#### Get suggestions

- Returns the search results for the query

Request:
```bash
SEND {
  query: "abc"
}
```

Response:
```bash
RECV {
  [ { queryResult: “abc”, frequency: 5 }, { queryResult: “abcde”, frequency: 3 } ]
}
```

### Insert into trie

Request:
```bash
POST /query
{
  query,
  frequency
}
```

## HLD

The system is broken down into 2 parts:

- Data gathering part:
  - This part will gather the user input queries, then aggregate them and update the Trie database / cache offline periodically. We'll update the Trie database / cache offline because it is not feasible to update it in real-time. Users might enter millions to billions of queries per day, and updating the trie on every query will slow down the system. Also, the top suggestions might not change as much once the trie is built, thus it is not necessary to update the trie frequently.
  - Depending on the use case, we can gather the data and aggregate at different rates. For example, Twitter gathers and aggregates the data more frequently.

- Querying part:
  - Given a search query or prefix, we'll return the 5 most frequently searched terms from the Trie cache

<br/>

Below are the components of the system:

### Analytics logs blob store
  
- The data used to build the trie will usually be from analytics logs collected from different sources in different formats, and then stored in a blob store. The Analytics logs blob store stores the raw data which is used to build the trie. The raw data is append-only and will not need to be directly indexed for queries. The Typeahead servers themselves could also provide the analytics logs after the Typeahead servers compile frequently searched queries.
- Because we'll likely be dealing with unstructured content which likely doesn't follow a specific format, and where the size of different analytics logs varies, we could use S3 to store these analytics logs. An entry in the analytics logs could look as follows:

```bash
{
  searchQuery,
  frequency (if necessary),
  queryTime (if necessary)
}
```

### MapReduce workers

- The MapReduce workers will take batches of the analytics logs, and aggregate them such that the aggregated data cen be used to update the trie. There will likely also be a job scheduler for a set of MapReduce workers, which will map batches of the analytics logs from S3 to the MapReduce workers.
- These workers will ensure the aggregated analytics logs are in the same format. During the MapReduce operation, the workers will perform the aggregation by combining entries in the analytics logs if the entry's searchQuery fields are the same. If entries have the same searchQuery, we'll also add up the entries' frequency values. The MapReduce workers will perform this aggregation, then store the aggregated analytics logs in the Analytics logs blob store, and also push the updates which need to be made on the trie to the message queue.
- Because these workers will likely need to frequently communicate with S3, message queues, etc and also perform repeated MapReduce operations, we can use IO optimized EC2 instances here along with spark which is able to set up pipelines of MapReduce operations. Also the workers themselves will be separate containers.

#### Aggregators MapReduce workflow

The MapReduce workflow will look as follows:

1. Each worker will be responsible for a set of analytics logs from the analytics logs blob store. There could be a separate job scheduler which maintains the number of workers depending on how many new analytics logs are in the blob store. This job scheduler could also have a cron job that watches the blob store for new analytics logs, and assigns specific workers to new analytics logs. We could also avoid using the job scheduler, and have each worker assigned to a specific container within the blob store OR assigned to a specific query time range of the analytics logs. Either way works fine, but a separate job scheduler might be more scalable because we could also implement health checks and scale the number of workers.
2. Parse through the entries of the batch of analytics logs, and group the entries with the same searchQuery together, and also add up the frequency value as well if provided
3. Once the workers have generated the aggregated analytics logs, the workers will store them in the blob store. The trie updates corresponding to these aggregated analytics logs will then be queued to the message queue.

### Message queue

- After the message queue receives the updates which need to be performed on the Trie database / cache, the Trie write workers will dequeue the messages from the queue and update the Trie database / cache. We'll position a message queue between the MapReduce workers and the Trie write workers because we'll likely want to buffer the Trie write workers, and ensure that no updates to the trie are lost - to ensure data accuracy of the search results.
- Because we'll want to maintain an exactly-once delivery, and ordering is not necessarily required, we can use a queue such as SQS. SQS will also allow exactly-once delivery by using it's visibility timeout to ensure only one Trie write worker consumes a message at a time. If a Trie write worker fails, another worker can still takeover and consume the message.

### Trie write workers

- The Trie write workers will be the final workers that updates the Trie database / cache. These workers will pull the messages from SQS, then also pull the corresponding aggregated analytics logs from the Analytics logs blob store, then update the Trie database / cache with the aggregated analytics logs.
- Note that we can thereotically combine the MapReduce workers, message queues and the Trie write workers together into one single worker that performs the MapReduce operation and updates the Trie. However, the MapReduce workers and the Trie write workers perform different tasks, where the MapReduce workers performs the aggregation of the analytics logs, and the Trie write workers writes to the Trie. There could be a scenario where we'll have numerous analytics logs to aggregate and combine, but we'll only need to make a few writes to the Trie - in this case, we'll need a lot of MapReduce workers, but not as many Trie write workers. Thus, we'll want to scale these 2 types workers independently via a message queue.
- Because we'll also update the Trie database / cache frequently, we can use IO optimized EC2 instances here, where the workers themselves will be separate containers.

### Trie database

- The Trie database stores the persistent view of the trie. It helps with storing the trie node entries, but it won't be directly queried, since queries on it would be too slow for typeahead suggestions. We'll use this database to provide weekly or bi-weekly snapshots to the Trie cache. This database will also be built using the Trie write workers.
- Since a single trie node is relatively simple, but does still have references to child nodes, the data type is unstructured. A KV store like DynamoDB or a document store like MongoDB will both work here.
- If we use MongoDB, we can set the primary key as the trie node's prefix. If we use DynamoDB, we can set LSIs and GSIs which allows for faster lookups. To create a GSI, we can set the first few characters of the trie node's prefix as the partition key, and set the sort key as the prefixFrequency, which will help in returning sorted results by the frequency. Also, in DynamoDB, the key itself could be the trie node's prefix, while the value will be the prefixFrequency, frequentQueries, childNodes, endOfWord fields of the trie node:

```bash
{
  prefix (key)
  prefixFrequency
  frequentQueries: [ { word, freq } ]
  childNodes: [ prefix1, prefix2 ]
  endOfWord
}
```

- Also, there is another option of storing the Trie, where the Trie itself is stored separately, however the Trie nodes are mapped to a KV pair within a KV store. This option is shown below, however it doesn't seem necessary to store the Trie structure from the Trie's node values separately.

<img width="800" alt="image" src="https://github.com/user-attachments/assets/005f5f43-dd81-4194-8db1-80e35f9f59ad" />

<br/>

#### Updating the Trie database / cache

We can update the Trie database / cache in the below ways:

1. Create an entire new trie, and replace the old trie with the new one
2. We can update individual trie nodes directly. This operation will likely be more appropriate since the trie is unlikely to change frequently, and only the changed nodes need to be updated.

#### Trie database fault tolerance

- To ensure that we can rebuild the trie, we can take a snapshot of our trie periodically and store it in a file within S3. The snapshots could also store which terms / prefixes the specific instance of the Trie database / cache managed. This will enable us to rebuild a trie if the server goes down. To store the snapshots, we can start with the root node and save the trie level-by-level. With each node, we can store what character it contains and how many children it has. Right after each node, we should put all of its children. Let's assume we have the following trie:

![image](https://github.com/user-attachments/assets/bca3e4d8-25d3-48db-a5cb-d8311d5b7cb1)

- If we store this trie in a file with the above-mentioned scheme, we will have: "C2,A2,R1,T,P,O1,D". From this, we can easily rebuild our trie.

- Note that we could or could not store the frequentQueries of each node. This is because the frequentQueries can be reconstructed using the aggregated analytics logs within the blob store. However, we could still store the frequentQueries, since it's only about 5 entries within a trie node.

### Trie cache

- The Trie cache will store the Trie in-memory for fast reads. When search queries come in, it will likely use the Trie cache since reading from the Trie database will be too slow. The Trie cache will also store a weekly or bi-weekly snapshot of the Trie database.
- It is debatable between using Redis or Memcached here. The data model for a trie might seem complex, but a single trie node's data is relatively simple. If we're only storing the tire node's prefix and frequentQueries in the cache, then Memcached might be more preferrable since the data is simple.
- If we plan on storing the full trie data structure, or a partial of it, Redis might be more suitable because it provides data structures like sorted sets which can be used to pre-sort the frequentQueries field within a trie node. But Redis might have higher latencies due to it's single-threaded approach, whereas Memcached can usually return results withn O(1) time for simple data types.

#### Returning search results

- The search queries will require very fast results, thus we'll use this Trie cache instead of the DB to return results. When search queries come in, the Typeahead servers will find the cached entry storing the prefix of the search query. The frequentQueries from this cached entry will then be returned to the client. This operation will happen every time the client types a letter or removes a letter into the search bar. Clients could also request the server only if there is a pause in the keystrokes. If the user types rapidly, there is no purpose in returning search results
- If there is a cache miss, then the Typeahead servers won't send the suggestions - instead of looking at the Trie database and retrieving them. We still won't use the Trie database to send results even after a cache miss because querying the database will take too long. During a cache miss, we'll instead update the cache with Trie database if necessary.

#### Updating the Trie cache

- The Trie write workers will update the Trie cache, and the Trie cache could also take periodic snapshots from the Trie database.
- Another option of updating the Trie cache is to maintain 2 sets of the Trie cache, a primary Trie cache and a secondary Trie cache. We can update the secondary while the primary is serving traffic. Once the update is complete, we can make the secondary our new primary. We can later update our old primary, which can then start serving traffic, too.
- It's also possible to have the client log searched queries to the Analytics logs blob store directly, such that the updating load is reduced from the Typeahead servers

### Typeahead servers

- The Typeahead servers will maintain a websocket connection with the client, and handle typeahead requests for getting back suggestions from the Trie cache. The Typeahead servers can also maintain an internal batch of analytics logs containing the searched queries, and later send the batch to the Analytics logs blob store to update the trie.

- When the user types, the client should be implemented to carefully observe the user’s keystrokes and only provide		search suggestions if the user types within a specific keystroke range. This is because if a user is typing too fast, then	they won’t need any search suggestions

#### Websocket connections in Typeahead servers

- An important part of the design is establishing the connection between the clients and the Typeahead servers. The connection	will require low latency and will pass lightweight data types, and as such, HTTP may not be suitable since it is not a		bidirectional communication, and will have higher latencies than other connection styles. Websockets will be suitable to	use, where a websocket connection is established as soon as the client visits the search bar page. Websockets also		operate using TCP, which will be faster than HTTP most of the times since TCP doesn’t hold as many metadata and		headers as HTTP.
- Websockets also only consumes bandwidth if there's actual traffic, so there is no bandwidth penalty for having too many search bars connected. 

#### Typeahead servers sending samples of search queries to Analytics logs blob store

- For a large scale system, logging every search query to the analytics logs requires a lot of processing power and storage. Therefore, data sampling is important. For instance, only 1 out of every N requests can be logged to the analytics logs.

#### AJAX requests

- For web applications, browsers usually send AJAX requests to fetch autocomplete results. The main benefit of AJAX is that sending/receiving a request/response does not refresh the whole web page. AJAX also allows web pages to exchange a small amount of data with the servers.

### L4 Load balancer

- We’ll need an L4 load balancer to support traffic at the TCP level. L4 load balancers,	let’s say using ELB in TCP mode can load balance websockets. When client’s need to	connect to a Typeahead server, the L4 load balancer will route them to the Typeahead server they	previously connected to or to a Typeahead server using the load balancing algorithm.		However, if a Typeahead server goes down, the L4 load balancer can route the client to		connect to another Typeahead server instead.

- When a client needs to connect to the Typeahead server, the request will first go to the L4	load balancer, then to the Typeahead server. There will actually be a symmetric websocket	connection between both the client to the L4 load balancer, and between the L4 load	balancer to the Typeahead server.

- L4 load balancers can be stateful and use sticky sessions to persist the server the	client previously connected to. The sticky session can be implemented by identifying	the user, usually with cookies or their IP address, and storing the user’s connected	server for handling future requests.

- If clients disconnect from a Typeahead server, they can automatically reconnect to the		same Typeahead server or another one via the L4 load balancer. Reconnecting to the same	Typeahead server may be easier, as the session data in the L4 load balancer doesn’t have to	be updated.

<img width="800" alt="image" src="https://github.com/user-attachments/assets/93955640-c964-4e63-a6c7-5e9dae0d77fa" />

## DD

Below are some deep dives of the system:

### Trie database / cache sharding

We can shard the Trie database / cache in the following ways:

#### Letter and range based sharding

- We could shard the trie database and cache by splitting the trie nodes based on the first character. This approach seems reasonable, but there will be an uneven distribution of		words in the shards as more words occur with "a" than lets say "x" or "z".

- We can shard instead based on the letter ranges and how many queries occur for the letter ranges along with how many search queries the letter range stores. For			example we can have shards for a-k and l-z which might produce a more even distribution. Additionally, we can		further shard by more granular ranges such as aa-ag and ua-uz. Using this approach, we can keep storing letter ranges onto the shards until the shard runs out of memory or reaches a certain limit. Let's say if our first shard can store all terms from 'A' to 'AABC', which means our next shard will store from 'AABD' onwards. If our second shard could store up to 'BXA', the next shard will start from 'BXB', and so on. We can use a KV store such as ZooKeeper to quickly access this partitioning scheme:

```bash
Server 1, AAABC
Server 2, AABD-BXA
Server 3, BXB-CDA
```

For querying, if the user has typed 'A', we have to query both servers 1 and 2 to find the top suggestions. When the user has typed 'AA', we still have to query servers 1 and 2, but when the user has typed 'AAA', we only need to query server 1.

- We can also have a shard manager which will maintain a shard mapping of shardID : letterRange. The shard		manager could use Zookeper to manage sharding for the trie database and cache. ZooKeeper provides a KV		store which provides this mapping functionality

#### Hash based sharding

- To ensure the shard distribution is even and randomized, we could use hash based sharding where each query will be passed to a hash function, where the hash of the query will be routed to a specific shard. The disadvantage of this scheme is, to find typeahead suggestions for a search query we have to ask all the shards (servers) and then aggregate the results.

### Trie database / cache replication

- We can apply replication of the trie shards containing the nodes. A primary-secondary replication may be		suitable as we’ll have a 1 : 1 ratio of reads and writes. Writes will happen when we’re updating the trie cache 		and database. If either a Trie database / cache server is down, we can still rebuild the trie based on the snapshots which were saved in S3.

### Supporting real-time search query updates to the Trie database / cache

- Our design updates the Trie database / cache offline, thus it doesn't support real-time updates. We can do the following to support real-time trending updates:
  - To support real-time or trendy search results, we could also increase the frequency at which the Trie gets updated or add more weight to recent searches.
  - Data may come as streams, so we don't have access to all the data at once. Streaming data means the data is generated continuously. We can instead use a streaming approach using a Kafka event stream which takes the typed search queries, then routes them to spark / kinesis based streaming workers. These spark / kinesis streaming workers will then update the Trie database / cache with real-time data.

### Multi language support

- We could store unicode characters in the trie nodes to handle multiple languages. Unicoding is an encoding standard which covers all characters for all the writing systems of the world.
- The trie data structure also may not be suitable for different languages since words in some languages could be		much longer or shorter, and some languages like chinese have hundreds of characters. Thus, we can use		algorithms and data structures catered to different languages.
- Load balancers, servers, databases and CDNs could also be moved to different geographic locations to 		support location specific languages and searches

### What if top search queries in one country are different from others?

- In this case, we might build different tries for different countries. To improve the response time, we can store tries in CDNs.

### Pause in keystrokes will initiate the search requests

- Clients could also request the server only if there is a pause in the keystrokes, let's say for 50 ms. If the user types rapidly, there is no purpose in returning suggestions

### Filter layer to remove harmful content

- We can also add a filter layer within the MapReduce workers, which will ensure the trie doesn't contain any harmful content


## Questions

Q: How would you handle misspelled or incomplete words in the Typeahead Suggestion System?

A: To handle misspelled or incomplete words in the typeahead, we can use several strategies: 

Fuzzy Matching: 
This allows us to find matches that are less than perfect. This technique is useful for		correcting minor misspellings. 

Autocorrect: 
This feature corrects the spelling of words as the user types. 

Predictive Text: 
- This feature suggests words or phrases that the user may intend to type next based on	their past typing habits. 

Contextual Suggestions: 
- This feature suggests words or phrases based on the context of what the user is typing.


## Wrap up

- Geo-replication
- Quorum based approach for inconsistency resolution
- Use other fields instead of frequency in the trie nodes, such as demographics, language, etc
- Use of CDN for geographical result oriented search results


