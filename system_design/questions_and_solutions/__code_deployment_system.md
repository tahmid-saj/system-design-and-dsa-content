# Code deployment system

## Requirements

### Questions

- What are you referring to by a code-deployment system? Is the system building, testing and shipping code?
  - We want to design a system that takes code, builds it into a binary format with the compiled code,		and deploys the result globally in an efficient and scalable way. Let’s not worry about testing

- What part of the SDLC are we designing this for? Is this process of building and deploying code happening when code is submitted for code review, PR, merging to a branch, or when the code is being shipped to an external source?
  - Once code is merged into the trunk or main branch of a repository, engineers should be able to		trigger a build and deploy via a UI (which we’re not designing). At that point, the code has already		been reviewed and is ready to ship. We’re not designing the system that handles code being			submitted for review or being merged into a branch - just the system that takes merged code, builds	it, and deploys it.

- Are we trying to ship code to production by sending it to application servers around the world?
  - Yes, correct

- How many machines are we deploying to? Are they located all over the world?
  - We want this system to scale massively to hundreds of thousands of machines spread across		5-10 regions around the world.

- How fast should a single deployment take? Can we afford failures in the deployment process?
  - We want decent availability, and many errors from deployed code can be resolved by rolling			forward or back buggy code. For failure tolerance, any build should eventually reach a success or		failure state. Once a binary has been built, it should be shippable to all machines globally within 30		minutes.

- Do we want our system to be available, but not very highly available - we want a clear end-state for builds, and we want the entire build and deployment process to take roughly 30 minutes?
  - Yes, correct

- How often will we be building and deploying code? How long does it take to build code, and how big can the built binaries that we’ll be deploying get?
  - Some engineering teams deploy hundreds of services thousands of times per day.
  - Building can take up to 15 minutes.
  - The final binaries size can reach up to 10 GB.

  - The different types of applications we’re dealing with shouldn’t matter - let’s assume the			application type such as API, cron job, etc are agnostic to the system. The system assumes all		applications are the same type.

- When building code, how can we access the code, can we assume all code is on GitHub?
  - Yes, let’s assume we’ll be building code when commits are merged into a master branch. These		commits have SHA identifiers which can be used to download the code that needs to be built.

- Can users cancel or reschedule the build, as well as query the build status?
  - Yes

### Functional

- Download and build code once it is merged into a main branch in GitHub (using SHA ID)
- Assume the system deals with the same application type, ie API, cron job, JS files, C++ files, etc
- Build should run for about 15 minutes and reach a success / failure
- If build fails, roll forward or back to a successful build
- After build finishes, deploy binaries (size of 10 GB) to relevant application servers (in 5-10 regions). The total build and deploy time should take at most 30 minutes

- Users should be able to query the status of their builds
- Users can cancel builds

### Non-functional

- Availability:
  - Deployed code should be running on likely replicated application servers across 5-10 regions
- Code build isolation / security
- Throughput:
  - We’ll need to build and deploy hundreds of services thousands of times per day, and deploy code		to hundreds of thousands of machines across 5-10 regions

## Code deployment 101

This system can very simply be divided into two parts:

### The build system that builds code into binaries

- The process of building code into a binary is called a build, and we can design the build system as a		queue of builds. Builds will get added to the queue, and each build will use the SHA ID for what version of		the code it should build, along with the commit being the name for the build.

- Since the application and language type is agnostic, we’ll assume the build system supports all			types

- We’ll have a pool of servers (workers) that will handle these builds from the queue. Each worker will		repeatedly take builds off the queue in a FIFO manner with no priority unless specified. 

- The worker will build the binaries (we’re assuming the actual implementation details of building the	code are given to us), and write the binaries to a blob store such as S3.

### The deployment system that deploys binaries to machines across the world

- The deployment system will need to distribute 10 GB binaries to hundreds or thousands of machines		across the world. We’ll also likely need "Replication workers" that will replicate the binaries to the blob stores for host machines to download from in multiple regions, such that the deployment could be started. Once these Replication workers have finished the replication, the deployment can be triggered by the user.
	
