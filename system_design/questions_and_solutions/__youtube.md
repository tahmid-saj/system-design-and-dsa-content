# YouTube

## Requirements

### Questions

- What features are important?
	- Ability to upload a video and watch (stream) a video

- What devices do we need to support?
	- Mobile, web and smart TV

- Do we need to support global users?
	- Yes a large percentage of users are global

- Should we support different video resolutions and formats?
	- Yes

- Is encryption required for videos and metadata?
	- Yes

- Can we leverage existing cloud services such as CDNs?
	- Yes

### Functional

- Ability to upload and watch (stream) a video
- Used in web, mobile and smart TV
- Global app
- Should support different video resolutions and formats
- Encrypted video and metadata

- Operations:
  - Search videos
  - View thumbnails
  - Like / dislike video
  - Add comments to videos

- YouTube typically has 1M uploads per day and 100M videos watched per day

### Non-functional

- Availability > consistency:
	- Clients don’t need the latest updates for video uploads right away
- Throughput:
	- Users should be able to upload large videos like 10	GB efficiently
	- Resumable uploads may be needed
- Low latency:
	- Streaming should have low latency
- Durability:
	- Videos and metadata should be durably stored

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

## Data model / entities

- Users:
	- userID
	- userName
	- userEmail

- Videos:
	- videoID
	- userID
	- channelID
	- title,  description
	- s3URLs
	- likes, dislikes, views etc
	- videoStatus: UPLOADING / UPLOADED

	- metadata: { videoSize, createdAt, updatedAt }

	- fingerprint

- Chunks:
	- chunkID
	- videoID
	- chunkStatus: enum UPLOADED / NOT_UPLOADED / FAILED

	- fingerprint

- Comments:
	- commentID
	- videoID
	- userID
	- comment

	- metadata: { createdAt, editedAt }

- Channels:
	- channelID
	- userID
	- name, description


## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Upload a video

- Note that there could likely be 2 types of uploads supported depending on the file size. A simple upload could be used when the file size is small, and can be uploaded in one go. A resumable upload could be used when the file size is large, as discussed in the DD.

- When uploading binary data, multipart/form-data / multipart/mixed or another MIME type such as	image/png is usually used

- The content type is set to multipart/mixed which means that the request contains different inputs	and each input can have a different encoding type (JSON or binary). The metadata sent will be in	JSON, while the video itself will be in binary. 

- The placeholder {---xxBOUNDARYxx—} will contain a text string for the boundary that			differentiates one part of the body from another. For example “__the_boundary__” could be used	as the string. Boundaries must also start with double hyphens and end with double hyphens too.

- Note that since this design is using a pre-signed URL to upload videos, the client will first request	for a pre-signed URL from the servers, then make a HTTP PUT request with the video data in the	request body to the pre-signed URL

- When the client requests for a pre-signed URL, the client will also send in the video metadata in	the request body, and the API servers will update the video metadata into the database.

#### Request for a pre-signed URL

Request:
```bash
POST /channels/:channelID/videos?uploadType={ SIMPLE / RESUMABLE }
{
  videoName
  title, description
  videoMetadata
}
```

Response:
```bash
{
  pre-signed URL
}
```

#### Upload to pre-signed URL

Request:
```bash
PUT /<pre-signed URL>
Content-Type: multipart/form-data; boundary={---xxBOUNDARYxx—}
{
—xxBOUNDARYxx–
<HEADERS of the boundary go here>

We’ll put the video binary data in this boundary:

<video’s binary data goes here>

—xxBOUNDARYxx–
}
```

Response:
```bash
{
	videoID
	metadata: { createdTIme, videoStatus }
}
```

### Stream a video

- When streaming binary content using HTTP, application/octet-stream can be used to receive	binary data

- The application/octet-stream MIME type is used for unknown binary files. It preserves the file	contents, but requires the receiver to determine file type, for example, from the filename		extension. The Internet media type for an arbitrary byte stream is application/octet-stream.

