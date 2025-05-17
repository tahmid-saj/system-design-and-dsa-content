# Chat app

## Requirements

### Questions

- What kind of chat app should this support, 1-1 or group chat?
  - Both 1-1 and group chat

- Is this a web or mobile app?
  - Both

- What is the limit on the users in a group chat?
  - 100

- Can the app support attachments?
  - Yes, if time permits

- Can users receive sent messages while they are not online (up to 30 days)?
  - Yes

- Can users see if other users are online?
  - Yes

- Do we want to bold the chats in the UI which have unread messages when users open the app?
  - Yes, include this feature and talk about how the data model will change to support this

- Is this a small scale or large scale app?
  - It should support 50 million DAU

### Functional

- The system should support both 1-1 and group chats
- It is a mobile and web app
- System should support text, images, videos
- It should store the chat history forever
- It should have push notifications
- Users can receive sent messages while they are not online for up to 30 days
- Online presence should be shown

### Non-functional

- Low latency:
  - Low latency in message delivery			(~500 ms)

- Throughout:
  - Multiple messages will be sent concurrently

- Consistency
  - Messages should be delivered in the		order they were sent
  - In the event of a network partition,		consistency will be prioritized over 			availability as the correct ordering of		messages is essential

## Chat messaging 101

- In chat applications, there is usually an intermediary server which receives the messages from the client, and sends the message to the recipients. The servers also establish the connection between the client and recipient

There are different ways in which the communication between the client and recipient could be done:

### HTTP

- HTTP creates a connection each time a HTTP request is sent. Using the keep-alive	header, the client can maintain a persistent connection with the servers, which		reduces the number of HTTP connections and TCP handshakes that need to be set 	up.
- However, HTTP is not bidirectional, and so both the client and server cannot send	messages using the same connection.

### Polling / long polling

- In polling, the client periodically sends requests to the server to check if there are	new messages or data available. Usually, the server won’t have any messages, and	so polling will be costly.
- In long polling, the client holds the connection open for a while and requests the		server to check if there are new messages. The server responds with any new		messages or the connection times out and closes. Long polling will still be costly and inefficient	as it creates multiple connections and waits for them to be timed out or for new 		messages to be sent. Also polling is not a bidirectional communication approach, 	which will be needed in a chat app.

### Websocket

- Websockets will be a good choice for bidirectional communication, and it will operate	over a TCP connection. A websocket connection is initiated by the client, which		requests for a connection upgrade via the HTTP headers. The server then			acknowledges the upgrade, and the websocket connection is established.
- Websockets also work over firewalls because they use port 80 or 443 which are		used by HTTP/HTTPS connections

- Websockets also communicates over an encrypted TLS connection, where the		messages sent are encrypted. TLS provides secure communication for bi-directional	communication, and is built on top of and supports both HTTP and HTTPS.

## Data model / entities

- Note that chat apps are usually 1 : 1 in read-write ratio

- We could use a local based unique ID for all the IDs such as via Redis if the chat app operates in a small-moderate scale. However, if operating in a global scale, we can use Twitter Snowflake

<br/>

- Messages:
	- This entity will store all the 1-1 and group chat messages. The chatID field will be	used to reference the 1-1 / group chat in which the message is located

	- Either the messageID could be used to sort the messages on the client side if using	a numeric timestamp value such as UNIX within the ID (Twitter snowflake provides	this) OR the sentAt can be used to sort the messages on the client side. Additionally, the frequently accessed chat’s messages		could be cached both on the server and client side via a TTL for low latency.

	  - messageID
	  - userID
	  - chatID
	  - message, attachmentIDs
	  - sentAt

- Chats:
	- This entity will store all the 1-1 and group chats
 	- To check if a user has any unread messages or mentions, we can have a lastActive field in this table which updates when any user in the chat sends a message. Note that mentions will also be in messages. When a user opens the app, we'll use the chatID and compare the lastSeen field in the Chat users table against the lastActive field in this table. If the lastSeen is before the lastActive, then there are unread messages / mentions for the user in the chatID - we'll bold the chat in the UI.

	  - chatID
	  - name
   	  - lastActive

