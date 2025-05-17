# Netflix

## Requirements

### Questions

- Netflix serves movies and shows to users at its core. Are we focusing on this core system, or should we design additional parts of Netflix?
  - Let’s focus only on the core system. Users should be able to view / search videos, view thumbnails, and like / dislike video

- Should we design additional services like authentication and payments?
  - Let’s ignore these services. However, Netflix uses user activity data for their			recommendation system. The design should still aggregate and process user activity data.

- For the recommendation system, should I think about the kind of algorithm that will be used?
  - No, don’t worry about the algorithm. Focus on how user activity data will be gathered and	processed.

- It seems like there are 2 main parts: the video serving service and recommendation engine. Is low latency a big requirement for the video serving service?
  - Yes, low latency is a strict requirement for the video serving service

- Is the recommendation engine a service that uses user activity data and suggests videos asynchronously to users?
  - Yes

- How many users will use this system?
  - Netflix has about 200M

- Should we design this system for various clients, such as web, mobile, TV, etc?
  - Let’s not optimize or cater the system to different types of clients. However, the streaming should still consider different types of video formats for different devices and clients

- Can we leverage existing cloud services such as CDNs?
  - Yes

### Functional

- Video serving service should allow users to stream videos without too much buffering. Video streaming should take into consideration different devices and clients
- Operations:
  - Search videos
  - View thumbnails
  - Like / dislike video

<br/>

- Recommendation engine should use large amounts of user activity data and suggest videos asynchronously

<br/>

- Netflix has about 200M users

### Non-functional

- Throughput:
  - Users should be able to stream large videos like 50 GB efficiently
- Low latency:
  - Streaming should have low latency
- Durability:
  - Videos and metadata should be durably stored

<br/>

Below is the YouTube 101 - not all parts might apply to this design, but understanding these concepts will help:

## Youtube 101

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
  - Apple HLS (HTTP Live Streaming)
  - Microsoft Smooth Streaming
  - Adobe HTTP Dynamic Streaming (HDS)

### FFMPEG

- A naive approach to encoding / transcoding can be done using FFMPEG, which is a command line tool that can convert video and audio to different formats and resolutions. It can also transform the video and audio in real time.

<br/>

## Netflix 101

The system can be divided into the below parts:

- Storage (stores video content, static content and user metadata)
- General client-server interaction (ie a search query from a client)
- Video content streaming
- User activity data processing - we’ll gather user activity data via the user’s interaction with the UI


## Data model

- Videos:
  - We're going to call this entity "Videos" instead of movies or shows, because at the end of the day, we're working with videos
	- videoID
	- title, description
	- s3URLs
	- cast: { actor / actress info }
	- rating
  	- fingerprint

- Chunks:
	- chunkID
 	- videoID
  	- fingerprint

- User watched:
  - A single row will contain a videoID watched by a userID
  - The lastWatchedTimestamp for a specific videoID will help us to render the exact spot a user left off in the video. It can help us understand where we need to start fetching the chunks of the video from
	- userID
 	- videoID
  	- rating
  	- lastWatchedTimestamp

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed messages quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

<br/>

### Stream a video

- When streaming binary content using HTTP, application/octet-stream can be used to receive	binary data

- The application/octet-stream MIME type is used for unknown binary files. It preserves the file	contents, but requires the receiver to determine file type, for example, from the filename		extension. The Internet media type for an arbitrary byte stream is application/octet-stream.

