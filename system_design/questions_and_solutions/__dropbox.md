# Dropbox

**Note that the design for Dropbox is similar to Google Drive and OneDrive**

## Requirements

### Questions

- Should the system allow users to upload / modify / download / delete files and folders?
  - Yes, and modified changes should be synchronized to all devices, local			workspaces and users

- Should there be file and folder synchronization between devices?
  - Yes

- Can users share files and folders with other users?
  - Yes

- Should the system allow offline support, where offline edits to a file are synchronized when the user is back online?
  - Yes

- Should there be versioning of the files, and should users be able to view the versions of the file?
  - This can be an extended requirement, but not immediately required

- This this a mobile app, web app or both?
  - Both

- What are the supported file types the system should support?
  - Any file type

### Functional

- Users can upload and download files
- Users can also share files or folders with other users
- The system should synchronize the updates to files / folders between devices (both the user’s devices and other user’s devices)

- The system should also support offline editing, where offline users can still upload, modify and delete files, and it will synchronize when they’re back online
- An extended requirement is versioning of the files, and allowing users to view versions of the file

### Non-functional

- Durability / availability:
  - The system should durably persist the files and folders

- File uploading / downloading throughput:
  - The system should handle throughput appropriately for uploading / downloading		large files like 50 GB

- Low latency in synchronization:
  - The system should make synchronization as fast as possible

- File uploads / downloads / syncing should take as low bandwidth as possible

## Dropbox 101

### Read and write ratio

- The read and write ratio will be nearly equal

### Chunking

- Files can be stored as fixed size chunks. This can help		when uploading large files, and also ensures that if the		chunk failed to be uploaded, then only that chunk needs to	be re-tried in uploading, instead of re-trying all the chunks		for the file.

- We can also reduce the amount of data uploaded by		comparing and uploading only the modified chunks when a	file is being updated

### Client-side caching

- Caching at the client side a copy of the metadata can		prevent multiple requests being made to	the databases

### Synchronization

Synchronization should be supported in the different ways	below:

#### Local-remote synchronization

- In a local-remote synchronization, a copy of a	file should be stored on each device (locally),		and in the remote storage.

- There are two directions we would need to				sync: local -> remote and remote -> local.
			When a user updates a file on their local		 device, we need to sync these changes to the remote servers and vice versa. The remove server will still be a source of truth, so it will need to be consistent as soon as possible, so that other devices can pull in the changes if they’re not synced.

#### Device synchronization

- Device synchronization means that devices belonging to the same user will still receive the same updates if a file is changed in one device

#### Synchronization between users

- Synchronization between users means that file changes by a shared user should be updated and synchronized for another shared user

### Client-side workspaces

- For a lot of cloud storages, the user could specify a local		workspace that directly connects to the remote storage for		the service. For example, in OneDrive, there are folders		which connects to the remove storage.

- When files / folders are uploaded to this workspace on the	client side, it will also be uploaded to the remote storage

## Data model / entities

- Users:
	- userID
	- userName
	- userEmail

- Files:
  - The Files and Chunks tables contains the info on the files	and chunks, such as the filePath, fileStatus, chunkStatus, etc, which		will be in a blob store

  - The checkSum field is a hash value verifying the integrity	of the data, and detecting if errors exist in the file

    - fileID
    - folderID
    - userID
    - fileName
    - s3URLs
    - fileStatus: enum UPLOADING / UPLOADED

    - checkSum
    - fingerprint
    - metadata: { fileSize, fileType, createdTime, updatedAt }


- Chunks:
  - chunkID
  - fileID
  - fingerprint
  - chunkStatus: enum UPLOADED / NOT_UPLOADED /		FAILED


- Folders:
	- folderID
	- ownerID (userID of the owner)
	- folderName
	- folderPath (path rendered on the UI)
	- metadata: { folderSize, createdTime }

- Shared files:
  - This entity will contain all the userIDs which have access 	to a fileID

    - fileID
    - userID

