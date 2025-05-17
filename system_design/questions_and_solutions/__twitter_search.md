# Twitter search

We'll design a service that can store and search over all the user tweets. This design is aimed at the data layout, indexing and scaling functions of the system.

Note that this SDI is different from the FB post search one in that we also need to design the storage of the tweets in here.

## Requirements

### Questions

- Are we designing the search functionality, or the typeahead functionality?
  - Search functionality only

- Will the search be performed on the attachments too? And will the tweets contain attachments?
  - For simplicity, leave out attachments from the design

- Is the search done by keywords in the search query, or are additional filters also applied?
  - Yes, search by keywords, but the search results may be returned in terms of other filters like sorting by date, like count, etc

- Should the search results be fuzzy matched or personalized to the user?
  - No

- When a user searches for tweets, should we return any tweet matching the query, or tweets which user's connections liked: maybe the user's tweets or a friend's tweet, trending tweet, etc?
  - Let's return any type of tweet, it could be the user's or a friend's tweet, or any other user's tweet

- Can users create and like tweets?
  - Yes

### Functional

- Users can create and like tweets
- Users can search tweets by keywords and filters:
  - Search results will be filtered based on sorting order like by date, like count, etc

- Twitter has 1.5B users with 800M DAU
- 400M tweets are generated per day on average
- Average size of a tweet is 300 bytes
- 500M searches every day

**Note that by not including fuzzy matching and personalization, the design will be simplified in that caching the search results will be much easier. Cached search results doesn't have to be catered to a specific user, and the fuzzy matching algorithm doesn't have to be designed**

### Non-functional

- Low latency:
  - Search results should be returned within 100 - 500 ms
  - New tweets should be typically searchable in a short amount of time, < 1 min
  - We could optimize to return newer tweets (warm data) faster, and return older tweets (cold data) slower
- Throughput:
  - There will be a high volume of search requests
- Durability:
  - The system should durably store indexes for tweets and the tweets themselves, from all time

## Estimations

- Since we have 400M tweets generated per day on average, and each tweet is 300 bytes, the total storage we'll need per day will be:
  - 400M * 300 bytes = 120 GB / day of tweets will be generated

- If we store the data for 10 years:
   - 120 GB * 365 days * 10 years = 438 TB of data will be stored in total after 10 years

- Also, there are 1M English words, and if we stored all these terms in an inverted index, assuming a single inverted index entry for a term contains 1M docIDs - we'll have 1M docIDs * 1 bytes = 1 MB for a single inverted index entry:
  - 1M * 1 MB = 1 TB of storage needed in the inverted index mappings storage

## Data model / entities

- User:
  - userID
  - userName
  - userEmail

- Tweets:
  - tweetID
  - userID
  - tweet
  - likes
  - metadata: { createdAt }

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Search tweets

- Searching for tweets will likely be handled by a search service, which will use the inverted index mappings to return search results

Request:
```bash
GET /tweets?query&sort={ LIKES / DATE }&nextCursor={ last tweetID on viewport if using LIKES as sort order OR oldest createdAt value on viewport if using DATE as sort order }&limit
```

Response:
```bash
{
  tweets: [ { tweetID, userID, userName, tweet, likes, metadata } ],
  nextCursor, limit
}
```

### Create a tweet

- Tweet creation is assumed to be done by a separate Tweet service, however, the created tweet will still be fed to an Indexing service to update the inverted index mappings. The same Tweet service will also store the created Tweet in the Tweets DB

Request:
```bash
POST /tweets
{
  tweet
}
```

### Like a tweet

- Liking a tweet is assumed to be done by a separate Likes service, however, the like event will still be fed to an Indexing service to update the inverted index mappings

Request:
```bash
PATCH /tweets/:tweetID?op={LIKE}
```

## HLD

### Indexing service

- The overall system is likely part of a larger system, so we can assume that there is a separate tweet and like service which are handling client requests when it comes to creating tweets / liking tweets. Thus, these separate tweet and like service will send similar tweet / like data to this indexing service, for the indexing service to build a searchable inverted index mappings.

### Inverted index mappings storage

- We'll use an inverted index to return faster results efficiently for a very large number of tweets, however the below approaches can be used and in 'Searching tweets / posts efficiently':
  - Scale an unindexed database
  - Create an inverted index:
    - Inverted index mappings contain a mapping as follows: term : { [ docIDs ], [ termFreqs in docs ], [ [ docLocations ], [ docLocations ] ] }
    - The structure of an inverted index mapping allows us to only look for the terms / keywords, and return the relevant docIDs sorted by the termFreqs (frequency of term in document) or any other values like likes count / date contained in the mapping.
    - To ensure we get fast results, we could store these mappings in Redis, as Redis provides functionality for complex data types such as matrices, which will be needed here. Since Redis mainly operates in-memory, there are also alternatives like MemoryDB we could use, which is an in-memory persistence DB.
    - When tweets or likes are created, the indexing service will break up the tweet's content into terms, and then update the tweet's terms in the inverted index mappings accordinghly using the term frequencies in the tweet, likes count, term locations in tweet, date of tweet, etc. This process of breaking the tweet is actually called tokenization.
    - Note that the value within a mapping will be very large, as there will be numerous tweetIDs (docIDs) for a single term. Thus, the indexing service and inverted index mappings storage will need to be scaled appropriately in the DD.

