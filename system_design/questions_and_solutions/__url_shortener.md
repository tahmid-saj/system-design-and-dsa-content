# URL shortener

## Requirements

### Questions

- How many short URLs should be generated per day?
	- 100 million URLs should be generated per day

- How short should the short URL be?
	- As short as possible

- What characters are allowed in the short URL?
	- It can contain a-z, A-Z, 0-9 only

- Can users specify a custom alias and expiration time for the shortURL?
  - Yes, and the system should also generate an expiration time

### Functional

- Given a URL, the system will return a short URL
- The system direct all requests to the short URL, to the original URL
- Optionally, users can specify a custom alias and expiration time (the system will also generate) for their short URL

- Only a-z, A-Z, 0-9 characters are allowed in the short URL
- shortURLs should be as short as possible

- The short URLs can be deleted or updated if necessary

### Non-functional

- Low latency:
  - Redirection should occur quick
  - The system will be more ready heavy than write heavy

- Unpredictability in generated short URLs for security purposes
	- If the shortURL is predictable, attackers can attack		that shortURL

- Availability:
	- We’ll prioritize availability over consistency since we	don’t need to register the generated shortURL right		away


## Data model / entities

- URL mapping:
	- This entity will contain the mapping between the originalURL to the shortURL, such	that the shortURL or the endpoint string of the short URL is used to find the			originalURL

	- Note that the expirationTime could also have a default value of let’s say 2 years

	  - shortURL
	  - originalURLID (generated via the sequencer if a sequencer is used)
	  - originalURL
	  - userID
	  - metadata: { options, customAlias, expirationTIme, createdAt }


## API design

### Generate a shortURL

- If the originalURL in the request already has an associated shortURL, the shortURL will be returned instead of		regenerating a new one. Additional options in the metadata could also be set, such as using only characters from a-z,	A-Z, 0-9.

Request:
```bash
POST /urls
{
	originalURL,
	metadata: { options, customAlias, expirationTIme }
}
```

Response:
```bash
{
	shortURL
}
```

### Redirect shortURL

- This endpoint will redirect the client to the originalURL using either the 301 (permanent redirection) or 302			(temporary redirection) HTTP status code. The location of the redirection will also be specified via the Location header	in the response
	
- The 301 redirect shows that the requested URL is permanently moved to the originalURL, while the 302 redirect shows	that the requested URL is temporarily moved to the originalURL. For a 301 redirect, the browser will cache the responses	so that any next few requests to go to the shortURL will actually go directly to the originalURL using the browser’s cache.
- However, the 302 redirect will not cache the redirection response as the shortURL is temporarily moved to the			originalURL. The request will still go to our servers.
	
- If the priority is to reduce the server load, then the 301 redirection may be suitable since the request is cached on the	browser, and there will be fewer requests for fetching the originalURL from the servers via the shortURL. 
- However, a 302 redirection still gives us more control on the redirection, ie if we need to update / delete the shortURL, then it wouldn’t be cached in the client side. Caching on the browser via 301 can cause issues if we need to update / delete the shortURL. It also allows us to track click statistics on the shortURL.

Request:
```bash
GET /urls/:shortURL
```

Response:
```bash
HTTP/1.1 301 / 302 Redirection
Location: originalURL
```

<br/>

Additional endpoints:

### Delete a shortURL

Request:
```bash
DELETE /urls/:shortURL
```

### Update a shortURL for an originalURL

- This endpoint will update the shortURL. The shortURL to be updated will also be marked as unavailable for future uses	 in the database for data integrity purposes, so that no two originalURLs may have the same shortURL

Request:
```bash
PUT /url/:shortURL
{
	originalURL,
	newURL,
	metadata: { options, customAlias, expirationTIme }
}
```

Response:
```bash
{
	updatedShortURL
}
```

## HLD

### Database

- The database will store the URL mapping, and	will potentially index and partition the fields used often to filter, such as shortURL. Most reasonable databases will work such as DynamoDB, PostgreSQL, etc. We could benefit from the fast reads /		writes of a KV store such as DynamoDB, thus we’ll use this as the DB.

- We can use a KV store like DynamoDB or a document store like MongoDB which also provides atomicity for			concurrent writes as opposed to Cassandra or Riak which has better write performance and less read performance

