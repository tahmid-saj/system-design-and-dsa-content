# Todo list app

## Requirements

### Questions

- What features should we design?
  - Task creation / modification, tasks can have sub-tasks, task notification, searching tasks, assigning tasks, viewing a task

- Do we also want to include recurring tasks?
  - Yes, also include recurring tasks

### Functional

- Task management (also allow task assignment to users)
- Tasks can have a hierarchical relationship with sub-tasks
- Users will get notification of tasks coming up
- Searching tasks
- Viewing a task

- The system should support recurring tasks

### Non-functional

- Low latency:
  - Searching tasks should be done in (10 - 500 ms)
- We want to efficiently store the tasks and sub-tasks

## Data model / entities

- User:
	- userID
	- userName
	- userEmail

- Tasks:
  - This entity will represent a single task. The task could also be a sub-task
  - Note that this entity represents the task itself, not its upcoming instances which are due. A task could be non-recurring, and in this case there will only be one instance of the task in the Task instances entity. However, if a task is recurring, then the recurring instances of the task will be in the Task instances table. We need to go by this data model because we're supporting recurring tasks - if we didn't need to support recurring tasks, then only this "tasks" entity could be used to store all the tasks, instead of having a Task instances entity as well.
  - Depending on if the task is non-recurring / recurring, it's schedule will either be a timestamp (non-recurring) or a cron expression (recurring)

    - taskID
    - creatorID, assigneeID
    - title, description
    - parentTaskID
    - subtasks: [ taskIDs ]
    - taskType: ROOT / SUBTASK
    - recurring? TRUE / FALSE
    - schedule:  timestamp OR cron expression

- Task instances:
  - This entity will store instances of a task. If a task is non-recurring, then the next instance of the task will be stored here once the task is created. If a task is recurring, then when the task is created, an entry in this entity will also be created for the next due task instance for this recurring task. Everytime a user completed a recurring task instance, the next recurring task instance will be created and stored in this entity. This is actually similar to how Microsoft to-do's UI works when tasks are completed.
  - We will still need to persist all the tasks, regardless if they're completed, overdue, due, non-recurring, recurring, etc, so that's why we'll put all of the task instances in here.
    
  	- taskInstanceID
  	- taskID
	- taskStatus: PENDING / COMPLETED
	- subtaskInstances: [ taskInstanceIDs ] (these are the taskInstanceIDs also created for all the sub-tasks, when we provide the taskIDs in the subtasks field when creating a task)
  	- dueTime


## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed messages quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Create task

- When a task is created, it's next task instance will also be created in the Task instances entity. If this created task has subtasks specified, then the subtaskIDs will also need exist, and for the all the taskIDs of the subtasks field of the request body, we'll also create the next task instances for them as well. The dueTimes of the subtasks' taskIDs will need to be prior to the time / schedule of the parent taskID. This is because a user will need to complete all the sub-tasks before completing the parent task.

Request:
```bash
POST /tasks
{
  title
  description
  assigneeID
  parentTaskID
  subtasks: [ taskIDs ]
  recurring?: TRUE or FALSE
  schedule
}
```

### Get task instances
  
- The nextCursor could point to the viewport's oldest dueTime of the task instance. This way, we can return the next paginated results which are task instances due after the viewport's oldest dueTime. The user could also specify if they want to get back ROOT or SUBTASKS, and if they want to see OVERDUE or COMPLETED or DUE task instances.
  - OVERDUE: these are PENDING task instances where the dueTime has passed
  - COMPLETED: these are COMPLETED task instances regardless if the dueTime passed or not
  - DUE: these are PENDING task instances with a dueTime in the future

- The taskStatus field will either be PENDING / COMPLETED. If the taskStatus is PENDING, it will be determined during search-time if the task is OVERDUE or DUE using the task instance's dueTime

Request:
```bash
GET /task-instances?query&nextCursor={ viewport's oldest dueTime time for task instance }&limit&filter={ ROOT or SUBTASK & OVERDUE or COMPLETED or DUE}
```

Response:
```bash
{
  tasks: [ { taskInstanceID, assigneeID, title, taskStatus, subtaskInstances, dueTime } ]
}
```

