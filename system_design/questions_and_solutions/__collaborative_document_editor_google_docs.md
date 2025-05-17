# Collaborative document editor like google docs

Google Docs is a browser-based collaborative document editor. Users can create rich text documents and collaborate with others in real-time.

## Requirements

### Questions

- In this system, users can create documents, users can edit the same document concurrently, users can also view each other's changes in real-time, and can also view the cursor position and presence of other users. Are we designing all of this?
  - Yes

- Are we designing both the storage of the binary data of the document itself, and the storage of the document's edits?
  - Yes, let's design both, but focus more on storing the edits themselves

- Should the system store document history and versioning, and allow users to revert back to a previous version?
  - Yes, if time permits, do a deep dive on this

- Should the system provide word suggestions using frequently used words and find grammitical mistakes?
  - Yes, if time permits, do a deep dive on this

- Should users be able to comment on documents?
  - No, let's ignore commenting

- Should users be able to view the "seen count" of a document?
  - No, let's ignore this feature

### Functional

- Users should be able to create documents
- Users can also share documents with other users
- Multiple users should be able to edit the same document concurrently
- Users should be able to view each other's changes in real-time

- Users should be able to see the cursor position and presence of other users
- Document history and versioning

Non-functional:
- Low latency:
  - The write updates made by users should be fast (10 - 200 ms)
- Consistency:
  - The system should also provide conflict resolution between users if they’re editing the same portion of the document
  - The system should be eventual consistent in that all users should eventually see the same document state
- Throughput:
  - Multiple users may be editing the same document
- Durability:
  - Document updates should be durable

**There may also be a constraint where no more than 100 concurrent editors can be on the same document. Having this constraint in place ensures fewer conflict resolutions need to be done when users edit the same section of a document**

## Collaborative editing 101

### Sending edits

#### Sending edits - wrong approach:

- It's very inefficient to send the whole document to the backend on each edit. This could mean sending 10s of MB through the network. Using this approach, let's assume the following:
  - Both userA and userB are editing the same document concurrently
  - We'll assume the document starts with a piece of text: "Hello!"
    - userA adds ", world!" to produce "Hello, world!" which they send
    - userB deletes the "!" to produce "Hello" which they send
  - If both users submit their edits at the same time, the actual document that gets stored depends on which request arrived first
 
#### Sending edits - better approach:

- Instead of sending the whole document, we can send just the edits themselves to the backend. Let's assume we initially have "Hello!" in the document:
  - userA adds ", world" and sends INSERT(page, 5, yValue, ", world")
  - userB deletes "!" and sends DELETE(6)
- If userA's request arrives first, we'll add ", world" and it'll be "Hello world!" since userB will delete the ",". However, if userB's request arrives first, we'll have "Hello, world". This approach is better than the one before, but we'll still have different results depending on which user's request arrived first.

- The critical missing piece here is that the edit is contextual, and is dependent on the current state of the document. We will discuss how to deal with the stream of edits in the HLD.

### Storing document binary data in blob store and document operations data in DB

- Before going forward, it's important to distinguish between storing the actual document's binary data in a blob store and storing the document operations (edits) in a database. The binary data within the document contains the raw document data, but it doesn't tell us anything about which userID made the edits, what time the edits were made, what were the edits themselves, etc. The actual edit info needs to be stored differently in another DB. Storing the edits will allows us to load the latest edits of a document after a user opens a document, and it will allows us to potentially include versioning to the system.
- This design will store both the document (blob store) and edits (DB), however, the actual storage and chunking aspect of the design should be handled by another system instead of Google Docs itself, such as Google Drive. The SDI on Google Drive and Dropbox goes more in depth on storing binary data.

## Data model / entities

- User:
  - userID
  - userName
  - userEmail
 
- Documents:
  - documentID
  - name
  - metadata: { createdAt, updatedAt }

- Edit:
  - This entity will represent a change made to a document by a user
    - editID
    - documentID
    - userID
    - editChanges: [ EditChange objects such as { INSERT, position, characters }, { DELETE, position, characters } ]
    - createdAt

