# Real-time gaming leaderboard

## Requirements

### Questions

- How is the score calculated for the leaderboard?
  - The user gets a point when they win a match. Let’s go with a simple point system where	each time a user wins a match, we add a point to their score

- Is there a time segment associated with the leaderboard?
  - Each month a new competition starts, a new leaderboard is created

- Can we assume we only care about the top 10 players?
  - For simplicity, let’s display the top 10 users - and if time permits, let’s discuss how to		return users who are 4 places above or below a specific user

- How many users are in a competition?
  - Average DAU is 5M in a competition
  - Average MAU (monthly active users) is 25M

- How many matches on average are played during a competition?
  - Let’s assume on average there are 10 matches in a competition

- What do we do if there is a tie between two users?
  - In this case, their ranks in the leaderboard are the same. If time permits, we can talk		about ways to break the ties

- Does the leaderboard need to be real-time?
  - Yes, it needs to be real-time, or as close as possible. We shouldn’t present a batched		history of results.

### Functional

- Display top 10 players on the leaderboard
- Show a user’s specific rank
- Display players who are 4 places above and below the selected user
- We may need a way to break ties

<br/>

- DAU is 5M in a competition, MAU is 25M
- 10 matches in a single competition

### Non-functional

- Low latency:
  - Real-time updates are displayed in the leaderboard
- Consistency of leaderboard:
  - We want the leaderboard to be sorted by the score accurately

### Data model / entities