- Since we’re going to deploy 10 GBs of binaries to hundreds of thousands of host machines, downloading		10 GB to a host machine from a blob store will be very slow. To speed up the downloads to the host		machines, a peer-to-peer network could be used, which contains the blob stores and relevant host			machines. We can setup different peer-to-peer networks within data centers of the 5-10 regions.
	
- Using a peer-to-peer network will allow us to hit the 30 min time frame for the build + deployment


## Data model / entities

- Builds:
  - The Builds table will contain the builds data, where each entry will represent a build that is queued, being built / deployed, failed, etc. The projectName will be the project which all the buildIDs are for
  - The build will change from QUEUED, BUILDING, DEPLOYING, to SUCCEEDED during the build and deployment processes

    - buildID
    - commitSHA, projectName
    - lastHeartbeat
    - buildDetails: { build type: cron job / JS / API / etc, environment variables, parameters }	
    - buildStatus: QUEUED / BUILDING / DEPLOYING / SUCCEEDED / FAILED
    - createdAt
    - retries

- Binary replication:
  - This table contains rows for a buildID's binary replicated to bucketIDs within a containerID. The replicationStatus of the buildID will also let us know about the replication status for the specific bucketID (in the containerID)

    - containerID
    - bucketID
    - buildID
    - replicationStatus: PENDING / REPLICATED / FAILED

- Configuration service KV store (ZooKeeper):
  - We want to replicate the binaries for the buildID to multiple different blob stores / host machines likely within P2P networks (for fast downloads of binary files). Therefore, we'll likely want to keep the following entries in a KV store such as ZooKeeper which specifies which P2P network has which current buildID.
    
    - p2pNetworkID
    - buildID
    - buildTimestamp


## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public


## Initiate a build

- We'll use this endpoint to initiate a build right after code is pushed to the main branch. We're assuming the projectName is connected to a GitHub repository, and that this endpoint will receive a commitSHA for initiating the build.

Request:

```bash
POST /projects/:projectName/builds
{
  commitSHA
}
```

## Cancel a build

Request:

```bash
PATCH /projects/:projectName/builds?op={ CANCEL }
```

## Query builds for projectName

- This endpoint will be used to query all the builds initiated for a projectName. Note that we'll set the nextCursor value to the viewport's oldest createdAt field for the buildID, so that buildIDs older than the viewport's oldest createdAt value will be returned in the next paginated result

Request:

```bash
GET /projects/:projectName/builds?nextCursor={ viewport's oldest createdAt field for buildID }&limit
```

Response:

```bash
{
  builds: [ { buildID, commitSHA, buildStatus, createdAt } ],
  nextCursor, limit
}
```

## Workflow

The build and deployment workflow will look as follows:

<br/>

Build process:

1. When a user initiates a build, the build will likely be put into a Build queue
2. Separate workers with the runtime and build logic will pull the build from the queue, and build the binaries using the GitHub codebase
3. These workers will then update the database and store the binaries in a blob store for the deployment process to start
4. These workers will also push the replication info to other "Replication workers" for the Replication workers to replicate the binaries to the other blob stores within other regions

<br/>

Deployment process:

1. The Replication workers will replicate the binaries to the other blob stores in the 5-10 regions
2. Once the replication is done, the buildStatus can be set to SUCCEEDED and the deployment trigger can be initiated. The replicated binaries could then be downloaded to the host machines running the actual binaries

## HLD

### Microservice architecture

- A microservice architecture is suitable for this system, as the system requires independent services such as initiating builds, querying builds, etc. These are all independent operations which could potentially be managed by separate services.

### API gateway

- The API gateway will provide rate limiting, authentication, and route requests to specific services. Depending on the request, its possible to forward a single request to multiple components, reject a request, or reply instantly using a cached response, all through the API gateway

<br/>

The system is broken down into the build and deployment parts:

<br/>

Build system:

### Build service

- The Build service will initiate requests for building the code from a Github commit. It will store a		build entry in the Builds table, and put the build in a QUEUED state, then enqueue the build into the Build queue.