- Also, if the sequencer the system uses has a high chance of collisions, then there could be a separate table for		storing the “used” or “seen” unique numerical IDs for the original URL to avoid any duplicate IDs for the original URL.	If there are any new requests, and a numerical ID for the original URL is generated, then this “used” database could		first be checked to verify if the numerical ID has been generated before

- Also, since shortURLs may have expiration times, a separate cron job (or job running during down-time) could delete	the expired URL mapping entries in the database OR during reads for the URL mapping, we could verify if the URL		mapping has expired or not, then delete it.

Additional points:
  - Both DynamoDB and MongoDB are read heavy and use locking for a particular record to prevent concurrent writes to	the same record.	 This further prevents different writes happening on the same record. 

  - Both DynamoDB and MongoDB also use single leader replication (only one primary node in a replica set), which also	means all write requests go to a single leader which prevents race conditions

  - MongoDB also ensures atomicity in concurrent write operations and avoids write collisions by returning an error if		there is a record duplication issue

  - Cassandra uses a write log and performs asynchronous writes to nodes to make it’s writes fast

  - Columnar databases like Cassandra or Riak have slower read performance (uses leaderless replication with nodes		performing both reads and writes, so reads are not optimized since there are no secondary nodes for them) as 	 	opposed to KV stores or document stores which have a single leader model, allowing availability for read intensive		tasks even when the leader is down

### API servers

The API servers will handle generating / redirecting a shortURL:

#### Generate a shortURL

- The API servers will validate if the originalURL exists by sending it a simple GET request. We can also use a popular open-source library like is-url to check if the original URL is valid. The API servers will also check if the		originalURL already exists in the database.

- The API servers will first use the sequencer to generate the unique numerical ID for the originalURL when a shortURL	generation request comes in. The API servers will then use the Base 58 / Base62 encoder to generate a shortURL,		and return it to the client. It will also write the created shortURL in the database.

- A custom short URL could also be generated via the custom alias. The API servers could first validate and check the	database if	the custom shortURL exists, and if it doesn’t exist, the API servers will save the mapping for the custom		shortURL

#### Redirecting shortURL

- For retrieving the originalURL from a shortURL, the API servers will first check the cache for the frequently accessed	shortURLs. If the shortURL is not in the cache, the servers will then find the originalURL from the database and return	a redirection response to the client

### URL shortening logic

We could implement the URL shortening logic using either a RNG / Hash function with a Base58 / Base62 encoder		OR by using a sequencer with a Base58 / Base62 encoder as explained below and in ‘URL shortening logic’:

#### RNG or Hash function with a Base58 / Base62 encoder

- This approach could use either a RNG to generate a random number / string OR a hash function (such as		SHA-1 or MD5 which produces a 128-bit string) to generate a hashed value of the originalURL. A RNG can be		implemented via cryptographic RNGs for increased unpredictability. The generated random number / string could	then be used as the shortURL.

- We could also get a fixed size hashed value of the originalURL from a hash function. Hash functions also		usually provide one-to-one mappings between the input and output hashed value - it is bijective.

- After we have the result from either the RNG or hash function, we can encode the result using a Base58 /		Base62 encoder, and then take the first N characters from the encoded result as our shortURL. N will be			determined based on the number of characters needed to minimize collisions. 

- A Base62 encoder leaves out the + and / characters from the Base64 encoder as they could cause issues in		URLs. Also, a Base58 encoder removes o, 0, I and 1 from the Base62 encoder as they can be confused and are	similar looking . Both of these encoders are used to ensure the shortURL is kept short as much as possible, ie		 1000000000 in Base62 is 15ftgG, which is just 6 characters.

- Using this approach, regardless of the randomness, there’s still a chance for collisions to occur, since we’re		retrieving the first N characters from the encoded result. We could increase the value of N OR perform collision		resolution by recursively appending a pre-defined string to the shortURL if there is a collision in the database. However, the resulting shortURL will be more predictable with the pre-defined string. However, both of these solutions add	latency and complexity.

#### Sequencer with a Base58 / Base62 encoder

- This approach uses a sequencer to generate a unique number, and then encodes the unique number via a			Base58 / Base62 encoder. 