- The */* means that the client can accept any type of content in the response - which could also	be used for sending / receiving binary data

- Note that to stream files, we could use either a pre-signed URL or a URL the client can request	to download from the CDN (let’s call it CDN URL). The process is similar to uploading videos,	where the client first requests the servers for a pre-signed	URL OR CDN URL, then the client will	stream the video from the pre-signed URL / CDN URL.

- Note that we’ll also request for a specific pre-signed URL / CDN URL for a segment / timestamp using the device and video format info such as codec and resolution (to support different devices and video formats)

#### Request for a pre-signed URL / CDN URL

- Note that we'll also specify the segment OR lastWatchedTimestamp to stream the video from

Request:
```bash
GET /videos/:videoID/pre-signed-url OR cdn-url?<segment OR lastWatchedTimestamp>&codec&resolution
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

### Update lastWatchedTimestamp for videoID

- This endpoint will update the videoID entry's lastWatchedTimestamp for the userID in the User watched entity

Request:
```bash
PATCH /videos/:videoID/last-watched-timestamp
{
  lastWatchedTimestamp
}
```

### Search for videos

Request:
```bash
GET /videos?searchQuery&nextCursor&limit
```

Response:
```bash
{
  videos: [ { videoID, title } ],
  nextCursor, limit
}
```

### Get thumbnail for video

- Using the pre-signed URL or CDN URL returned by this endpoint, likewise with video streaming,	the client will request the pre-signed URL or CDN URL to fetch the thumbnail from the blob store

Request:
```bash
GET /videos/:videoID/thumbnail
```

Response:
```bash
{
  pre-signed URL or CDN URL
}
```

### Like / dislike video

Request:
```bash
PATCH /videos/:videoID?op={ LIKE OR DISLIKE }
```

## HLD

This design can be divided into the "video streaming" and "recommendation engine" components:

<br/>

Video streaming:

### Client

- The client will be downloading video data, thus there will be a section in the client-code for a “downloader”:
  
#### Downloader

- The downloader will likely use a client based video player developed via a SDK such as Video.js. The downloader will use websockets or WebRTC to request for video segments via pre-signed URLs / CDN URLs 
	
Additionally, the client will contain the following internal components which will communicate with the downloader. This is also shown in ‘Client components’:

Client components:

<img width="350" alt="image" src="https://github.com/user-attachments/assets/ef2b80cc-e8b9-4e1b-9f74-1b19fd18b7bc" />

#### Chunker
		
- The client will also have a chunker functionality that will reconstruct the files from the downloaded video segments when streaming the video. 
- Note that chunks and video segments are different, in that a chunk is a fixed size part of a file, whereas a video segment will consist of the manifest files and actual segment files for a few secs of the video

#### Client database

- To maintain the metadata for the local video and it’s chunks, we’ll store it in a client database such as Indexed DB. The client will use this client database to compare local chunks (which are already downloaded) against the remote chunks when streaming the video.


### API servers
  
- The API servers will handle CRUD based requests which don’t directly involve downloading videos or searching videos, such as updating the video metadata, updating the User watched entity, liking / disliking videos, etc. To speed up querying, the API servers could		also maintain a cache of the video and user metadata.
- The API servers will also provide pre-signed URLs / CDN URLs for downloading / viewing thumbnails stored in the blob store. Also, the API servers will allow admins to update the video metadata database when new videos are		added or removed.

- Also, when the user interacts with the UI, the	user activity data will be logged to the S3 data lake		containing user activity logs. This logging can be done asynchronously via traditional message queues		such as SQS, and doesn’t need to be done on the client’s critical path.
  
### Metadata database / cache

- The metadata database will store the video, chunks, and user watched metadata which doesn’t include the actual binary data.	

- The amount of videos being uploaded per day will be great, and thus we could either use a SQL database or a highly horizontally scalable NoSQL database like Cassandra. We could choose SQL if the design is for a small to moderate scale, however the design will likely require maintaining multiple partitions and the data may also contain some unstructured pieces, such as segments of a video, etc. SQL can still provide these features, but won’t be optimized for them - thus, Cassandra may be more suitable. Also, Cassandra provides CQL, similar to SQL, which will be helpful for complex queries.

#### Sharding metadata DB

- We could also partition / shard on the videoID (via consistent hashing which Cassandra already implements) so that fetching data about a single videoID will only happen within a single partition / shard. Also similar videoIDs could also be placed in the same shard for faster querying.

#### Cache

- Also, a cache of the metadata could be maintained using either Redis or Memcached. Since we'll likely need to cache info about the different chunks and segments of a video, likely by their timestamps or another field to help with ordering, we can use Redis sorted sets. This cache will also prevent hotspots of frequently viewed videoIDs by caching the metadata for those videoIDs.

#### User watched SQL table / cache

- We’ll need to store user's activity for each video such as where the user left a video at, the user’s		rating, etc. Assuming a user watches on average 100 videos, at the upper-end, we’ll have (200M users *		100 videos) = 20B of rows in the User watched table. An entry here will likely be 100-200		bytes. 20B rows * 100 bytes = 2 TB.

- We’ll need to perform complex queries and joins on this data for the recommendation engine, and to		produce different views of the user’s data on the client side via dimension tables, using this User watched table. If we do need to perform complex queries (which can't be performed by Cassandra), then we could use a SQL DB such as PostgreSQL here instead.

- We can also split this database (this database containing only the User watched table) into shards based on a userID. We’ll use userID to shard since videoIDs accessed by a single userID would be inside a single shard. We could also		index the tables by the videoID, however, this may impact the write latencies, as the videoID and it’s		values would need to be updated in the table’s indexing data structure on each write operation.

- Operations such as getting the user’s watched videos and their lastWatchedTimestamp would		require low latency, thus for specific operations such as these which are performed often, the		data could also be cached in Redis.

### Blob store

- The blob store will store the video data. The video data stored in the blob store can be the following, and in ‘Video storage logic in blob store’:
  - Store the raw video
  - Store different video formats
  - Store different video formats as segments	

- When users stream a video, they will request the servers for the video metadata and appropriate pre-signed URLs / CDN URLs to fetch the video data. The video data can be streamed from these URLs as follows and in ‘Streaming video from blob store’:
  - Download the video file
  - Download segments incrementally
  - Adaptive bitrate streaming

#### Scaling the blob store

- A Netflix video can be about 1 hr, and can have both a standard definition (SD) and high definition (HD)		version. SD may be about 10 GB, while HD may be 20 GB of space. If we assume Netflix stores		about 10k videos, 30 GB * 10k = 300 TB. 300 GB is a moderate amount, but not as large as storage in services like		YouTube, Google Drive and Facebook, which allows any user to upload content.

- A blob store like S3 can store the video content, and we can also apply		replication as well as segmenting of the video content for faster processing.

- A single video could be split into segments within a bucket, such that the individual segments		could be retrieved in parallel as the video is being streamed. On the infrastructure side, these segments		may be stored in separate servers, which can allow them to be fetched in parallel. 
- As S3 are cloud services, Netflix may work with the vendors to provision separate replicated servers for		a single bucket, such that segments can be mapped to different servers. Thus, if a single server is down,		the whole bucket’s data is not lost. The DD will discuss more on the segmenting and streaming of the video.

### Video CDN
  
- As some users may be farther away from S3 servers, which may affect the streaming quality, we can use Video CDN POPs to cache frequently accessed video data (both segment files and manifest files). Clients can then use the CDN URLs from the API servers to stream and fetch the video data from the CDN POPs

- Because video data is static, push based CDNs will be more appropriate, where the origin servers will push the content from the blob store to the CDN POPs. CDNs may be more expensive, but will only be necessary for a large scale app

- The CDNs will likely not be able to keep the entire video content data in cache, thus we can have a		separate service called a Video distribution service, which communicates with the CDN’s origin servers		to distribute the most frequently accessed video content to the POPs.

- Netflix actually partners with ISPs, and uses their IXPs (internet exchange points), which are spread		across thousands of servers across the world. ISP IXP are more optimized and low latency versions of		CDNs, which are used for low latency jobs such as video streaming.

### Video distribution service

- The Video distribution service will communicate with the CDN’s origin servers and add or remove video		content in the CDN’s POPs from the video content blob store. It will also use the Metadata database to			cache frequently watched or high rated videos in the CDN using the rating.

IXP:
- A physical location where internet service providers (ISPs) and other internet infrastructure companies connect to exchange traffic. IXPs are a key part of the internet, allowing networks to share traffic and making the internet faster and more affordable. 

### Search service
  
- The search service will handle requests for searching videos. The search service will maintain inverted index mappings of the text based data for videos using the title and description fields - which will be retrieved from the Metadata database.
- The inverted index mappings can be developed via Lucene or Elasticseearch, and updates to the Metadata database can be reflected to the search service’s inverted index mappings via CDC which Elasticsearch provides (change data capture).

### L4 Load balancer

- We’ll need an L4 load balancer to support traffic at the TCP level. L4 load balancers, let’s say	using ELB in TCP mode can load balance websockets and WebRTC. When client’s need to connect to a video CDN, the L4 load balancer will route them to the server they previously connected to or to any server using the load balancing algorithm. However, if a server goes down, the L4 load balancer can route the client to connect to another server instead.

- When a client needs to connect to the server, the request will first go to the L4 load balancer,	then to the server. There will actually be a symmetric websocket / WebRTC connection between both the client to the L4 load balancer, and between the L4 load balancer to the server.

- L4 load balancers can be stateful and use sticky sessions to persist the server the client		previously connected to. The sticky session can be implemented by identifying the user, usually	with cookies or their IP address, and storing the user’s connected server for handling future		requests.

- If clients disconnect from a server, they can automatically reconnect to the	 same server or		another one via the L4 load balancer. Reconnecting to the same server may be easier, as the	session data in the L4 load balancer doesn’t have to be updated.

<br/>
<br/>

Recommendation engine:

### MapReduce user activity processing jobs

- The user activity data will likely be gathered from analytics logs via the API servers as users interact		with the UI. There may be terabytes of logs generated per day.

- We can use MapReduce, where we store the logs in a data lake like S3 and run			MapReduce jobs on chunks of the logs to process them in parallel. The output of these jobs may be the		video’s overall rating by the user, user’s most liked videos, etc. The output can then be fed into the			Recommendation engine which will use it’s own algorithms or ML pipelines to generate suggestions to		the user asynchronously.

- The Map inputs in the logs may look like:

```bash
{ userID1, videoID1, event: LIKE }
{ userID2, videoID2, event: CLICK }
{ userID3, videoID3, event: PAUSE }
```

- The Map function will split logs based on the userID, and compile all the events for a single userID in a single KV pair. The KV pair may contain the userID, multiple videoIDs and the events as follows:

```bash
{ userID1: [ (videoID1: event: LIKE), (videoID2: event: CLICK) ] }
{ userID2: [ (videoID2: event: LIKE), (videoID3: event: PAUSE) ] }
```

- The chunks of the KV pairs will then be fed into the Reduce function. The Reduce function could return different outputs such as the video’s overall rating by the user, user’s most liked videos, most watched videos, etc:

```bash
{ userID1: { mostWatched: [ videoID2, videoID3 ], ratings: [ (videoID1: rating ), (videoID2: rating ) ] } }
{ userID2: { mostLiked: [ videoID1, videoID2 ], mostWatched: [ videoID2, videoID3 ] } }
```

- MapReduce jobs could be implemented and configured manually or using EMR which allows the running of MapReduce jobs. 

- The MapReduce jobs themselves can be implemented via multiple message queues and workers using standard SQS queues and memory or IO optimized EC2 instances running separate containers performing the jobs. For the MapReduce jobs, the main requirements will be throughput and performing multiple in-memory operations (aggregating events) and IO operations (feeding or storing output to the recommendation engine). If throughput is a very strict requirement, an event streaming service such as Kafka can instead be used.

### Recommendation engine

- The recommendation engine will use the MapReduce outputs and use it’s own algorithm or ML			pipelines to generate suggestions to the user asynchronously and possibly provide the suggestions to a		User recommendation cache, which the user could fetch from.

- Note that the SDI 'Recommendation engine' talks more about the design of MapReduce vs stream processing, and it's use in a recommendation engine

<img width="1150" alt="image" src="https://github.com/user-attachments/assets/5f5d450a-fa1b-47b4-b34b-dddb54297658" />


## DD

### Implementing adaptive bitrate streaming

- This design will use adaptive bitrate streaming to stream video data as clients will likely have changing network quality, and adaptability to different video formats is needed. After a video is uploaded in it’s original format by an admin, it will be post-processed to convert it to different video formats. The output of the post-processing will contain the following:
  - Segment files in different video formats stored in S3
  - Manifest files (both a primary manifest file and several media manifest files) in S3. The media manifest files will reference segment files
  - Video thumbnail

The SDI 'YouTube' talks more about uploading, which won't be discussed in this design, since we're mainly concerned about downloading.

**Note that video segments can sometimes be known as GOP (group of pictures)**

#### Video streaming with adaptive bitrate streaming

- Using the post-processing logic, the video will be in different video formats. Thus clients can request for pre-signed URLs / CDN URLs for video segments at a specific video format depending on their network quality and video quality settings. The returned video segments’ video formats may also change over time, but the system now returns segments catered to the client.


### Scaling servers and storage

#### API servers

- The API servers are stateless and will provide pre-signed URLs / CDN URLs, and also update the Metadata database. It can easily be horizontally scaled.

#### Metadata database

- The metadata database will use Cassandra, which is optimized to be horizontally scalable by following leaderless replication and internal consistent hashing. Availability is thus prioritized over consistency in Cassandra. If more leaderless nodes are needed, they could be added. However, if a node contains a popular videoID, it might become a hotspot.

- If a videoID does become a hotspot, Cassandra can be tuned to replicate the videoID’s data to a few extra nodes, so that it can handle the read intensity for that videoID.

#### Scaling CDN

- We'll likely use video CDNs from CDN providers. Most CDN providers like CloudFlare and AWS allow us to increase the cache capabity, however it may be costly. Instead of sticking to one CDN provider which imposes some limits on the caching and has high costs, we can distribute the cached content across multiple CDN providers using cheaper subscription options provided by those CDN providers. This way, we'll still cache the content to servers world-wide using those multiple CDN providers - but storage / caching will be cheaper.

### Resume watching a video where the user left off

- Netflix provides the feature to resume watching from where a user left off. This can be implemented by storing the previous timestamp and other details from the user’s session in a client DB such as Indexed DB or with the User watched entity's lastWatchedTimestamp field. Also Indexed DB can be used to store previous video segments (as a blob) such that a user can go back a few seconds in the video.

### Video file security

Security can be improved via the following approaches:

#### Encryption in transit

- We will of course use HTTPS to encrypt the data as it’s transferred between the				client and server.

#### Encryption at rest

- We should also encrypt the files stored in S3. S3 has an encryption at rest feature			that is easy to enable. S3 will then encrypt the file using a unique key and store the			key separately from the file. Users cannot decrypt the file without this unique key.

#### Pre-signed URL / CDN URL prevents unauthorized users

- Pre-signed URLs and CDN URLs will also prevent unauthorized users from				uploading / downloading to the blob store / CDN. Even if unauthorized users have the			URL, because there is a TTL on the URLs, they won’t be able to use expired URLs.

- These URLs work for modern CDNs like CloudFront, and are a feature of S3. They			work as shown in ‘Workings of pre-signed URL / CDN URL’