#### Canceling a build

- The Build service will also allow users to cancel a build. The Build service itself will likely maintain a mapping between the buildID : workerID, which will allow the Build service to request the workerID to cancel the build process. The worker's (which is likely a container) isolated container (handling the actual build) could be stopped or killed via a docker command.

### Database / cache

- The database will store all the builds and binary replication data, so that we can recover any builds and binary replication data if the workers building the code crashes.

- The hard truth is that most modern databases will work for storing this kind of data. We don't require strong consistency where a SQL DB would be suitable. We also do have a few relationships, but nothing too complex. Either PostgreSQL or DynamoDB will work just as well with a few modifications such as indexing and partitioning to speed up queries.

- We'll use DynamoDB, because we could set a GSI on the Builds table with the partition key as the projectName, and the sort key as the createdAt time. This allows us to quickly find builds for a specific projectName, and get the paginated results in sorted order by the createdAt time.

- We could also further partition the binary replication table based on the projectName or buildID so that querying the binary replication entries for a specific project or buildID is fast.

#### Cache

- Because the builds and replication data will likely be frequently queried by both the Query service and the Build workers, we can also store recent builds and replication data updates in a cache. Redis will be suitable, since we can sort a project's buildIDs by their createdAt field in a Redis sorted set, where the score is createdAt.
- An appropriate TTL of about 15 mins or so could also be placed for cached entries, so that after a build process, the entries will be removed

#### Lost builds
  
- During a network partition within the Build workers or when an isolated container is down during the build process, we want	to avoid having a “lost build” in the 15 minutes duration. Since the worker / container is down or can’t communicate due	to a network partition, the builds the worker is processing will be forever in a BUILDING state.
	
- To fix the “lost build” and forever BUILDING issue, a lastHeartbeat column can be used in the Builds	table. The lastHeartbeat field will be updated via heartbeats, let’s say every 1 mins by the Build worker handling	the buildID

- We can also use a separate Monitoring service that polls the Builds table, let’s say every 1 minutes to check for BUILDING builds, and if their lastHeartbeat was not modified in the past 3 mins or so. If their lastHeartbeat	was not modified in the past 3 mins, this Build worker likely crashed or a network partition occurred. In this	case, the Monitoring service can reset the buildStatus to QUEUED, and re-enqueue the same	build with an appropriate visibility timeout and increment the retries field for the build entry.

### Query service

- The Query service will allow users to query the builds for a specific projectName. If we use DynamoDB for the database, DynamoDB allows us to set multiple GSIs within a table, therefore we can set a GSI on the Builds table, where the partition key is the projectName, and the sort key is createdAt. This allows us to quickly find builds for a specific projectName, and get the paginated results in sorted order by the createdAt time.

- GSIs add some write overhead and latency, but it's a worthwhile trade-off to support efficient queries, since we'll also have high read loads when constantly updating the buildStatus through the build process.

### Build queue

- The Build queue will contain the enqueued builds which can soon be built via the Build workers. The API servers will first enqueue the build to the queue, then Build workers will pull the build from the queue and build the code. Because we'll want exactly-once delivery, where one single Build worker works on building a single build, we can use SQS, since it provides a visibility timeout, which will also further support in re-trying the build process via exponential backoff. Additionally, the build can be queued by priority as well if needed using SQS's delayed message delivery feature. SQS also stores messages for at least 4 days, thus it is a highly persistent solution.

**Note that we could also use a persistent DB to hold the queue, however, coordinating between workers, and making sure that only one worker builds a specific build has it's overhead. Also, if we used a persistent DB as the queue, we'll need a separate "watcher" cron job which will keep querying the DB to look for builds in a QUEUED state. The frequency at which this watcher queries the DB will need to be very small, and querying hundreds of thousands of entries every second is not feasible**

### Build workers

- These workers are stateless containers which will continuously pull QUEUED builds from the Builds queue. After pulling the build, the workers will update the buildStatus in the Builds table to BUILDING, since the build process has now started.

#### Isolated containers for building code