- Chat users:
  - This entity will store the users within a chatID
	
  - The lastSeen field will be the last timestamp at which the user had opened the		chatID. We’ll use lastSeen to render the messages as “unread” or “read” on the UI.	As soon as the user opens a specific chatID, their lastSeen will update and the		messages will be rendered as “read” instead of “unread”.

  - The lastSeen timestamp can also help us find the number of unread messages	a user has for a specific chatID. The lastSeen field can be compared against the		sentAt time of the messages in the Messages table, and a count of the		message entries after the lastSeen timestamp can be returned to the user as the	count of “unread” messages.

  - We can also use the lastSeen time to find the number of unread mentions in a chat. When checking for the unread messages when the user opens the app (where the lastActive time in the Chats table is after the lastSeen time), we'll check which of these unread messages have mentions of the userID. We'll return the count (via the API endpoint) of the unread messages with mentions - which will be the number of unread mentions for the chat.

	- chatID
	- userID
	- lastSeen

- Users:
	- userID
	- userName, userEmail, userPhoneNumber
	- userStatus
	- lastOnline

- Devices:
	- Since a user could have multiple devices, this entity will store all deviceIDs		belonging to a userID

	  - deviceID
	  - userID

- Inbox:
	- This entity is only required if we need to satisfy the requirement where the user		should be able to receive messages sent while they are not online (up to 30 days). In	a SDI, if this isn’t required, then we don’t need this entity.

	- When messages are sent, they’ll be written to both the Messages and this Inbox	table regardless if the recipient is online / offline. If they’re online, the messages in the	Inbox table will be deleted after the recipient has sent the acknowledgement that		they’ve read the messages. 

  - The inbox table will help retain unread messages for 30 days via the expirationTime,	and retrieve the actual message content from the Messages table, using the		messageID in this Inbox table. Once clients come online, they’ll request for unread	messages in this Inbox table, and use the messageID to fetch the actual message	content from the Messages table. 

  - After acknowledging that the recipient has read the messages, these messages in	the Inbox table will be deleted via a request from the recipient client. A simple cron job could also periodically delete expired messages in this Inbox table

	- messageID
	- recipientUserID
	- expirationTime

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed messages quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

- Note that we’ll use a combination of HTTP and websocket requests, where HTTP requests will be sent for workloads not requiring a bidirectional component, such as creating a chat, getting messages, uploading / downloading attachments, etc. Websocket requests will be sent for sending / receiving messages in real-time

- Note that the requests in the API are split into the HTTP and websocket requests. This is to separate the stateless operations (HTTP) from the stateful operations (websockets), as they could be scaled independently via the API servers and chat servers respectively. Also uploading / downloading attachments via chat servers will use up their bandwidth, when “sending message” based operations are meant to have low latency. Also, splitting the operations will make debugging easier where different operations are handled by different components.

### HTTP requests

#### Get chats

- We could set the nextCursor value to the viewport's oldest lastActive time, such that the next paginated results will have chats which were active after the viewport's oldest lastActive time

Request:
```bash
GET /chats?nextCursor={ viewport's oldest lastActive time of chat }&limit
```
Response:
```bash
{
  chats: [ { chatID, name } ],
  nextCursor, limit
}
```

#### Create a chat

Request:
```bash
POST /chats
{
	chatUsers: [ userIDs ]
	name
}
```

#### Get messages

- Fetches all messages (as well as unread messages) when the userID opens the chat:
  - If the user has unread messages in this chat, then the nextCursor value will be the client's "last active" time, which will specify the last time the client was online. This "last active" time will likely be stored in session storage on the client-side. If this last active time is not in the session storage, we could instead use the lastSeen field from the Chat users table as the cursor value, and return a paginated list of the messages which are newer than this lastSeen field.
  - If the user does not have unread messages in this chat, then the nextCursor value will point to the viewport's oldest sentAt time for the message. This way, the next paginated result will contain the messages which are older than the viewport's newest sentAt time, since we'll be returning older messages as the user is scrolling up.

