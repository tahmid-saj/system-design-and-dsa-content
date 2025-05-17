# FB post search

We'll design the search functionality for FB posts. This design is aimed at the data layout, indexing and scaling functions of the system.

We're going to assume that the SDI requires us to not use a search tool like Elasticsearch or Lucene or a pre-built index (like PostgreSQL full-text)

## Requirements

### Questions

- Are we designing the search functionality, or the typeahead functionality?
  - Search functionality only

- Will the search be performed on the attachments too? And will the posts contain attachments?
  - For simplicity, leave out attachments  from the design

- Is the search done by keywords in the search query, or are additional filters also applied?
  - Yes, search by keywords, but the search results may be returned in terms of other filters like sorting by date, like count, etc
 
- Should the search results be fuzzy matched or personalized to the user?
  - No

- When a user searches for posts, should we return any post matching the query, or posts which user's connections liked: maybe the user's post or a friend's post, trending post, etc?
  - Let's return any type of post, it could be the user's or a friend's posts, or any other user's post.
 
- Can users create and like posts?
  - Yes

### Functional

- Users can create and like posts
- Users can search posts by keywords and filters:
  - Search results will be filtered based on sorting order like by date, like count, etc

**Note that by not including fuzzy matching and personalization, the design will be simplified in that caching the search results will be much easier. Cached search results doesn't have to be catered to a specific user, and the fuzzy matching algorithm doesn't have to be designed**

### Non-functional

- Low latency:
  - Queries should be returned within 100 - 500 ms
  - New posts should be typically searchable in a short amount of time, < 1 min
  - We could optimize to return newer posts (warm data) faster, and return older posts (cold data) slower
- Throughput:
  - There will likely be a high volume of search requests
- Durability:
  - The system should durably store indexes for posts, from all time

## Estimations

We're obviously dealing with a large-scale system. In our estimations, we need to know a few numbers such as:
- How often are we writing to the system
- How frequently are we searching
- How much data are we storing

FB has 1B users, and each user produces 1 post per day on average (maybe 20% do 5 posts and 80% do 0 posts) and likes 10 posts. We'll assume there's 100k seconds in a day (rounding up for convenience):

- The volume of writes per second will be:
  - Posts created: (1B * 1 post / day) / (100k seconds / day) = 10k posts / second
  - Likes created: (1B * 10 likes / day) / (100k seconds / day) = 100k likes / second
  - Thus, we'll likely have 10x more likes than posts created

- The volume of searches per second will be:
  - Searches: (1B * 5 search / day) / (100k seconds / day) = 50k searches / second

**While the number of searches per second may be a lot, our system is actually more write heavy than read heavy since there will be more like events than searches happening**

We now want to calculate how much data we are storing. We'll assume FB is 10 years old and that a single post entry is 1 KB (excluding attachments of course):

- Posts created in 10 years: (1B * 1 post / day) * (365 days / year) * (10 years) = 3.6T posts created in 10 years
- Total posts storage needed: (3.6T posts) * (1 KB / post) = 3.6 PB

**This also shows that our system will need to store a very large number of posts optimally**

- Also, there are 1M English words, and if we stored all these terms in an inverted index, assuming a single inverted index entry for a term contains 1M docIDs - we'll have 1M docIDs * 1 bytes = 1 MB for a single inverted index entry:
  - 1M * 1 MB = 1 TB of storage needed in the inverted index mappings storage

## Data model / entities

- User:
  - userID
  - userName
  - userEmail

- Posts:
  - postID
  - userID
  - post
  - likes
  - metadata: { createdAt }

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public


### Search posts

- Searching for posts will likely be handled by a search service, which will use the inverted index mappings to return search results

Request:
```bash
GET /posts?query&sort={ LIKES / DATE }&nextCursor={ last postID on viewport if using LIKES as sort order OR oldest createdAt value on viewport if using DATE as sort order }&limit
```

Response:
```bash
{
  posts: [ { postID, userID, userName, post, likes, metadata } ],
  nextCursor, limit
}
```

### Create a post

- Post creation is assumed to be done by a separate Post service, however, the created post will still be fed to an Indexing service to update the inverted index mappings

Request:
```bash
POST /posts
{
  post
}
```

### Like a post

- Liking a post is assumed to be done by a separate Likes service, however, the like event will still be fed to an Indexing service to update the inverted index mappings

Request:
```bash
PATCH /posts/:postID?op={LIKE}
```

## HLD

### Indexing service