- We can build the code in isolated docker containers within the Build service itself or in a separate environment. These isolated containers will have the necessary dependencies and build logic to build the code for a specific build type using the buildDetails field.
- We could also use serverless functions (Lambda has a max time limit of 15 mins, which is fine for us), however it will have a cold start time.
  
- The workers will pull the codebase for the build from Github, and build the code in an isolated container which will ensure safe code execution. It's also assumed that the containers building the code have the appropriate runtime and build logic for generating the binaries. Once the code is built in the isolated containers, the built binaries will be sent back to the workers. The Build workers will then set the buildStatus as DEPLOYING, and store the binaries to the blob store for the deployment process to use. It will also add entries in the Binary replications table for this buildID, and set the replicationStatus to PENDING. Lastly, the Build worker will enqueue the new Binary replication entries (the containerIDs and bucketIDs which the buildID should replicate the binaries to) to the Replication queue.

- Note that the Build workers are separate from the isolated containers - the Build workers will just be containers which pull from the queue, then build the code in the isolated containers to ensure safe code execution.

Below are the ways in which we can build the code / run the code (taken from the SDI 'Leetcode'):

<img width="750" alt="image" src="https://github.com/user-attachments/assets/99dd93cb-3156-40b0-bdd0-f4b4ab59b954" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/d1f77e2e-e148-4a71-8194-78f04722cb0a" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/50d003f2-4e91-4279-ba43-67b0aa249390" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/d171e816-0a55-494c-b148-7978ab1c3aae" />

- If the build was cancelled, then the Build worker will update the status to CANCELLED. If the build failed, the Build worker will update the status to FAILED, then potentially re-enqueue the build by using exponential backoff with an appropriate visibility timeout, and increment the retries field for the buildID. If the build has failed past a limit, then the buildStatus could be marked as DEAD - such that there won't be any future re-tries.

#### Scaling build workers

- Multiple VM based cloud services such as EC2, Azure VMs, GCP Compute Engine, etc could be used as the Build workers. Since	the Build workers will frequently read and write to the Builds table, we might prefer an IO optimized EC2 instance. 

- Build workers can also be easily horizontally scaled by adding or removing containers, or vertically scalled by adding more CPU to the servers which are running the containers. We’ll also prefer a VM based instance like EC2 in which we can manage the infrastructure instead of a serverless service such as	AWS Lambda which has a cold start latency. Based on the load, we could have roughly 50 - 100 workers, with a single EC2 instance containing multiple workers and isolated containers.

### Blob store

- When a Build worker completes a build, it will store the binaries in the primary blob store before updating the buildStatus in	the Builds table to DEPLOYING, and setting the replicationStatus to PENDING. Since the system will have machines across the world, it would make		sense to push the binaries to multiple blob stores in separate regions close to the regional machines.

- We can follow a primary-secondary replication approach where the Build worker synchronously pushes the binaries to a primary blob store, and the Replication workers using the Replication queue will asynchronously replicate to the other blob stores within separate regions. Given 5-10 regions and 10 GB for the build files, the build + replication should take no more than 20-25 mins (15 mins of build, and 5-10 mins for replication)

<br/>

Deployment system:

### Replication queue

- The Replication queue will contain the Binary replication entries which the Build workers enqueued after the build process ended. We could also use SQS here, as it provides visibility timeouts, exactly-once delivery, delayed message delivery, etc - features which will be helpful for Replication workers pulling the messages.

### Replication workers

- The Replication workers will pull the Binary replication entries from the Replication queue and replicate the primary blob store's binaries to the replica blob stores in 5-10 other regions. As the worker is replicating, it can update the Binary replication table's replicationStatus to REPLICATED.
- Once the replicationStatus for a binary is REPLICATED, that binary is then deployable within the blob store’s region or network. After all the replicationStatus fields for the buildID entries is set to REPLICATED, the buildID is set to SUCCEEDED by the Replication worker - the build is considered deployable.

- The infrastructure of the Replication workers will be similar to that of the Build workers, but they'll perform completely different things, and it's better to separate them out since the Build workers will need to maintain secure code builds and isolation from other workloads like binary replication, which the codebase could potentially access.

