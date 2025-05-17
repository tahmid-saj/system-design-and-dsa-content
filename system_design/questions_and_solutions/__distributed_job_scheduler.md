# Distributed job scheduler

A job scheduler is a program that automatically schedules and executes jobs at specified times or intervals. It is used to automate repetitive tasks, run scheduled maintenance, or execute batch processes.

There are two key terms worth defining:

- Task:
  - A task is the abstract concept of work to be done. For example, "send an email". Tasks are reusable and can be executed multiple times by different jobs.

- Job:
  - A job is an instance of a task. It is made up of the task to be executed, the schedule for when the task should be executed, and parameters needed to execute the task. For example, if the task is "send an email" then a job could be "send an email to john@example.com at 10:00 AM Friday".

The main responsibility of a job scheduler is to take a set of jobs and execute them according to the schedule.

## Requirements

### Questions

- What is this job scheduler for?
  - Let's assume it's a generic job scheduler for simple tasks such as sending emails, notifications, making API calls, etc.

- In this system, users can schedule jobs and query the status of their jobs. Are we designing this?
  - Yes
 
- Will we keep track of the userID creating a specific job, and executing it?
  - Yes
    
- Can users cancel or reschedule jobs?
  - Yes, they can cancel jobs, but let's ignore rescheduling of jobs

### Functional

- Users should be able to schedule jobs to be executed immediately, at a future date or on a recurring schedule
- Users should be able to query the status of their jobs
- Users can cancel jobs

### Non-functional

- Availability > consistency:
  - Some jobs may be mission critical, and needs to be highly available
- Low latency:
  - The wait time for jobs should have low latency (< 5 seconds)
- The system should ensure at-least-once execution of jobs

## Data model / entities

- Tasks:
  - This entity represents a task to be executed. A job will be an instance of a task
    - taskID
    - taskDetails

- Jobs:
  - This entity represents a job, an instance of a task, which should be executed (at a given time or on a recurring basis), either using a cron expression or a specific date and time in the "schedule" field. A job will also have a jobType and parameters to be used when the job is executed

  - Note that a jobID and executionID will belong to a single userID, however a taskID is abstract in that it doesn't necessarily need to be created by a user

  - Depending on the jobType, the schedule field will be different for the job entry:
    - ONE_TIME_IMMEDIATELY / ONE_TIME_FUTURE:
      - The schedule field will have the type DATE, and an UNIX timestamp for the time field
    - RECURRING:
      - The schedule field will have the type CRON, and a cron expression for the time field

      <br/>
  
    - jobID
    - taskID, userID
    - jobType: ONE_TIME_IMMEDIATELY / ONE_TIME_FUTURE / RECURRING
    - schedule: { type: { CRON / DATE }, time }
    - parameters
 
- Executions:
  - The executions entity will represent an instance of a job to be run (or is running)
  
  - We'll use a Executions entity because there are 3 types of jobs: immediately executing jobs, jobs scheduled for the future, recurring jobs. Therefore, for all of these jobs, we'll have to execute them once or on a recurring basis which we need to track. If the design only had to support a one time immediately / future executing job, then we wouldn't need this Executions entity.
 
  - We'll also have a separate Executions entity because we need to separate a job from it's one time or recurring instance, which will have it's own status for those separate instances. For example there can be multiple running containers for a single Docker image.
 
  - We might also have both a timeBucket (UNIX timestamp) that is the time the execution should run at, and the actual startTime / endTime which the execution actually ran in. timeBucket will be discussed more in the HLD.

    - executionID
    - jobID, userID
    - executionStatus: NOT_QUEUED / QUEUED / RUNNING / COMPLETED / CANCELED / FAILED
    - timeBucket (partition key), startTime, endTime
    - retries

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Create a job

- We'll use this endpoint to create a job using an already defined task. This job will contain the taskID, jobType, schedule, and parameters fields. Therefore, this endpoint will create a job entry, and also an execution entry for the next occurence (if the job is a one time, then there will only be one occurence) of the job.

