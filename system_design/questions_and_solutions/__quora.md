# Quora

Quora is a social question-and-answer service that allows users to ask questions to other users. Quora was created because of the issue that asking questions from search engines results in fast answers but shallow information. Instead, we can ask the general public, which feels more conversational and can result in deeper understanding, even if it’s slower. Quora enables anyone to ask questions, and anyone can reply. Furthermore, there are domain experts that have in-depth knowledge of a specific topic who occasionally share their expertise by answering questions.

## Requirements

### Questions

- Quora has a question-answer hierarchy, where a question can have multiple answers. For the question and answers, there may be any number of comments (replies). There could also be comments for other comments as well. Are we following this hierarchy?
  - Yes

- What is the DAU, and number of concurrent users?
  - Assume 100M DAU, and 20k concurrent users per second

### Functional

- Questions and answers:
  - Users can ask questions and post answers
  - Questions and answers can include images and videos
- Users can upvote / downvote and comment
- Users can search questions, answers and comments

<br/>

- Recommendation system:
  - Users can view their feed, which includes similar questions, answers, comments, etc, they're interested in - the system should facilitate user discovery with a Recommendation service
  - The feed can also include questions that need answers
- The system should also rank answers according to their usefulness, and the most helpful answer will be ranked highest and listed at the top

- Assume 100M DAU, and 20k concurrent users per second

### Non-functional

- Availability > consistency:
  - Users posting a question might not necessarily need to see the latest view of answers right away, since the purpose of Quora is to create slow conversational question-answer content
- Low latency of searches:
  - Searching of questions and answers should be returned in < 500 ms
  - We want to efficiently store questions, answers and comments (replies) for those questions / answers. It's likely that these entities will have a hierarchy, and we want to efficiently store and fetch them

## Data model / entities

- Users:
  - userID
  - userName
  - email

<br/>
 
- Questions:
  - This entity will store all the questiona asked by users
	  - questionID
	  - userID
	  - question
	  - s3URLs
	  - createdAt
 
- Answers:
  - This entity will store all the answers posted by users, along with the answer's upvotes / downvotes. Note that the rank field will be the calculated rank done in the background
    - answerID
    - userID
    - questionID
    - answer, upvotes / downvotes
    - s3URLs
    - rank
    - createdAt
 
- Comments:
  - This entity will store all the comments sent by users, for questions / answers
	  - commentID
	  - userID
	  - entityID: { questionID or answerID or commentID }
    	  - comment
	  - createdAt

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed messages quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

Note: We don’t consider APIs for a recommendation system or ranking because they are not placed as an explicit request by the user. Instead, the servers coordinates with other components to ensure the service.

### Post a question

- This endpoint will be used to post a question, and store the question in storage

Request:
```bash
POST /questions
{
  question
}
```

### Post an answer

- This endpoint will be used to post an answer for a questionID

Request:
```bash
POST /questions/:questionID/answers
{
  answer
}
```

#### Upload attachments

- When uploading binary data, multipart/form-data / multipart/mixed or another MIME	type such as image/png is usually used

- The content type is set to multipart/mixed which means that the request contains	different inputs and each input can have a different encoding type (JSON or binary).	The metadata sent will be in JSON, while the file itself will be in binary. 

- The placeholder {---xxBOUNDARYxx—} will contain a text string for the boundary	that differentiates one part of the body from another. For example				“__the_boundary__” could be used as the string. Boundaries must also start with		double hyphens and end with double hyphens too.

- Note that since this design is using a pre-signed URL to upload files, the client will	first request for a pre-signed URL from the servers, then make a HTTP PUT request	with the file data in the request body to the pre-signed URL 

##### Request for a pre-signed URL

Request:
```bash
POST /questions/pre-signed-url (for questions)
POST /questions/:questionID/pre-signed-url (for answers)
{
	attachmentName, fileType
}
```

Response:
```bash
{
	pre-signed URL
}
```

##### Upload to pre-signed URL

Request:
```bash
PUT /<pre-signed URL>
Content-Type: multipart/form-data; boundary={---xxBOUNDARYxx—}
{
—xxBOUNDARYxx–
<HEADERS of the boundary go here>

We’ll put the file binary data in this boundary:

<attachment contents go here>

—xxBOUNDARYxx–
}
```