- Redis will be helpful in implementing this sequencer / unique number generator as it is single-threaded and			processes one thread at a time - thus eliminating race conditions. It’s INCR command is atomic, which means		that INCR will execute without interference from other operations. However, managing a global sequencer using 		Redis may be complex due to synchronization issues if we’re using multiple Redis instances, thus Twitter 			snowflake for the sequencer may be more appropriate for a global scale.

- Redis stores the data in memory by default, but it could be configured via the Redis Auto Tiering feature to save		data in both RAM and on disk (SSDs) for persistence.

- However, for short URL generation to remain unique, the unique number also needs to be globally unique. A			single Redis instance will provide the single source of truth for the next unique number to be generated. Thus, it		is more appropriate to use a centralized Redis instance to generate the unique numbers, since we likely won’t			have as many write requests as opposed to read requests. Redis also is single-threaded and provides atomic			increment operations to increment the counter for the unique numbers, without facing any collisions.

- The centralized Redis instance will have a very low chance of being a SPOF, however we could do the following:
  - Shadow Redis instance:
    - A shadow Redis instance could be started up if the main one is down
  - Counter batching:
    - We could use “counter batching” to reduce the number of unique number generation requests the			centralized Redis instance receives. In counter batching, Redis provides a batch of unique numbers ahead	of time, let’s say 1000, and sends it to the API servers to use locally for the next 1000 shortURL generation	requests without contacting Redis directly.
    - Redis will also increase it’s counter / previous unique number by	1000. When the batch has been used up by the API servers, Redis will again provide a new batch of		unique numbers.
    - Counter batching will reduce the load on Redis and will save on multiple network requests	being made.

- Depending on the sequencer used, ie if it goes up by 1, the shortURL may be predictable.

- Twitter snowflake is also another approach we could use to implement a sequencer, however it is more complex		to maintain and is only necessary if the shortener operates on a large scale.

- A range handler is also another sequencer approach that could be used for a small to moderate scale.

- Overall, the design will go with this approach as it more scalable and has much lower chances of	collisions			happening

#### Generating shortURLs offline

- Also, if generating shortURLs may have some latency during high write volumes, we can generate the				shortURLs offline beforehand using unique randomized strings and store them in a separate table. The				pre-generated shortURLs cannot be present in the URL mappings table. When new requests come in, a				pre-generated shortURL can be pulled from the table, and the URL mapping should be recorded in the database		to make sure it is not used again.
		
- Thus, the system will use two tables, one with unused pre-generated unique shortURLs, and another containing	used URL mappings. When a shortURL generation request comes in, the API servers will move the			pre-generated shortURL to the URL mappings table.

- Also, the API servers could cache some of the pre-generated shortURLs in-memory, however making sure the		cache is consistent with the database tables will have some overhead.

### Cache

- Without any optimizations on the read latencies, we’ll have to do a “full table scan” on the database to retrieve a URL	mapping

- Since our system will be more read heavy than write heavy, we can greatly benefit from a read-through LRU cache		such as Redis or	Memcached which will store the shortURL : originalURL mappings. The cache can also be			horizontally scaled to support more reads. Possible solutions are below and in ‘Indexing / caching solutions’:
  - Adding an index to the database
  - In-memory cache
  - CDN and edge computing

- A modern day cache server can have 256 GB of RAM, which can easily fit 50% of the URL mappings table. However,	only the most recently or frequently used URLs will be cached, thus about 10-20% of the whole table may be cached.
	
- The cache could also be replicated via leaderless replicas (replica servers get updates from	 other replicas if there are	cache misses) if necessary for supporting multiple reads, but this is only necessary to support a lot of reads.


<img width="494" alt="image" src="https://github.com/user-attachments/assets/3c82dd37-78b5-4476-aeb0-002faba9526a" />


## Questions

Q: Consider a situation where your TinyURL service is suddenly getting a massive influx of traffic for URL shortening. The database is starting to slow down under the write load. Propose short-term and long-term solutions to scale the system.

A: Short-term Solutions: 

Caching:
Implement a caching layer to reduce the read load on the database, enhancing performance. 

Database 
Optimization/Indexing: Optimize the database by indexing URLs/tables to speed up read/write operations. 

Load Balancing: 
Use a load balancer to distribute traffic evenly across multiple servers, preventing any single server from becoming a bottleneck. 

