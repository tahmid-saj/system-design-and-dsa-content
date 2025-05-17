# Twitch / Hotstar livestreaming

We will design Twitch (and Hotstar) which allows users to watch a live-stream and view / respond to live chat messages. Note that this design is similar to the SDIs 'YouTube', 'Netflix', 'Chat app' and 'FB live comments'

## Requirements

### Questions

- A user can watch the streamer’s livestream (and pause / unpause it), they can see the stream’s chat in real time, send messages in the chat, see the streamer’s channel info, follow / unfollow the streamer, subscribe / unsubscribe from the streamer (they have to pay to subscribe), can see the current number of viewers on the stream, can also see other recommended channels that they follow on the left navbar. Should we design all of this?
  - Yes, but ignore the recommended channels on the left navbar. Focus only on the functionality relevant to	the livestream.

- For subscriptions, a user subscribes on a monthly basis for a monthly fee, is this correct?
  - There might be different tiers of subscriptions - you can capture that in a SubscriptionInfo entity that you	don’t need to explicitly define.

- Info in a livestream will get updated very frequently, ie follower count, current watcher count, chat messages, livestream video, etc. Should we design the system with real-time updates in mind?
  - Let’s make sure the video and chat are updated in real-time. Let’s update the current watcher count every	30 secs or so, and update the current follower count only during page refreshes.

- Do we want to display on the page if the user is currently following / subscribed to the streamer? And update the UI immediately if the user clicks “follow”, “subscribe”, “unfollow”, “unsubscribe”?
  - Yes, the UI should show this and update immediately

- Users can send custom emotes and cheermotes in chats via Bits, Twitch’s virtual currency. Should we handle these emotes / cheermotes? Should we also handle chat bans and the presence of chat moderators?
  - Yes, let’s handle basic emotes that are available to all Twitch users, but disregard custom emotes / 		cheermotes that are available to subscribers. Disregard Bits and chat moderators as well. But include the	chat banning feature. If a user is banned from the chat, they can’t send messages, but they still need to be	alerted.

- What devices do we need to support?
  - Mobile, web and smart TV
 
- Do we need to support global users?
  - Yes a large percentage of users are global

- Should we support different video resolutions and formats?
  - Yes
 
- Can we leverage existing cloud services such as CDNs?
  - Yes

- Should users be able to view chat messages before they joined the livestream?
  - Twitch doesn't provide this, but let's include it

- Do we want to support searching for streamers?
  - For simplicity, let's ignore this

### Functional

- In out API, we'll design endpoints a user uses when they’re on a specific streamer’s channel page, watching their livestream:
  - Channel info endpoints:
    - Users can visit the streamer’s channel and see the streamer’s name and description
    - Users can see the streamer’s follower (on page refresh) / current livestream watcher count (every 30 secs)
  - Livestream endpoints:
    - Users can watch the streamer’s livestream (pause / unpause it) (real-time)
  - Chat endpoints:
    - Users will get real-time updates on the chat (real-time)
    - Users can also see messages posted before they join the livestream
    - Users can send chat messages (real-time)
    - Chats should support basic emotes
    - Chats should support banning users, and users should be alerted
  - Folloing / subscription endpoints: 
    - Users can follow / subscribe / unfollow / unsubscribe to a streamer (should update UI immediately)

<br/>

- The system should also allow a streamer to live-stream their video and audio content:
  - We should support video encoding / transcoding to various resolutions and codecs, and manageable formats

<br/>

- The app will be used in web, mobile and smart TV, and will be a global app
- A single livestream can reach 1-3M watchers, but will be on average in the hundreds or thousands.

### Non-functional

- Availability > consistency:
  - If we have a strongly consistent system, we may expect higher latencies, thus the system could prioritize availability + low latency over consistency
- Throughput:
  - Users should be able to stream video data efficiently
  - The system should also handle high throughput for sending and receiving messages
- Low latency:
  - Streaming and viewing live messages should have low latency
- Durability:
  - Videos and metadata should be durably stored

  



## Video streaming 101 (taken from YouTube 101)

### Encoding

- Encoding involves compressing the raw video into a more manageable format via compression so that it is easier to stream. Encoding may sometimes be lossy, meaning that some of the original video data is lost

### Transcoding
  
- Transcoding involves taking an already compressed or encoded video and converting it to		multiple formats, resolutions or bitrates so that it is compatible with different devices.			Transcoding involves decompressing and compressing the video in different formats,			resolutions or bitrates. Transcoding is used to adapt the video to different network qualities		and devices.
- To transcode an input video, we’ll have a matrix containing different resolution-codecs combinations. The raw video should be transcoded to all of these different combinations to have the best experience. However, transcoding to any uncommon resolutions and codecs may not always be needed.

- Also, video quality can depend on both resolutions and codecs