- File versions (Optional - only for supporting versioning):
  - This table will contain the versionIDs for a fileID. New		entries will be added when new file changes are uploaded.

  - This table is only necessary if file versioning is in scope

    - versionID
    - fileID
    - s3URLs
    - createdAt

- Devices (Optional - only for supporting different types of devices like mobile and laptop):
  - Since a user could have multiple devices, this entity will store all deviceIDs		belonging to a userID

    - deviceID
    - userID

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Uploading a file to a folder

- Note that there could likely be 2 types of uploads supported depending on the file size. A simple upload could be used when the file size is small, and can be uploaded in one go. A resumable upload could be used when the file size is large, as discussed in the DD.

- When uploading binary data, multipart/form-data / multipart/mixed or another MIME	type such as image/png is usually used

- The content type is set to multipart/mixed which means that the request contains	different inputs and each input can have a different encoding type (JSON or binary).	The metadata sent will be in JSON, while the file itself will be in binary. 

- The placeholder {---xxBOUNDARYxx—} will contain a text string for the boundary	that differentiates one part of the body from another. For example				“__the_boundary__” could be used as the string. Boundaries must also start with		double hyphens and end with double hyphens too.

- Note that since this design is using a pre-signed URL to upload files, the client will	first request for a pre-signed URL from the servers, then make a HTTP PUT request	with the file data in the request body to the pre-signed URL

- When the client requests for a pre-signed URL, the client will also send in the file	metadata in the request body, and the API servers will update the file metadata into	the database.

#### Request for a pre-signed URL

Request:
```bash
POST /folders/:folderID/pre-signed-url?uploadType={ SIMPLE / RESUMABLE }
{
	fileName
	folderPath
	fileMetadata
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

We’ll put the file binary data in this boundary:

<file’s binary data goes here>

—xxBOUNDARYxx–
}
```

Response:
```bash
Content-Type: application/json
{
	fileID
	folderID
	metadata: { createdTime, fileStatus }
}
```

### Downloading a file in a folder
  
- When downloading binary content using HTTP, application/octet-stream can be		used to receive binary data

- The application/octet-stream MIME type is used for unknown binary files. It		preserves the file contents, but requires the receiver to determine file type, for		example, from the filename extension. The Internet media type for an arbitrary byte	stream is application/octet-stream.

- The * / * means that the client can accept any type of content in the response -		which could also be used for sending / receiving binary data

- Note that to download files, we could use either a pre-signed URL or a URL the		client can request to download from the CDN (let’s call it CDN URL). The process is	similar to uploading files, where the client first requests the servers for a pre-signed	URL OR CDN URL, then the client will download the file from the pre-signed URL /	CDN URL.

#### Request for a pre-signed URL / CDN URL

Request:
```bash
GET /folders/:folderID/files/:fileID/pre-signed-url OR cdn-url
```

Response:
```bash
{
	pre-signed URL or CDN URL
}
```

#### Download from pre-signed URL / CDN URL

Request:
```bash
GET /<pre-signed URL or CDN URL>
Accept: application/octet-stream
```

- The response body contains the file chunks. The chunks can also be returned	using multiplexing via HTTP/2.0. Multiplexing will allow the client to send		requests for the chunks of a file, then the server will send the responses		containing the file chunks in any order. The returned chunks can be used to		reconstruct the file on the client side.

Response:
```bash
Content-Type: application/octet-stream
Content-Disposition: attachment; filename=”<FILE_NAME>”
{
	file’s binary data used to generate the file on the client side
}
```

### Sharing a file

- This endpoint will create a new entry in the Shared files table

Request:
```bash
POST /folders/:folderID/files/:fileID/share
{
	userEmails (userEmails to share with)
}
```

### Synchronize file changes for user’s devices, and for different users

- After the client detects changes in the remote storage, or the remote servers notify the client that there are remote changes, the client will download changes via a pre-signed URL or	CDN URL sent by the servers

- Note that the client will likely get notified of remote changes from servers via a websocket connection or polling.

Request:
```bash
GET /folders/:folderID/files/:fileID/changes
```

Response:
```bash
{
	pre-signed URL or CDN URL

	fileName
	filePath
	fileMetadata
}
```