- If the jobType is ONE_TIME_IMMEDIATELY (immediately executing), then the schedule field will have a date time for the current time
- If the jobType is ONE_TIME_FUTURE (executing in the future), then the schedule field will have a a date time for the future time
- If the jobType is RECURRING, then the schedule field will have a cron expression

Request:
```bash
POST /jobs
{
  taskID,
  jobType,
  schedule: { type: { CRON / DATE }, time },
  parameters: { to: john@example.com, subject: Daily report }
}
```

### Cancel an execution

Request:
```bash
PATCH /jobs/:jobID/executions/:executionID?op={ CANCEL }
```

### Query jobs

- This endpoint will be used to query all the jobs created or a single jobID

Request:
```bash
GET /jobs (Query all the jobs)
GET /jobs/:jobID (Query a single jobID)
```

Response:
```bash
{
  jobs: [ { jobID, taskID, userID, jobType, schedule } ],
  nextCursor, limit
}
```

### Query executions

- This endpoint will be used to query all the executions for a jobID or a single executionID, and filter on the executionStatus, startTime, endTime. We can also perform cursor based pagination using the startTime, where nextCursor points to the viewport's oldest execution's startTime. This way, we'll query for the N executions (using limit) after the viewport's oldest execution's startTime

Request:
```bash
GET /jobs/:jobID/executions?status&startTime&endTime&nextCursor={ viewport's oldest execution's startTime }&limit (Query all execution)
GET /jobs/:jobID/executions/:executionID?status&startTime&endTime (Query an executionID)
```

Response:
```bash
{
  executions: [ { executionID, jobID, executionStatus, startTime, endTime } ],
  nextCursor, limit
}
```

## Workflow / data flow

The workflow of the system will be as follows:

1. A user creates a job by providing the taskID, jobType, schedule details and parameters to be used during an execution of the job.
2. The job and the next occurence's execution will then be persisted in the Jobs and Executions entity
3. At the timeBucket timestamp provided in the execution entry, the execution will be queued and then picked up by a worker (a separate process running the execution). If the execution fails, it is retried with exponential backoff
4. The executionStatus will then update in the Executions entity

## HLD

### Microservice architecture

- A microservice architecture is suitable for this system, as the system requires independent services such as creating jobs, querying executions, etc. These are all independent operations which could potentially be managed by separate services.

- Microservices can benefit from a gRPC communication as there will be multiple channels of requests	being sent / received in inter-service communication between microservices. Thus, gRPC could be the	communication style between microservices, as it supports a higher throughput, and is able to handle multiple channels of requests as opposed to REST, which uses HTTP, that is not optimized for		multi-channel communication between services.

### API gateway

- The API gateway will provide rate limiting, authentication, and route requests to the specific services. Depending on the request, its possible to forward a single request to multiple components, reject a request, or reply instantly using a cached response, all through the API gateway

### Scheduler service

#### Creating a job

- The Scheduler service will allow users to create a job (using taskID, jobType, schedule, parameters, etc) and next occurence's execution. The Scheduler service will then store the job and execution in the Jobs database.


#### Canceling an execution

- The Scheduler service will also allow users to cancel an execution of a job. The Job executor will likely maintain a mapping between the executionID : workerID, which will allow the Scheduler service to request the Job executor to stop cancel the executionID at the specific workerID. If the worker was a container, the container could either be stopped or killed via a docker command.

### Query service

- The Query service will allow users to query for the executions of all jobIDs belonging to a specific userID. DynamoDB allows us to set multiple GSIs within a table, therefore we can set a GSI on the Executions table, where the partition key is the userID and the sort key is startTime. This allows us to quickly find executions for a specific userID, and get the paginated results in sorted order by the startTime.

- GSIs add some write overhead and latency, but it's a worthwhile trade-off to support efficient queries if there are high read loads.

**This is a common pattern in DynamoDB (and similar NoSQL databases) where you maintain multiple access patterns through GSIs rather than denormalizing the data. The alternative in DynamoDB is to duplicate a specific field from the parent table to the child table, which would make the data model more complex and harder to maintain.**

