# Leetcode

## Requirements

### Questions

- Leetcode allows users to view problems, submit code against test cases for problems, get feedback on their code, and view a live leaderboard for competitions. Are we designing all of this?
  - Yes, all of these features are important. Also competitions should support 100k users

- Are we designing additional features, like authentication, payments, posting solutions, posting comments on problems, etc?
  - Let’s not focus on those features for simplicity, and focus on the core Leetcode			functionalities

- Should the questions be marked by their difficulty and tags, to help with filtering results?
  - Yes, both difficulty and tags for simplicity

- How many users can we expect?
  - Leetcode has around a few hundred thousands to 1M users, but DAU should be 100k

### Functional

- Users can view a list of coding problems, by the difficulty and tags
- Users can view a problem, code a solution and submit the code in multiple languages to a judge
- Users should get feedback on their submitted code within 5-10 secs
- Users can view a live leaderboard for competitions

<br/>

- Few hundred thousands to 1M users, and 100k DAU - thus it is a relatively small system

### Non-functional

- Availability > consistency / scalability (competitions should support 100k users)
- Code submission isolation / security
- Low latency:
  - Low latency in getting back code submission results should be supported

## Leetcode 101

### Code execution

- Note that it is a bad design to run the submitted code in the API servers. It might be a good		solution to run the code in a VM, but it is much safer to run the code in a Docker			container or a serverless function. The comparisons and approach for each solution is shown		in ‘Comparison of code execution’. We'll talk more about code execution in the HLD and DDD.

### Competitions

- Leetcode competitions can be 90 mins, have 10 problems, and have around 100k users. The	score for a user is determined by the number of problems solved in 90 mins, and to prevent ties, the score is also assigned using the time it took to solve the problems (starting from the		competition start time)

## Data model / entities

- Problems:
  - This entity will store the problem title, description, and any image URLs needed to render the		problem on the client side. Note that the sample test cases with the expected outputs will be		provided in the description field

  - The codeStubs field, which contains the boilerplate code for the starting function / class could	be generated manually, or generated via LLMs for each language

  - Note that the test cases could be nested inside the Problems table as the test cases will not		contain too much data based on the calculations - 1 kB at maximum. This nesting will		help to speed up queries, since we’ll only have to fetch from a single table, when querying		problems and their test cases.

	- problemID
	- title, description
	- s3ImageURLs
	- difficulty
	- tags
	- codeStubs: { python: string, javascript: string, go: string, etc }
  	- testCases: [ { testCaseID, testCaseInput: string, testCaseOutput: string } ]


- Submission:
  - This entity will store the user’s code submissions and the result of running the code against		the test cases

	- submissionID
	- userID
	- problemID
	- competitionID (If the problemID belongs to a competition)
	- submission: string
	- language
	- testCasesPassed: [ { testCaseID, testCaseInput: string, testCaseOutput: string } ], testCasesFailed: [ { testCaseID, testCaseInput: string, testCaseOutput: string, error } ]
	- acceptedSubmission: bool
	- submittedAt

- Leaderboard:
  - This entity will store the scores for users for competitions, and will help in generating the		leaderboard for competitions

    - userID
    - competitionID
    - score
    - acceptedSubmissions: [ problemIDs accepted ] 

## API design

- Note that we’ll use userID if the user is authenticated when sending submissions. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed entries quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Get problems
  
- We’ll use cursor based pagination, along with filtering based on the difficulty and additional		tags. The nextCursor will point to the viewport's largest problemID, to get back the next set of paginated results containing the problemIDs higher than the viewport's largest problemID. We'll do this since the problemID can easily be the actual problem number or contain the problem number

Request:
```bash
GET/problems?nextCursor={ viewport's largest problemID }&limit&difficulty&tags={ GRAPHS or STACK or ARRAY }
```

Response:
```bash
{
  problems: [ { problemID, title, difficulty, tags } ],
  nextCursor, limit
}
```

### Get problem

Request:
```bash
GET /problems/:problemID
```

Response:
```bash
{
  problemID,	
  title, description,
  s3ImageURLs,
  difficulty, tags,
  codeStubs
}
```

### Submit code for a problem
  
- This endpoint will accept the submitted code in a specific language for a problem, and return	a list of the test cases passed and failed, as well the test case input / output, and if the submission was accepted or not. The submitted code will be assessed against the test cases via	the API servers

Request:
```bash
POST /problems/:problemID/submit
{
	submission: string,
	language
}
```

Response:
```bash
{
  testCasesPassed: [ testCaseID: { testCaseInput, testCaseOutput } ],
  testCasesFailed: [ testCaseID: { testCaseInput, testCaseOutput, error } ],
  acceptedSubmission
}
```