### Listing uploaded files in a folder

Request:
```bash
GET /folders/:folderID/files?nextCursor&limit
```

Response:
```bash
{
	files: [ { fileID, folderID, fileName } ],
	nextCursor, limit
}
```

### Deleting a file in a folder

- Note that this endpoint may use a cron job as a garbage collector to delete the files	with the fileStatus as UNDER_DELETETION, after the fileStatus is updated via this	endpoint

Request:
```bash
DELETE /folders/:folderID/files/:fileID
```

### Getting file versions (Optional - only necessary if versioning and retrieving file versions are needed)

- Retrieves all the file versions for the fileID using cursor based pagination, using the createdAt field in the File versions table as the nextCursor field.

Request:
```bash
GET /folders/:folderID/files/:fileID/versions?nextCursor={ createdAt value for the oldest versionID in the view port - it is assumed that the versionIDs are ordered by creation time }&limit
```

Response:
```bash
{
  versions: [ { versionID, createdAt, s3URLs } ],
  nextCursor, limit
}
```

## HLD

### Client

The client will be both uploading and downloading files, thus there will be separate sections in	the client code for an “uploader” and “downloader”:

#### Uploader

- The uploader will receive local file changes from the watcher, and then upload the file			changes in chunks via a pre-signed URL

#### Downloader

- The downloader will use either websockets or polling to receive file changes from the			remote servers, then download the file changes via a pre-signed URL or CDN URL

<br/>
<br/>

Additionally, the client will contain the following internal components which will communicate with	the uploader and downloader. This is also shown in ‘Client components’:

#### Chunker

- The client will also have a chunker functionality that splits the files when uploading to			the blob store, and also reconstructs the files from the downloaded chunks

#### Watcher (client-side sync agent)

- The watcher will monitor the local workspace for any updates, and also request the		synchronization service via websockets / polling for remote updates. It will initiate	the		synchronization for both directions: local -> remote and remote -> local.

- The watcher will likely use a chunk difference algorithm that compares the calculated		local fingerprint to the fingerprint in the DB to perform the necessary synchronization

- The Watcher may also batch the changes into chunks and request for upload every few seconds or so via a continuously running process, instead of uploading everytime a change happens

#### Client database

- To maintain the metadata for the files, chunks and folders on the local side, we’ll			store it in a client database. The watcher will frequently use the client database to			store local fingerprints, file / chunk metadata, and compare it against the remote Metadata DB.

Client components:

<img width="300" alt="image" src="https://github.com/user-attachments/assets/5b5263b0-e2f8-414d-9a63-e167053fa15f" />


<br/>
<br/>

As mentioned in Dropbox 101, there are two directions we need to sync in:

#### Local -> remote

- To sync in this direction, we’ll use a watcher that monitors the local Dropbox folder for			changes using OS-based file system APIs like FileSystemWatcher on Windows or			FSEvents on macOS. 

- When the watcher detects changes, it will locally queue (maintains a local queue of	changes) the modified file changes for upload. The watcher will then dequeue the		changes, then request for a pre-signed URL to upload the modified file changes to.			
- Conflicts will be resolved using a “last write wins” approach, which means that if two	users edit the same file, the most recent change detected will be the one that’s		queued.

- To ensure offline updates, when clients come back online, the queued file changes	can be dequeued by the watcher, then they could be uploaded to the blob store

#### Remote -> local

In this direction, clients will need to know when changes happen on the remote				server, so they can pull those changes. We can use two approaches, polling or				websockets or SSE:

##### Polling

- Via polling, the client periodically requests the server for any changes for					a specific fileID. The servers would query the database to see if the fileID					on the Files table has a newer updatedAt field than the updatedAt field for					the same fileID stored locally.

- Polling is simple, but can be slow to detect changes and wastes						bandwidth if done frequently

##### Websockets

- Using websockets, the server maintains a connection with each client					and pushes notifications to them when changes occur remotely. This is					more complex, but provides real-time updates for recently changed files.

##### SSE

- Via SSE, the server uses a HTTP connection to send events to the local					devices when file changes occur remotely. SSE may be more complex and					takes up bandwidth, but provides near real-time updates