- The inverted index mappings could also contain the text content of the tweetID, however this will be quite a lot of textual data (3.6 PB) - and searching through this much data is not optimal. Thus, the inverted index mappings could instead store only relevant IDs and values needed for searching, and another DB (Tweet DB) will likely store the actual text content. The inverted index mappings will then return tweetIDs for a search query, and the text content for those tweetIDs will be retrieved from the Tweets DB, then returned to the client (client will have tweetIDs from mappings, and text content from Tweets DB).

- This might seem like the data is split in two places now, however the inverted index mappings should only store fields which will support fast searches - storing textual data will not help with the searches.

#### Sharding the inverted index mappings storage

- The inverted index mappings storage could also be sharded based on the term, however this could produce an uneven distribution of the terms, and if a term becomes a hotspot, then the term's shard could be a SPOF.
- Thus, we could instead apply consistent hashing on the terms and sharded inverted index mappings to have an even distribution, where terms of a created tweet will be hashed to the hash ring, then the N closest clockwise shards will store the tweet's terms hashed to the hash ring. This way, when a new search query comes in, we'll also hash the search query terms to the hash ring, and find the N closest clockwise shards that we can query the inverted index mappings from - which should contain the query terms.
- Redis Cluster provides features to configure sharding, however it doesn't directly provide consistent hashing, but provides a similar sharding technique known as hash slots where every key (term) is part of a hash slot. There are 16384 hash slots in Redis Cluster, and to compute the hash slot for a given key, we simply take the CRC16(key) % 16384. Every node / shard in a Redis Cluster is then responsible for a subset of the hash slots. 

### Search service

- The search service will handle requests for searching tweets using the inverted index mappings. To sort the returned tweetIDs by date, likes count, frequency, etc, and return the search results to the user, we can do the below or in 'Returning tweets from inverted index mappings logic':
  - Request-time sorting
  - Multiple indexes:
    - We can maintain two different inverted index mappings, one with tweetIDs sorted by date (creation index), and another sorted by the likes count (likes index). We can potentially also have another one sorted by term frequency within the document (frequency index) if necessary. The actual sorted dates and likes count data will be in the second list in: term : { [ docIDs ], [ sorted dates / likes count ], [ [ docLocations ], [ docLocations ] ] }. This means that for a specific term in these mappings, all the docIDs, sorted dates / likes count, docLocations will be sorted based on date OR likes count - and the second list will contain the actual dates / likes count data.
    - The creation index can be implemented using a standard Redis list, since we're always going to append the most recently created tweet to this list, and the results will only be returned from the last elements of this list (since it's sorted by date)
    - The likes index can be implemented using a Redis sorted set, where the sorted set can maintain a list of unique elements (tweetIDs) ordered by a score (likes count). Insertions, deletions, queries and range queries are all performed in O(logn) time in a sorted set.
    - When a new tweet is created, the indexing service will add mappings for every term in the tweet, or update the mappings - for both the creation and likes index. For adding a new tweetID to a mapping in the creation index, we'll just append the tweetID to the end of the Redis list. For adding a new tweetID to a mapping in the likes index, we'll insert a new element with the (tweetID, likes count) into the Redis sorted set.
- The search service will also be responsible for aggregating the returned tweetIDs such that no duplicate tweetIDs exist in the result, and they adhere to any sorting or filtering logic, either by date, likes or frequency.

### Tweets database / cache

- The Tweets database will store all the tweets generated via the Tweet service. The likes service will also update the tweets stored in this database. We could either use a SQL or NoSQL DB here, and either will likely work fine.
- However, we won't maximize on the ACID or relationships SQL databases provides. A KV store such as DynamoDB may work better since we can partition by a primary key, tweetID, and use GSI (global secondary index) to further search entries which are not the primary key, such as using userID. This will improve the search functionality, and provide low latency reads.
- It may be better to partition by tweetID, as opposed to userID since a single userID could have numerous tweets, while another userID could have 0 tweets - making the partition distribution uneven.

#### Cache

- We could also store frequently accessed tweets in a cache such as Memcached. We can use Memcached here instead of Redis because the list / sorted set data structures are not needed to store the tweet data, which is simple in structure. Also, we can utilize the multi-threaded nature of Memcached to perform reads in parallel.

### Search cache

- We can also cache the frequently accessed search results returned by searching inverted index mappings. In this way, not all of the tweetIDs within the inverted index mappings will be stored, but instead only the most frequently accessed mappings will be stored. Because this search cache will need to be consistent in the data structures with the inverted index mappings, we can use Redis lists / sorted sets within this search cache as well.

- However, the TTL on the search cache will need to be configured appropriately so that stale search results are evicted - a possible TTL could be 1 - 10 min