- The overall system is likely part of a larger system, so we can assume that there is a separate post and like service which are handling client requests when it comes to creating posts / liking posts. Thus, these separate post and like service will send similar post / like data to this indexing service, for the indexing service to build a searchable inverted index mappings.

### Inverted index mappings storage

- We'll use an inverted index to return faster results efficiently for a very large number of posts, however the below approaches can be used and in 'Searching posts efficiently':
  - Scale an unindexed database
  - Create an inverted index:
    - Inverted index mappings contain a mapping as follows: term : { [ docIDs ], [ termFreqs in docs ], [ [ docLocations ], [ docLocations ] ] }
    - The structure of an inverted index mapping allows us to only look for the terms / keywords, and return the relevant docIDs sorted by the termFreqs (frequency of term in document) or any other values like likes count / date contained in the mapping.
    - To ensure we get fast results, we could store these mappings in Redis, as Redis provides functionality for complex data types such as matrices, which will be needed here. Since Redis mainly operates in-memory, there are also alternatives like MemoryDB we could use, which is an in-memory persistence DB.
    - When posts or likes are created, the indexing service will break up the post's content into terms, and then update the post's terms in the inverted index mappings accordinghly using the term frequencies in the post, likes count, term locations in post, date of post, etc. This process of breaking the post is actually called tokenization.
    - Note that the value within a mapping will be very large, as there will be numerous postIDs (docIDs) for a single term. Thus, the indexing service and inverted index mappings storage will need to be scaled appropriately in the DD.

- The inverted index mappings could also contain the text content of the postID, however this will be quite a lot of textual data (3.6 PB) - and searching through this much data is not optimal. Thus, the inverted index mappings could instead store only relevant IDs and values needed for searching, and another DB (Posts DB) will likely store the actual text content. The inverted index mappings will then return postIDs for a search query, and the text content for those postIDs will be retrieved from the Posts DB, then returned to the client (client will have postIDs from mappings, and text content from Posts DB).
- This might seem like the data is split in two places now, however the inverted index mappings should only store fields which will support fast searches - storing textual data will not help with the searches.

### Search service

- The search service will handle requests for searching posts using the inverted index mappings. To sort the returned postIDs by date, likes count, frequency, etc, and return the search results to the user, we can do the below or in 'Returning posts from inverted index mappings logic':
  - Request-time sorting
  - Multiple indexes:
    - We can maintain two different inverted index mappings, one with postIDs sorted by date (creation index), and another sorted by the likes count (likes index). We can potentially also have another one sorted by term frequency within the document (frequency index) if necessary. The actual sorted dates and likes count data will be in the second list in: term : { [ docIDs ], [ sorted dates / likes count ], [ [ docLocations ], [ docLocations ] ] }. This means that for a specific term in these mappings, all the docIDs, sorted dates / likes count, docLocations will be sorted based on date OR likes count - and the second list will contain the actual dates / likes count data.
    - The creation index can be implemented using a standard Redis list, since we're always going to append the most recently created post to this list, and the results will only be returned from the last elements of this list (since it's sorted by date)
    - The likes index can be implemented using a Redis sorted set, where the sorted set can maintain a list of unique elements (postIDs) ordered by a score (likes count). Insertions, deletions, queries and range queries are all performed in O(logn) time in a sorted set.
    - When a new post is created, the indexing service will add mappings for every term in the post, or update the mappings - for both the creation and likes index. For adding a new postID to a mapping in the creation index, we'll just append the postID to the end of the Redis list. For adding a new postID to a mapping in the likes index, we'll insert a new element with the (postID, likes count) into the Redis sorted set.
- The search service will also be responsible for aggregating the returned postIDs such that no duplicate postIDs exist in the result, and they adhere to any sorting or filtering logic, either by date, likes or frequency.

### Search cache

- We can also cache the frequently accessed search results returned by searching inverted index mappings. In this way, not all of the postIDs within the inverted index mappings will be stored, but instead only the most frequently accessed mappings will be stored. Because this search cache will need to be consistent in the data structures with the inverted index mappings, we can use Redis lists / sorted sets within this search cache as well.

- However, the TTL on the search cache will need to be configured appropriately so that stale search results are evicted - a possible TTL could be 1 - 10 min

### CDN

- CDNs will also further support in caching at the edge, where clients can go directly to the CDN POPs to fetch search results for queries as opposed to requesting the search service to search the inverted index mappings.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/d277997a-1f01-48d6-b77c-37ec4e4ffa4e" />

## DD

### Handling multi-keyword queries