Request:
```bash
GET /chats/:chatID/messages?nextCursor={ client's "last active" time OR viewport's oldest sentAt time for message }&limit
```

Response:
```bash
{
  messages: [ { messageID, userID, message, sentAt } ],
  nextCursor, limit
}
```

#### Add / remove users to the chat

Request:
```
POST /chats/:chatID?op={ ADD or REMOVE }
{
	userID
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
POST /chats/:chatID/pre-signed-url
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

#### Download attachments

- Downloads an attachment via the attachmentID (we're using attachmentIDs instead of sending the pre-signed URLs ahead of time to the client because the pre-signed URLs have an expiration time)

- When downloading binary content using HTTP, application/octet-stream can be		used to receive binary data

- The application/octet-stream MIME type is used for unknown binary files. It		preserves the file contents, but requires the receiver to determine file type, for		example, from the filename extension. The Internet media type for an arbitrary byte	stream is application/octet-stream.

- The */* means that the client can accept any type of content in the response -		which could also be used for sending / receiving binary data

- Note that to download files, we could use either a pre-signed URL or a URL the		client can request to download from the CDN (let’s call it CDN URL). The process is	similar to uploading files, where the client first requests the servers for a pre-signed	URL OR CDN URL, then the client will download the file from the pre-signed URL /	CDN URL. However, using a CDN may be an overkill for this design.

##### Request for a pre-signed URL / CDN URL

Request:
```bash
GET /chats/:chatID/attachments/:attachmentID/pre-signed-url OR cdn-url
```

Response:
```bash
{
	pre-signed URL or CDN URL
}
```

##### Download from pre-signed URL / CDN URL

Request:
```bash
GET /<pre-signed URL or CDN URL>
Accept: application/octet-stream or */*
```

Response:
```bash
Content-Type: application/octet-stream or */*
Content-Disposition: attachment; filename=”<FILE_NAME>”
{
	attachment’s binary data used to generate the attachment on the client side
}
```

### Websocket requests

#### Upgrade connection to websocket

- This endpoint will be used to establish the websocket connection. The			Sec-WebSocket-Key header will be a value that the server will use to generate a		response key to send websocket requests. The Sec-WebSocket-Version will be the	websocket protocol version, usually 13.

Request:
```bash
GET /chats/:chatID
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

#### Send message

- The clients will send messages via an established websocket connection

Request:
```bash
WS /chats/:chatID/messages
SEND {
	message
}
```

Response:
```bash
RECV {
	enum SUCCESS / FAILURE
}
```

#### Client receives acknowledgement on messages received by other clients

- When a message has been received by other clients, they’ll send an				acknowledgement back to the servers, which will let the sender client know that the	message has been received. This will help us ensure the messages haven’t been		lost.

```bash
RECV {
	messageID
	RECEIVED
}
```

## HLD

**The high level design if using message queues is in ‘High level design - message queues’, and for Redis PubSub it is in ‘High level design - Redis PubSub’**

### L4 Load balancer

- We’ll need an L4 load balancer to support traffic at the TCP level. L4 load balancers,	let’s say using ELB in TCP mode can load balance websockets. When client’s need to	connect to a chat server, the L4 load balancer will route them to the chat server they	previously connected to or to a chat server using the load balancing algorithm.		However, if a chat server goes down, the L4 load balancer can route the client to		connect to another chat server instead.

- When a client needs to connect to the chat server, the request will first go to the L4	load balancer, then to the chat server. There will actually be a symmetric websocket	connection between both the client to the L4 load balancer, and between the L4 load	balancer to the chat server.

- L4 load balancers can be stateful and use sticky sessions to persist the server the	client previously connected to. The sticky session can be implemented by identifying	the user, usually with cookies or their IP address, and storing the user’s connected	server for handling future requests.

- If clients disconnect from a chat server, they can automatically reconnect to the		same chat server or another one via the L4 load balancer. Reconnecting to the same	chat server may be easier, as the session data in the L4 load balancer doesn’t have to	be updated.

### API servers
  