##### Message queues using lastUpdated cursor

- Any remote file changes will be put into message queues via the 						synchronization service. The client will pull the file changes from the						message queues, and download them via a pre-signed URL / CDN URL.					

- Dropbox closely uses message queues, and thus we could have a		message queue for each folderID (since fileID will be very granular). After	the client downloads the modified chunks, it can update the client database	and set the “lastUpdated cursor” / updatedAt field for the folderID.

- Message queues using cursors at the folder level is much more complex,					and additional design choices such as partitioning the messages by the					fileID, and chunkID will cause overhead and is an overkill.

<br/>
<br/>

We can use a hybrid approach with websockets and polling. Files can be classified			into two categories, and we could apply websockets / polling for these different				categories. A hybrid approach uses less bandwidth for stale files and provides				real-time updates for fresh files:

##### Fresh files

- For files that have been recently edited in the past few hours, we can					maintain a websocket connection to ensure real-time sync. These are files which have been recently updated on a frequent basis, and thus would require a websocket connection to get real-time updates.

##### Stale files

- For files that haven’t been updated recently, we can use polling since					immediate updates are not needed. The polling can be done every 30 mins					or so, since the files haven’t been updated recently.
		
**Note that synchronization could be done only for files in the client’s currently opened	local folder / directory to lower bandwidth usage from polling / websockets**

### API servers

- The API servers will handle generic CRUD based requests which don’t directly involve		uploading, downloading and file sync operations. The API servers will handle requests for sending	pre-signed URLs / CDN URLs to clients for uploading / downloading files, and also handle		requests for sharing files, listing files, etc.

- The API servers will also handle requests for updating the metadata database during uploads / 	downloads.

### SQL Metadata database / cache
  
- The metadata database will store the metadata for files, chunks, folders, shared files, etc.

- The database could either be a SQL or NoSQL database such as DynamoDB or MongoDB.		Either one could potentially do the job, however, relations and transactions may be easier to		maintain within a SQL database. The tables do have relations among them and transactions may	still need to be performed on the file metadata, thus a DB such as PostgreSQL will be suitable,	which also provides functionality for custom types incase we need to grow the schema. However,	a NoSQL database could perform just as well - but it may not be as easy to maintain relations or	transactions.

- Clients can request the API servers to share files with other users, where they can just enter the	email they want to share with, assuming the email is already authenticated. File sharing can be	implemented using the below and in ‘File sharing solutions’:
  - Add a sharelist to metadata
  - Caching to speed up fetching the sharelist
  - Create a separate table for shares:
    - The Shared files table can also be used to enforce permissions when a user tries to			access a fileID

#### Cache

- Additionally, the metadata could be cached. Either Redis or Memcached could be used here -	Redis may be suitable if the data types are more complex and we require flexibility in the writes.	Also, Redis provides Redis Sentinel and Redis Cluster for cluster management, while Memcached	itself has no support for replication.

- Memcached may be more suitable if the data types are simple, static and has more read		intensity. Most of the metadata might benefit from Redis' data structures such as lists. Redis lists could also potentially be used to store the folder-file relationship, where a folderID will contain multiple fileIDs.

Note: A high-end memory optimized server can have 144GB of RAM, which should be able to easily	cache 10s of thousands of metadata entries.

### Blob store
  
- The blob store will store the file chunks. The file itself can be uploaded in the below ways and in	‘Uploading file to storage solutions’:
  - Upload file to a single server
  - Store file in blob storage:
    - A lot of the times, having the client upload the file to the API servers, then having the			API servers upload to the blob store is redundant and slow especially for large files			because the uploading process has to be done twice. Clients could directly upload to			the blob store via a pre-signed URL, and any security or validation checks can be				performed via the blob store client interfacing the blob store after the user has			 	uploaded to the pre-signed URL.

    - However, in some applications, such as YouTube, where the videos will need				additional transformation, having intermediary API servers may be suitable.

  - Upload file directly to blob storage:
    - We can use pre-signed URLs to upload files directly to the blob store. Pre-signed			URLs can be sent via the servers to the clients. Clients can then use the pre-signed			URL, which may have a TTL to upload / download their files. Pre-signed URLs are			explained in ‘Pre-signed URLs’.