Response:
```bash
Content-Type: application/json
{
  UPLOADED / FAILED
}
```

### Upvote / downvote answer

Request:
```bash
PATCH /questions/:questionID/answers/:answerID?op={ UP_VOTE or DOWN_VOTE }
```

### Comment on an answer for a question

Request:
```bash
POST /questions/:questionID/comments (for comments)
POST /questions/:questionID/answers/:answerID/comments (for answers)
{
  comment
}
```

### Search questions / answers / comments

- Because the system will perform some ranking in the background, the returned paginated results can also adhere to the ranking

Request:
```bash
GET /search?query&nextCursor={ viewport's oldest createdAt timestamp OR viewport's lowest ranked answer }&limit
```

Response:
```bash
{
  results: [ { questionID, question, s3URLs, createdAt } ],
  nextCursor, limit
}
```

## HLD

### API gateway

- The API gateway will provide rate limiting, authentication, and route requests to the specific services. For example, for a post creation request, the API gateway could route the request to the Posts service.

### Posts service

- The Posts service will handle posting questions / answers / comments, uploading attachments and upvoting / downvoting answers. The Posts service will also store the created question, answer, comment (post) in the database. Overall, this service will be stateless and can be easily scaled horizontally.

#### Querying for answers and comments for a questionID

- Below is how a query might look like when querying for the answers and comments for a requested questionID:

```sql
select questionID, s3URLs, question, answer, comment, createdAt as questionCreatedAt from (
select  question, s3URLs, createdAt
from questions where questionID = :questionID
inner join answers on questions.questionID = answers.questionID
inner join comments on questions.questionID = comments.questionID)
```

### Database / cache

- The database will store all the entities. We can use either a SQL or NoSQL database such as PostgreSQL vs DynamoDB here. The data does contain some relationships which can be more optimally managed using SQL. Also, because a lot of the entities will need to be joined together when returned to the client, DynamoDB may not be the most suitable because it doesn't directly provide support for joins - and implementing a scan / query to mimic a join will be more expensive. Thus, we'll use PostgreSQL here.

#### Top ranked answers cache

- Quora will have a higher read load than write load, thus it will be suitable to cache the highest ranked answers (which are also frequently accessed) in a Redis sorted set. The key can be associated to a specific questionID, while the members will be the answerID and additional answer related fields. The score of the sorted set could also be the rank of the answer, so that the top answers are always shown at the top of a specific question in the frontend UI.

#### Feed cache

- The Feed cache will store the generated feed / recommendations for users. The feed / recommendations will contain questions / answers for different topics the user might be interested in, and also include questions that need answers. The feed will be generated by the Recommendations service via ML logic like topic modeling and NLP.

- A feed entry for a userID may look as follows (TTL may be a small value like 2 mins - which is the amount of time we can tolerate for the feed to update):

```bash
userID: { posts: [ { questionID, question, createdAt } ], TTL }
```

- We can use Redis for the Feed cache, since we can benefit from Redis's support for complex data structures such as lists / sorted sets, which will further help in storing the feed in a sorted fashion using the createdAt or rank fields. We can store each user's feed as a list or sorted set (ZSET in Redis). The members in the sorted set will be the posts, and the scores will be the createdAt / rank field (or some other similarity field calculated by the Recommendation service).

### Search service

- The search service will search for questions, answers and comments via inverted index mappings built using the the database, most likely using both a creation (where entries are sorted based on createdAt - more appropriate for questions and comments) and rank (where entries are sorted based on the calculated rank - more appropriate for answers) inverted index using a Redis list and sorted set respectively. The design for the search service is similar to the SDI 'FB post search and Twitter search'.

### Blob store

- The blob store will contain the attachments uploaded by users. The Post service will provide pre-signed URLs to this blob store (S3), such that the user can upload the attachments.

### Kafka

- Two of our functional requirements is to rank answers, and to provide feed / recommendations to users. Because for both of these requirements, we'll need to collect data (the answers and activity from the user), we'll use Kafka between the Posts service and the Ranking and Recommendations service.

- The Posts service will contain a Kafka producer which will feed the created answerID into a "Ranking topic", which a Kafka consumer in the Ranking service will pull from. The Ranking service will then retrieve the answer for the answerID from the database, then assign a rank to it.