### Jobs database / cache

- The Jobs database will store all the tasks, jobs, and executions so that we can recover executions if the workers running the executions crashes AND so that we can query the executions.

- The hard truth is that most modern databases will work for storing this kind of data. We don't require strong consistency where a SQL DB would be suitable. We also do have a few relationships, but nothing too complex. Either PostgreSQL or DynamoDB will work just as well with a few modifications such as indexing and partitioning to speed up queries.
- We'll use DynamoDB, because we could set a GSI on the Executions table with the partition key as the timeBucket UNIX timestamp rounded down to the nearest hour, and the sort key as the startTime. This way we'll have fast lookups when checking for due executions by only looking at the current hour's and next hour's timeBucket partition, then sorting based on the startTime. The Jobs table could also be partitioned by jobID to efficiently query the jobs by jobID. 

#### Partitioning using timeBucket

- By using timeBucket as our partition key, we achieve efficient querying while avoiding hot partition issues. For example, to find executions that need to run in the next few minutes, we only need to query the current hour's and possibly the next hour's timeBucket partition from the Executions table - we don't have to do a full table scan.

- Partitioning using timeBucket also ensures that executions are distributed across partitions, preventing hotspots.

#### Recurring executions

- Also, when a recurring execution completes, we can easily schedule its next occurence by calculating the timeBucket of the next occurence, then store the next execution entry in the Executions table. We keep creating the next occurence's execution entry right after a recurring execution completes.

**This pattern of separating the definition of something from its instances is common in system design. You'll see it in calendar systems (event definition vs. occurrences), notification systems (template vs. individual notifications), and many other places. It's a powerful way to handle recurring or templated behaviors. See the GoPuff Breakdown for another example of this.**

#### Cache

- Because the jobs and executions data will be frequently queried by both the Query service and the Job executor's cron job (the watcher), we can store the jobs and executions in a cache. Redis will be suitable, since we're sorting the data within partitions in DynamoDB (Jobs database) using the sort key as the startTime. We can use Redis sorted sets to sort a jobID's executions by setting the score as the startTime.
- A separate cron job could also place executions with timeBucket values within the next hour or so from the Jobs database to this Jobs cache, so that the Job executor's cron job query can directly fetch from this Jobs cache, which will be faster.

### Job executor

- The Job executor will allocate the executions to workers, which are processes each running with their own storage and memory allocated to run an execution. The Job executor can likely be an IO optimized EC2 instance since multiple requests will need to be made to the Jobs database and likely the message queue and workers.
- The Job executor (IO optimized EC2 instance) will run a cron job which will simply query the Executions table for executions which are due, where the timeBucket is within the next few minutes and the executionStatus is NOT_QUEUED. These executions which are due will then be pushed to a message queue, then the workers will pull and run the executions from the message queue.

- As the worker is running the execution, it will also update the executionStatus in the Executions table from NOT_QUEUED -> QUEUED -> RUNNING -> COMPLETED. If the execution was cancelled, then the worker will update the status to CANCELLED. If the execution failed, the worker will update the status to FAILED, then potentially create another execution entry in the Executions table by using exponential backoff and increasing the re-try time (visibility timeout) on every failure. If the execution has failed past a limit, then the executionStatus could be marked as DEAD - such that there won't be any future executions for the job.

<img width="1031" alt="image" src="https://github.com/user-attachments/assets/306d275b-9664-454d-9614-3deee6bfdf6b" />

## DD

### Ensuring workers run executions within 5s of their timeBucket timestamp

#### Bad approach - Job executor's cron job querying Executions table

- In the HLD, we're querying the Executions table every few minutes / seconds or so to find executions which are due. The frequency with which we decide to run our cron that queries for upcoming execution is naturally the upper bound of how often we can be executing jobs. If the Job executor ran a cron job every 2 minutes to check for executions which are due, then an execution could be run as much as 2 minutes early or late depending on when the cron job queries the Executions table.

