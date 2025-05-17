# Slack / Discord

Note that this design is similar to the SDI 'Chat app'

## Requirements

### Questions

- In Slack / Discord, users can communicate in one-one channels, private or public channels within an organization. You could also create or delete channels, update channel settings, invite people to channels, etc. What features are we designing?
  - We’re designing the core messaging functionality, which involves one-one channels and group channels in	an organization. Let’s not focus on channel settings and extra functionalities.

- Should we incorporate private channels to the design?
  - No, let’s not focus on private channels or the access control behind them

- Should users be able to see if other users are online?
  - Yes

- When we open the Slack / Discord app, we can see the channels with unread messages and unread mentions, where the channel with the unread messages / mentions are in bold, and have the number of unread mentions visible next to the channel name. Should our design incorporate this?
  - Yes, the design should add this. Also, we’ll want cross-device synchronization. Unread messages and		mentions should show in both the web and mobile app, and if on one device the messages are read, the		other device should synchronize and get updated when you’ve read those messages.

- Are we designing the various frontends for the web and mobile apps, or are we also designing the backend that will communicate with the frontends?
  - Focus only on the backend systems

- There are additional features for Slack messages, such as adding custom emojis, attachments, pinning messages, saving messages, writing code snippets, etc. Should we include this?
  - No, treat all messages as plain text. Also, let's ignore attachments in this design

- How many users will there be? How large is the largest organization on Slack? How many users does the largest channel have?
  - Slack has about 20M users. 
  - Let’s say the largest single Slack customer has 50k users in the same organization. 
  - We can also approximate that the largest channel has 50k users from the largest organization - all of them will likely be in the typical #general channel.

- For a chat app, low latency is a top priority, in addition to consistency in keeping the messages ordered. Is this correct?
  - Yes, low latency is a top priority, but consistency should also be focused on. But let's first focus on the core design before diving into the scalability of the system

- Are we building this at a global level, or focusing on a single region?
  - Let’s focus on a single region, and not worry about optimizing for availability at a global level.

### Functional

- Should support core messaging functionality for one-one and group channels:
  - There will be different organizations, and channels inside the organization, as well as one-one chats. Users could be in these		channels or one-one chats
  - Users can send and receive messages	
  - Load the most recent messages (both unread and seen) when the user clicks on a channel
  - Notify users of unread messages / mentions (the channel with unread messages / mentions should be bolded in the UI) and number of unread mentions when users open the app
  - Support cross-device synchronization
  - Keep all messages as plain text
  - Online presence should be shown

<br/>

- 20M users
- Maximum of 50k users in an organization and channel

### Non-functional

- Low latency:
  - Low latency in message delivery (~500 ms)

- Throughput:
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

## Slack 101

The system can be divided into 2 main parts:

- Handling what happens when a Slack app loads:
  - The first part can be further divided as follows:
    - Displaying all the channels the user is a part of
    - Displaying what channels have unread messages / mentions, and how many unread mentions are there
    - Displaying messages for a channel the client clicks on

- Handling real-time messaging and cross-device synchronization:
  - Sending / receiving messages in real time
  - Cross-device synchronization in real time

## Data model

- Note that chat apps are usually 1 : 1 in real-write ratio

- We could use a local based unique ID for all the IDs such as via Redis if the chat app operates in a small-moderate scale. However, if operating in a global scale, we can use Twitter Snowflake

<br/>

- Messages:
  - This entity will store messages for both one-one chats and channels. Also, as some messages may be very old, they could be stored in a separate cold storage, separated	from the frequently accessed messages.
  - Either the messageID could be used to sort the messages on the client side if using	a numeric timestamp value such as UNIX within the ID (Twitter snowflake provides	this) OR the sentAt can be used to sort the messages on the client side. Additionally, the frequently accessed channel’s messages		could be cached both on the server and client side via a TTL for low latency.
  - When userIDs are mentioned in the message, we can also store the userID in the mentions list

	- messageID
	- channelID
	- userID
	- message
	- mentions: [ userID ]
	- sentAt