### Get task instance

Request:
```bash
GET /task-instances/:taskInstanceID
```

Response:
```bash
{
  taskInstanceID
  creatorID
  assigneeID
  title, description
  taskStatus
  subtaskInstances: [ taskInstanceIDs ]
  dueTime
}
```

### Update task

Response:
```bash
PATCH /tasks/:taskID
{
  title
  description
  assigneeID
  parentTaskID
  subTasks: [ taskIDs ]
  recurring?: TRUE or FALSE
  schedule
}
```

### Complete a task instance

Response:
```bash
PATCH /task-instances/:taskInstanceID?op={ COMPLETED }
```

**Note how the endpoints either have a /tasks or /task-instances endpoint for the Tasks and Task instances entities respectively**

## HLD

### Microservice vs monolithic

- Majority of large scale systems with multiple required services and entities may be better managed using a microservice architecture. However, a monolithic architecture might be more appropriate for a todo list app. The system is small enough that it can be managed in a single codebase, and it will create more overhead to manage multiple services.

### API servers

- The API servers will handle CRUD based operations for creating a task, updating a task, searching task instances and viewing a task instance. The API servers can also be used to complete a task instance. If the task instance belongs to a recurring task, then the next task instance can be created and placed in the Task instances entity.

- When the API server is also returning a specific taskInstanceID, and potentially it's taskInstanceIDs of the subtaskInstances field, the taskInstanceIDs will ultimately be what's used to also view a task instance via /task-instances/:taskInstanceID

### Databases / cache