- Likewise, the Kafka producer will also feed the user's created questionID, answerID and commentID, or posts the user interacted with into the "Recommendation topic". A Kafka consumer in the Recommendations service will pull from this topic, and perform ML predictions (via topic modeling / NLP) on the user's created posts or user's activity. These ML predictions will essentially be similar questions, answers, comments, etc, which the user might be interested in. These recommendations will then be stored in the Feed cache by the Recommendation service.

- Because upvoting / downvoting on a single post can lead to race conditions, it may be helpful to instead push these upvotes / downvotes into a Kafka topic, where separate consumers can asynchronously consume from the topic and update the database without producing race conditions. Exactly-once delivery will also need to be achieved here via <a href="https://www.google.com/search?q=kafka+exactly+once+using+transction+API&sca_esv=988d71235c9faee3&source=hp&ei=gczsZ5etMPWbptQPwI7QkQo&iflsig=ACkRmUkAAAAAZ-zakec32YKD8lBaWGBLH9wG-sWgkISu&ved=0ahUKEwjX8Z2c0LiMAxX1jYkEHUAHNKIQ4dUDCBo&uact=5&oq=kafka+exactly+once+using+transction+API&gs_lp=Egdnd3Mtd2l6IidrYWZrYSBleGFjdGx5IG9uY2UgdXNpbmcgdHJhbnNjdGlvbiBBUEkyBxAhGKABGAoyBxAhGKABGAoyBxAhGKABGAoyBxAhGKABGApI5FBQAFjwTnACeACQAQCYAZkDoAGFGKoBCDI3LjQuNC0xuAEDyAEA-AEBmAIioAL5GMICCBAAGIAEGLEDwgIFEC4YgATCAgsQLhiABBixAxjUAsICBRAAGIAEwgIIEC4YgAQYsQPCAgcQABiABBgKwgILEAAYgAQYhgMYigXCAgYQABgWGB7CAggQABgWGAoYHsICBRAhGKABwgIFECEYnwXCAgUQABjvBcICCBAAGIAEGKIEmAMAkgcIMjguNS40LTGgB7OoAbIHCDI2LjUuNC0xuAf0GA&sclient=gws-wiz">Kafka's Transactional API<a/>
- In addition, we can also use sharded counters where different shards manage a subset of the upvote / downvote counters, and the upvote / downvote request could be routed to these different shards.

<br/>

- By using Kafka, we can separate synchronous operations from asynchronous operations such as ranking / recommendations. For this purpose, we'll use Kafka to disseminate jobs among different asynchronous services, where the services may be run via a cron job periodically.

### Ranking service

- The Ranking service will implement a Kafka consumer which will pull the posted answerIDs. The Ranking service will then retrieve the answers for the answerIDs and then assign a rank to them.
- The Ranking service can also be scheduled periodically via a cron job, where the ranks of answers with frequent activity (upvoting / downvoting) will be adjusted.

Note: We cannot use the number of upvotes as the only metric for ranking answers because a good number of answers can be jokes—and such answers also get a lot of upvotes. It is good to implement the Ranking service offline because good answers get upvotes and views over time. Also, the offline mode poses a lesser burden on the infrastructure.

### Recommendation service

- The Recommendation service will implement a Kafka consumer which will pull the user activity, and IDs of the created posts, and then retrieve the posts to find similarities between other posts via topic modeling / NLP. Topic modeling / NLP will generate groups of topics with similar questions, answers, comments (using a scheduled cron job). These similar posts can then be stored in the Feed cache for the user to retrieve them by requesting the Recommendation service.

#### Frequently online vs offline users

- It's also likely a lot of users don't frequently log-in, and thus we don't need to store their generated feed in the Feed cache. If a user hasn't logged in for a long time, the feed could be generated when they request for it, but if the user frequently logs in, the feed could be pre-generated and stored in the Feed cache. The Recommendation service could implement the logic to regularly pre-generate the feed for frequently online users.

<img width="1000" alt="image" src="https://github.com/user-attachments/assets/9d14e7d6-705c-478b-b0a4-99dee9537e06" />

## DD

### Separation of synchronous vs asynchronous operations