- The API servers provides endpoints to manage user profile, chats, requesting		pre-signed URLs / CDN URLs, etc. The endpoints handled by the API servers will not	require a bidirectional communication

- The idea is that the client will use the API servers to retrieve their paginated		messages when they first open a chat, and they will use the chat servers to send /	receive messages from then onwards after a websocket connection is set up.

- Chats can be created and users can be added / removed from a chat through the	API servers. The API servers will create a Chat entry in the Chats table, and add the	userIDs and chatID entries into the Chat users table, all within a transaction.

#### API servers viewing all chats, all messages in a chat, and viewing all users in a chat

- The API servers can also be used to view the chats from the Chats table via chatID,	and view all the userIDs in the chat by filtering on the chatID from the Chat users		table. We can also view all the messages for a chatID from the Messages table using the API servers.

- Since these operations will be done frequently, we can add a GSI on DynamoDB on the Messages table, where the partition key is the chatID and the sort key is the sentAt. We'll do this to return the messageIDs sorted by the sentAt for a single partition containing the chatID. Also, we can add another GSI on the Chat users table, where the partition key is the userID and the sort key is the lastSeen field. This will help in finding the chatIDs a single userID belongs to when we'll return the chats the userID is in when the user first opens the app (we'll also use the sorted lastSeen fields to return channels with unread messages first in a sorted order when returning the chats).

### Chat servers
  
- The client maintains a websocket connection with the chat servers to send		messages to other clients. The chat servers will store the messages in the Messages	table asynchronously, and also forward the messages to the appropriate recipient via	Redis PubSub. Upon receipt, the recipient can send an acknowledgement back to the	sender via Redis PubSub.
	
- Thus, if any messages are lost in Redis PubSub, due to let’s say the recipient not	being subscribed, the messages will still be persisted in the Messages table

- We’ll use a websocket connection as opposed to a HTTP connection (hanging GET), polling, etc, because it offers a	bidirectional communication between the clients. When a client sends messages via HTTP, the connection will need to be	re-opened on every request / message, as opposed to a websocket.

- It's possible to connect clients directly via a peer-to-peer connection like WebRTC, which will reduce the load on the	servers. However, without a mediator such as a server in between the clients, clients have an easier way of attacking	the app or other clients as there are no servers handling the security.

### Key value store / cache

- A KV store could store the messages, chats, chat users, user / device profiles data.	A KV store	will be suitable here as the data type is relatively simple and will be		frequently accessed. There will likely be equal number of reads and writes happening	and so a KV store such as DynamoDB will be used here. 

- DynamoDB follows a primary-secondary model where it can be used for both read	and write intensive tasks. Also DynamoDB is optimized for low latency reads / writes	via eventual consistency, providing both LSIs and GSIs indexing, and using SSDs - 	which will be beneficial for read latencies

- Note that both Facebook / WhatsApp and Discord use KV stores such as Mnesia to	temporarily store messages as well

#### Cache

- As only recent messages may be accessed, a cache will also be suitable in storing	the recent messages. Redis could be used here as it provides complex data		structures such as sorted sets which will be needed to store the messages.
- We can cache on the browser side or use Redis to cache static data for users and	chats, and cache messages on the client-side or server-side using a short lived TTL of 15-20	mins or so as they likely won’t be viewed repeatedly.

### Message delivery from one Chat server to another Chat server

Because we'll have users in the same chat connected to different chat servers, to deliver messages from one chat server to another chat server, we can do the	below and in ‘Message delivery between chat servers’:
- Keep a Kafka topic per user:
  - This approach mainly won’t work because Kafka is not built for billions of			topics (chat apps usually have billions of topics), and it will carry too much overhead for each topic, which may be			50 KB in size. This will result in terabytes of data to maintain for the Kafka			topics.

  - Kafka is not optimal for short lived “micro topics” which are needed for a			chat app, where there can be numerous topics for chats, users, etc, and			subscribers	 can subscribe or unsubscribe at any point. 

  - Redis PubSub is a lightweight solution which may be more appropriate	for message delivery between chat servers, since only currently			subscribed subscribers will receive any messages sent to the topic.

- Consistent hashing of Chat servers:
  - By using a separate service discovery service using ZooKeeper to keep			track of which clients should connect to which chat servers, there will still			be an overhead of maintaining those mappings during both disconnections			and scaling events. Clients may frequently disconnect then reconnect to			different chat servers, and all of this will need to be maintained and				updated in service discovery, which will be complex to handle. Additionally,			during scaling events in consistent hashing, chat servers will handle a 			different set of clients in the hash ring - thus the mappings in ZooKeeper			will need to be updated frequently during scaling of chat servers.

- Offload to Redis PubSub:
  - Redis PubSub can maintain a lightweight hashmap of websocket 				connections. With Redis PubSub, a subscription can be created for an			userID / chatID, and messages can be published to that subscription which will be			received at-most-once by the subscribers.

  - Receiving messages from other clients:
    - When recipient clients connect to the chat server, the chat server will			subscribe to the sender userID’s / chatID’s topic via Redis PubSub. Any			messages published to that sender userID’s / chatID’s topic will be				forwarded to the recipient client by the recipient’s chat server (since the			chat servers are currently subscribed). 

  - Sending messages to other clients:
    - The chat server of the sender userID / chatID will publish the message to			their topic. Any currently subscribed recipient chat servers will receive that			message published in that topic. The recipient chat servers can then				deliver the message to the appropriate recipient userIDs.

- Message queues for 1-1 chats:
  - We could also place message queues between chat servers only for 1-1 chats		as there is one producer and consumer only. The mapping between the chat 		servers to the message queues will be maintained in the chat servers				themselves (as they’re stateful) or maintained in service discovery. However, 		maintaining the client to server mappings in service discovery will be an			overhead, as clients will frequently disconnect and reconnect to different chat		servers.

  - The message queues will follow a strict order, or a best effort ordering using		the sentAt field for the message OR using the messageID 			generated via a sequencer such as Twitter snowflake which increases the ID		values with time.

#### Redis PubSub

- The topic represents the sender userID in a 1-1 chat, and the chatID in a			group chat in this approach

- Redis PubSub is lightweight and is an at-most-once delivery, which means that it			doesn’t guarantee message delivery. If there’s no subscribers listening,			then the message will be lost, and stored in the Messages and Inbox				table. 

- Redis PubSub is appropriate for this design because it sends messages	only when there are currently subscribed chat servers, and if there are no	subscribed chat servers, then the message is not received. This is a mock	of how a chat app operates as well.

- One issue with this approach is that there is an all-to-all relationship		between chat servers and Redis cluster servers, where we’ll need		connections for all those relationships. However, Redis PubSub is much more	lightweight than Kafka, and will not take up as much bandwidth. 

#### Redis cluster

- Topics will also be distributed across nodes within a Redis cluster.

- Also, the Redis clusters could also be replicated - when one cluster is down, another replica can still receive from / send to subscribed chat servers. There may be overhead in replication of Redis clusters, however Redis PubSub is more lightweight than most queue solutions (due to it’s at-most-once delivery) such as Kafka and SQS, thus it will be less complex in replicating it since there’s less persisted data to replicate.

### Blob store
  
- The attachments can actually be uploaded / downloaded directly from the blob store	via a pre-signed URL sent by the API servers. In WhatsApp, attachments are actually	uploaded / downloaded using this approach with a separate HTTP service. Thus, we	could do the below and in ‘Uploading / downloading attachments solutions’:
  - Keep attachments in DB

  - Send attachments via chat / API servers:
    - A lot of the times, having the client upload the file to the API servers,			 	then having the API servers upload to the blob store is redundant and				slow especially for large files because the uploading process has to be			done twice. Clients could directly upload to the blob store via a pre-signed			URL, and any security or validation checks can be performed via the blob			store client interfacing the blob store after the user has uploaded to the			pre-signed URL.

    - However, in some applications, such as YouTube, where the videos will			need	additional transformation, having intermediary API servers may be			suitable.

  - Manage attachments separately:
    - We can use pre-signed URLs to upload files directly to the blob store.			Pre-signed URLs can be sent via the servers to the clients. Clients can			then use the pre-signed URL, which may have a TTL to upload / download			their files. Pre-signed URLs are explained in ‘Pre-signed URLs’.


### Service discovery

- The service discovery is used to route the client to an appropriate chat server using their geographic location, the server capacity, etc to initiate the			websocket connection.

- Zookeper is frequently used for service discovery. This service essentially maintains a mapping of the userID : chatServerID, which can be maintained in a KV	store such as ZooKeeper. Zookeper can register all the		chat servers and their info in a KV store, and find an appropriate server for the client	based on some criteria. Zookeper can also maintain the ports on the chat servers that	clients will connect to in order to establish a websocket connection

- After the user logs in, the service discovery service gives a list of DNS host names to	the chat servers that the client could connect to. This is done only once every time the	user logs in. Every time afterwards when the client	opens the app, the API servers will use this service discovery service to find the Chat server to connect to from the		mappings. Zookeper will maintain the mapping between the chat servers,	ports and	users so that they can reconnect to the same chat server. When the user disconnects,	and reconnects to a new chat server, the service discovery service will update this	mapping.

- By using a separate service discovery service using ZooKeeper to keep			track of which clients should connect to which chat servers, there will still			be an overhead of maintaining those mappings during both disconnections			and scaling events. Clients may frequently disconnect then reconnect to			different chat servers, and all of this will need to be maintained and				updated in service discovery, which will be complex to handle. Additionally,			during scaling events in consistent hashing, chat servers will handle a 			different set of clients in the hash ring - thus the mappings in ZooKeeper			will need to be updated frequently during the scaling of chat servers.

- This design will not use a service discovery component, as we’ll use Redis PubSub	which is lightweight and thus will allow all the chat servers to directly connect to the	Redis clusters.

### Presence servers

- The presence servers manage the online/offline status of the clients. Clients can	send periodic heartbeats to the presence servers (let’s say every 10 mins) for		the presence servers to update their online / offline status

### Notification service

- This service will use third party notification services like mailchimp, SNS, SES, APN,	android push notifications for generating notifications

High level design - Redis PubSub:

<img width="900" alt="image" src="https://github.com/user-attachments/assets/04410034-a96d-44a4-b2f4-0956e708b01b" />

<br/>

High level design - message queues:

<img width="900" alt="image" src="https://github.com/user-attachments/assets/13a0eff4-aae2-4548-afc9-88c676cab55e" />

## DD

We’ll dive deep into some parts of the system:


### Online presence

- Presence servers will update the KV store of the lastOnline timestamp via HTTP when users login or logout
	
- If a user disconnects, the websocket connection will be lost. It is also common for users to disconnect and then reconnect frequently in	unstable network conditions, therefore frequently changing the lastOnline timestamp will not be useful. We can have the client send		periodic heartbeats (every 10 mins) to the presence servers to update the lastOnline timestamp. If the client has disconnected and		hasn't sent the heartbeat, the presence servers will set the client as offline in the KV store.

- Via Redis PubSub, friends of users who are subscribed to their friend’s topics could also receive updates on the friend’s presence when	they go offline or come back online. Presence could also be fetched only for the usersIDs within the viewport via lazy loading.

- Also, friends of users could also subscribe to the presence servers of the user to receive updates on the friend’s presence as shown in ‘Online presence subscription’. If we're using Redis PubSub, friends of users could subscribe to the user's topic, and when the user logs in / out, that user will send a message to the subscribed friends of their topic

<br/>

Online presence subscription:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/96e2a094-81ea-4c3a-a8d7-57ae83aff9cf" />

### Device synchronization

- To ensure device synchronization, where if a user views their messages on their laptop, it should be registered as “read” on their mobile	device as well - we’ll use the Devices table which contains deviceIDs for each userID. Instead of relying on the userID for sending /		receiving message operations, we’ll use the deviceID to differentiate between devices belonging to a user.

- Chat servers will subscribe to a topic with the deviceID instead of userID. This also means that each deviceID will instead	establish a websocket connection to the chat servers instead. This way, a message will be sent to all the	devices of a user. A device limit	can also be introduced for a single user.

- To ensure device synchronization, where read receipts on the laptop should be immediately registered on mobile - when the deviceID	has sent the acknowledgement that they’ve read and received the messages, their lastSeen timestamp in the Chat users table will		update to the current time. After the lastSeen timestamp updates, the UI should render the messages as “read” on page refresh for all deviceIDs belonging to the userID.

- If we want read recipients on the laptop to immediately register on mobiles without having to refresh the page, then when a userID reads a message on one device, their read receipts could also be sent as a separate message to all the other deviceIDs belonging to this userID via the websocket connection. This way, the client doesn't have to refresh their page, and can receive read receipts from any of their devices using the websocket connection.

### Message delivery status

- The message delivery status on the client side will change depending on where the message currently is. 

- After the client sends a message to the chat server, the chat server will send an acknowledgement back to the client and mark the		message as “Delivered”.

- After the message reaches the Redis cluster or message queue and is forwarded to the other client or notification servers, the			message status will be marked as	“Sent” after the chat server sends an acknowledgement back to the client.

- Once the other client has seen the message on their viewport, the other client will send an acknowledgement to the chat server, and		the chat server will subscribe and send to the recipient userID’s topic / message queue to mark the message as “Seen”.

### Database sharding

We can shard the database tables in the following ways:

#### Partitioning based on userID

- Because we have many tables which have userID, a single shard could represent a hash range for the userIDs. When a new 			entry comes in, the hash value of the userID could be mapped to a specific shard via consistent hashing with the hash range. This		way, entries such as messages for the same userID are within a single shard, and can be easily accessible. 

#### Partitioning based on messageID

- If we partition by messageID, where different messageIDs for a single userID are distributed across shards, then fetching the			messages for a single userID will be very slow - thus this approach is not appropriate.

### Database replication
  
- Additionally, we can replicate the database tables / shards to prevent a SPOF

### 1 to 1 chat flow (if using message queues for 1-1 chats)

- If using a message queue approach for message delivery between chat servers, referring to the diagram ‘1 to 1 chat flow’, the message	will also be stored in the KV store upon message delivery via the chat server. If User B is online, they will retrieve the message from the	message queue. If User B is offline, then the message will be sent to the notification service (if the design is using it). Once User B		comes back online, they will fetch the messages from the KV store via the API servers.

<br/>

1 to 1 chat flow:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/d19530c1-3790-4648-a69c-f8d01056a78b" />

<img width="800" alt="image" src="https://github.com/user-attachments/assets/11687861-f284-43f6-a854-edffd412e09d" />


### Group chat flow (if using Kafka or message queues for group chats)

- Referring to the diagram ‘Group chat flow’, where client A / B / C are in a group chat and assuming all the clients are online,	when client A sends a message to the chat server, the chat server will forward the message to distinct message queues for client B / C.
- For better message delivery in group chats, a Pub-Sub service using GCP Pub-Sub, Kafka, SQS and SNS could be used instead as		the number of users and messages grow in the group chat. 

- If using Kafka for group chats, a group chat can be a topic, and senders and receivers can be producers and consumers respectively

<br/>

Group chat flow:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/82b566d1-3676-4172-8f97-16c692384e67" />

## Wrap up

- End-to-end encryption of messages and user data
- Caching of messages on the client side
- Error handling for messages not being delivered (retry policy)

- HBase as database:
	- A wide-column database such as HBase or Cassandra could also be used. HBase is a column oriented 	KV NoSQL database that can store multiple values against one key into multiple columns. HBase is also		modeled after Google’s BigTable and runs on top of HDFS. HBase groups data together to store new		data in a memory buffer (temporary storage in computer’s memory, while data moves from one place to		another), and once the buffer is full, it dumps the data to the disk. THis way of storage not only helps to		store a lot of small data quickly but also fetching rows by the key or scanning ranges of rows. HBase is		also an efficient database to store variable-sized data, which may be needed for a chat app.