- Channels:
  - A single row contains the channel info.
  - To check if a user has any unread messages or mentions, we can have a lastActive field in this table which updates when any user in the channel sends a message. Note that mentions will also be in messages. When a user opens the app, we'll use the channelID and compare the lastSeen field in the Channel users table against the lastActive field in this table. If the lastSeen is before the lastActive, then there are unread messages / mentions for the user in the channelID - we'll bold the channel in the UI.
    
	- channelID
	- orgID
	- name
	- lastActive

- Channel users:
  - A single row contains a user within a channelID
 
  - The lastSeen field will be the last timestamp at which the user had opened the channelID. We'll use lastSeen to render the messages as "unread" or "read" on the UI. As soon as the user opens a specific channelID, their lastSeen will update and the messages will be rendered as "read" instead of "unread".
 
  - The lastSeen timestamp can also help us find the number of unread messages a user has for a specific channelID. The lastSeen field can be compared against the sentAt time of the messages in the Messages table, and a count of the message entries after the lastSeen timestamp can be returned to the user as the count of "unread" messages.

  - We can also use the lastSeen time to find the number of unread mentions in a channel. When checking for the unread messages when the user opens the app (where the lastActive time in the Channels table is after the lastSeen time), we'll check which of these unread messages have mentions of the userID. We'll return the count (via the API endpoint) of the unread messages with mentions - which will be the number of unread mentions for the channel.

	- channelID
	- userID
	- lastSeen


- Users:
	- userID
 	- userName, userEmail
  	- userStatus
  	- lastOnline


- Devices:
  - Since a user could have multiple devices, this entity will store all deviceIDs belonging to a userID
  	- deviceID
   	- userID

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed messages quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

- Note that we’ll use a combination of HTTP and websocket requests, where HTTP requests will be sent for workloads not requiring a bidirectional component, such as creating a channel, getting messages, etc. Websocket requests will be sent for sending / receiving messages in real-time

- Note that the requests in the API are split into the HTTP and websocket requests. This is to separate the stateless operations (HTTP) from the stateful operations (websockets), as they could be scaled independently via the API servers and Channel servers respectively. Also, splitting the operations will make debugging easier where different operations are handled by different components.

### HTTP requests

#### Get channels

- We could set the nextCursor value to the viewport's oldest lastActive time, such that the next paginated results will have channels which were active after the viewport's oldest lastActive time

Request:
```bash
GET /organizations/:orgID/channels?nextCursor={ viewport's oldest lastActive time of channel }&limit
```
Response:
```bash
{
  channels: [ { channelID, name } ],
  nextCursor, limit
}
```

#### Create a channel

Request:
```bash
POST /organizations/:orgID/channels
{
  channelUsers: [ userIDs ],
  name
}
```

#### Get messages

- Fetches all messages (as well as unread messages) when the userID opens the channel:
  - If the user has unread messages in this channel, then the nextCursor value will be the client's "last active" time, which will specify the last time the client was online. This "last active" time will likely be stored in session storage on the client-side. If this last active time is not in the session storage, we could instead use the lastSeen field from the Channel users table as the cursor value, and return a paginated list of the messages which are newer than this lastSeen field.
  - If the user does not have unread messages in this channel, then the nextCursor value will point to the viewport's oldest sentAt time for the message. This way, the next paginated result will contain the messages which are older than the viewport's newest sentAt time, since we'll be returning older messages as the user is scrolling up.

Request:
```bash
GET /organizations/:orgID/channels/:channelID/messages?nextCursor={ client's "last active" time OR viewport's oldest sentAt time for message }&limit
```

Response:
```bash
{
  messages: [ { messageID, userID, message, sentAt, mentions: [ userIDs ] } ],
  nextCursor, limit
}
```

#### Add / remove users to the channel

Request:

```bash
POST /organizations/:orgID/channels/:channelID?op={ ADD or REMOVE }
{
  userID
}
```

<br/>

Additional endpoints:

- Getting unread channels / mentions count:
  - getUnreadMessagesCount(channelID) (the endpoint can be called checkIfChannelHasUnreadMessages if we just want to check if the channel has unread messages instead of getting the count of unread messages)
  - getUnreadMentionsCount(channelID)
 
<br/>

### Websocket requests

#### Upgrade connection to websockets

- This endpoint will be used to establish the websocket connection. The			Sec-WebSocket-Key header will be a value that the server will use to generate a		response key to send websocket requests. The Sec-WebSocket-Version will be the	websocket protocol version, usually 13.

Request:
```bash
GET /organizations/:orgID/channels/:channelID
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
WS /organizations/:orgID/channels/:channelID/messages
SEND {
  message
  mentions: [ userIDs ]
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

### L4 Load balancer

- We’ll need an L4 load balancer to support traffic at the TCP level. L4 load balancers,	let’s say using ELB in TCP mode can load balance websockets. When client’s need to	connect to a Channel server, the L4 load balancer will route them to the Channel server they	previously connected to or to a Channel server using the load balancing algorithm.		However, if a Channel server goes down, the L4 load balancer can route the client to		connect to another Channel server instead.

- When a client needs to connect to the Channel server, the request will first go to the L4	load balancer, then to the Channel server. There will actually be a symmetric websocket	connection between both the client to the L4 load balancer, and between the L4 load	balancer to the Channel server.

- L4 load balancers can be stateful and use sticky sessions to persist the server the	client previously connected to. The sticky session can be implemented by identifying	the user, usually with cookies or their IP address, and storing the user’s connected	server for handling future requests.

- If clients disconnect from a Channel server, they can automatically reconnect to the		same Channel server or another one via the L4 load balancer. Reconnecting to the same	Channel server may be easier, as the session data in the L4 load balancer doesn’t have to	be updated.

### API servers

- The API servers will handle CRUD based operations for users, channels and messages which don’t directly involve or 	require bidirectional communication between two users. These operations can include retrieving all the user’s channels and	unread message / mentions indicator when the app first opens, retrieving a paginated view of a channel’s messages,	adding a user to a channel, etc.

- The idea is that the client will use the API servers to retrieve their paginated		messages when they first open a channel, and they will use the Channel servers to send /	receive messages from then onwards after a websocket connection is set up.

#### API servers viewing all channels, all messages in a channel, and viewing all users in a channel

- The API servers can also be used to view the channels from the Channels table via channelID,	and view all the userIDs in the channel by filtering on the channelID from the Channel users		table. We can also view all the messages for a channelID from the Messages table using the API servers.

- Since these operations will be done frequently, we can add a GSI on DynamoDB on the Messages table, where the partition key is the channelID and the sort key is the sentAt. We'll do this to return the messageIDs sorted by the sentAt for a single partition containing the channelID. Also, we can add another GSI on the Channel users table, where the partition key is the userID and the sort key is the lastSeen field. This will help in finding the channelIDs a single userID belongs to when we'll return the channels the userID is in when the user first opens the app (we'll also use the sorted lastSeen fields to return channels with unread messages first in a sorted order when returning the channels).

### Channel servers
  
- The client will maintain a websocket connection with the Channel servers to send messages to other clients. The Channel servers will store the messages in the Messages table, and also forward the messages to the appropriate		recipient. The websocket connection could initiate when the client opens a channel. The Channel servers could forward messages to the appropriate recipient via Redis PubSub. Upon receipt, the recipient can send an acknowledgement back to the sender via Redis PubSub.

- Thus, if any messages are lost in Redis PubSub, due to let’s say the recipient not	being subscribed, the messages will still be persisted in the Messages table

- We’ll use a websocket connection as opposed to a HTTP connection (hanging GET), polling, etc, because it offers a	bidirectional communication between the clients. When a client sends messages via HTTP, the connection will need to be	re-opened on every request / message, as opposed to a websocket.

- It's possible to connect clients directly via a peer-to-peer connection like WebRTC, which will reduce the load on the	servers. However, without a mediator such as a server in between the clients, clients have an easier way of attacking	the app or other clients as there are no servers handling the security.

### KV store / cache

- A KV store could store the messages, channels, channel users, user / device profiles data.	A KV store	will be suitable here as the data type is relatively simple and will be		frequently accessed. There will likely be equal number of reads and writes happening	and so a KV store such as DynamoDB will be used here. 

- DynamoDB follows a primary-secondary model where it can be used for both read	and write intensive tasks. Also DynamoDB is optimized for low latency reads / writes	via eventual consistency, providing both LSIs and GSIs indexing, and using SSDs - 	which will be beneficial for read latencies

- Note that both Facebook / WhatsApp and Discord use KV stores such as Mnesia to	temporarily store messages as well

#### Cache

- As only recent messages may be accessed, a cache will also be suitable in storing	the recent messages. Redis could be used here as it provides complex data		structures such as sorted sets which will be needed to store the messages.
- We can cache on the browser side or use Redis to cache static data for users and	channels, and cache messages on the client-side or server-side using a short lived TTL of 15-20	mins or so as they likely won’t be viewed repeatedly.



### Message delivery from one Channel server to another Channel server

Because we'll have users in the same channel connected to different Channel servers, to deliver messages from one Channel server to another Channel server, we can do the	below and in ‘Message delivery between Channel / Chat servers’:
- Keep a Kafka topic per user / channel:
  - This approach mainly won’t work because Kafka is not built for billions of			topics (chat apps usually have billions of topics), and it will carry too much overhead for each topic, which may be			50 KB in size. This will result in terabytes of data to maintain for the Kafka			topics.

  - Kafka is not optimal for short lived “micro topics” which are needed for a			chat app, where there can be numerous topics for channels, users, etc, and			subscribers	 can subscribe or unsubscribe at any point. 

  - Redis PubSub is a lightweight solution which may be more appropriate	for message delivery between Channel servers, since only currently			subscribed subscribers will receive any messages sent to the topic.

- Consistent hashing of Channel servers:
  - By using a separate service discovery service using ZooKeeper to keep			track of which clients should connect to which Channel servers, there will still			be an overhead of maintaining those mappings during both disconnections			and scaling events. Clients may frequently disconnect then reconnect to			different Channel servers, and all of this will need to be maintained and				updated in service discovery, which will be complex to handle. Additionally,			during scaling events in consistent hashing, Channel servers will handle a 			different set of clients in the hash ring - thus the mappings in ZooKeeper			will need to be updated frequently during scaling of Channel servers.

- Offload to Redis PubSub:
  - Redis PubSub can maintain a lightweight hashmap of websocket 				connections. With Redis PubSub, a subscription can be created for an			userID / channelID, and messages can be published to that subscription which will be			received at-most-once by the subscribers.

  - Receiving messages from other clients:
    - When recipient clients connect to the Channel server, the Channel server will			subscribe to the sender userID’s / channelID’s topic via Redis PubSub. Any			messages published to that sender userID’s / channelID’s topic will be				forwarded to the recipient client by the recipient’s Channel server (since the			Channel servers are currently subscribed). 

  - Sending messages to other clients:
    - The Channel server of the sender userID / channelID will publish the message to			their topic. Any currently subscribed recipient Channel servers will receive that			message published in that topic. The recipient Channel servers can then				deliver the message to the appropriate recipient userIDs.

- Message queues for 1-1 chats:
  - We could also place message queues between Channel servers only for 1-1 chats		as there is one producer and consumer only. The mapping between the Channel 		servers to the message queues will be maintained in the Channel servers				themselves (as they’re stateful) or maintained in service discovery. However, 		maintaining the client to server mappings in service discovery will be an			overhead, as clients will frequently disconnect and reconnect to different Channel		servers.

  - The message queues will follow a strict order, or a best effort ordering using		the sentAt field for the message OR using the messageID 			generated via a sequencer such as Twitter snowflake which increases the ID		values with time.

#### Redis PubSub

- The topic represents the sender userID in a 1-1 chat, and the channelID in a			channel in this approach

- Redis PubSub is lightweight and is an at-most-once delivery, which means that it			doesn’t guarantee message delivery. If there’s no subscribers listening,			then the message will be lost, and stored in the Messages			table. 

- Redis PubSub is appropriate for this design because it sends messages	only when there are currently subscribed Channel servers, and if there are no	subscribed Channel servers, then the message is not received. This is a mock	of how a chat app operates as well.

- One issue with this approach is that there is an all-to-all relationship		between Channel servers and Redis cluster servers, where we’ll need		connections for all those relationships. However, Redis PubSub is much more	lightweight than Kafka, and will not take up as much bandwidth. 

#### Redis cluster

- Topics will also be distributed across nodes within a Redis cluster.

- Also, the Redis clusters could also be replicated - when one cluster is down, another replica can still receive from / send to subscribed Channel servers. There may be overhead in replication of Redis clusters, however Redis PubSub is more lightweight than most queue solutions (due to it’s at-most-once delivery) such as Kafka and SQS, thus it will be less complex in replicating it since there’s less persisted data to replicate.


### Service discovery

- The service discovery is used to route the client to an appropriate Channel		server using their geographic location, the server capacity, etc to initiate the			websocket connection.

- Zookeper is frequently used for service discovery. This service essentially maintains a mapping of the userID : channelServerID, which can be maintained in a KV	store such as ZooKeeper. Zookeper can register all the		Channel servers and their info in a KV store, and find an appropriate server for the client	based on some criteria. Zookeper can also maintain the ports on the Channel servers that	clients will connect to in order to establish a websocket connection

- After the user logs in, the service discovery service gives a list of DNS host names to	the Channel servers that the client could connect to. This is done only once every time the	user logs in. Every time afterwards when the client	opens the app, the API servers will use this service discovery service to find the Channel server to connect to from the		mappings. Zookeper will maintain the mapping between the Channel servers,	ports and	users so that they can reconnect to the same Channel server. When the user disconnects,	and reconnects to a new Channel server, the service discovery service will update this	mapping.

- By using a separate service discovery service using ZooKeeper to keep			track of which clients should connect to which Channel servers, there will still			be an overhead of maintaining those mappings during both disconnections			and scaling events. Clients may frequently disconnect then reconnect to			different Channel servers, and all of this will need to be maintained and				updated in service discovery, which will be complex to handle. Additionally,			during scaling events in consistent hashing, Channel servers will handle a 			different set of clients in the hash ring - thus the mappings in ZooKeeper			will need to be updated frequently during the scaling of Channel servers.

- This design will not use a service discovery component, as we’ll use Redis PubSub	which is lightweight and thus will allow all the Channel servers to directly connect to the	Redis clusters.


### Presence servers

- The presence servers manage the online/offline status of the clients. Clients can	send periodic heartbeats to the presence servers (let’s say every 10 mins) for		the presence servers to update their online / offline status

### Notification service

- This service will use third party notification services like mailchimp, SNS, SES, APN,	android push notifications for generating notifications

<img width="600" alt="image" src="https://github.com/user-attachments/assets/d34faf8e-0b37-43f8-9db8-3a8dd2096487" />


## DD

We’ll dive deep into some parts of the system:

### Online presence

- Presence servers will update the KV store of the lastOnline timestamp via HTTP when users login or logout
	
- If a user disconnects, the websocket connection will be lost. It is also common for users to disconnect and then reconnect frequently in	unstable network conditions, therefore frequently changing the lastOnline timestamp will not be useful. We can have the client send		periodic heartbeats (every 10 mins) to the presence servers to update the lastOnline timestamp. If the client has disconnected and		hasn't sent the heartbeat, the presence servers will set the client as offline in the KV store.

- Via Redis PubSub, friends / connections of users who are subscribed to their friend’s topics could also receive updates on the friend’s presence when	they go offline or come back online. Presence could also be fetched only for the usersIDs within the viewport via lazy loading.

- Also, friends of users could also subscribe to the presence servers of the user to receive updates on the friend’s presence as shown in ‘Online presence subscription’. If we're using Redis PubSub, friends of users could subscribe to the user's topic, and when the user logs in / out, that user will send a message to the subscribed friends / connections of their topic

<br/>

Online presence subscription:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/96e2a094-81ea-4c3a-a8d7-57ae83aff9cf" />

### Device synchronization

- To ensure device synchronization, where if a user views their messages on their laptop, it should be registered as “read” on their mobile	device as well - we’ll use the Devices table which contains deviceIDs for each userID. Instead of relying on the userID for sending /		receiving message operations, we’ll use the deviceID to differentiate between devices belonging to a user.

- Channel servers will subscribe to a topic with the deviceID instead of userID. This also means that each deviceID will instead	establish a websocket connection to the Channel servers instead. This way, a message will be sent to all the	devices of a user. A device limit	can also be introduced for a single user.

- To ensure device synchronization, where read receipts on the laptop should be immediately registered on mobile - when the deviceID	has sent the acknowledgement that they’ve read and received the messages, their lastSeen timestamp in the Channel users table will		update to the current time. After the lastSeen timestamp updates, the UI should render the messages as “read” on page refresh for all deviceIDs belonging to the userID.

- If we want read recipients on the laptop to immediately register on mobiles without having to refresh the page, then when a userID reads a message on one device, their read receipts could also be sent as a separate message to all the other deviceIDs belonging to this userID via the websocket connection. This way, the client doesn't have to refresh their page, and can receive read receipts from any of their devices using the websocket connection.

### Message delivery status

- The message delivery status on the client side will change depending on where the message currently is. 

- After the client sends a message to the Channel server, the Channel server will send an acknowledgement back to the client and mark the		message as “Delivered”.

- After the message reaches the Redis cluster and is forwarded to the other client or Notification servers, the			message status will be marked as	“Sent” after the Channel server sends an acknowledgement back to the client.

- Once the other client has seen the message on their viewport, the other client will send an acknowledgement to the Channel server, and		the Channel server will subscribe and send to the recipient userID’s topic / message queue to mark the message as “Seen”.

### Database sharding

We can shard the database tables in the following ways:

#### Partitioning based on userID

- Because we have many tables which have userID, a single shard could represent a hash range for the userIDs. When a new 			entry comes in, the hash value of the userID could be mapped to a specific shard via consistent hashing with the hash range. This		way, entries such as messages for the same userID are within a single shard, and can be easily accessible. 

#### Partitioning based on messageID

- If we partition by messageID, where different messageIDs for a single userID are distributed across shards, then fetching the			messages for a single userID will be very slow - thus this approach is not appropriate.

####  Sharding based on orgID and using a Sharding service to monitor organization size

- As these tables may be large, especially the Messages table, we may need to shard the tables. We could use	the orgID and channelID to shard the tables, where larger organizations will take up more shards than smaller			organizations. However, organization and channel sizes may double overnight, due to acquisitions etc, which may		create a SPOF. To handle rebalancing shards, we can add a Sharding service that will asynchronously measure		organization activity within channels and rebalance the shards accordingly when an organization’s number of users		grows rapidly.

- The Sharding service to measure organization activity and user counts to perform rebalancing using a KV store like		ZooKeeper, which maintains a mapping of the orgID : [ shardIDs ]. The API servers will also communicate with this		Sharding service to route requests to the appropriate shardID.

### Database replication
  
- Additionally, we can replicate the database tables / shards to prevent a SPOF