Vertical Scaling: 
Increase the capacity of the current server by adding more resources (CPU, RAM). 

Long-term Solutions: 

Separating Read/Write: 
Use separate databases or instances for read and write operations to reduce contention and improve resource utilization. 

Horizontal Scaling: 
Add more servers to distribute the load, enhancing the system’s ability to handle increased traffic. 

Database Partitioning/Sharding: 
Split the database into smaller, manageable parts (shards) placed on different servers to improve performance. 

Use a CDN: 
Implement a Content Delivery Network to cache URLs at various geographical locations, reducing latency.

Microservices Architecture: 
Break down the application into smaller, independent services that can be scaled individually based on demand.

<img width="600" alt="image" src="https://github.com/user-attachments/assets/a91056ba-1bd2-40f1-83a2-60ae1b1f0802" />


## DD

### Encoder

- To generate a Base58 / Base62 encoded value, we keep performing the mod operation on the numeric ID,	where we do numerical ID % 58 or numerical ID % 62. We then assign the character indexes from a-z, A-Z,	0-9 excluding o, 0, I, 1 (if using Base58), to the remainder after the mod operation. Then we take the		remainders in order from the most recent to the oldest to get the Base58 / Base64 encoded value

- The Base58 encoding process is to the right in ‘Base 10 to Base 58 conversion’

### Decoder

- For the decoding process, we need to multiply each number in the Base58 encoded value by 58^(place in 	the Base58 encoded value) and add all the results up to get the base 10 value

- For example, for 27qMi57J, we would first multiple 1 by 58^(7). 1 is the base 10 value for 2, where 2 is the	first number in 27qMi57J. We would repeat this process and add all of the multiplied values up to get the		base 10 result.

### Scalability

We can scale different components of the system:

#### Scaling the database

- If we store 1B URL mappings in the database, and a single URL mapping entry is 500 bytes, we’ll			store in total:
  - 1B * 500 bytes = 500 GB of storage in the database
  - 500 GB is definitely possible within a KV store such as DynamoDB utilizing SSDs or within a			SQL DB
		
- The database itself may not be large enough that it needs to be sharded, however if necessary to		avoid losing a whole database, the database could be sharded using the below approaches:
  - Range based partitioning:
    - The URL mappings can be sharded based on ranges of the first few characters of the					shortURL, thus some entries can be mapped to the “A-D” shard, and others to the “E-F”				shard, etc. The ranges could be calculated to ensure an even distribution, and this range				based partitioning approach will be static. However, even after calculating the ranges, there				may still be an uneven distribution of URL mappings in the shards.
  - Hash-based partitioning:
    - In hash-based partitioning, we’ll take a hash of the shortURL and map it to a shard with a				hash range. This will have a better distribution in URL mappings than range based					partitioning, but could still have some uneven distributions which could be solved using					consistent hashing via virtual nodes.

#### Scaling the API servers

- Since the system has more reads than writes, we can separate the read and write operations such		that we horizontally scale the servers performing the reads, and not scale the servers handling writes		as much. 

### Fault tolerance of database

To ensure the fault tolerance of the database, we can apply the following:

#### Database replication

- Multiple replicas of the database can be created via a primary-secondary replication approach. This		may add complexity to the system, but will prevent a SPOF. Also, because the shortURL creations /		updates may not be expected to take effect right away, an asynchronous replication can be made to		the servers in different AZs, while synchronous replication happens within the AZ.

#### Database backups

- Database backups taken periodically via snapshots and operations written to an operation log and		stored in S3 could be implemented. This also adds complexity to the system, but will be necessary if		the shortener operates at a large scale.

### Allowing only specific set of users to access a shortURL (optional)

- To allow only specific users to access a shortURL, we can store the permissions info (public / private) for	each shortURL in the database. We can also maintain a separate table containing the encrypted userIDs 	and the private shortURLs only that userID has access to (cardinality is a userID and shortURL). 

- If the shortURL is private, then the API servers could first  check the Authorization header’s user auth token	/ JWT to verify using this table if the user has permissions to access the shortURL.

Base 10 to Base 58 conversion:

<img width="650" alt="image" src="https://github.com/user-attachments/assets/e4ad8949-fb97-417c-aa7a-909bb7b8d51b" />