### Peer-to-peer network and host machines

- Since we’re going to deploy 10 GBs of binaries to hundreds of thousands of machines, downloading		10 GB to a host machine from a blob store will be very slow. To speed up the downloads to the host		machines, a peer-to-peer network could be used, which contains the blob stores and relevant host			machines. We can setup different peer-to-peer networks within data centers of the 5-10 regions.
		
- Using a peer-to-peer network will allow us to hit the 30 min time frame for the build + deploy. Also, a P2P	is usually the go-to solution for servers communicating large files. It's also good to incorporate chunking as discussed in the SDI 'Dropbox'.

### Deployment trigger

- Via the UI, the user could press the “deploy <buildID>” button after the binaries have been			replicated to the blob stores and the buildID is showing as SUCCEEDED. This is the action that triggers the binary downloads from the blob stores to the host machines		within the peer-to-peer networks.

### ZooKeeper containing P2P's and global buildID

- To maintain the currently deployed buildID, we can maintain the current buildID within a	peer-to-peer network by using a KV store for configuration such as a ZooKeeper instance per P2P. The current		buildID for different P2P can differ, thus we’ll use ZooKeeper to track the current buildID - the		build the P2P is running.

- We’ll also maintain a global KV store using ZooKeeper which maintains the current global buildID.		The “deploy buildID” trigger will be sent to the global KV store to update the global buildID.

- P2P KV stores will continuously poll the global KV store for changes in the global buildID, let’s say	every 30 secs. If the global buildID changes or is different from the P2P’s current buildID, the		P2P KV store’s buildID will change to the global buildID, and it will download the binaries from	the P2P's blob stores to the host machines within the P2P.

- Additionally, there can be individual API servers within the P2P networks and with the global KV store to	allow the P2P networks to poll the global KV store. These API servers can be servers or VM instances		within the P2P network which implements the polling functionality.

- Using this overall process, the deployment trigger will complete the deployment on the P2Ps.

<img width="1200" alt="image" src="https://github.com/user-attachments/assets/113ccc61-f7a8-419a-b031-77b735ca8192" />

## DD

### Supporting code building isolation and security

We can set up the isolated containers building the code using the following, to support isolation and security:

- Configure a read only file system:
  - To prevent users from writing to the system’s files, we can mount the directory of the system files			as read only and write any output within the container to a temporary directory that is deleted after			the completion

- Set CPU and memory limits:
  - To prevent users from consuming excessive resources, we can set CPU and memory limits on			the container. If these limits are exceeded, the container will be killed, preventing any resource			exhaustion.

- Add a timeout:
  - To prevent users from running infinite loops, we can wrap the submitted code in a timeout that			kills the container if it runs longer than a predefined time limit. This will also help us meet our requirement of building within 15 mins.

- Limit network access:
  - To prevent users from making network requests, we can disable network access in the container, ensuring that users can't make any external calls. If working within AWS, we can use Virtual Private Cloud (VPC) Security Groups and NACLs to restrict all outbound and inbound traffic except for predefined, essential connections.

- Restrict system calls (seccomp):
  - To prevent users from making system calls that would take control or access the host system, we			can use seccomp (a Linux kernel feature to restrict actions available within a container) to restrict			system calls that the container can make. We’ll need to predefine the system calls policy that				seccomp should use, and provide a reference to the file containing the policy when running the			container.

- Prevent running very large code sizes:
  - There could be a predefined validation in the Build service to limit the code sizes if necessary

### Updating users about the build and deployment process status

- Because the Query service cannot return the build and deployment process status to the user directly since these processes are asynchronous, it likely that the client will need to poll every 30 secs or so to retrieve the build and deployment updates. The client can likely poll the Query service, which will return the buildStatus and the replicationStatus for the different binaries replicated to the blob store. This simple polling approach will ensure a good user experience, and inform the client about any updates.


### Ensuring the system is scalable to support hundreds of thousands of builds

We can scale the system by looking from left to right looking for any bottleneck and addressing them:

#### Build initiation