- The blob store client could also handle conflicts from concurrent updates by using S3 Object	Locks at the chunk level, instead of locks for the whole file. Additionally, vector clocks and		versioning could be used to detect conflicts within chunks - if two users updated the same chunk	at the same time
	
### CDN
  
CDNs will support in downloading files, as explained below and in ‘Downloading file solutions’:
- Download through file server:
  - In this approach the file is downloaded twice, once from the blob store to the servers,			then another time from the servers to the client. This will be both slow and expensive

- Download from blob storage:
  - This approach will work for small to moderate scale apps, however, for large scale			apps such as Dropbox, the files may need to be downloaded from CDN POPs spread			across globally

- Download from CDN:
  - In this approach, servers can send a CDN URL to the client, similar to a pre-signed			URL of a blob store. The client will request the CDN URL, and download the file. This			CDN URL will give the user the permission to download the file from a specific CDN			POP for a limited time.

  - CDNs are usually expensive, thus the files can be strategically cached using a TTL			and invalidation techniques to remove less frequently accessed files

### Synchronization service
  
- The synchronization service will allow clients to connect via websockets OR poll to receive		updates when files change remotely. It will be used to deliver updates in the direction: remote ->	local.

- Any client or user could update the file either locally or remotely, and this update will be		reflected in the blob store and the DB. Other clients (currently in the share list for the fileID) will	receive the same file changes via websocket / polling.

- When a user is offline, they won’t be able to establish a websocket or poll. When they come back	online, they’ll establish the websocket / poll for any remote file changes.

### L4 Load balancer

- We’ll need an L4 load balancer to support traffic at the TCP level. L4 load balancers, let’s say	using ELB in TCP mode can load balance websockets. When client’s need to connect to a		websocket server, the L4 load balancer will route them to the server they previously connected to	or to a server using the load balancing algorithm. However, if a server goes down, the L4 load	balancer can route the client to connect to another server instead.

- When a client needs to connect to the server, the request will first go to the L4 load balancer,	then to the server. There will actually be a symmetric websocket connection between both the	client to the L4 load balancer, and between the L4 load balancer to the server.

- L4 load balancers can be stateful and use sticky sessions to persist the server the client		previously connected to. The sticky session can be implemented by identifying the user, usually	with cookies or their IP address, and storing the user’s connected server for handling future		requests.

- If clients disconnect from a server, they can automatically reconnect to the	 same server or		another one via the L4 load balancer. Reconnecting to the same server may be easier, as the	session data in the L4 load balancer doesn’t have to be updated.

<img width="750" alt="image" src="https://github.com/user-attachments/assets/e9d740d7-bdf1-4a39-9fbd-18ee9bd92d70" />

## DD

### Versioning
  
- To implement file versioning, we could maintain a separate File versions table which contains the	versionIDs for the same fileID.

We can implement file versioning using the below approaches:
- Upload a completely new file on each change, and add a new version to the File versions	table:
  - Instead of overwriting the only stored file in the blob store, we could upload a		completely	new file when the file changes locally / remotely, and set a new version for	it by adding a new entry to the File versions table

- Upload only modified chunks, and add a new version to the File versions table:
  - We could only upload the modified chunks and set a new version for the file with the	modified chunks by adding a new entry to the File versions table. Also, because we've now uploaded new modified chunks, we'll include a new versionID field to the Chunks table. We'll also add these new modified chunks to the Chunks table.

### Supporting large files

Two main design choices can be implemented to support uploading / downloading large files:

#### Progress indicator
  
- Users should be able to see the progress on the UI so that they could resume or			retry uploads / downloads if needed
		
#### Resumable uploads

- Users should be able to pause and resume uploads. If they lose internet connection,		they should be able to pick up where they left off rather than re-uploading the entire		file again

<br/>
<br/>

Uploading a large file via a single POST request has the following limitations:

#### Timeouts

- Servers and clients usually have timeout settings, which prevents long running				processes. A single POST request for a 50 GB file could easily exceed these				timeouts.

- If we have a 50 GB file, an an internet connection of 100 Mbps, it will take 					(50 GB * 8 bits / byte) / 100 Mbps = 4000 seconds = 1.11 hours to upload a file
		
#### Browser and server limitation

- Usually browsers and servers will also impose limits on the size of a request or data	being transferred. The default is usually less than 2 GB for web servers like Apache /	NGINX, but can be configured. AWS services also have default limits, which		sometimes cannot be increased.		

#### Network interruptions

- Large files are more prone to network interruptions. If a user is uploading a 50 GB file			and their internet connection drops, they may have to restart the entire upload.

#### User experience

- Users are also blind on the “actual progress” of sending a large file, as they have no			idea how long it will take

<br/>
<br/>

#### We can perform chunking for large file transfers

- To address the limitations of large files, we can use chunking to break the file into smaller		fixed size pieces, and upload them in parallel (or one at a time if network quality is bad).		Chunking will need to be done on the client side, so that the client can split the file into			chunks, and send them to the blob store.

- The client can calculate the optimal chunk size based on the client device being used, the		client’s network connection, average file size in the blob store, etc. The average chunk size		is usually 5-10 MB.

- Chunking can also be used to show a progress indicator, where the uploaded chunks			updates the progress bar.
	
#### Resumable uploads using chunking

- To handle resumable uploads, we need to keep track of which chunks have been uploaded		and which haven’t. The status of the chunk can be maintained in the Chunks table, which		will contain the chunkStatus.

- If a user resumes the upload, we can check the Chunks table to check which chunkIDs for		the fileID have been UPLOADED / NOT_UPLOADED, and then resume uploading the				NOT_UPLOADED chunkIDs.
<br/>
<br/>

Because we need to update the chunkStatus fields of the Chunks table after the chunks have	been successfully UPLOADED / FAILED to upload, we can do the following or in ‘Updating Chunks	table upon chunkID upload success / failure’:

##### Update based on client PATCH request
- In this approach, the client will send a PATCH request to the servers to update the			Chunks table entries after a chunk has UPLOADED / FAILED, and the client has received			the response from the blob store client. This may not be secure,	 since malicious				actors could potentially send the PATCH request to update the Chunks table.

##### Rely on S3 Event Notifications

- We could instead use S3 event notifications to keep the Chunks table updated when			chunkIDs uploaded successfully / failed. This is done on the server side as opposed to			the client side using a PATCH request, thus it will be more secure. S3 event					notifications could be sent to a Lambda function, which will update the DB.

<br/>
<br/>

#### Fingerprint of files to check which parts of the file have been uploaded

- A fingerprint is a mathematical calculation that generates a unique hash value based on		the content of the file. The hash value can be created using SHA-256 or other cryptographic		hash functions. The hash value can be used as a unique ID for the file. Using the fingerprint,		we can check if any part of the file has already been uploaded before, since the fingerprint		will change on each upload depending on the content of the file / chunk.

- The uploader on the client side will fingerprint the entire local file and also the chunks. The		uploader will then send a request to the servers to check if the local file’s and chunks’			fingerprints exist for the fileID and chunkIDs in the Files and Chunks tables. If the local			fingerprints don’t exist in the tables, the client will then use a pre-signed URL from the			servers to upload the local file / chunks. After the servers have sent the pre-signed URL to		the client, the servers will also update the fileID’s and chunkID’s fileStatus and chunkStatus		values respectively to UPLOADING (for the fileID) / NOT_UPLOADED (for the chunkIDs). After the blob		store client receives the uploaded chunks, it will send S3 event notifications to a Lambda		function to update the fileID and chunkIDs to UPLOADED.
		
- Throughout this process, the uploader will also track the chunks uploading progress and	update the UI

- This upload process with fingerprints is not unusual, it is actually used via S3 multipart		upload as explained in ‘S3 multipart upload’.

### Making uploads / downloads / syncing as fast as possible