- The database will store the users profile, tasks, and task instances data. Either a SQL or NoSQL database will work here with tweaks such as indexing and partitioning made within the database. We'll use DynamoDB here, where we can set GSIs on the tasks and task instances data. The partition key can be the hour part of the schedule and dueTime fields respectively, and the sort key can be the full schedule and dueTime fields respectively. This way, when we are returning paginated results of both upcoming tasks and task instances, we'll only look at a specific partition containing the tasks and task instances for the current hour (we can also see previous tasks as well by querying the previous hour's partition). We'll also get back the entries in a sorted order by the task instances' schedule and dueTime fields.

#### Redis sorted set to store tasks / task instances & upcoming task instances

- Because the tasks, task instances and upcoming task instances might be frequently accessed, we can use Redis sorted sets to sort the entries by their respective time based fields

- Redis sorted sets can be used to store the frequently accessed tasks and task instances by their schedule and dueTime fields respectively. Also, we can store the upcoming task instances and their dueTimes in sorted sets, let's say for the next 12 hours or so. In total, we'll store 3 different types of entries in sorted sets:
  - Frequently accessed taskIDs, with the score being the schedule field (we can convert the cron expression to an exact timestamp)
  - Frequently accessed taskInstanceIDs, with the score being the dueTime field
  - Upcoming taskInstanceIDs, with the score being the dueTime field

- A separate cron job could also place task instances with dueTime values within the next hour or so from the Task instances table to the Redis sorted set, so that the client can query upcoming tasks directly from this Redis sorted set
 
### Search service

- If we want to incorporate a sophisticated search service to return tasks from a large number of entries, then we can use build an inverted index mappings within a tool like Lucene or Elasticsearch:
  - Inverted index mappings contain a mapping as follows: term : { [ docIDs ], [ termFreqs in docs ], [ [ docLocations ], [ docLocations ] ] }
  - The structure of an inverted index mapping allows us to only look for the terms / keywords, and return the relevant docIDs sorted by the termFreqs (frequency of term in document) or any other values like date contained in the mapping.
  - To ensure we get fast results, we could store these mappings in Redis, as Redis provides functionality for complex data types such as matrices, which will be needed here. Since Redis mainly operates in-memory, there are also alternatives like MemoryDB we could use, which is an in-memory persistence DB.
  - When tasks and task instances are created, the API servers could send them to this search service, and the search service could break up the text based fields like title, description, etc and update the terms in the inverted index mappings accordingly.
  - To sort the tasks and task instances within the inverted index mappings, so that we can get back the results from the mappings by their respective time based fields, we can maintain an index which sorts the taskIDs and taskInstanceIDs by their schedule and dueTime fields respectively, within a single mapping. This means that for a term in these mapings, all the docIDs, schedule / dueTime fields, docLocations, etc in the mapping will be sorted based on the schedule or dueTime fields in descending order. We can implement this using Redis sorted sets as well (however, Elasticsearch should be able to provide this sorted set feature, where we can provide a value to sort by within a single mapping), where each mapping will likely contain a sorted set. The sorted set can maintain a list of unique elements (taskIDs and taskInstanceIDs) ordered by a score like the schedule and dueTime fields.

### User service

- The user service will handle user authentication, registration and profile			management

<img width="550" alt="image" src="https://github.com/user-attachments/assets/e12dbff5-7393-4187-b344-b9a863456fb3" />


## DD

### Maintaining task hierarchy

- Rather than storing the entire task tree or hierarchy all within a single KV pair in DynamoDB, it's much more efficient to store the individual tasks themselves as separate KV pairs. We're also linking which taskIDs are sub-tasks to which other taskIDs.

### Subtasks need to be completed before completing a parent task

- We can also impose validations when users are completing task instances. For example, a user will need to complete all the sub-task's task instances before marking a parent task as completed. This logic can be implemented in the API servers.

### Handling multi-keyword queries

- To support searches for multi-keyword queries like "This is a multi-keyword query", we can do the following and in 'Handling multi-keyword queries' (taken from the SDI 'FB post search'):
  - Intersection and filter:
    - Intersecting the results from a multi-keyword search will be very compute intensive since some results may contain millions of entries. Also, implementing the intersection between the search results would mean that we may need to maintain a hash map of the taskIDs / taskInstanceIDs - which will further increase both storage and latency as we'll need to perform a complex operation everytime a user searches.
  - Bigrams of shingles

### Handling large volume of search requests

- The system should return non-personalized results (we could put a requirement like in the SDI 'FB post search' where we have up to 1 min before a task or task instance needs to appear in the search results). Caching the results to handle large volume of search results may be the best solutions as explained below and in 'Handling large volume of search requests' (taken from the SDI 'FB post search'):
  - Use a distributed cache alongside our search service
  - Use a CDN to cache at the edge

Additional deep dives:

### Fault tolerance of inverted index mappings

- To ensure fault tolerance of the inverted index mappings, we can replicate the inverted index mappings. Redis Cluster provides built-in asynchronous primary-secondary replication by default, which should be suitable here since write inconsistencies via a leaderless approach could have issues in the inverted index mappings (which requires low latency reads).

#### Keeping a reference to the searchServerID in the database to recover when inverted index mappings are down / erased

- If both the primary and secondary nodes for the search service are down, then it would be really difficult to rebuild the search service instance's inverted index mappings again without knowing which terms were stored in this crashed search service instance.

- We can store a reference to the searchServerID for a taskID / taskInstanceID in the DB or ZooKeeper. This will allow us to query the DB, and look for tasks / task instances with the searchServerID that crashed. Afterwards, we can rebuild the index for those tasks / task instances with the crashed searchServerID.

- However, maintaining this searchServerID field may have some overhead if we need to update the searchServerID during scaling events, but it ensures fast recovery time if the inverted index mappings are down / erased within a searchServerID. Thus, this overall mapping between the searchServerID: [ taskIDs / taskInstanceIDs ] could instead be maintained in a service like ZooKeeper, which provides a KV store for maintaining server-side mappings like these.

### Reduce storage space of inverted index mappings in Search service

- Users are usually only interested on a small portion of tasks / task instance, thus we can do the following optimizations:
  - Ignore stopwords like "a", "of", etc (when updating the inverted index) which provide no value in searching.
  - In-frequently accessed terms and their index mappings could instead be moved to a cold storage such as in S3 Standard-IA. If there are queries for these in-frequent terms, the query could first check the Elasticsearch or Redis inverted index mappings, and if results are not found there, then it could instead be queried from S3 via Athena and returned to the client with a small increase in latency.