### Video codec

- A video codec is an algorithm which compresses and decompresses video, making it more efficient for storage and transmission. Codec stands for “encoder and decoder”. Codecs will reduce the size of the video while preserving quality. Codecs may have the below trade-offs:
  - Time required to compress a file
  - Codec support on different machines
  - Compression efficiency
  - Compression quality - if it is lossy or lossless

- Some popular codecs include: H.264, H.265 (HEVC), VP9, AC1, MPEG-2, MPEG-4

### Video container

- A video container is a file format / space that stores video data (frames, audio, etc), and metadata. A video container may store info like video transcripts as well. Codecs determine how a video is compressed / decompressed, whereas a video container is a file format for how the video is actually stored. Supported video containers varies by devices / OS. The video container could have file extensions like mp4, avi, mov etc

### Bitrate
  
- Bitrate is the number of bits transmitted over a period of time (usually in kbps / mbps). The video size and video quality affects the bitrate. High resolution videos with higher framerates (measured in FPS) have much higher bitrates than low resolution videos at lower framerates. This is because there’s more video data to transfer. Compression via codecs may also affect the bitrate, since more efficient compression algorithms can lead to much less video data that needs to be transferred.

### Manifest files

Manifest files are text based files that give details about video streams. There’s usually 2 types of manifest files:

- Primary manifest files:
  - A primary manifest file lists all the available versions and formats of a video. The primary is the “root” file and points to all the media manifest files
- Media manifest files:
  - Media manifest files each represent a different version or format of the video. A video version or format will be split into small segments of a few seconds. Media manifest files list out the links to these segment files, and will be used by video players to stream the video by serving as an “index” to these segment files

### Video format
  
- A video format will usually represent both the video codec and video container being used

### Streaming protocols

- Streaming protocols are a standardized way to control data transfer for video streaming

- Popular streaming protocols are:
  - MEGA-DASH
  - Apple HLS (HTTP livestreaming)
  - Microsoft Smooth Streaming
  - Adobe HTTP Dynamic Streaming (HDS)

### FFMPEG

- A naive approach to encoding / transcoding can be done using FFMPEG, which is a command line tool that can convert video and audio to different formats and resolutions. It can also transform the video and audio in real time.

### RTMP

- We can use RTMP (Real time messaging protocol), a common protocol for livestreaming video, audio and additional metadata across the internet. RTMP uses a continuous TCP connection to stream video and audio fragments from a source to a single destination. It is often used in livestreaming services, because it can maintain persistent connections and causes minimal buffering and low latency.

- In RTMP, the data is split into fragments, and their size is negotiated dynamically between the client and the server performing the encoding / transcoding. TCP also has ordering, and acknowledgements of packet delivery, which is utilized in RTMP to correctly order the livestreaming fragments. Additionally, as RTMP uses TCP, there is no data loss, unlike UDP.




## Data model / entities

- Channels:
  - This table will contain static data about the streamer / channel
	
	- channelID
	- name, description
	- currentStreamInfo: { title, currentWacherCount }
	- followerCount

- Channel users:
  - This table will contain the users who are following / subscribed / banned from the channelID. If a userID doesn’t meet this	criteria for a specific channelID (the userID is not following / subscribed / banned from the channelID), then the userID and		channelID pair will not appear in this table.

  - Storing the users within a channel in this table is a better approach than storing this user-channel relationship info in a list within the user’s profile		table, because a user can follow / subscribe / banned from hundreds or thousands of different channelIDs, and we’ll	need to	parse through all those channelIDs within the list

	- channelID
	- userID
	- isFollowing: boolean
	- subscriptionInfo: SubscriptionInfo entity
	- isBanned: boolean

- Livestream:
  - This entity is the livestream that is being broadcasted by a userID, and which messages will be posted to
  	- streamID
   	- userID
    	- title
     	- s3URLs
      	- fingerprint
      	- createdAt

- Chunks:
  - chunkID
  - streamID
  - chunkStatus: enum UPLOADED / NOT_UPLOADED / FAILED
  - fingerprint

- Messages:
  - This table contains all the messages for a specific streamID sent from a user

	- messageID
	- streamID
	- userID
	- message
	- sentAt




## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

<br/>
<br/>

Livestreaming endpoints:

### Stream a video

- When streaming binary content using HTTP, application/octet-stream can be used to receive	binary data

- The application/octet-stream MIME type is used for unknown binary files. It preserves the file	contents, but requires the receiver to determine file type, for example, from the filename		extension. The Internet media type for an arbitrary byte stream is application/octet-stream.