### CDN

- CDNs will also further support in caching at the edge, where clients can go directly to the CDN POPs to fetch search results for queries as opposed to requesting the search service to search the inverted index mappings.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/21b2dd61-bad2-436f-9926-745000a0f190" />

## DD

### Handling multi-keyword queries

- To support searches for multi-keyword queries like "This is a multi-keyword query", we can do the following and in 'Handling multi-keyword queries':
  - Intersection and filter:
    - Intersecting the results from a multi-keyword search will be very compute intensive since some results may contain millions of entries. Also, implementing the intersection between the search results would mean that we may need to maintain a hash map of the tweetIDs - which will further increase both storage and latency as we'll need to perform a complex operation everytime a user searches.
  - Bigrams of shingles

### Handling large volume of writes

We have two sources of writes - tweet creation and likes which we'll need to handle:

#### Tweet creation

- When a tweet is created, we'll need to tokenize the tweet and then write to both the creation and likes indexes. If a tweet has 100 words, we might trigger 100+ writes one for each word (if we use bigrams of shingles, we'll have a lot more writes). With a large number of tweets being created concurrently, the indexing service may become a SPOF.
- To prevent the indexing service from becomming a SPOF, we can easily horizontally scale the servers as this is a stateless service.

Kafka queues between tweets / likes service and indexing service servers:

- Also, to prevent tweet creation data from being lost as it is waiting to be indexed via the indexing service, a Kafka queue can be positioned between the tweet / like services and the indexing service's servers. Also Kafka can be configured such that it buffers messages so that the data is not lost within the queue. Buffering in Kafka will also handle bursts of messages being sent since the message data can be stored temporarily to prevent message loss during bursts.
- The Kafka messages could also be deleted periodically via a TTL of a few mins - since the indexing service will index the tweet within 1 min. The number of Kafka queues can be configured according to the number of indexing service servers, where if the number of workers in an indexing service server grows, the number of queues will also grow.

Sharding the inverted index mappings:

- Lastly, we can shard the creation and likes indexes on the term, so that queries for a single term will only need to search through a single shard, and the search for multiple terms can be done in parallel by querying all the term's corresponding shards.

#### Likes

- Likes occur much more frequently than tweet creations (10x more frequently). We can reduce the number of writes we need to do for "like events" by doing the below, and in 'Reducing writes for like events':
  - Batch likes before writing to the database
  - Two stage architecture

### Handling large volume of search requests

- The system should return non-personalized results, and we have up to 1 min before a tweet needs to appear in the search results. Caching the results to handle large volume of search results may be the best solutions as explained below and in 'Handling large volume of search requests':
  - Use a distributed cache alongside our search service
  - Use a CDN to cache at the edge

### Fault tolerance of inverted index mappings

- To ensure fault tolerance of the inverted index mappings, we can replicate the inverted index mappings. Redis Cluster provides built-in asynchronous primary-secondary replication by default, which should be suitable here since write inconsistencies via a leaderless approach could have issues in the inverted index mappings (which requires low latency reads).

#### Keeping a reference to the indexServerID in the Tweets DB to recover when inverted index mappings are down / erased

- If both the primary and secondary nodes for an inverted index mapping shard are down, then it would be really difficult to rebuild the shard's inverted index mappings again without knowing which terms were stored in this crashed shard.
- We can store a reference to the indexServerID for a tweetID in the Tweets DB or ZooKeeper. This will allow us to query the Tweets DB, and look for tweets with the indexServerID that crashed. Afterwards, we can rebuild the index for those tweets with the crashed indexServerID.
- However, maintaining this indexServerID field may have some overhead if we need to update the indexServerID during scaling events, but it ensures fast recovery time if the inverted index mappings are down / erased. Thus, this overall mapping between the indexServerID: [ tweetIDs ] could instead be maintained in a service like ZooKeeper, which provides a KV store for maintaining server-size mappings like these.

### Reduce storage space of inverted index mappings

- Users are usually only interested on a small portion of tweets, thus we can do the following optimizations:
  - Put limits on how many tweetIDs a single term in the inverted index will contain. We probably don't need all tweetIDs with "dog" in the tweet content - only about 1k - 10k tweetIDs for "dog" should be fine.
  - Ignore stopwords like "a", "of", etc (when updating the inverted index) which provide no value in searching.
  - In-frequently accessed terms and their creation / likes index mappings could instead be moved to a cold storage such as in S3 Standard-IA. If there are queries for these in-frequent terms, the query could first check the Redis inverted index mappings, and if results are not in Redis, it could instead be queried from S3 via Athena and returned to the client with a small increase in latency.

### Ranking responses

- In order to return ranked responses, such as ranking by likes, date, frequency of terms, etc. We can use Redis' built-in data structures such as lists / sorted sets to sort the tweetIDs within a single inverted index mapping.
- We can then compile the top N tweetIDs from each term's mappings (from the lists / sorted sets) from the search query, and then the search service will do a final aggregated ranking / sorting on the compiled tweetIDs before sending it to the client.