- Due to the variety of functionalities offered by Quora, different consistency types may be selected for different types of operations. For example, posting a question, answer, comment, should be done synchronously, because users need to receive an acknowledgement that their post has been created. Post creations are also less frequent, thus we can have them be synchronous operations end-to-end.

- Other operations like upvote / downvote updates, ranking, and recommendations may not need to be synchronous operations, because they'll take some time to process. It's not a goal for Quora to ensure that all users see the same consistent data for upvotes / downvotes, thus we can store the upvote and downvote requests in a "Votes topic" in Kafka, which will be produced to by a Kafka producer in the Posts service. A separate Votes service could then implement a Kafka consumer and update the upvotes / downvotes periodically in the database so that there are no race conditions. If we went with just allowing the Posts service to update the shared upvotes / downvotes field, then there may be some race conditions if locking or transactions are not used properly.

- Likewise, we can also have asynchronous operations for the Ranking and Recommendation service via Kafka as discussed in the HLD. The actual scheduling of these Votes, Ranking and Recommendation services could be done using a cron job which can run every 5 minutes or so, and will run the job for the services to update the database (upvotes / downvotes fields), rank field, and Feed cache as new entries come in for the past 5 minutes.

### Scaling Kafka for asynchronous operations

Because we're using Kafka to handle the asynchronous operations, we'll need to efficiently distribute the messages across Kafka partitions:

#### Partitioning Votes and Ranking topics by the questionID

- To distribute the messages to the Votes and Ranking topics, we'll set the message key as questionID to ensure that answers for a specific questionID are always routed to the same partition. This way, in particular the Ranking service's consumers in a consumer group can directly read answers belonging to the same questionID from a single partition. This means that a consumer doesn't need to read from multiple partitions when consuming answers for single questionID. Also, this means that the Ranking service will have an easier time to group the answers belonging to the same questionID, and thus understand how relevant those answers are to the question (so that it can assign a rank to the answers).

#### Partitioning Recommendation topic by a "topicTag"

- Because we want to group similar questions, answers and comments, we can use a "topicTag" field in the posts as the message key to ensure the posts for the same topicTag is published to the same partition. This way, the Recommendation service's consumer can read posts for a specific topicTag from a single partition. The output to the Recommendation service will then already be grouped by the topicTag, which will make finding similar posts easier.

### Handling uneven reads of posts

- Certain posts within the database may be read much more often (like questions, answers, comments from experts) than other posts. This will cause uneven reads of posts, which could also cause hot key problems. This issue can be solved by the below approaches, and in 'Handling uneven reads of posts' (taken from the SDI 'FB news feed'):
  - Post cache with large keyspace
  - Redundant post cache

### Handling large volume of writes

We have two types of writes - post creations and like events which we'll need to scale for:

#### Question / answer / comment creations

**Scalability of handling large volumes of post creation still needs to be addressed when it comes to updating the search service when new posts are created.**

- When a post is created, we'll need to tokenize the post and then write to likely both a creation and likes index within the Search service. If a post has 100 words, we might trigger 100+ writes one for each word (if we use bigrams of shingles, we'll have a lot more writes). With a large number of posts being created concurrently, the Search service may become a SPOF.

- To prevent the Search service from becomming a SPOF, we can easily horizontally scale the servers as this is a stateless service.

Kafka queues between Posts service and Search service servers:

- Also, to prevent Post creation data from being lost as it is waiting to be indexed via the search service, a Kafka queue can be positioned between the Posts service and the Search service's servers. Also Kafka can be configured such that it buffers messages so that the data is not lost within the queue. Buffering in Kafka will also handle bursts of messages being sent since the message data can be stored temporarily to prevent message loss during bursts.