- The */* means that the client can accept any type of content in the response - which could also	be used for sending / receiving binary data

- Note that to stream files, we could use either a pre-signed URL or a URL the client can request	to download from the CDN (let’s call it CDN URL). The process is similar to uploading videos,	where the client first requests the servers for a pre-signed	URL OR CDN URL, then the client will	stream the video from the pre-signed URL / CDN URL.

- Note that we’ll also request for a specific pre-signed URL / CDN URL for a segment / timestamp using the device and video format info such as codec and resolution (to support different devices and video formats)

#### Request for a pre-signed URL / CDN URL

- Note that we'll also specify the segment OR the user's last watched timestamp to stream the video from

- When this endpoint is invoked, the API servers will increase the currentWatcherCount of the streamID in the	Channels table. If the user exits the stream by		closing the tab, the websocket connection will be closed and the currentWatcherCount field for the	stream will be			decreased.

- When the user pauses the video, the client will still stream the video and receive real-time video content and store it			temporarily, likely in a client-side database, but will simply not display it on the screen until they unpause the video.

Request:
```bash
GET /channels/:channelID/live-stream/pre-signed-url OR cdn-url?<segment OR timestamp>&codec&resolution
```

Response:
```bash
{
  pre-signed URL or CDN URL
}
```

#### Stream from pre-signed URL / CDN URL

Request:
```bash
GET /<pre-signed URL or CDN URL>
Accept: application/octet-stream
```

- The response body contains the video chunks. The chunks can also be returned			using multiplexing via HTTP/2.0. Multiplexing will allow the client to send requests for the		chunks of a video, then the server will send the responses	 containing the video chunks in		any order. The returned chunks can be used to reconstruct the video on the client side.

Response:
```bash
Content-Type: application/octet-stream
Content-Disposition: attachment; filename=”<FILE_NAME>”
{
  video’s binary data used to generate the file on the client side
}
```

### Get currentWatcherCount

- Getting the current watcher count for a stream can be done with the client polling the API servers every 30 sec or so. The	API servers will then return the currentWatcherCount from the Channels entity.

Request:
```bash
GET /channels/:channelID/live-stream/currentWatcherCount
```

Response:
```bash
{
  currentWatcherCount
}
```

<br/>
<br/>

Chat endpoints:

### Websocket endpoints

- We will likely use websockets to send and receive messages, however we could either use polling vs SSE vs websockets. We'll discuss in the HLD why websockets might be more suitable here.

#### Upgrade connection to websocket

- This endpoint will be used to establish the websocket connection. The			Sec-WebSocket-Key header will be a value that the server will use to generate a		response key to send websocket requests. The Sec-WebSocket-Version will be the	websocket protocol version, usually 13.

Request:
```bash
GET /channels/:channelID/live-stream
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

- The API servers will verify if the userID is banned before sending the message to the chat
- Basic emotes can also be represented using a special string format, “:<emoteID>”, and receiving clients’ UI will register		this format as an emote, and style it as such.

Request:
```bash
WS /channels/:channelID/live-stream/messages
SEND {
  message
}
```

Response:

- We can also receive messages

```bash
RECV {
  userID
  message
  sentAt
}
```

### Get past messages

- The nextCursor will be set to the viewport's oldest sentAt value of the messages. This way, as the user is scrolling up, in the next paginated result, we'll return the messages which are older than the viewport's oldest sentAt value

Request:
```bash
GET /channels/:channelID/live-stream/messages?nextCursor={ viewport's oldest sentAt value of message }&limit
```

Response:
```bash
{
  messages: [ { messageID, userName, message, sentAt } ],
  nextCursor, limit
}
```

<br/>

- banUserInChat(channelID):
	- This endpoint will ban the userID for the channelID’s livestream chat and alert the user immediately. It will add or update		the userID’s isBanned field in the Channels users table.

<br/>
<br/>

Channel info endpoints:

### Get channel info

Request:
```bash
GET /channels/:channelID
```

Response:
```bash
{
  channelID, name, description,
  currentStreamInfo: { name, currentWatcherCount }, followerCount
}
```

### Get channel relationship to user

- This endpoint will return the relationship between the channelID and userID (if they’re following / subscribed / banned from	a channelID) using the Channels users table

Request:
```bash
GET /channels/:channelID/relationship
```

Response:
```bash
{
  isFollowing, subscriptionInfo, isBanned
}
```

<br/>
<br/>

Following / subscription endpoints:

### Follow / unfollow streamers

- The UI will update immediately when follow / unfollow / subscribe / unsubscribe is performed

Request:
```bash
POST /channels/:channelID/following?op={ FOLLOW or UNFOLLOW }
```

### Subscribe / unsubscribe streamers

- The subscribing function is similar to following, however it will accept additional fields like a SubscriptionInfo entity  which will contain the subscription tier. These two entities may be filled out via a UI form, or already stored in another database.
- Note that after this endpoint is called, the server will likely send a paymentInputURL to the client such that the client will enter their payment details in the request and complete the subscription request

Request:
```bash
POST /channels/:channelID/subscriptions?op={ SUBSCRIBE or UNSUBSCRIBE }
{
  SubscriptionInfo entity
}
```


## HLD

### Client

- The streamer's client will be uploading video data as they're streaming, and the viewer's client will be downloading video data if they're watching a livestream. Thus there will be two separate sections in the client code for an “uploader” and “downloader”:

#### Uploader

- The uploader will upload the local video chunks generated during the livestream to the blob store via a pre-signed URL
  
#### Downloader

- The downloader will likely use a client based video player developed via a SDK such as Video.js. The downloader will use websockets, WebRTC or RTMP to request for video segments via pre-signed URLs / CDN URLs 
	
Additionally, the client will contain the following internal components which will communicate with the uploader and downloader. This is also shown in ‘Client components’:

Client components:

<img width="350" alt="image" src="https://github.com/user-attachments/assets/7e1de751-fc32-400a-8d4e-f2c91a67b841" />

#### Chunker
		
- The client will also have a chunker functionality that splits the local video into chunks when uploading to the blob store, and also reconstructs the files from the downloaded video segments. 
- Note that chunks and video segments are different, in that a chunk is a fixed size part of a file, whereas a video segment will consist of the manifest files and actual segment files for a few seconds of the video

#### Client database

- To maintain the metadata for the local video and it’s chunks, we’ll store it in a client database such as Indexed DB. The client will use this client database to compare local chunks and uploaded chunks when uploading video content to the blob store.


### API servers

- The API servers will handle CRUD based requests which doesn't directly involve livestreaming, such as getting the streamer's channel info, getting messages posted before the livestream, banning users in the chat, getting the currentWatcherCount, getting the channel relationship to user, following / subscribing to a channel, etc.

- The API servers will also provide pre-signed URLs / CDN URLs for uploading and downloading video data stored in the blob store or CDN.

- Also, the idea is that the client will use the API servers to retrieve their paginated messages when they first open a livestream, and they will use the Livestream servers to send / receive messages from then onwards after a websocket connection is set up.

### Metadata database / cache

- The Metadata database will store the channels, channel users, livestream, chunks and messages data, which doesn't include the actual binary data.

- The amount of video chunks and messages being written will be great, and thus we could either use a SQL database or a highly horizontally scalable NoSQL database like Cassandra. We could choose SQL if the design is for a small to moderate scale, however the design will likely require maintaining multiple partitions and the data may also contain some unstructured pieces, such as messages, and segments of a livestream video, etc. SQL can still provide these features, but won't be optimized for them - thus, Cassandra may be more suitable. Also, Cassandra provides CQL, similar to SQL, which will be helpful for complex queries.

#### Sharding metadata DB

- We could also partition / shard the Livestream table on the livestreamID (via consistent hashing which Cassandra already implements) so that fetching data about a single livestreamID will only happen within a single partition / shard. Sharding by livestreamID is also more optimal than sharding by channelID because a single channelID could have 10s of thousands of videos, and another channelID could have just a few videos - making the shards uneven, and also might create hotspots if some channels are accessed much more frequently.

#### Livestream cache

- Also, a cache of the livestream / video metadata could be maintained using either Redis or Memcached. Since we'll likely need to cache info about the different chunks and segments of a video, likely by their timestamps or another field to help with ordering, we can use Redis sorted sets. This cache will also prevent hotspots of frequently viewed livestreamIDs by caching the metadata for those livestreamIDs.

#### Messages cache

- As only recent messages may be accessed, a cache will also be suitable in storing the recent messages. Redis could be used here as it provides complex data structures such as sorted sets which will be needed to store the messages.

- We can cache on the browser side or use Redis to cache messages on the client-side or server-side using a short lived TTL of 5 mins or so as they likely won’t be viewed repeatedly.

### Blob store

- The blob store will store the video data. The video data can be uploaded in the below ways (the Dropbox design also goes over these different options):
	- Upload file to a single server
	- Store file in blob storage:
		- A lot of the times, having the client upload the file to the API servers, then having the API servers upload to the blob store is redundant and slow especially for large files because the uploading process has to be done twice. Clients could directly upload to the blob store via a pre-signed URL, and any security or validation checks can be performed via the blob store client interfacing the blob store after the user has uploaded to the pre-signed URL.
	- Upload file directly to blob storage:
		- We can use pre-signed URLs to upload files directly to the blob store. Pre-signed URLs can be sent via the servers to the clients. Clients can then use the pre-signed URL, which may have a TTL to upload / download their files. Pre-signed URLs are explained in ‘Pre-signed URLs’.

- The video data stored in the blob store can be the following, and in ‘Video storage logic in blob store’:
  - Store the raw video
  - Store different video formats
  - Store different video formats as segments	

- When users stream a video, they will request the servers for the video metadata and appropriate pre-signed URLs / CDN URLs to fetch the video data. The video data can be streamed from these URLs as follows and in ‘Streaming video from blob store’:
  - Download the video file
  - Download segments incrementally
  - Adaptive bitrate streaming
 
- Note that both the raw chunks (raw chunks are received directly from the streamer) and		transformed segment files could be stored in a blob store for persistence. The DD will discuss more on the Video processing service which will handle transforming the raw chunks into segment files for various video formats, so that it can be viewed by other users.

### Livestream servers

#### Livestream servers handling livestreaming

- Clients could connect to the Livestream servers via HLS, DASH, RTMP, WebRTC, etc. Client’s could	also directly connect to the POPs, as CDNs will provide catered functionality for streaming content to	clients using different streaming protocols.

#### Livestream servers handling live messages

- Also, the client will maintain a websocket connection with the Livestream servers to send messages to other clients. The Livestream servers will store the messages in the Messages table, and also forward the messages to the appropriate recipients via Redis PubSub. Upon receipt, the recipient can send an acknowledgement back to the sender via Redis PubSub.

- Thus, if any messages are lost in Redis PubSub, due to let’s say the recipient not being subscribed, the messages will still be persisted in the Messages table

- We’ll use a websocket connection as opposed to a HTTP connection (hanging GET), polling, etc, because it offers a bidirectional communication between the clients. When a client sends messages via HTTP, the connection will need to be re-opened on every request / message, as opposed to a websocket.

- It's possible to connect clients directly via a peer-to-peer connection like WebRTC, which will reduce the load on the servers. However, without a mediator such as a server in between the clients, clients have an easier way of attacking the app or other clients as there are no servers handling the security.


### Video processing service

- The Video processing service will consist of a post-processing DAG which will be run when a user uploads chunks of a video. The source for the livestreaming, which will be the streamer, will send chunks of video / audio / metadata, likely using websockets, WebRTC, or RTMP to the blob store. The Video processing service will then transform the chunks into segments for different video formats, and store it in the blob store.

- The Video processing service may contain a message queue either with SQS or Kafka to maintain a list of tasks it needs to execute for different video chunks / segments, such as transcoding the video / audio / transcripts, and also creating the manifest files. Thus, there could be a temporary message queue for each video being uploaded. 

- The message queue could also be maintained via an in-memory cache such as Redis which contains the queued tasks, and the task’s status (COMPLETE / PENDING / FAILED).

- The video processing service will also contain the post-processing DAG and relevant workers (which could be compute optimized EC2 instances) to run the tasks, and generate the manifest files + segment files for different video formats.

- Once the video processing is done, the transformed video data will be sent to the Livestream servers and CDN for streaming the content. It's likely that viewers can expact a lag of about 15 - 30 seconds (viewer doesn't directly receive streamer's uploaded video data right away) depending on the efficiency of the Video processing service.

- The video processing service and it’s workflow is explained more in depth in the DD.


### Message delivery from one Livestream server to another Livestream server

Because we'll have users in the same chat connected to different Livestream servers, to deliver messages from one Livestream server to another Livestream server, we can do the	below and in ‘Message delivery between Livestream servers’:
- Keep a Kafka topic per user / livestream:
  - This approach mainly won’t work because Kafka is not built for billions of			topics (messaging apps usually have billions of topics), and it will carry too much overhead for each topic, which may be			50 KB in size. This will result in terabytes of data to maintain for the Kafka			topics.

  - Kafka is not optimal for short lived “micro topics” which are needed for messaging, where there can be numerous topics for livestreams, users, etc, and			subscribers	 can subscribe or unsubscribe at any point. 

  - Redis PubSub is a lightweight solution which may be more appropriate	for message delivery between Livestream servers, since only currently			subscribed subscribers will receive any messages sent to the topic.

- Consistent hashing of Livestream servers:
  - By using a separate service discovery service using ZooKeeper to keep			track of which clients should connect to which Livestream servers, there will still			be an overhead of maintaining those mappings during both disconnections			and scaling events. Clients may frequently disconnect then reconnect to			different Livestream servers, and all of this will need to be maintained and				updated in service discovery, which will be complex to handle. Additionally,			during scaling events in consistent hashing, Livestream servers will handle a 			different set of clients in the hash ring - thus the mappings in ZooKeeper			will need to be updated frequently during scaling of Livestream servers.

- Offload to Redis PubSub:
  - Redis PubSub can maintain a lightweight hashmap of websocket 				connections. With Redis PubSub, a subscription can be created for an			userID / livestreamID, and messages can be published to that subscription which will be			received at-most-once by the subscribers.

  - Receiving messages from other clients:
    - When recipient clients connect to the Livestream server, the Livestream server will			subscribe to the sender userID’s / livestreamID’s topic via Redis PubSub. Any			messages published to that sender userID’s / livestreamID’s topic will be				forwarded to the recipient client by the recipient’s Livestream server (since the			Livestream servers are currently subscribed). 

  - Sending messages to other clients:
    - The Livestream server of the sender userID / livestreamID will publish the message to			their topic. Any currently subscribed recipient Livestream servers will receive that			message published in that topic. The recipient Livestream servers can then				deliver the message to the appropriate recipient userIDs.

#### Redis PubSub

- The topic represents the livestreamID in a			livestream's chat in this approach

- Redis PubSub is lightweight and is an at-most-once delivery, which means that it			doesn’t guarantee message delivery. If there’s no subscribers listening,			then the message will be lost, and stored in the Messages and Inbox				table. 

- Redis PubSub is appropriate for this design because it sends messages	only when there are currently subscribed Livestream servers, and if there are no	subscribed Livestream servers, then the message is not received. This is a mock	of how a chat app operates as well.

- One issue with this approach is that there is an all-to-all relationship		between Livestream servers and Redis cluster servers, where we’ll need		connections for all those relationships. However, Redis PubSub is much more	lightweight than Kafka, and will not take up as much bandwidth. 

#### Redis cluster

- Topics will also be distributed across nodes within a Redis cluster.

- Also, the Redis clusters could also be replicated - when one cluster is down, another replica can still receive from / send to subscribed Livestream servers. There may be overhead in replication of Redis clusters, however Redis PubSub is more lightweight than most queue solutions (due to it’s at-most-once delivery) such as Kafka and SQS, thus it will be less complex in replicating it since there’s less persisted data to replicate.

### Video CDN

- As some users may be farther away from S3 servers, which may affect the streaming quality, we can use Video CDN POPs to cache frequently accessed video data (both segment files and manifest files). Clients can then use the CDN URLs from the API servers to stream and fetch the video data from the CDN POPs

- Usually when transporting videos or images to a client, it is done via a Video CDN such as			CloudFront or Cloudflare. Clients will establish websocket or RTMP connections to the CDN’s POPs,	and intake transformed video data delivered by the POPs. The POPs will receive the content from the	origin servers, which will likely be the S3 blob store (CloudFront allows directly streaming video data from S3).

- Because video data is static, push based CDNs will be more appropriate, where the origin servers will push the content from the blob store to the CDN POPs

- CDNs may be more expensive, but will only be necessary for a large scale app

#### Livestreaming protocols

- CDNs can use RTMP to stream video and audio to clients. This process works by establishing a TCP	connection between the client and the POPs. The client sends an RTMP request to the POP, which	then starts delivering the transformed video data.

- It is also common for clients to connect to the POPs via the HTTP livestreaming or DASH protocols.	Both of these protocols including RTMP have adaptive bitrate, where the video quality is adjusted and	sent to the client depending on their internet connection and device performance. For example, if a		client is not able to support 4K, it will request the POP to send video data at a lower video quality in		real time.

- It may be preferred to use HLS or DASH between the POPs and clients as opposed to RTMP,		because not all devices support RTMP, such as iOS devices. HLS and DASH also work over an		established TCP connection. However, when the video data is sent from the streamer to the			 blob store, it will be preferred to use RTMP to ensure no data loss via the TCP			connection as RTMP is designed for livestreaming, whereas HLS / DASH may have some data loss	depending on the client’s network.

- WebRTC is another option for the client to stream content from the POPs. It is able to transport the	video data, audio and metadata to the clients. However, WebRTC works using UDP, which is		faster than TCP, but will not ensure delivery acknowledgement or in-order delivery of the video data's segments.

### Service discovery

- The service discovery is used to route the client to an appropriate Livestream server using their geographic location, the server capacity, etc to initiate the			websocket connection.

- Zookeper is frequently used for service discovery. This service essentially maintains a mapping of the userID : livestreamServerID, which can be maintained in a KV	store such as ZooKeeper. Zookeper can register all the		Livestream servers and their info in a KV store, and find an appropriate server for the client	based on some criteria. Zookeper can also maintain the ports on the Livestream servers that	clients will connect to in order to establish a websocket connection

- After the user logs in, the service discovery service gives a list of DNS host names to	the Livestream servers that the client could connect to. This is done only once every time the	user logs in. Every time afterwards when the client	opens the app, the API servers will use this service discovery service to find the Livestream server to connect to from the		mappings. Zookeper will maintain the mapping between the Livestream servers,	ports and	users so that they can reconnect to the same Livestream server. When the user disconnects,	and reconnects to a new Livestream server, the service discovery service will update this	mapping.

- By using a separate service discovery service using ZooKeeper to keep			track of which clients should connect to which Livestream servers, there will still			be an overhead of maintaining those mappings during both disconnections			and scaling events. Clients may frequently disconnect then reconnect to			different Livestream servers, and all of this will need to be maintained and				updated in service discovery, which will be complex to handle. Additionally,			during scaling events in consistent hashing, Livestream servers will handle a 			different set of clients in the hash ring - thus the mappings in ZooKeeper			will need to be updated frequently during the scaling of Livestream servers.

- This design will not use a service discovery component, as we’ll use Redis PubSub	which is lightweight and thus will allow all the Livestream servers to directly connect to the	Redis clusters.

### L4 load balancer

- We’ll need an L4 load balancer to support traffic at the TCP level. L4 load balancers,	let’s say using ELB in TCP mode can load balance websockets. When client’s need to	connect to a Livestream server, the L4 load balancer will route them to the Livestream server they	previously connected to or to a Livestream server using the load balancing algorithm.		However, if a Livestream server goes down, the L4 load balancer can route the client to		connect to another Livestream server instead.

- When a client needs to connect to the Livestream server, the request will first go to the L4	load balancer, then to the Livestream server. There will actually be a symmetric websocket	connection between both the client to the L4 load balancer, and between the L4 load	balancer to the Livestream server.

- L4 load balancers can be stateful and use sticky sessions to persist the server the	client previously connected to. The sticky session can be implemented by identifying	the user, usually with cookies or their IP address, and storing the user’s connected	server for handling future requests.

- If clients disconnect from a Livestream server, they can automatically reconnect to the		same Livestream server or another one via the L4 load balancer. Reconnecting to the same	Livestream server may be easier, as the session data in the L4 load balancer doesn’t have to	be updated.



## DD

We'll dive deep into some parts of the system:

<br/>
<br/>

Livestream deep dives:

### Implementing adaptive bitrate streaming

- This design will use adaptive bitrate streaming to stream video data as clients will likely have changing network quality, and adaptability to different video formats is needed. As the video data is being uploaded in it’s original format, it will be post-processed to convert it to different video formats. The output of the post-processing will contain the following:
  - Segment files in different video formats stored in S3
  - Manifest files (both a primary manifest file and several media manifest files) in S3. The media manifest files will reference segment files

To generate segments and manifest files, the operations below (and in ‘Upload post-processing DAG’) will be performed within a DAG structure via the client and a separate Video processing service which will connect to S3:
1. The client will split up the original video data into chunks using a tool like ffmpeg. These chunks will then be uploaded to S3. S3 will then send a S3 event notification to a Lambda function, which will trigger the video processing service to start the post-processing. The chunks may be very small (5-10 MB) and may be combined into video segments by the Video processing service. The video processing service could also inspect the uploaded chunks in this step.
2. The video processing service will then transcode the video segments to generate the segment files at different video formats in parallel
3. The video processing service will transcode / process other aspects of the segments, such as audio, transcript, etc to also generate segment files for audio, transcript, etc
4. The video processing service will create manifest files (for different video formats), which will reference the segment files
5. We’ll mark the upload as complete, and store all the video segment files, and manifest files for the video formats in S3. The hierarchy will be as follows: video data -> primary manifest file -> media manifest files -> segment files

**Note that video segments can sometimes be known as GOP (group of pictures)**

Upload post-processing DAG:

<img width="1200" alt="image" src="https://github.com/user-attachments/assets/f12cf30e-bf33-4f87-a839-cf723cef71ae" />


- In the post-processing DAG steps, the most expensive operation will be the video segment transcoding, which can be done in parallel and on different machines which are compute (CPU) optimized such as compute based EC2 instances, since transcoding is a compute bound task.

#### DAG orchestration tool

- Building the actual DAG and it’s logic can be done using a DAG orchestration tool specific for media processing such as Temporal. Temporal can be used to build the DAG, and also to assign workers for specific steps of the DAG. 

#### S3 storing temporary data + outputs

For storing temporary data exchanged between steps in the DAG, S3 can be used so that the temporary data between steps is not lost. If post-processing is interrupted or a worker is down, another worker can fetch the temporary data from the output of the previous step and continue the post-processing. Thus, S3 will store the below for a single video:
  - Original uploaded video chunks / segments (manifest files + video segment files included)
  - A single primary manifest file
  - Multiple media manifest files referencing segment files
  - Segment files: both video segment files AND audio, transcript, etc segment files
  - Temporary data from each DAG step

#### Video streaming with adaptive bitrate streaming

- Using the post-processing logic, the video will be in different video formats. Thus clients can request for pre-signed URLs / CDN URLs for video segments at a specific video format depending on their network quality and video quality settings. The returned video segments’ video formats may also change over time, but the system now returns segments catered to the client.


### Scaling servers and storage 

#### API servers

- The API servers are stateless and will provide pre-signed URLs / CDN URLs, and also update the metadata database. It can easily be horizontally scaled.

#### Metadata database

- The Metadata database will use Cassandra, which is optimized to be horizontally scalable by following leaderless replication and internal consistent hashing. Availability is thus prioritized over consistency in Cassandra. If more leaderless nodes are needed, they could be added. However, if a node contains a popular livestreamID, it might become a hotspot.

- If a livestreamID does become a hotspot, Cassandra can be tuned to replicate the livestreamID’s data to a few extra nodes, so that it can handle the read intensity for that videoID.

#### Video processing service

- The Video processing service will be stateless, and can also be easily scaled horizontally. As the Video processing service will have many tasks for a single video, it can manage them via a message queue such as a SQS standard queue. SQS standard queues guarantee that messages are delivered at-least-once, and also can guarantee the order of segments to process using SQS's delayed message delivery feature.
  
- Since Kafka is optimized for large scale event streaming such as video processing for large scale apps, it could be used instead of SQS as well.

### Resuming watching a livestream where the user left off

- YouTube provides the feature to resume watching from where a user left off. This can be implemented by storing the previous timestamp and other details from the user’s session in a client DB such as Indexed DB. Also Indexed DB can be used to store previous video segments (as a blob) such that a user can go back a few seconds in the video.


### Uploaded livestream video file security

Security can be improved via the following approaches:

#### Encryption in transit

- We will of course use HTTPS to encrypt the data as it’s transferred between the				client and server.

#### Encryption at rest

- We should also encrypt the files stored in S3. S3 has an encryption at rest feature			that is easy to enable. S3 will then encrypt the file using a unique key and store the			key separately from the file. Users cannot decrypt the file without this unique key.

#### Pre-signed URL / CDN URL prevents unauthorized users

- Pre-signed URLs and CDN URLs will also prevent unauthorized users from				uploading / downloading to the blob store / CDN. Even if unauthorized users have the			URL, because there is a TTL on the URLs, they won’t be able to use expired URLs.

- These URLs work for modern CDNs like CloudFront, and are a feature of S3. They			work as shown in ‘Workings of pre-signed URL / CDN URL’



### Thundering herd when multiple clients are expecting transformed video data

- Multiple clients may be expecting to receive transformed video data from a Livestream server (which	it may not currently have at first). Once the Livestream server has the transformed video data, multiple	clients may try to pull it OR the Livestream server will have to send it to multiple clients. This might		cause a thundering herd, where multiple clients are awaiting for the video data to correctly		stream the video in-order on the client-side.

To solve the issue of the thundering herd, we could: 

- Scale the livestream servers, so that the system can support more clients.

- Reduce the video quality so that there are fewer transformed video data which will need to be	sent to clients - thus the Video processing service will take less time in transforming the video. Less time in transforming the video data results in more video segments being delivered per sec because the Video processing service doesn't have to transform the video data to as many formats. This will further ensure a thundering herd is not caused.

### Can we use MapReduce for transforming video data?

- The response time of a MapReduce approach is dependent on how we choose to send the data from	one layer to another, the frequency of the jobs, and the time spent waiting for a job to be accepted by	a machine. 

- A MapReduce approach can have the Map layer send a single video chunk to multiple machines to		transform the chunk into different resolutions, codecs, formats, etc. and then the Reduce layer can	aggregate the results in the correct order, and store them in the blob store. 

- We could use a MapReduce approach, however we’ll need to implement the ordering logic within the	Reduce layer to order the video segments correctly - whereas within a Kafka queue, best effort ordering is	usually guaranteed within a topic and partition. Additionally, SQS also provides ordering using it's delayed message delivery feature.

<br/>
<br/>

Chat deep dives:

### Message delivery status

- The message delivery status on the client side will change depending on where the message currently is. 

- After the client sends a message to the Livestream server, the Livestream server will send an acknowledgement back to the client and mark the		message as “Delivered”.

- After the message reaches the Redis cluster or message queue and is forwarded to the other clients, the			message status will be marked as	“Sent” after the Livestream server sends an acknowledgement back to the client.

- Once the other client has seen the message on their viewport, the other client will send an acknowledgement to the Livestream server, and		the Livestream server will subscribe and send to the recipient livestreamID’s topic  to mark the message as “Seen”.

### Messages table partitioning

We can partition the Messages tables in the following ways:

#### Partitioning based on livestreamID

- A single partition could represent a range of livestreamID. When a new 			entry comes in, the livestreamID could be mapped to a specific partition. This		way, entries such as messages for the same livestreamID are within a single partition, and can be easily accessible. 

#### Partitioning based on messageID

- If we partition by messageID, where different messageIDs for a single livestreamID are distributed across partitions, then fetching the			messages for a single livestreamID will be very slow - thus this approach is not appropriate.

### Database replication

- Additionally, we can replicate the database tables / shards to prevent a SPOF