- We could try running the Job executor's cron job more frequently, like 5 seconds, but this won't scale well for the below reasons:
  - If there are 10K executions due per second, then the cron job would need to query 50K executions in 5 seconds (10K executions * 5 secs = 50K), every 5 seconds, which is a bottleneck.
  - With indexing on the timeBucket and executionStatus, it would still not be safe to query that much data in 5 seconds, repeating every 5 seconds
  - After receiving the 10K executions which are due, the Job executor would still need to push them to the message queue which will take additional time and eat up the time from those 5 seconds
  - Running the cron job query every 5 seconds would put significant load on the database, and could potentially create a SPOF

#### Great approach - Querying the Executions table and using a message queue

- A better approach is to use a two-layered scheduler architecture with a watcher and a message queue:
  - Watcher (cron job) - querying the Executions table:
    - Just like in our HLD, the watcher is a cron job that will query the Executions table for jobs that are due in the next 5 mins or so, every 5 mins or so, which will leave some buffer for network and querying latency
  - Message queue:
    - The message queue will take the list of executions sent by the watcher, and order them by the timeBucket within the queue. Workers will then pull the executions from the queue in order and run the execution.

- The two-layered approach ensures the querying for due executions are separated from the queue and workers running the actual executions. By also running the query every 5 mins, we reduce the database load while maintaining precision through the message queue ordering.

#### Two-layered approach running executions which need to run in less than 5 mins, and ensuring execution is run at the timeBucket

- What happens if a new OR recurring execution needs to run in less than 5 mins?

For the new execution, we could try to put the new execution (created just now) happening within 5 mins directly into the message queue, but this introduces a new problem. Message queues like Kafka process messages in order, so any new execution would go to the end of the queue. This means if we have a 5 minute window of executions in the queue, the new execution would wait behind all of them before being processed - even if it's scheduled to run sooner.

For the recurring execution, the watcher would miss the second next occurence since only the next occurence of the execution within the next 5 mins would be created. ie, if a job's recurring execution happened every 2 mins, then within the 5 mins window, we would miss the second next occurence of the execution at the 4 min mark. We need to put those second, third, fourth, etc next occurences in the queue as well.

- Also, how can we ensure the execution is run at the timeBucket timestamp, where the execution is sent to the queue only when the timeBucket time comes up?

Instead of a log-based message queue like Kafka, we can use the different types of queues outlined below which acts as a priority queue based on the timeBucket value (execution time) ('Handling issue when recurring execution needs to be run in less than 5 mins'):
  - Redis sorted sets
  - RabbitMQ
  - Amazon SQS:
    - For our use case, SQS would be the best choice due to its native support for delayed message delivery (effectively making it a priority queue based on time), automatic handling of worker failures through visibility timeouts (if a worker fails during the visibility timeout, the message will be visible again and another worker can take over the message), and excellent scaling characteristics
    - With SQS, recurring executions which need to be run in less than 5 mins can just be added into SQS with the appropriate delay using the timeBucket value for the second next occurence. This way, the message is not visible until the delay ends

#### Two-layered approach workflow

Out two-layered approach would then look like this:

1. The watcher will query for due executions in the next 5 mins, every 5 mins
2. The watcher will send the due executions to SQS with appropriate delay values of timeBucket - current time
3. If a worker is free, they will pull the message from SQS
4. If a new job and execution is created all of a sudden with a timeBucket in the next 5 mins (the job just got created and needs to be executed within the next 5 mins), it could be sent directly to SQS with an appropriate delay

### Ensuring the system is scalable to support thousands of executions per second

We can scale the system by looking from left to right looking for any bottleneck and addressing them:

#### Job creation

- If the workers are running thousands of executions, there are likely a large number of jobs being created as well - likely thousands created per second. To handle the job creation rate, we can introduce a message queue like Kafka or SQS between the API gateway and Scheduler service. The queue acts as a buffer during traffic spikes, allowing the Scheduler service to process requests at a sustainable rate rather than being overwhelmed.
- The message queue also allows us to horizontally scale the Scheduler service servers to consume the job creation requests, while providing durability to ensure no request is dropped if the Scheduler service experiences issues.