- The Kafka messages could also be deleted periodically via a TTL of a few mins. The number of Kafka queues can be configured according to the number of Search service servers (or rather the Search service's indexing servers - which will perform the actual indexing), where if the number of workers in an Search service server grows, the number of queues will also grow.

Sharding the inverted index mappings:

- Lastly, we can shard the creation and likes indexes on the term, so that queries for a single term will only need to search through a single shard, and the search for multiple terms can be done in parallel by querying all the term's corresponding shards.

#### Likes

- Likes occur much more frequently than post creations (10x more frequently). We can reduce the number of writes we need to do for "like events" by doing the below, and in 'Reducing writes for like events' (taken from the SDI 'FB post search'):
  - Batch likes before writing to the database
  - Two stage architecture

### Feed generation workflow

The feed generation workflow will work as follows:

1. A user will post a question, answer or comment, or they will interact with other posts by upvoting or searching. The activity will be sent by the Posts service to the Recommendation Kafka topic, where messages into Kafka might look like:

```bash
{ topicTag: "soccer", userID, type: QUESTION_CREATION, questionID },
{ topicTag: "sports", userID, type: UPVOTE, answerID },
{ topicTag: "running", userID, type: SEARCH, searchQuery },
```

2. These messages will then be consumed by the Recommendation service's consumer via the message key topicTag. The Recommendation service will then run via the cron job, which will pull new messages and also fetch the corresponding questions, answers, comments, etc, from the database for the IDs in the messages.

3. The Recommendation service will feed the retrieved text data from the database into a topic modeling / NLP model (through an ML pipeline) which will preprocess, infer, then postprocess the predictions.

4. The predictions will be similar posts or content which the user will be interested in. These predictions will then be stored within the Feed cache, and may look like:

```bash
userID: { posts: [ { questionID, question, createdAt } ], TTL }
```

### Partitioning and sharding the database tables for fast reads

- Note that partitioning and sharding the database is not always required, however if we have 20k concurrent users per second, and we assume that only 10k users are concurrently writing to the database:
  - 10k writes / sec * (100k secs in a day) = 1B writes per day
  - 1B writes per day * (200 bytes for a single questions / answers / comments entry) = 200 GB of data to the DB every day
  - In our case, 200 GB / day may require sharding / partitioning of the database

#### Questions table

- The Questions table's primary key is the questionID. For faster lookups to get questionIDs pertaining to a topic, we can set an index on a "topicTag" field.

- Read latency is one of the non-functional requirements, thus the Questions table could also be sharded by the userID to support with even faster lookups. If we shard / partition the Questions table by userID, then we'll be able to quickly display questions asked by a specific userID.

#### Answers and Comments table

- Becuase we want to further improve the read latency when the user searches and retrieves answers and comments for a question, we'll need to shard the Answers and Comments table by the questionID. This way, all the answers and comments belonging to the same questionID will be in their own shard / partition - thus, we don't have to read from multiple shards when retrieving the answers and comments.

<br/>
<br/>

Additional deep dives:

### Fault tolerance of inverted index mappings in Search service's inverted index mappings cache

- To ensure fault tolerance of the inverted index mappings, we can replicate the inverted index mappings in the cache. Redis Cluster provides built-in asynchronous primary-secondary replication by default, which should be suitable here since write inconsistencies via a leaderless approach could have issues in the inverted index mappings (which requires low latency reads).

#### Keeping a reference to the indexServerID in the database tables to recover when inverted index mappings are down / erased

- If both the primary and secondary nodes for an inverted index mapping shard are down, then it would be really difficult to rebuild the shard's inverted index mappings again without knowing which terms were stored in this crashed shard.

- We can store a reference to the indexServerID for a questionID / answerID / commentID in the database tables. This will allow us to query the tables, and look for posts with the indexServerID that crashed. Afterwards, we can rebuild the index for those posts with the crashed indexServerID.

- However, maintaining this indexServerID field may have some overhead if we need to update the indexServerID during scaling events, but it ensures fast recovery time if the inverted index mappings are down / erased. Thus, this overall mapping between the indexServerID: [ questionID / answerID / commentID ] could instead be maintained in a service like ZooKeeper, which provides a KV store for maintaining server-side mappings like these.

### Reduce storage space of inverted index mappings

- Users are usually only interested on a small portion of posts, thus we can do the following optimizations:
  - Put limits on how many posts a single term in the inverted index will contain. We probably don't need all posts with "dog" in the post content - only about 1k - 10k posts for "dog" should be fine.
  - Ignore stopwords like "a", "of", etc (when updating the inverted index) which provide no value in searching.
  - In-frequently accessed terms and their creation / likes index mappings could instead be moved to a cold storage such as in S3 Standard-IA. If there are queries for these in-frequent terms, the query could first check the Redis inverted index mappings, and if results are not in Redis, it could instead be queried from S3 via Athena and returned to the client with a small increase in latency.



