- Cursors:
  - This entity will represent the position of the user's cursor in a document. It will also be used to show the presence of that user in the document.
  - Also, inactive cursor entries could be removed from this entity via a cron job.
    - userID
    - documentID
    - position: { page, x, y }
    - lastActive

- Shared documents:
  - This entity will contain all the userIDs which have access to a documentID
    - documentID
    - userID

- Document versions:
  - This entity is only necessary if versioning is in scope
  - This entity will contain the versionIDs and the version's editIDs for a documentID. New editIDs will be appended to a versionID when concurrent edits are made within a few mins or so (let's say 1 hr) OR the number of editIDs reaches a limit, let's 100 edits or so.
  - If after 1 hr or so, there are no edits, then new editIDs will instead be appended to a new versionID
    - versionID
    - documentID
    - edits: [ editIDs ]
    - createdAt

- Word suggestions:
  - This entity is only necessary if word suggestions is in scope
  - This entity will contain a sorted set of frequently used words, and the word frequency. A separate typeahead service will likely use this entity, along with it's own Trie database / cache to return word suggestions and grammatical suggestions. We could also set a limit on the frequentWords sorted set, and only update it if a word within the document exceeds the least frequent word in frequentWords.
  - Using this approach, the frequentWords could also be added to the userID's own Trie cache, such that a typeahead service will look through both the global Trie and the userID's trie and return word / grammatical suggestions.
    - documentID
    - frequentWords: [ { word, frequency }, { word, frequency } ]

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

Websocket endpoints:

- We will definitely need a websocket based approach between the client and the backend, since there will be a bidirectional communication requirement where the client sends edit updates, and the server sends those edits to the other clients viewing the same document.

### Client will first establish a websocket with the server

- Clients will use this endpoint to first establish a websocket connection with the servers when they open the document.

- The		Sec-WebSocket-Key header will be a value that the server will use to generate a		response key to send websocket requests. The Sec-WebSocket-Version will be the	websocket protocol version, usually 13.