### Get live leaderboard

- This endpoint will return a live leaderboard for a competition. The leaderboard will contain a		ranked list of users based on their performance for a competitionID

Request:
```bash
GET /competitions/:competitionID/leaderboard?nextCursor={ last score in viewport - since the score will be ranked in descending order on the viewport }&limit
```


## HLD

### Microservice vs monolithic

- Majority of large scale systems with multiple required services and entities may be better		managed using a microservice architecture. However, a monolithic architecture might be more	appropriate for Leetcode. The system is small enough that it can be managed in a single		codebase, and it will create more overhead to manage multiple services.

### Client

- The client side will need to support a code editor to allow clients to type their code. An editor	such as a Monaco editor will be suitable here, which is the editor powering VS code, and		which could be used on the browser.

### API servers

- We’ll have a few servers which will handle requests for getting problem(s), submitting the		code, returning the assessed results, and generating the live leaderboard. These servers		will communicate frequently with a database which will store all the problems, test cases,		submissions and leaderboard data.
- Because most of the operations will be communicating with a database, cache and likely multiple containers, we can use IO optimized EC2 instances here

### Database / cache

- The database will store the problems, submissions and leaderboard data. The		database will be indexed and partitioned on the respective IDs of the tables, for instance			problemID may be used to index / partition the Problems table.

- Either a SQL or NoSQL database could work here, however we won’t require complex		transactions or queries which SQL will provide. We may require unstructured data types to		store the test cases for binary trees, graphs, linked lists, etc, and store unstructured data for		the problem description, ie if it has multiple s3ImageURLs. Thus, a NoSQL database like DynamoDB will be suitable here, however a SQL DB can work just as well with some tweaks. DynamoDB also allows us to index and partition using both the primary key and secondary		values within a KV pair using LSIs and GSIs, which will speed up queries.

<br/>

#### Database estimations

The storage needed will also be pretty low:

- We’ll have 4k problems * 50 test cases = 200k rows of test cases + problems
- 200k * 1 kB for a single row of test cases + problem = 100 MB for all test cases + problems
- 100 MB * 1M users * 5 submissions per question on average = 500 TB of data for the	Submissions table (on the upper end - which is highly unlikely since this means that users solved all 4K problems - we'll have more like **250 TB** of data for the largest table (Submissions table))

#### Cache

- Also, we could store the frequently accessed problems and submissions in-memory via Memcached / Redis (in	the API servers or near them) as the space for 4k problems is small and can be cached easily. We could likely store the problem's and submissions' test cases within Redis lists.

#### Competition live leaderboard

- We can query the Leaderboard table to retrieve the scores for users for a		competitionID via SQL shown in ‘Querying for competition leaderboard’.
	
- Since the competition score is dependent on the number of accepted submissions, the score in the Leaderboard table will be updated when the user submits an accepted submission. To prevent ties, the score is also calculated using the time it took to solve the questions, therefore we’ll use the competition’s start / end time and the submissionAt field in the Submissions table to calculate the score for the users to prevent any ties.
- To also speed up querying, we can have a GSI on the Leaderboard table, and set the partition key as the competitionID, and the sort key as the score, such that paginated results from the Leaderboard table could be sorted by the score.

- Note that the clients will need to request the leaderboard again every 30 seconds or so, thus	they can poll the live leaderboard endpoint. However, it's inefficient for the API servers to get the leaderboard data from the Leaderboard table every 30 secs, which changes frequently during a competition. Although there are sort keys, DynamoDB tables are not			pre-optimized to store sorted data such as in a Redis sorted set. A Redis sorted set can easily		handle frequent reads and writes, and store the live leaderboard in a sorted set data structure.	Thus	the DynamoDB queries will not need to be performed - the Redis sorted set can be		updated by	adding or removing users and their scores (which can be re-calculated via the API	servers when a user submits a submission).
	
- Using a Redis sorted set, clients can poll the API servers for live leaderboard updates every		30 seconds (we can also reduce it to 10 secs since we have the data in-memory), and the API servers will return the top users via pagination from the Redis sorted set.

Querying for competition leaderboard:

```sql
select userID, score, acceptedSubmissions from leaderboardTable
where competitionID = ${competitionID}
order by score, numAcceptedSubmissions
```

#### Redis sorted set as live leaderboard

- Using sorted sets, the re-calculated score and acceptedSubmissions can be stored in-memory by the API servers, and the Leaderboard table can be updated from the API servers only when the client sends a NEW submission that passes. It's worth noting that the API servers will perform the score calculation whenever clients send accepted submissions - the API servers will use the Submissions and Leaderboard table to calculate the score using the acceptedSubmissions field in the sorted set, competition's start / end times, and the submittedAt field in the Submissions table.
	
An entry in a Redis sorted set for a competitionID might look like this:

```bash
{
  userID (key)
  score
  acceptedSubmissions: [ problem1, problem2, problem3 ]
}
```

The workflow when a client sends a new accepted submission in a competition is as follows:
1. Client sends the submission to the API servers
2. The API servers first check if the submitted code is for a new problem in the acceptedSubmissions list in the sorted set - so that it can let the containers know if the submission is for a new problem or not.
3. The API servers will then run the submission in the containers, and the containers will send the submission results to the API servers.
4. The API servers will update the sorted set, and the Problems and Leaderboard tables if the submission passes. Even if the submission is not for a new problem, if the submission still increases the score, the API servers will still update the sorted set accordingly.
5. Other clients can then poll the API servers and view the leaderboard with the updated scores

**We'll talk more about Redis sorted sets for the live leaderboard in the DD**

### Docker containers

- We can run the submitted code in isolated docker containers within the API servers or in a		separate environment. The containers will have the necessary dependencies and runtime		environments to run the submitted code for a specific language. 

- We could also use serverless functions, however it will have a cold start time, and low		latency is preferred for returning results of the submitted code.

- When a code is submitted to the API server, the code will be sent to the appropriate			container for the language specified. The isolated container will run the code against the test		cases in a sandboxed environment, and return the result to the API server. The API server will	store the submission results in the database, and return the results to the client.

<br/>

Below are the ways in which we can run the code:

Comparison of code execution:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/99dd93cb-3156-40b0-bdd0-f4b4ab59b954" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/d1f77e2e-e148-4a71-8194-78f04722cb0a" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/50d003f2-4e91-4279-ba43-67b0aa249390" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/d171e816-0a55-494c-b148-7978ab1c3aae" />

<br/>

<img width="750" alt="image" src="https://github.com/user-attachments/assets/6ca047e9-7e70-478e-8fb2-ff5c131a7511" />

## DD

### Supporting code submission isolation and security

We can set up the container using the following, to support isolation and security:

- Configure a read only file system:
  - To prevent users from writing to the system’s files, we can mount the directory of the system files			as read only and write any output within the container to a temporary directory that is deleted after			the completion

- Set CPU and memory limits:
  - To prevent users from consuming excessive resources, we can set CPU and memory limits on			the container. If these limits are exceeded, the container will be killed, preventing any resource			exhaustion.

- Add a timeout:
  - To prevent users from running infinite loops, we can wrap the submitted code in a timeout that			kills the container if it runs longer than a predefined time limit. This will also help us meet our requirement of returning submission results within a few seconds.

- Limit network access:
  - To prevent users from making network requests, we can disable network access in the container, ensuring that users can't make any external calls. If working within AWS, we can use Virtual Private Cloud (VPC) Security Groups and NACLs to restrict all outbound and inbound traffic except for predefined, essential connections.

- Restrict system calls (seccomp):
  - To prevent users from making system calls that would take control or access the host system, we			can use seccomp (a Linux kernel feature to restrict actions available within a container) to restrict			system calls that the container can make. We’ll need to predefine the system calls policy that				seccomp should use, and provide a reference to the file containing the policy when running the			container.

- Prevent running very large code sizes:
  - There could be a predefined validation in the API servers to limit the code sizes so			that a 100k LOC submission isn’t sent

### Efficiently fetching from live leaderboard

To efficiently fetch from the live leaderboard, we can do the following and in ‘Efficiently fetching from the live leaderboard’:

- Polling with database queries

- Caching with periodic updates:
  - Using this approach, we will still cache majority of the queries, but when there are cache misses,			the API servers will run the query on the database, which may still be expensive. To make sure			there are more cache hits using this approach, we could still use a cron job which runs every 10-20			secs or so and updates the cache. Thus, only the cron job will be running the expensive query on			the database, and clients will have reduced cache misses.

  - The issue with using a cron job is that if it is down, then the cache will not be updated, and it will			cause multiple cache misses OR a thundering herd due to the clients requesting the API servers to			run the expensive database query

  - If using another cache such as Memcached, it may cause race conditions if the same entry on			the cache is being updated by multiple processes, however Redis is single threaded, and thus will			likely not have this issue within a single instance

- Redis sorted set with periodic polling: 
  - There may be inconsistencies between the database and cache, thus we could add CDC			(change data capture). For different databases like DynamoDB, there is DynamoDB streams, and		for PostgreSQL, there is PostgreSQL CDC. CDC is used to capture updates on the database in		the form of WAL or another operations log, and replay any missed operations on other services. Usually CDC functionalities for various databases will store the operations in the WAL, and push		it to a queue such as Kafka - then there will be workers within the other service which will pull			operations from the queue and perform the operations on the other service
  - In		this case, we can use CDC to replay operations on the DynamoDB database to the cache using		DynamoDB streams to ensure the cache and database have the same consistent data

- Note that we could also use a websocket connection between the API servers and the clients, however this		may be an overkill, because we don’t require very strict low latency updates like 1 sec for the live			leaderboard. Also scaling up websocket connections may be more difficult than polling, as we’ll need a		separate service discovery component or an L4 load balancer managing the client to websocket server mappings and any sticky			sessions.


Efficiently fetching from the live leaderboard:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/d5e1c28a-6bce-4801-b146-f55688d3e78b" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/a44ce39d-b012-4e50-957e-14b8baec10af" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/7a420fec-d6be-4908-87db-e28c8e384fde" />


**The Redis Sorted Set with Periodic Polling solution strikes a good balance between real-time updates and system simplicity. It's more than adequate for our needs and can be easily scaled up if required in the future. If we find that the 5-second interval is too frequent, we can easily adjust it. We could even implement a progressive polling strategy where we poll more frequently (e.g., every 2 seconds) during the last few minutes of a competition and less frequently (e.g., every 10 seconds) at other times.**

### Scaling to support competitions with 100k users

- 100k is not a lot of users, and normally API servers would be able to scale up horizontally. However,		code execution is CPU intensive where some requests might take 10 seconds to handle, therefore the containers need to be scaled and managed properly. They		could be scaled using the below and in ‘Scaling containers during competition and spikes’:
	
  - Vertical scaling
  - Dynamic horizontal scaling
  - Horizontal scaling with queue:
    - The containers could be scaled horizontally via ECS auto scaling, if the containers are run via			ECS. Using SQS queues and workers (containers within API servers or EC2 instances), the				submissions sent to execute could be buffered within the queues.

    - When a user submits their code, the API server will add the submission to the queue and the			workers will pull the submissions off the queue, then run the submission on the container. Note that these workers are separate from the code execution containers - but these workers will just be containers which pull from the queue, then runs the code in the isolated containers.
    - The containers will run the submitted code			against the test cases and return the results to the workers to update both the database and cache. Note that it's safer for the container to send back the submission results to the workers, so that the workers can update the database, instead of the containers updating the database directly. This is because the code in the containers will then have access to update the database, which is not safe.

    - Because the API servers will not be able to return the results of the submission directly, as the			code submission design is now asynchronous with the introduction of a queue - traditionally				leaving a REST request for the code submission open for 10 seconds is too long. Thus the clients			will need to poll the API server for results of their submission. This is polled every second simply to			check and retrieve the submission results in the database. Leetcode actually implements this				polling per sec feature when we submit code. The polling endpoint could be as follows: GET /problems/:problemID/submissions/:submissionID

    - While the queue may seem like an overkill, it allows retries via SQS's visibility timeout, if a container crashed and the error was			not from the submitted code itself. Also, queues will further help in buffering the submitted code			and in parallel processing.

Scaling containers during competition and spikes:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/c59030f6-356f-4a7b-b760-0d923c912614" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/7fd078a5-7772-4be7-95c2-0febc5607c8a" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/0b4ec7b4-24e0-432a-b033-af75a41d6674" />

### Serialization and deserialization of test cases

How would you take the submitted code and run them against the test cases, for any language?
	
- We definitely don’t want to write a set of test cases for each problem in each language - we want to		instead write a single set of test cases per problem, which can be run against any language. We need a standard way to serialize / deserialize the test cases input and output, such that the test		cases become language agnostic. We can deserialize the test cases inputs / outputs for the specific		language (the serialization / deserialization process will be different for different languages - for example		deserializing [1, 2, 3] in Java will be a Java array, and a list in Python). Then we’ll compare against the		deserialized test case outputs and executed submission output, then return the serialized submitted		code’s outputs to the user.

<br/>

- The serialized value is what’s displayed on the UI and stored in the databases
- The deserialized value is the actual language-specific value, for example an ArrayList in Java, or list in		Python
- The serialization / deserialization process for the specific language / data structures / values / objects		can be stored in a pre-configured file within the container. The container will use this file to perform the		serialization / deserialization.

- Let’s say the language we’ll submit with is Java, then a deserialized array will be:

```java
int[] myArr = { 1, 2, 3, 4, 5 }
```

- The serialized array will be:
```bash
[ 1, 2, 3, 4, 5 ]
```

- An example of the serialization / deserialization process can be found in ‘Running test cases on a container using serialization / deserialization’

Running test cases on a container using serialization / deserialization:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/ec2b403a-21e1-4c7c-86b5-75d7b5e2e2c5" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/672efe31-d7a5-4c9c-a55a-91f39068ce40" />