- To support searches for multi-keyword queries like "This is a multi-keyword query", we can do the following and in 'Handling multi-keyword queries':
  - Intersection and filter:
    - Intersecting the results from a multi-keyword search will be very compute intensive since some results may contain millions of entries. Also, implementing the intersection between the search results would mean that we may need to maintain a hash map of the postIDs - which will further increase both storage and latency as we'll need to perform a complex operation everytime a user searches.
  - Bigrams of shingles

### Handling large volume of writes

We have two sources of writes - post creation and likes which we'll need to handle:

#### Post creation

- When a post is created, we'll need to tokenize the post and then write to both the creation and likes indexes. If a post has 100 words, we might trigger 100+ writes one for each word (if we use bigrams of shingles, we'll have a lot more writes). With a large number of posts being created concurrently, the indexing service may become a SPOF.
- To prevent the indexing service from becomming a SPOF, we can easily horizontally scale the servers as this is a stateless service.

Kafka queues between posts / likes service and indexing service servers:

- Also, to prevent post creation data from being lost as it is waiting to be indexed via the indexing service, a Kafka queue can be positioned between the post / like services and the indexing service's servers. Also Kafka can be configured such that it buffers messages so that the data is not lost within the queue. Buffering in Kafka will also handle bursts of messages being sent since the message data can be stored temporarily to prevent message loss during bursts.
- The Kafka messages could also be deleted periodically via a TTL of a few mins - since the indexing service will index the post within 1 min. The number of Kafka queues can be configured according to the number of indexing service servers, where if the number of workers in an indexing service server grows, the number of queues will also grow.

Sharding the inverted index mappings:

- Lastly, we can shard the creation and likes indexes on the term, so that queries for a single term will only need to search through a single shard, and the search for multiple terms can be done in parallel by querying all the term's corresponding shards.

#### Likes

- Likes occur much more frequently than post creations (10x more frequently). We can reduce the number of writes we need to do for "like events" by doing the below, and in 'Reducing writes for like events':
  - Batch likes before writing to the database
  - Two stage architecture

### Handling large volume of search requests

- The system should return non-personalized results, and we have up to 1 min before a post needs to appear in the search results. Caching the results to handle large volume of search results may be the best solutions as explained below and in 'Handling large volume of search requests':
  - Use a distributed cache alongside our search service
  - Use a CDN to cache at the edge

### Fault tolerance of inverted index mappings

- To ensure fault tolerance of the inverted index mappings, we can replicate the inverted index mappings. Redis Cluster provides built-in asynchronous primary-secondary replication by default, which should be suitable here since write inconsistencies via a leaderless approach could have issues in the inverted index mappings (which requires low latency reads).

#### Keeping a reference to the indexServerID in the Posts DB to recover when inverted index mappings are down / erased

- If both the primary and secondary nodes for an inverted index mapping shard are down, then it would be really difficult to rebuild the shard's inverted index mappings again without knowing which terms were stored in this crashed shard.
- We can store a reference to the indexServerID for a postID in the Posts DB or ZooKeeper. This will allow us to query the Posts DB, and look for posts with the indexServerID that crashed. Afterwards, we can rebuild the index for those posts with the crashed indexServerID.
- However, maintaining this indexServerID field may have some overhead if we need to update the indexServerID during scaling events, but it ensures fast recovery time if the inverted index mappings are down / erased. Thus, this overall mapping between the indexServerID: [ postIDs ] could instead be maintained in a service like ZooKeeper, which provides a KV store for maintaining server-side mappings like these.

### Reduce storage space of inverted index mappings

- Users are usually only interested on a small portion of posts, thus we can do the following optimizations:
  - Put limits on how many postIDs a single term in the inverted index will contain. We probably don't need all postIDs with "dog" in the post content - only about 1k - 10k postIDs for "dog" should be fine.
  - Ignore stopwords like "a", "of", etc (when updating the inverted index) which provide no value in searching.
  - In-frequently accessed terms and their creation / likes index mappings could instead be moved to a cold storage such as in S3 Standard-IA. If there are queries for these in-frequent terms, the query could first check the Redis inverted index mappings, and if results are not in Redis, it could instead be queried from S3 via Athena and returned to the client with a small increase in latency.

### Ranking responses

- In order to return ranked responses, such as ranking by likes, date, frequency of terms, etc. We can use Redis' built-in data structures such as lists / sorted sets to sort the postIDs within a single inverted index mapping.
- We can then compile the top N postIDs from each term's mappings (from the lists / sorted sets) from the search query, and then the search service will do a final aggregated ranking / sorting on the compiled postIDs before sending it to the client.