- The */* means that the client can accept any type of content in the response - which could also	be used for sending / receiving binary data

- Note that to stream files, we could use either a pre-signed URL or a URL the client can request	to download from the CDN (let’s call it CDN URL). The process is similar to uploading videos,	where the client first requests the servers for a pre-signed	URL OR CDN URL, then the client will	stream the video from the pre-signed URL / CDN URL.

- Note that we’ll also request for a specific pre-signed URL / CDN URL for a segment / timestamp using the device and video format info such as codec and resolution (to support different devices and video formats)

#### Request for a pre-signed URL / CDN URL

- Note that we'll also specify the segment OR the user's last watched timestamp to stream the video from

Request:
```bash
GET /channels/:channelID/videos/:videoID/pre-signed-url OR cdn-url?<segment OR timestamp>&codec&resolution
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

### Search for videos

Request:
```bash
GET /videos?searchQuery&nextCursor&limit
```

Response:
```bash
{
	videos: [ { videoID, channelID, title, description } ],
	nextCursor, limit
}
```

### Get thumbnail for video

- Using the pre-signed URL or CDN URL returned by this endpoint, likewise with video streaming,	the client will request the pre-signed URL or CDN URL to fetch the thumbnail from the blob store

Request:
```bash
GET /channels/:channelID/videos/:videoID/thumbnail
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
PATCH /channels/:channelID/videos/:videoID?op={ LIKE OR DISLIKE }
```

### Comment on a video

Request:
```bash
POST /channels/:channelID/videos/:videoID/comment
{
	comment
}
```

## HLD

### Client

- The client will be both uploading and downloading video data, thus there will be two separate sections in the client code for an “uploader” and “downloader”:

#### Uploader

- The uploader will upload the local video file chunks to the blob store via a pre-signed URL
  
#### Downloader

- The downloader will likely use a client based video player developed via a SDK such as Video.js. The downloader will use websockets or WebRTC to request for video segments via pre-signed URLs / CDN URLs 
	
Additionally, the client will contain the following internal components which will communicate with the uploader and downloader. This is also shown in ‘Client components’:

Client components:

<img width="350" alt="image" src="https://github.com/user-attachments/assets/7e1de751-fc32-400a-8d4e-f2c91a67b841" />

#### Chunker
		
- The client will also have a chunker functionality that splits the local video file into chunks when uploading to the blob store, and also reconstructs the files from the downloaded video segments. 
- Note that chunks and video segments are different, in that a chunk is a fixed size part of a file, whereas a video segment will consist of the manifest files and actual segment files for a few secs of the video

#### Client database

- To maintain the metadata for the local video and it’s chunks, we’ll store it in a client database such as Indexed DB. The client will use this client database to compare local chunks and uploaded chunks when uploading videos to the blob store.

### API servers
  
- The API servers will handle CRUD based requests which don’t directly involve uploading / downloading videos or searching videos, such as updating video / chunk metadata, posting comments, liking / disliking videos, etc.
- The API servers will also provide pre-signed URLs / CDN URLs for uploading / downloading / viewing thumbnails stored in the blob store.

### Metadata database / cache

- The metadata database will store the video, chunks, channels, comments metadata which doesn’t include the actual binary data.	

- The amount of videos being uploaded per day will be great, and thus we could either use a SQL database or a highly horizontally scalable NoSQL database like Cassandra. We could choose SQL if the design is for a small to moderate scale, however the design will likely require maintaining multiple partitions and the data may also contain some unstructured pieces, such as comments, segments of a video, etc. SQL can still provide these features, but won’t be optimized for them - thus, Cassandra may be more suitable. Also, Cassandra provides CQL, similar to SQL, which will be helpful for complex queries.

#### Sharding metadata DB

- We could also partition / shard on the videoID (via consistent hashing which Cassandra already implements) so that fetching data about a single videoID will only happen within a single partition / shard. Sharding by videoID is also more optimal than sharding by userID because a single userID could have 10s of thousands of videos, and another userID could have just a few videos - making the shards uneven, and also might create hotspots if some channels are accessed much more frequently.

#### Cache

- Also, a cache of the metadata could be maintained using either Redis or Memcached. Since we'll likely need to cache info about the different chunks and segments of a video, likely by their timestamps or another field to help with ordering, we can use Redis sorted sets. This cache will also prevent hotspots of frequently viewed videoIDs by caching the metadata for those videoIDs.

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

### Video processing service
  
- The video processing service will consist of a post-processing DAG which will be run when a user uploads chunks of a video. 

- The video processing service may contain a message queue either with SQS or Kafka to maintain a list of tasks it needs to execute for different video chunks / segments, such as transcoding the video / audio / transcripts, and also creating the manifest files. Thus, there could be a temporary message queue for each video being uploaded. 

- The message queue could also be maintained via an in-memory cache such as Memcached which contains the queued tasks, and the task’s status (COMPLETE / PENDING / FAILED).

- The video processing service will also contain the post-processing DAG and relevant workers (which could be compute optimized EC2 instances) to run the tasks, and generate the manifest files + segment files for different video formats.

- The video processing service and it’s workflow is explained more in depth in the DD.

### Video CDN
  
- As some users may be farther away from S3 servers, which may affect the streaming quality, we can use Video CDN POPs to cache frequently accessed video data (both segment files and manifest files). Clients can then use the CDN URLs from the API servers to stream and fetch the video data from the CDN POPs

- Because video data is static, push based CDNs will be more appropriate, where the origin servers will push the content from the blob store to the CDN POPs

- CDNs may be more expensive, but will only be necessary for a large scale app

### Search service
  
- The search service will handle requests for searching videos	

- The search service will maintain inverted index mappings of the text based data for videos, comments and channels - which will be retrieved from the metadata database. The inverted index mappings can be developed via Apache Lucene or Elasticseearch, and updates to the metadata database can be reflected to the search service’s inverted index mappings via CDC which Elasticsearch provides (change data capture).

### L4 Load balancer

- We’ll need an L4 load balancer to support traffic at the TCP level. L4 load balancers, let’s say	using ELB in TCP mode can load balance websockets and WebRTC. When client’s need to connect to a websocket / WebRTC server, the L4 load balancer will route them to the server they previously connected to or to any server using the load balancing algorithm. However, if a server goes down, the L4 load balancer can route the client to connect to another server instead.

- When a client needs to connect to the server, the request will first go to the L4 load balancer,	then to the server. There will actually be a symmetric websocket / WebRTC connection between both the client to the L4 load balancer, and between the L4 load balancer to the server.

- L4 load balancers can be stateful and use sticky sessions to persist the server the client		previously connected to. The sticky session can be implemented by identifying the user, usually	with cookies or their IP address, and storing the user’s connected server for handling future		requests.

- If clients disconnect from a server, they can automatically reconnect to the	 same server or		another one via the L4 load balancer. Reconnecting to the same server may be easier, as the	session data in the L4 load balancer doesn’t have to be updated.

<img width="800" alt="image" src="https://github.com/user-attachments/assets/03991f2a-1e06-4def-b175-ed464d6a19a2" />

## DD

### Implementing adaptive bitrate streaming

- This design will use adaptive bitrate streaming to stream video data as clients will likely have changing network quality, and adaptability to different video formats is needed. After a video is uploaded in it’s original format, it will be post-processed to convert it to different video formats. The output of the post-processing will contain the following:
  - Segment files in different video formats stored in S3
  - Manifest files (both a primary manifest file and several media manifest files) in S3. The media manifest files will reference segment files

To generate segments and manifest files, the operations below (and in ‘Upload post-processing DAG’) will be performed within a DAG structure via the client and a separate Video processing service which will connect to S3:
1. The client will split up the original video file into chunks using a tool like ffmpeg. These chunks will then be uploaded to S3. S3 will then send a S3 event notification to a Lambda function, which will trigger the video processing service to start the post-processing. The chunks may be very small (5-10 MB) and may be combined into video segments by the Video processing service. The video processing service could also inspect the uploaded chunks in this step.
2. The video processing service will then transcode the video segments to generate the segment files at different video formats in parallel
3. The video processing service will transcode / process other aspects of the segments, such as audio, transcript, etc to also generate segment files for audio, transcript, etc
4. The video processing service will create manifest files (for different video formats), which will reference the segment files
5. We’ll mark the upload as complete, and store all the video segment files, and manifest files for the video formats in S3. The hierarchy will be as follows: video -> primary manifest file -> media manifest files -> segment files
6. At the end, the video thumbnail can be generated from a random segment’s frame if not provided

**Note that video segments can sometimes be known as GOP (group of pictures)**

Upload post-processing DAG:

<img width="1200" alt="image" src="https://github.com/user-attachments/assets/8f2adb93-f84d-4e77-bc46-39c731ea1188" />

#### Making post-processing faster

- In the post-processing DAG steps, the most expensive operation will be the video segment transcoding, which can be done in parallel and on different machines which are compute (CPU) optimized such as compute based EC2 instances, since transcoding is a compute bound task.

- If we want to speed up the post-processing done by the video processing service, we can start post-processing early right after the client uploads enough chunks instead of waiting for all the video chunks to be uploaded first. This will speed up the upload process for the user.

#### DAG orchestration tool

- Building the actual DAG and it’s logic can be done using a DAG orchestration tool specific for media processing such as Temporal. Temporal can be used to build the DAG, and also to assign workers for specific steps of the DAG. 

#### S3 storing temporary data + outputs

For storing temporary data exchanged between steps in the DAG, S3 can be used so that the temporary data between steps is not lost. If post-processing is interrupted or a worker is down, another worker can fetch the temporary data from the output of the previous step and continue the post-processing. Thus, S3 will store the below for a single video:
  - Original uploaded video chunks / segments (manifest files + video segment files included)
  - A single primary manifest file
  - Multiple media manifest files referencing segment files
  - Segment files: both video segment files AND audio, transcript, etc segment files
  - Video thumbnail
  - Temporary data from each DAG step

#### Video streaming with adaptive bitrate streaming

- Using the post-processing logic, the video will be in different video formats. Thus clients can request for pre-signed URLs / CDN URLs for video segments at a specific video format depending on their network quality and video quality settings. The returned video segments’ video formats may also change over time, but the system now returns segments catered to the client.

### Supporting large file uploads via resumable uploads

- To support large files and resumable uploads, we’re using chunking. The clients will calculate a fingerprint for the video and the chunks to uniquely reference as a hash value - for comparing different chunks. 

- Resumable uploads ensure that the client doesn’t upload all of the video data at once, and that chunks can instead be used to provide an upload status indicator in the UI - so that clients can resume uploading the local chunkIDs if needed.
 
- When a client prepares to upload chunks of a video, they’ll request the servers to create Chunks table entries for all the chunkIDs they will upload, and set the chunkStatus to NOT_UPLOADED. Once a chunkID is uploaded successfully, it’s chunkStatus could be updated to UPLOADED in the DB via a S3 event notification sent to a Lambda function (Lambda will update the DB).

- If the client stops uploading or uploading gets interrupted, it could resume the upload by fetching the NOT_UPLOADED chunkIDs for the videoID, and upload only those chunkIDs from the client database.

- This overall practice of chunking and uploading is handled by AWS multipart upload as explained in ‘S3 multipart upload’.

### Scaling servers and storage

#### API servers

- The API servers are stateless and will provide pre-signed URLs / CDN URLs, and also update the metadata database. It can easily be horizontally scaled.

#### Metadata database

- The metadata database will use Cassandra, which is optimized to be horizontally scalable by following leaderless replication and internal consistent hashing. Availability is thus prioritized over consistency in Cassandra. If more leaderless nodes are needed, they could be added. However, if a node contains a popular videoID, it might become a hotspot.

- If a videoID does become a hotspot, Cassandra can be tuned to replicate the videoID’s data to a few extra nodes, so that it can handle the read intensity for that videoID.

#### Video processing service

- The Video processing service will be stateless, and can also be easily scaled horizontally. As the Video processing service will have many tasks for a single video, it can manage them via a message queue such as a SQS standard queue. SQS standard queues guarantee that messages are delivered at-least-once, and also can guarantee the order of segments to process using SQS's delayed message delivery feature.
  
- Since Kafka is optimized for large scale event streaming such as video processing for large scale apps, it could be used instead of SQS as well.

### Resume watching a video where the user left off

- YouTube provides the feature to resume watching from where a user left off. This can be implemented by storing the previous timestamp and other details from the user’s session in a client DB such as IndexedDB. Also IndexedDB can be used to store previous video segments (as a blob) such that a user can go back a few seconds in the video.

### Video file security

Security can be improved via the following approaches:

#### Encryption in transit

- We will of course use HTTPS to encrypt the data as it’s transferred between the				client and server.

#### Encryption at rest

- We should also encrypt the files stored in S3. S3 has an encryption at rest feature			that is easy to enable. S3 will then encrypt the file using a unique key and store the			key separately from the file. Users cannot decrypt the file without this unique key.

#### Pre-signed URL / CDN URL prevents unauthorized users

- Pre-signed URLs and CDN URLs will also prevent unauthorized users from				uploading / downloading to the blob store / CDN. Even if unauthorized users have the			URL, because there is a TTL on the URLs, they won’t be able to use expired URLs.

- These URLs work for modern CDNs like CloudFront, and are a feature of S3. They			work as shown in ‘Workings of pre-signed URL / CDN URL’

<br/>
<br/>

Additional deep dives:

### Video deduplication
  
- Duplicate videos can take up extra storage, require more bandwidth usage, etc. When a user uploads a video, the Video processing service could perform deduplication of the video chunks by using the chunks’ fingerprints to verify if the same chunk has already been uploaded by another userID.
	
- Also, video matching algorithms like Block Matching and Phase Correlation can be used to find duplicate videos. If a chunk already exists in the blob store (and the chunkID with the same fingerprint exists in the DB), the algorithm could skip the duplicated chunk before it is uploaded, and proceed with the other unique chunks being uploaded. 

- However, deduplication may be very complex to maintain, as multiple users may now perform writes to the same unique chunk - but we could use S3 Object Locks to maintain transactions for the unique chunks.

### Vitess
  
- YouTube uses Vitess to put an abstraction layer on top of the database layers so clients think it is talking to a single database server. 
- Additionally, Vitess performs the replication, sharding and disaster recovery of YouTube’s metadata.
- Vitess maintains ACID properties and it’s underlying database is a combination of MySQL with very high levels of partitioning to enable scalability


## Wrap up

- Live streaming using CDN
- Video takedowns