#### Making uploads fast

- Chunking will already speed up file uploading, as only necessary chunks via the calculated		fingerprints will need to be uploaded. Chunks can also be uploaded and downloaded in			parallel, and chunks can be adjusted depending on the network quality, which will maximize		the use of available bandwidth.

#### Making downloads fast

- File downloads will become faster if using chunking and a CDN to store the files and chunks closer to the	user	

#### Making syncing fast

- Chunking can also be used for syncing files - when a file changes, only the chunks with		different local fingerprints and remote fingerprints (in DB) will need to be synced.

#### Compression

- Compression can also speed up both uploads / downloads, where the file size is reduced		while preserving the content via a lossless compression algorithm. Fewer bytes will also		need to be transferred. The compression algorithm can be located in both the client and		server side. We can compress a file on the client before uploads, and compress the file on		the server before downloads. The recipient will then decompress the file. ‘Compression			algorithms’ explains some suitable compression algorithms.

- Usually, media files like images, videos and audio have very low compression ratios which		makes compression not worth it. However, for text files, the compression ratio is much			higher and can be compressed much more. The compression can be done based on the		fileType and size of the file.

### Support for user's device synchronization

- To ensure support for different types of devices, we can have a Devices table where a single userID could have multiple deviceIDs. When file changes occur remotely, these changes can be fetched via the websocket connections / polling for all the deviceIDs belonging to a userID. This way, when changes are being synchronized from both directions, remote -> local or local -> remote, we'll synchronize the changes to all the deviceIDs of a userID - instead of only relying on the userID, we'll use the deviceID to differentiate between devices belonging to a user. A device limit can also be introduced for a single user.

### File security

Security can be improved via the following approaches:

#### Encryption in transit

- We will of course use HTTPS to encrypt the data as it’s transferred between the				client and server.

#### Encryption at rest

- We should also encrypt the files stored in S3. S3 has an encryption at rest feature			that is easy to enable. S3 will then encrypt the file using a unique key and store the			key separately from the file. Users cannot decrypt the file without this unique key.

#### Access control

- The Shared files table also contains the basic ACL and can be used to validate				permissions of userIDs accessing a fileID.
		
#### Pre-signed URL / CDN URL prevents unauthorized users

- Pre-signed URLs and CDN URLs will also prevent unauthorized users from				uploading / downloading to the blob store / CDN. Even if unauthorized users have the			URL, because there is a TTL on the URLs, they won’t be able to use expired URLs.

- These URLs work for modern CDNs like CloudFront, and are a feature of S3. They			work as shown in ‘Workings of pre-signed URL / CDN URL’

### Sync conflicts during writes by multiple users

- When multiple users are modifying the same file, there will likely be sync conflicts. Due to this, it's likely that there is another service like a Document service which performs a conflict resolution algorithm like OT or CRDT to produce finalized writes / edits from multiple users. This Document service will likely also maintain a websocket connection with clients and allow clients to send edits. The SDI on 'Collaborative document editing - Google docs' goes over OT / CRDT in detail.

### Saving blob store storage space

- When supporting file versioning, the storage space can be filled up very quickly. Therefore, we can include the following techniques to reduce storage space:
  - Deduplicate chunks:
    - We can remove duplicate chunks in the blob store, and determine if the chunks are duplicates by using their fingerprint values
  - Limit the number of versions of a file if necessary
  - Move infrequently used chunks to cold storage:
    - If a file's chunks have not been accessed for months or years, we could move them to a cold storage like the Standard-IA tier within S3, which should be cheaper to store data.

### Partitioning / sharding database

- Because we want to group the chunkIDs together for a specific fileID, and we want to group the fileIDs together for a specific folder - we can partition / shard the Chunks table using the fileID, and partition / shard the Files table using the folderID. This way, chunk data for a specific file will reside on a single shard / partition, and files metadata for a specific folder will reside on a single shard / partition, which will mean only a single shard / partition needs to be read.

- Likewise, because we want to efficiently retrieve a specific userID's folders, we can shard / partition the Folders table using the userID, so that only a single shard / partition needs to be read.