Request:
```bash
GET /documents/:documentID
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

### Perform a write using an insert or delete (the user will insert or delete characters on the document)

- Clients will use the websocket connection to send updates when they insert or delete characters on the document

Request:

```bash
WS /documents/:documentID
SEND {
  type: INSERT / DELETE,
  position: { page, x, y },
  characters
}
```

### Update the cursor

- Clients will use this endpoint when they move the cursor either manually or by inserting / deleting characters

Request:

```bash
WS /documents/:documentID
SEND {
  type: UPDATE_CURSOR,
  position: { page, x, y }
}
```

### Receive other user's edits via websocket

Response:

```bash
RECV {
  type: INSERT / DELETE,
  position: { page, x, y },
  characters
}
```

### Receive other user's cursor updates via websocket

Response:

```bash
RECV {
  type: UPDATE_CURSOR,
  userName,
  position: { page, x, y }
}
```

**When your API involves websockets, you'll be talking about messages you send over the websocket vs endpoints you hit with HTTP. The notation is completely up to you, but having some way to describe the protocol or message schema is helpful to convey what is going over the wire.**

REST endpoints:

### Share document with other user

- This endpoint will create a new entry in the Shared documents entity

Request:

```bash
POST /documents/:documentID/share
{
  userEmails (userEmails to share with)
}
```

## HLD

### Microservice architecture

- A microservice architecture is suitable for this system, as the system requires independent services such as updating document files / metadata, sharing, etc. These are all independent operations which could potentially be managed by separate services.

- Microservices can benefit from a gRPC communication as there will be multiple channels of requests	being sent / received in inter-service communication between microservices. Thus, gRPC could be the	communication style between microservices, as it supports a higher throughput, and is able to handle multiple channels of requests as opposed to REST, which uses HTTP, that is not optimized for		multi-channel communication between services.

### API gateway

- The API gateway will provide rate limiting, authentication, and route requests to the specific services. Depending on the request, its possible to forward a single request to multiple components, reject a request, or reply instantly using a cached response, all through the API gateway
- The API gateway will also allow initiating 2 requests to separate services via 1 single request. For example, if a user edits a document, both the document binary data and metadata could be updated in 2 separate requests in the backend.

### Document metadata service

- The document metadata service will handle document based requests which include updating the metadata in the Document metadata database. The metadata should be separated from the document binary data and the document operations data, since there is data such as title, updatedAt, etc which needs to be updated separately. The Document metadata service will also be stateless, and can be horizontally scaled very easily.
- When a user wants to create a document or share a document, they'll request this endpoint. If they want to create a document, they'll send the title, and if they want to share the document, they'll send the userEmails they want to share with.

### Document metadata database / cache

- We'll also have a database containing the users, document metadata, and shared documents entities. Because we'll likely perform complex queries on the metadata, we may require a SQL DB such as PostgreSQL. The metadata also has many relationships, which could be maintained within a SQL DB.

#### Cache

- The document metadata will not be as frequently accessed, but it is a static data that doesn't change frequently. Therefore, the data could also be cached within Redis, which provides data structures like lists, which will be helpful for storing the list of shared users for a document.
- Also, because the document metadata may be updated by multiple users concurrently, we could introduce a Redis distributed lock with a TTL to prevent concurrency conflicts for the data within the Document metadata database.

### Document service

#### Document service handling edits

- The document service will handle the websocket connection with the client. This service will also handle edit requests for a document, and maintain the consistency of the edit stream using Operational Transformation discussed below. We'll perform OT within the Document service before writing the final edit results to the Document Operations database. Once the final edits have been successfully stored in the Document Operations database, we'll send the edit results to the clients viewing the document via the websockets.

- Dealing with a stream of edits has a lot of consistency problems. We can solve this consistency issue for edits using the below options, and in 'Handling edit streams and consistency':
  - Operational transformation:
    - Let's assume the starting text is "Hello!" in the document for this approach. OT essentially adjusts the edits in the stream before they're applied. It adjusts the edit's position according to the edits which came before it. If userA's edit came before userB's edit, then userB's edit (it's position) will be adjusted according to userA's edit. OT allows us to scale to a small number of collaborators, but not an enormous number.
    - We'll use OT since it is the approach that Google Docs actually takes and it benefits from requiring low memory, and it may be faster than CRDT in some cases because it is not as computation or memory heavy.
    - OT can be implemented using a FIFO queue such as a SQS FIFO queue, or an in-memory queue using a Redis sorted set (not Redis queue) where the score is the time the edit was received by the Document service. Since most queues such as SQS and Kafka don't allow modifying the messages in-place inside the queue (queued messages are immutable), it may be much easier to implement OT using an in-memory queue using a Redis sorted set since we can modify the entries in-place in the sorted set in and out without needing to dequeue then enqueue like in a traditional queue.
    - Every time an editID arrives for a documentID, we'll modify the editID's position and other metadata according to the edits which came before (via OT) and are already in the in-memory queue. Afterwards, we'll place this adjusted edit in the in-memory queue. Once the number of edits for a documentID reach a specific limit within the in-memory queue, the Document service can dequeue the editIDs then store the finalized edits within the Document Operations database in a transaction. 
    - The disadvantage of OT is that the order of operations are still dependent on each other, regardless if the order doesn’t affect the result. Also OT needs to happen within a centralized server such as Document service server. It may be difficult to distribute an OT process across multiple servers since we would have to share the adjusted edits across all servers.
  - Conflict-free replicated data types:
    - If we need to support a larger number of collaborators, CRDT may be more suitable than OT because using real numbers gives us more room in adding edits from a large number of users.
    - CRDT ensures strong consistency between users and it is order independent. CRDT is preferable for users editing a portion and they have different internet speeds.

**Both OT and CRDT are lock-free approaches. Locks can have high latencies and bad user experience since we have to split the document into sections where users could lock the section and edit it. However, locks may be more suitable in a service like Google Sheets where the cells could be locked.**

#### Document service handling reads

- The document service should handle reads for the following cases:
  - When the document is loaded:
    - When someone initially loads the document, they should receive the current state of the document
  - When updates happen:
    - When a user makes an edit, other users viewing the document need to be notified of the edits
  - Cursor position and presence changes

##### When the document is initially loaded

The steps of initially loading a document on the client-side are as follows:

1. The client will first connect to the Document service via a websocket connection
2. This client will then receive the finalized edits on the current document via the Document service within the websocket connection. The client will also download the actual document itself from the blob store via a pre-signed URL. Lazy loading could also be applied, where only the data for the viewport is returned because there could be numerous edits for a single document

##### When real-time updates happen

The steps of loading real-time updates happening on a document on the client side are as follows:

1. After the finalized edits are stored in the Document Operations database, the Document Service will send the finalized edits to all the connected clients
2. When users make edits to a document, they'll see their changes immediately. The edits will always be applied first to their local document on the client side (most likely stored in an internal client DB such as Indexed DB within Google Drive), then the edits will be sent to the Document service.

<br/>

What happens if another user lands an edit on the server after we've applied our local change but before it can be recorded to the sever?

Our OT gives us a way of handling out of order edits. Remember that OT takes a sequence of edits in an arbitrary order and rewrites them so they consistently return the same final document. We can do the same thing here!
So so if User A submits Ea to the server, and User B submits Eb (which arrives after Ea), the perceived order of operations from each site is:

Server: Ea, Eb

User A: Ea, Eb

User B: Eb, Ea

Regardless of the ordering, by applying OT to the operations we can guarantee that each user sees the same document! Therefore, OT will also be performed on the client-side, whenever the client is receiving edits from the Document service. This way, OT ensures any edits made by other users will not conflict with edits made by the user - the received edits will also be adjusted according to OT.

**Note that we're not positioning a queue between the Document service and the Document operations database due to latency reasons. Including a queue will ensure there are no lost messages, however it will still increase the latency between clients receiving the edits from each other. This increase in latency will increase the number of editing conflicts and resolutions which need to be done with OT. However, a queue will work in apps like a chat app, where there is no dependency between messages, and a slight increase in latency is fine to ensure messages are not lost**

<br/>

#### Document service handling cursor position and presence

- Showing other users' cursor positions helps to avoid situations where users are editing the same spot at the same time. We only need to display the cursor position and presence in real-time when the user is connected.
- When the user moves their cursor or closes the connection, they'll send a request to the Document service to update the cursor data in the Cursors table of the Document Operations database via the websocket. The Document service will also forward the user's cursor position and presence changes to other clients.

- Finally, the Document Service can keep track of socket hangups / disconnects and remove those users from it's internal list of users connected for a specific Document, and notify other users about the cursor's presence change (cursor is no longer active in the document's UI for that user)

### Document operations database / cache

- The document operations database will contain edits, cursors, and document versions data. It will contain data which have very high write loads.

- The final edits after performing OT in the Document service will be written to the Document operations database - this DB will store the edits and cursors entities. Because we want to optimize on the write load, Cassandra may be suitable since it can handle very high write loads with it's leaderless replication approach.
- We could also partition this database by the documentID, and order the data based on the createdAt (edits) and lastActive (cursors) fields. We'll partition based on the documentID because this means the edits and cursors for a single document will be within a single partition / shard.

#### Cache

- The document operations data changes very frequently, and thus stale data won't be useful to the clients. Caching approaches for the edits, cursors and document versions will need to be smart enough to evict entries which are no longer relevant, and only store entries which are currently relevant.
- Caching of this frequently data may be very complex, but it might still be possible to cache only the document versions data because this is the least frequently changing entity.

### Blob store

- The blob store will store the actual chunks of the document's binary data. The edits are different from the data stored here in that the edits links to a specific userID, time, version, etc, while the raw data doesn't have this info.
- The client will likely have a chunking functionality, which will both upload the chunks for edits, and download chunks when receiving edits via the websocket.

- When the client is making edits, they'll likely send the edits and modified chunks via the websocket to the Document service, and the Document service will apply OT from the edits and modified chunks received by all the clients editing a document. The finalized edits and chunks after applying OT will then be saved to the Document Operations database and blob store respectively. This way, the blob store will contain the modified chunks after OT as well.
- If a client receives the edits from the Document service, they'll request for a pre-signed URL from the Document service, then download the chunks corresponding to the edits from the blob store. The client will then use both the edits data and the chunks to render the document content within the UI.

### L4 Load balancer

- We’ll need an L4 load balancer to support traffic at the TCP level. L4 load balancers,	let’s say using ELB in TCP mode can load balance websockets. When client’s need to	connect to a Document service server via websocket, the L4 load balancer will route them to the Document service server they	previously connected to or to a server using the load balancing algorithm.		However, if a server goes down, the L4 load balancer can route the client to		connect to another Document service server instead.

- When a client needs to connect to the Document service server, the request will first go to the L4	load balancer, then to the Document service server. There will actually be a symmetric websocket	connection between both the client to the L4 load balancer, and between the L4 load	balancer to the Document service server.

- L4 load balancers can be stateful and use sticky sessions to persist the server the	client previously connected to. The sticky session can be implemented by identifying	the user, usually with cookies or their IP address, and storing the user’s connected	server for handling future requests.

- If clients disconnect from a server, they can automatically reconnect to the		same server or another one via the L4 load balancer. Reconnecting to the same	server may be easier, as the session data in the L4 load balancer doesn’t have to	be updated.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/5c95c19c-69c8-4cc2-b63d-b2de4e71f47e" />

## DD

### Chunking and document binary data upload / download

- Note that this is a separate SDI on it's own, and it's discussed more in depth in the Dropbox SDI.

### Versioning and reverting to previous versions

- To implement document versioning using the edits, we could maintain a separate Document versions table in Cassandra, within the Document operations database, which contains the versionIDs for a documentID. Each versionID will also contain a list of editIDs (and other edit metadata)

- We can implement document versioning using the below approaches:
  - Upload a completely new document on each edit performed by a client, and add a new version to the Document versions table:
    - Instead of overwritting the only stored document in the blob store, we could upload a completely new one when the file changes locally or remotely, and we'll then set a new version for it by adding a new entry to the Document versions table
  - Upload only modified chunks, and add a new version to the Document versions table:
    - We'll only upload the modified chunks and add a new versionID in the Document versions table for the editIDs corresponding to the modified chunks. Because we'll need to upload the modified chunks after OT (edits conflict resolution), instead of having the client upload directly to the pre-signed URL, we'll likely need the Document service to upload the chunks after the changes by OT are performed on the chunks too. This way, the blob store will contain the modified chunks after OT as well.
   
    - Likewise, when clients open a document, they'll receive the latest version from the Document service, and they'll also download the chunks for the latest version 

#### Reverting to a specific version

- Clients can also revert back to a specific versionID by requesting the Document service to send the "inverse edits" from the current versionID up to a previous versionID we're reverting to. The Document service will also send a pre-signed URL to the client, where the client could download the "inverse chunks" stored from current versionID up to a previous versionID we're reverting to.
- These inverse edits and chunks in this case applies the opposite operation of the edits - ie, if the edit has an INSERT, then the inverse chunk / edit would now instead be a DELETE because we're reverting back. This way, the client can go back to a specific versionID. When the client is downloading these inverse edits and chunks, the client can instead apply the inverse operation for each downloaded edit and chunk on the client-side. Afterwards, the client can send this revert operation as an edit itself to the Document service - this revert will be it's own edit.

- If the versionID goes way back, and it might actually be more efficient to recreate the file from the edits and chunks between the very first versionID up to the versionID we're reverting to, then the client could instead download all the edits and chunks between the very first versionID up to the versionID we're reverting to without applying the inverse operation.

### Scaling to millions of websocket connections

- We'll need to scale the Document service as we'll be handling a lot of websocket connections. It's best if each connection is maintained by a single server for the duration of the connection. If users editing the same document are connected to different servers, then those servers would need to communicate together, which will make the design more complex. 
- This means that we need to scale the number of servers to the number of concurrent connections - not necessarily scaling to the number of documents! Concurrent connections will happen when multiple clients are connected, and are editing the same document.
- Ideally, we want to have all the concurrent connections for the same same document connected to the same Document service server. We can solve this by using the below approaches, and in 'Scaling to millions of websocket connections':
  - Pub/Sub
  - Consistent hash ring:
    - We'll assign new documentIDs to specific Document service servers via consistent hashing, where the hash value of the documentID will be mapped to the hash ring. The first server clockwise will then handle the concurrent connections for this documentID. The mapping of documentID : documentServiceServerID in ZooKeeper will also be updated.
    - ZooKeeper will maintain the mapping between the documentID : documentServiceServerID, such that connections for the same documentID are routed to the same server to set up a websocket. If we had multiple servers handling connections for the same documentID, updates received in one server would be sent to all the servers for the same documentID via the ZooKeeper mapping.
    - We'll opt for the consistent hashing approach because it also solves a related problem of how we can scale our Document Service while maintaining a singular owner maintaining all the concurrent connections for the same document.

### Reducing storage of Document Service DB

- We can improve the storage usage by using OT instead of CRDT, where OT takes up less memory and storage. To further reduce the storage, we can periodically make the edits within the Document Operations database more compact. We can periodically combine multiple finalized edits (after OT) into one single edit to save on storage.
- We can reduce the storage within the Document Operations database using the below approaches, and in 'Reducing storage of Document Service DB':
  - Offline snapshot / compact
  - Online snapshot / compact operations

#### Reducing OT in-memory queue memory usage

- We can also reduce the memory usage in the in-memory queue within the Document service by using the same logic where we periodically combine the edits and make the edits more compact within the in-memory queue itself.

### Word and grammar suggestions

- To implement a typeahead feature, we can store a user's frequently used words in a separate Word suggestions table / cache.
- The table will store the persistent data and can be a KV store such as DynamoDB, which provides fast reads / writes.
- Also, we can store the frequently used words within a Trie data structure in a Redis cache on the server-side, which the Document service communicates with when returning word suggestions. We can use Redis since we'll likely need Redis sorted sets containing the frequent words in the trie nodes. We could also store the same frequently used words on the client-side on the browser via session storage. The purpose of this Trie based cache will be to provide word suggestions specific to the user, ie which words they use frequently - this data will also have a limit and be relatively small.
- Additionally, we can also have a global Trie table / cache using DynamoDB / Redis respectively which will provide the actual grammitical suggestions. This global Trie will essentially act very similar to a typeahead service. Therefore, the suggestions provided to the user will be from both the user's frequently used words (user's own Trie) and the grammitical suggestions (from the global Trie).

Additional deep dives:

### Real-only mode

- To implement a read-only mode feature, we can do the following:
  - Read-only mode when user opens a document, and chooses "read-only" mode:
    - If the user explicitly chooses "read-only" mode after opening a document, then the client will block the user from typing or sending edits. The client will have this feature within the UI components.
  - Read-only mode when user has read-only access:
    - If the user has only read-only access, we can have a separate "access" field within the Shared documents table, where the access can be READ_ONLY / WRITE / WRITE_AND_SHARE / OWNER, etc.
    - Whenever a user opens the document, the Document Metadata service will authorize the user using this access field and provide the necessary permissions for reading, editing, sharing the document.

### Offline mode

- If a client is offline, we can temporarily store the user's edits within the session storage OR a client DB such as Indexed DB. When the client comes back online, the edits stored internally will be sent to the Document service, and OT will be performed on these edits.
- The OT performed for these internal edits will adjust these edits according to the edits which we're already registered in the Document Operations database while the client was still offline. The OT for offline edits will in this case need to perform an extra step, where it checks Document Operations database which edits were made after the client went offline, then adjust the internal edits' positions to these edits in the DB. Thus, these internal edits will seem like it's actually modifying the same document the client had when they went offline, as opposed to modifying the current latest docment.
- The edits after OT will then be stored in the Document Operations database, and the client can then pull the latest changes for the document.

### Saving blob store storage space

- When supporting file versioning, the storage space can be filled up very quickly. Therefore, we can include the following techniques to reduce storage space:
  - Deduplicate chunks:
    - We can remove duplicate chunks in the blob store, and determine if the chunks are duplicates by using their fingerprint values
  - Limit the number of versions of a file if necessary
  - Move infrequently used chunks to cold storage:
    - If a file's chunks have not been accessed for months or years, we could move them to a cold storage like the Standard-IA tier within S3, which should be cheaper to store data.