- Leaderboard:
  - Note that this competition / leaderboard entity could either be maintained in a SQL database	or a Redis sorted set or a NoSQL database as we’ll discuss in the HLD / DD	

    - userID
    - score
    - rank (the rank field will likely not be explicitly in the table itself, but will be generated when we're querying for the top 10 players)


## API design

- Note that we’ll use userID if the user is authenticated to call endpoints requiring the user’s profile data. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- Update a user’s score and rank in leaderboard:
	- This endpoint will update a user’s score and rank on the leaderboard when a user wins a		match. Only the match servers should be able to call this endpoint on the Leaderboard service	- the client should not be able to directly update their score or the leaderboard

### Updating user's score

- We'll use this endpoint when we need to update the user's score, likely after they've won a match

Request:
```bash
POST /scores
{
   pointsGained (this will be the points gained from a match)
}
```

### Get top 10 players from the leaderboard

Request:
```bash
GET /scores
```

Response:
```bash
{
  topPlayers: [ { userName, rank, score } ]
}
```

### Get the rank of a specific user

- Note that we’ll use the encrypted userID provided in the header to retrieve the user’s score.

- If the encrypted userID is sent as a query parameter, it may be logged to a request		history database and will be visible. However, headers containing the user data isn’t		commonly logged or tracked in request histories, thus it is safer if an attacker has			access to the request history database. Also, if a user calls an endpoint with their			userID in the query parameter, such as /users/:userID, it doesn’t directly tell us if the		user is authenticated or not. However, headers are frequently used to verify				authentication of users, which will tell us if the user should be authenticated or not, as		opposed to /users/:userID.

Request:
```bash
GET /scores/user
Authorization: Bearer <JWT>
```

Response:
```bash
{
  userName, rank, score
}
```


## HLD

### Game service

- The Game service handles requests when a player wins a match. It will also perform validation to verify if the user		actually won the match, depending on the logic of the match. The Game service will then call the Leaderboard service	to update the player’s score and rank.

- We use the Game service to validate if the score and rank should change for a user, since the client should not be		able to directly update via the Leaderboard service. The score change request should be sent on the server-side so that the client cannot modify any of the score update requests.
	
- The Game service will also manage all operations during the competition, such as when clients win a match, lose a		match, play the game, etc.

- If after a user wins / loses a match, the Game service should notify other users via a notification service, or log it via a	logging service, etc, then we could add a message queue using Kafka, between the Game service and the additional		services (leaderboard / notification / log service). However, these additional services are not a requirement.

### Leaderboard service
	
- The Leaderboard service handles requests for getting / updating the leaderboard and the player’s score. Players can	request this service to get the top 10 players in the leaderboard and get the rank of a specific user in the leaderboard. The past competition data could also be stored in a separate Competition history database once the game ends

- Since our design will use a Redis sorted set to store the real-time leaderboard, clients can poll the Leaderboard service via the endpoint 'GET /scores' every few seconds, and the service will return the real-time leaderboard from the Redis sorted set. Polling for the real-time view may seem inefficient, however, it's more efficient than using websockets which is better suited for bidirectional communication.

- SSE could also be used, where the score update events from the Game service will send requests to the Leaderboard service, then the Leaderboard service will send the real-time leaderboard updates to the client after updating the sorted set - a cron job could be scheduled in the Leaderboard service to return the real-time leaderboard to the client every few seconds or so via SSE. SSE is more complex, and has more overhead in maintaining the connection, however, if users stay on the real-time leaderboard page for long periods then SSE might be more suitable because SSE generally takes up less bandwidth.

- Polling may be a more simpler solution, because the client will poll every few seconds, rather than receiving updates whenever scores update (which might occur frequently). The DD will discuss more on this, and offer some alternatives.

### Leaderboard database or cache

We could use different solutions to store the real-time leaderboard data such as:

#### SQL database solution

- If the number of users in a competition is not that much, we could use a SQL database for storing user’s		score per competitionID, and directly update that score for the user and competitionID. To return the leaderboard, we	could also retrieve the top 10 scores for a competitionID, and sort them based on the score field. 

- When a user wins / loses a point, we’ll insert	or update this table shown in ‘Updating user’s score in SQL leaderboard		table’. To get the leaderboard sorted by the score, we’ll use ‘Getting the leaderboard in SQL leaderboard table’
	
- The SQL database solution works when the dataset is small, but the query will become very slow with millions of		rows added on a monthly basis (25M new rows per month). There can also be ties, thus we’ll need to compare user’s	matches in a different way. 

- Additionally, the SQL database will change very frequently during a competition as new scores are being assigned. It	would also not be appropriate to use a cache + database to reduce latency since the data will be changing very			frequently, and there will be inconsistencies between the cache and database. However, we could still use a SQL		database if we could perform batch writes - but the system requires a real-time leaderboard,

- We could also index on the score and include a limit of 10, as in ‘Indexing + limit in SQL leaderboard table’, however,	indexing will only help with filtering, ie if we have ‘where’ or ‘having’ clauses, and since we still need to sort all the		scores, both index + limit will not help much.

<br/>

Updating user's score in SQL leaderboard table:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/cb914ac7-1764-4d47-a510-eff01ac36f42" />

<br/>
<br/>

Getting the leaderboard in SQL leaderboard table:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/6e15491e-7c63-4a6d-b12d-a443da47a615" />

<br/>
<br/>

Indexing + limit in SQL leaderboard table:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/0a61937e-089f-4cd7-8bab-16cf2e7e1480" />


#### Redis solution

- Redis provides an in-memory solution via a Redis sorted set, which is ideal for storing live leaderboards for frequent	reads and writes.
	
- A sorted set is a data structure similar to a set, but each element in the sorted set has a value which is used to keep	the elements in the set sorted. The values may repeat, however there can be keys which are unique in the set. A		sorted set is usually implemented by using a hash map and a skip list. A skip list is built on top of a LL, but has			different layers of the original LL, where each additional layer contains fewer elements from the original LL, but no new	elements. A skip list will be sorted on the score, and a single node will contain the score + userID. Also, the hash map will	store the KV pair of the score : userID.

- A skip list will allow for efficiently searching through the original LL sorted on the score, and containing the userID. An	overview of the skip list and it’s advantages is in ‘Skip list overview’.

- Sorted sets are much more efficient for storing and searching sorted data, because the elements are already			positioned in a sorted order, thus improving reads and writes, which are both O(logn) operations.
- We’ll use the Redis operations in ‘Redis sorted set operations’ to build the leaderboard.

<br/>

Skip list overview:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/984642b9-12d3-41de-a861-4ae0cd9cfd34" />

<br/>
<br/>

Redis sorted set operations:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/208d053d-ae94-4e6f-9c06-a05f912d978e" />

#### Redis sorted set workflow
	
##### Increasing user’s score
 
- Every month, a new leaderboard sorted set will be created, and the previous ones will be moved to a database.		When a user wins a match, we’ll increase their score or add the user if they weren’t in the sorted set using ZINCRBY.	The syntax for ZINCRBY is shown in ‘Increase score using ZINCRBY’

<br/>

Increase score using ZINCRBY:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/55a8028e-6401-4c8b-b5ab-dab5dcf7f54e" />


##### Getting top 10 players

- To fetch the top 10 players in sorted order, we’ll use ZREVRANGE (we’ll use rev since we want to reverse sort the scores in		descending order), and pass it 0, 9 and WITHSCORES to ensure that it returns the scores for the users as well, as		shown in ‘Getting top 10 players using ZREVRANGE’.

<br/>

Getting top 10 players using ZREVRANGE:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/4ef943e8-fd33-46e6-96db-16946a550fdb" />

##### Getting the player’s leaderboard position

- We’ll use ZREVRANK to get a user’s rank on the leaderboard as shown in ‘Getting a user’s rank on leaderboard		using ZREVRANK’.

<br/>

Getting a user’s rank on leaderboard using ZREVRANK:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/149891d9-3ac1-46b6-8451-c9e67a656195" />

##### Getting the 4 players above and below a user
   
- To get the 4 players above / below a user, we’ll first use ZREVRANK to get the player’s leaderboard position, then		use ZREVRANGE to get the 4 players above / below that player’s position as shown in ‘Getting the 4 players above / below a	user using ZREVRANGE’.

<br/>

Getting the 4 players above / below a user using ZREVRANGE

<img width="750" alt="image" src="https://github.com/user-attachments/assets/541708f3-760c-4e8e-bc76-3153308f1f1e" />

##### Redis sorted set storage estimation

If we have at max 25M users in a competition (we have average 25M per month), and we have about 50 bytes of		storage for a single leaderboard entry in the sorted set, then the total space needed for the sorted set will be:
- 25M * 50 bytes = 1250 MB or 1.25 GB of storage needed for a single leaderboard / sorted set
- Redis is definitely capable of handling this in-memory

- Also, if a single Redis sorted set is down, Redis provides both Redis sentinel (used for monitoring and managing		Redis primary-secondary instances) and Redis cluster (used for splitting datasets among multiple nodes). Also, Redis	provides built-in replication which could also be configured

### User profile DB / cache
  
- Since we may need to frequently fetch the user profile data via userID during a competition, we could store the		user profile in a User profile cache (also storing it in the User profile DB), which will be very infrequently changing.

<img width="824" alt="image" src="https://github.com/user-attachments/assets/36b0a4b8-de45-4089-b13b-5f8a4a290cad" />

## DD

### Efficiently fetching from live leaderboard

Note that in our design, we only use a DB to store completed competitions, and we'll store the entire live leaderboard in a Redis sorted set. However the SDI 'Leetcode' stores the leaderboard in both the DB (DynamoDB / PostgreSQL) and a Redis sorted set. We could still introduce a DB as discussed below, but we'll go with a Redis sorted set for efficiency.

<br/>

To efficiently fetch from the live leaderboard, we can do the following and in ‘Efficiently fetching from the live leaderboard’ (taken from the SDI 'Leetcode'):

- Polling with database queries

- Caching with periodic updates:
  - Using this approach, we will still cache majority of the queries, but when there are cache misses,			the API servers will run the query on the database, which may still be expensive. To make sure			there are more cache hits using this approach, we could still use a cron job which runs every 10-20			secs or so and updates the cache. Thus, only the cron job will be running the expensive query on			the database, and clients will have reduced cache misses.

  - The issue with using a cron job is that if it is down, then the cache will not be updated, and it will			cause multiple cache misses OR a thundering herd due to the clients requesting the API servers to			run the expensive database query

  - If using another cache such as Memcached, it may cause race conditions if the same entry on			the cache is being updated by multiple processes, however Redis is single threaded, and thus will			likely not have this issue within a single instance

- Redis sorted set with periodic polling: 
  - We're not using a DB with CDC, however, there may be inconsistencies between the database and cache, thus we could add CDC			(change data capture). For different databases like DynamoDB, there is DynamoDB streams, and		for PostgreSQL, there is PostgreSQL CDC. CDC is used to capture updates on the database in		the form of WAL or another operations log, and replay any missed operations on other services. Usually CDC functionalities for various databases will store the operations in the WAL, and push		it to a queue such as Kafka - then there will be workers within the other service which will pull			operations from the queue and perform the operations on the other service
  - In		this case, we can use CDC to replay operations on the DynamoDB database to the cache using		DynamoDB streams to ensure the cache and database have the same consistent data

- Note that we could also use a websocket connection between the API servers and the clients, however this		may be an overkill, because we don’t require very strict low latency updates like 1 sec for the live			leaderboard. Also scaling up websocket connections may be more difficult than polling, as we’ll need a		separate service discovery component or an L4 load balancer managing the client to websocket server mappings and any sticky			sessions.


Efficiently fetching from the live leaderboard:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/d5e1c28a-6bce-4801-b146-f55688d3e78b" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/a44ce39d-b012-4e50-957e-14b8baec10af" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/7a420fec-d6be-4908-87db-e28c8e384fde" />


**The Redis Sorted Set with Periodic Polling solution strikes a good balance between real-time updates and system simplicity. It's more than adequate for our needs and can be easily scaled up if required in the future. If we find that a 2-3-second interval is too frequent, we can easily adjust it. We could even implement a progressive polling strategy where we poll more frequently (e.g., every 1 second) during the last few minutes of a competition and less frequently (e.g., every 5 seconds) at other times.**

### Scaling Redis and the sorted set

- We can definitely handle 25M users or triple that amount in a single Redis cache, however if the amount is 500M users in a	single competition, then we’ll need to include sharding in the cache. Below are 2 solutions we can use:
	
#### Fixed partitioning using score range

- In fixed partitioning, a single shard could contain a score range that it manages, ie shard1 has the score range [0,			100]. However, we’ll need to make sure there is an even distribution of the scores across the shards. We could maintain		an additional cache (User score cache) which stores the userID : score mapping (score in this mapping will be the previous score if the score updates) to help us find the shard which the			score / user should belong to. Fixed partitioning is shown in ‘Redis fixed partitioning via score’

- When a user’s score updates, we’ll retrieve the previous score of the user from the User score cache, and use the			previous score to find the shard in which the user / previous score belongs to. Then we’ll update the user / previous			score in that shard, or move it to a different shard if the updated score belongs to a new shard.

- To get the top 10 players, we only need to retrieve the top 10 players from the shards with the highest scores. For example, there can be a shard for the range [900, 1000], and assuming the maximum obtainable score is 1000, then this shard will contain the top 10 players.
- To get the rank of a user, we’ll need to retrieve the user’s local rank in the shard, then add the total number of users in	all the other shards managing higher score ranges, so that we can get the user's overall rank taking into account of all the other users in the other higher score shards: userLocalShardRank + total number of users in all higher score		shards. This query is actually O(1) and the number of entries in a shard can be found using “info keyspace” in Redis. 

<br/>

Redis fixed partitioning via score:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/21cfa096-7fd3-444a-8342-5122d7a347b2" />

#### Hash partitioning via Redis cluster

- Redis provides Redis cluster which performs sharding across multiple Redis nodes. It doesn’t use consistent hashing		but a different form of sharding, where every key is part of a hash slot. There are 16384 configured hash slots, and we		can compute the hash slot a given key belongs to via CRC16(key) % 16384. This way, we can add / remove nodes in		the cluster without redistributing the keys. 

- In ‘Redis hash slot sharding’, there are 3 nodes / shards each maintaining a hash slot range. An update to the Redis	sorted set would change the score for the user in the shard via CRC16(key) % 16384. 

- However, for retrieving the top 10 players, we would need to retrieve the top 10 players from each shard, and then sort	all the players from the shards, then return the final top 10 players as shown in ‘Getting top 10 players from Redis		shards’. Since each shard has it’s own instance of Redis, the queries to retrieve the top 10 players in each shard can be	run in parallel.

- Getting the top 10 players from each shard has latency issues. If K in top K query is very high, retrieving K values from each	shard will be slow, and combined shard scores will need to be re-sorted. Also, we’ll have to wait for the slowest shard to	return the top K values. Also, we can’t retrieve the rank of a user directly when using Hash partitioning (it will be very slow to retrieve a specific user's rank because we have to query all the shards and find other users with higher scores than them - then return this number of users with higher scores than them).

- Thus, because retrieving the top K values will have high latency and no direct way to retrieve the user’s rank, we’ll go	with the Fixed partitioning solution.

<br/>

Redis hash slot sharding:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/ed575301-6f13-4786-b046-2002dd615bfe" />

<br/>
<br/>

Getting top 10 players from Redis shards

<img width="750" alt="image" src="https://github.com/user-attachments/assets/829b7e67-76de-4c34-91fc-3136e642d372" />


#### Sizing a Redis node

- Write-heavy workloads such as this will require us to write all the operations to a operations log and create snapshots.		Also, twice the dataset memory is usually required for write-heavy workloads.

- Redis also provides Redis-benchmark that allows us to view the performance of a Redis setup and nodes.

### Redis sorted set fault tolerance

- The Redis sorted sets will already be replicated, however we could also take the operations log produced from the SQL		database containing the competition history to re-create the leaderboard using Redis sorted set commands if any Redis instances are down (updates to the user’s score for the current competition could be logged to the		Competition history database).

### Breaking ties
  
- Tie breakers could be implemented by storing additional data such as how long it took for a user to win a match. A lower		“match win time” can be used as a tie breaker if two users have the same score. We could also break the tie based on whoever	received the score first.

### NoSQL leaderboard database solution

- For a NoSQL database, we’ll want fast writes + efficiency in sorting the items within the same partition by the user’s score

- Instead of a Redis sorted set, we could use a NoSQL database such as a KV store like DynamoDB, for efficient writes, and partitioning by both the primary keys and secondary indexes. A secondary index contains a selection of fields from	the original DynamoDB table, but will have a different primary key from the original table.

- We’ll assume we’re using AWS API gateway + Lambda + DynamoDB for this solution. The updated solution and it’s		workflow is in ‘NoSQL leaderboard database solution’

<br/>

NoSQL leaderboard database solution:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/00363d4a-433f-4412-96d3-298a463b3020" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/aa368707-871a-4c21-be67-64f33195a06c" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/e2ea068a-c5fa-43de-9db6-42536224f242" />

Additional deep dives:

### Whether or not to use cloud solutions

#### Managing our own services

- Using our own services, we’ll create a Redis sorted set for every competition, and store the userID and score. The 			other details such as user profile and past competition data could be stored in a separate User profile and Competition history database.		Since the servers in the Leaderboard service will need to fetch the user profile data during a competition, we could also		use a User profile cache which will change very infrequently.

#### Using cloud solutions

- If we use cloud solutions, we could potentially use AWS API gateway to route the API endpoints to a Lamda function.		The mapping between the endpoints and the Lambda functions is in ‘API endpoints to Lambda functions mapping’.

- We’ll use Lambda to perform the queries and updates on both Redis and any databases, and return the results back to		the API gateway, then to the client. Lambda also allows auto-scaling, however because we’ll require low latency reads		and writes, Lambda’s cold start times will not be appropriate. We could instead use IO optimized EC2 instances, since		we need to frequently update the Redis sorted set and database.

<br/>

API endpoints to Lambda functions mapping:

<img width="500" alt="image" src="https://github.com/user-attachments/assets/b9bf6040-93d6-42d1-86f2-0ad5ffc5d647" />