- Since there are hundreds of thousands of builds - to handle the build creation rate, we can introduce a message queue like Kafka or SQS between the API gateway and Build service. The queue acts as a buffer during traffic spikes, allowing the Build service to process requests at a sustainable rate rather than being overwhelmed.
- The message queue also allows us to horizontally scale the Build service servers to consume the Build initiation requests, while providing durability to ensure no request is dropped if the Build service experiences issues.

**Adding a message queue between the API and Build service is likely overcomplicating the design. The database should be able to handle the write throughput directly, and we'll always need some service in front of it that can scale horizontally. Unless there's expensive business logic in the Build service that we want to isolate, it's better to keep the architecture simpler and just scale the service itself.**

**In an interview setting, while this pattern might impress some interviewers, it's worth noting that simpler solutions are often better. Focus on properly scaling your database and service layer before adding additional components. I'll leave it in the diagram but consider it optional.**

#### Database

- We could choose either DynamoDB or Cassandra for storing the builds and binary replication data depending on how many writes we'll need to support. If we have a much higher write load for builds and binary replication entries, then we could move the data to Cassandra, and provision multiple leaderless replicas to support the write load.

- Also, we can move the older ebuilds and binary replication data to a cheaper storage like S3.

#### Message queue capacity

- SQS automatically handles scaling and message distribution across consumers. We don't necessarily need to worry about manual sharding or partitioning of the messages - AWS handles all of that for us under the hood. However, we'll likely need to request for quota increase since the default limit is receiving 3K messages per second with batching within a single queue.
- We might still want multiple queues, but only for functional separation (like different queues for different build types or priorities), not for scaling purposes.

**Even if you went with an in-memory queue with a Redis sorted set as the Build / Replication queue, 3 million jobs would easily fit in memory, so there's nothing to worry about there. You would just end up being more concerned with fault tolerance in case Redis goes down.**

#### Build / Replication Workers

- We can have the workers be either containers (using ECS or Kubernetes) or Lambda functions. These are the main choices which can be started up quickly, without much downtime:
  - Containers:
    - Contains tend to be more cost-effective if they're configured properly, and are better for long-running builds since they maintain state between builds inside volumes. However, they do require more operational overhead and don't scale as well as serverless options.
    - In this case, the containers will have code to pull the messages from the SQS queue
  - Lambda functions:
    - Lambda functions provide very minimal operational overhead. They're perfect for short-lived builds under 15 minutes, and can auto-scale instantly to match the workload. However, Lambda functions have a cold start-up time which could impact any latency requirements.
    - In this case, the Lambda functions will directly pull the messages from the SQS queue

- We went with using a container mainly due to more flexibility in ensuring the build isolation and security. Containers also allow us to optimize the configuration such that we can have different types of containers catered to different build types (compute, memory, IO, network, etc optimized). We can also set up scaling policies within ECS to start up more containers - such as scaling the containers based on the SQS queue size.

- We could also use spot instances instead of containers to reduce costs by 70%.

### Ensuring at-least-once processing of builds

- If a worker fails to process a build, we want to ensure that the build is re-tried a few times before setting the status to DEAD. Builds can fail within a worker for the below reasons:
  - Visible failure:
    - The build fails visibly in some way, likely due to a bug in the codebase or incorrect input parameters in the buildDetails field.
  - Invisible failure:
    - The build fails invisibly, likely due to the Build / Replication worker crashing

#### Handling visible failures

- Handling visible failures is easier, and can be wrapped up in a try / catch block so that we can log the error and set the buildStatus to FAILED. The build can then be re-tried a few times (and update the retries field for the build entry) with exponential backoff by increasing the visibility timeout on each re-try as well if needed (SQS provides exponential backoff via it's visibility timeout), before being set to DEAD.

#### Handling invisible failures

- When a worker crashes or becomes unresponsive, we need a reliable way to detect this and retry the build using the below approaches, and in 'Handling invisible failures' (taken from the SDI 'Distributed job scheduler'):
  - Health check endpoints
  - Job leasing
  - SQS visibility timeout


 