**Adding a message queue between the API and Job Creation service is likely overcomplicating the design. The database should be able to handle the write throughput directly, and we'll always need some service in front of it that can scale horizontally. Unless there's expensive business logic in the Job Creation service that we want to isolate, it's better to keep the architecture simpler and just scale the service itself.**

**In an interview setting, while this pattern might impress some interviewers, it's worth noting that simpler solutions are often better. Focus on properly scaling your database and service layer before adding additional components. I'll leave it in the diagram but consider it optional.**

#### Jobs DB

- We could choose either DynamoDB or Cassandra for storing the tasks, jobs and executions depending on how many writes we'll need to support. If we have a much higher write load for jobs and executions, then we could move the jobs and executions data to Cassandra, and provision multiple leaderless replicas to support the write load.

- Also, we can move the older executions and jobs which had no executions for, let's say 1 year old, to a cheaper cold storage like S3.

#### Message queue capacity - two-layered approach

- SQS automatically handles scaling and message distribution across consumers. We don't necessarily need to worry about manual sharding or partitioning of the messages - AWS handles all of that for us under the hood. However, we'll likely need to request for quota increase since the default limit is receiving 3K messages per second with batching within a single queue.
- We might still want multiple queues, but only for functional separation (like different queues for different job priorities or types), not for scaling purposes.

**Even if you went with the Redis sorted set, 3 million jobs would easily fit in memory, so there's nothing to worry about there. You would just end up being more concerned with fault tolerance in case Redis goes down.**

#### Workers

- We can have the workers be either containers (using ECS or Kubernetes) or Lambda functions. These are the main choices which can be started up quickly, without much downtime:
  - Containers:
    - Contains tend to be more cost-effective if they're configured properly, and are better for long-running executions since they maintain state between executions inside volumes. However, they do require more operational overhead and don't scale as well as serverless options.
    - In this case, the containers will have code to pull the messages from the SQS queue
  - Lambda functions:
    - Lambda functions provide very minimal operational overhead. They're perfect for short-lived executions under 15 minutes, and can auto-scale instantly to match the workload. However, Lambda functions have a cold start-up time which could impact the <5 seconds requirement to run executions.
    - In this case, the Lambda functions will directly pull the messages from the SQS queue

- Because we have a hard limit on the <5 seconds requirement to run executions, containers may be more suitable. Containers also allow us to optimize the execution configuration such that we can have different types of containers catered to different executions (compute, memory, IO, network, etc optimized). We can also set up scaling policies within ECS to start up more containers - such as scaling the containers based on the SQS queue size.

- We could also use spot instances instead of containers to reduce costs by 70%.

### Ensuring at-least-once execution of jobs

- If a worker fails to process an execution, we want to ensure that the job is re-tried a few times before setting the status to DEAD. Executions can fail within a worker for the below reasons:
  - Visible failure:
    - The execution fails visibly in some way, likely due to a bug in the task code or incorrect input parameters.
  - Invisible failure:
    - The job fails invisibly, likely due to the worker crashing

#### Handling visible failures

- Handling visible failures is easier, and can be wrapped up in a try / catch block so that we can log the error and set the executionStatus to FAILED. The execution can then be re-tried a few times (and update the retries field for the execution entry) with exponential backoff by increasing the visibility timeout on each re-try as well if needed (SQS provides exponential backoff via it's visibility timeout), before being set to DEAD.

#### Handling invisible failures

- When a worker crashes or becomes unresponsive, we need a reliable way to detect this and retry the execution using the below approaches, and in 'Handling invisible failures':
  - Heartbeats / health check endpoints
  - SQS visibility timeout

#### Ensuring idempotent task code
 
- Lastly, we might also need to ensure that the task code is idempotent, in that running the same task code multiple times should have the same outcome as running it just once. We can do the following, and in 'Ensuring idempotent task code':
  - No idempotency controls
  - Deduplication table
  - Idempotent job design
 


