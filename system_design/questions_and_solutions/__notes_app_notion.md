# Notes app like Notion

Create a notes app like Notion, MS OneNote, etc, where you can create notes, and also nest notes inside notes.

**Note that this SDI is similar to the SDI 'Todo list app' and 'Dropbox'**

## Requirements

### Questions

- Should we focus on how the notes hierarchy should be stored and efficiently fetched, or should we also focus on the design of how the notes data (binary data) is stored in the backend via chunking?
  - Yes, focus on both the notes hierarchy and how the binary data is stored
 
- Should our system focus on the uploading and downloading of the notes binary data, as notes are being updated and fetched?
  - Yes

- Is the note data only text based, or can users also upload image based content?
  - For simplicity, let's assume that notes are only text based

- Should there be notes synchronization between devices belonging to the same user?
  - Yes, talk about this in the DD

- What is the DAU, and how many concurrent users will there be?
  - Assume 100M DAU, and 20k concurrent users per second

### Functional

- Notes can be nested inside another note
- Users can list their notes
- Users can create (upload) / read (download) notes from the backend
- Users can write to a note

<br/>
<br/>

- The system should also synchronize the note updates across a user's devices
- Assume 100M DAU, and 20k concurrent users per second

### Non-functional

- The system should efficiently store the notes hierarchy
- Notes data uploading / downloading throughput:
  - The system should handle throughput appropriately for uploading / downloading large volumes of note data like 50 GB
- Durability / availability:
  - The system should durably persist the notes data
- Low latency in synchronization:
  - The system should make synchronization between devices as fast as possible

<br/>
<br/>

Before going further, it's best to review the Dropbox 101 section in the SDI 'Dropbox'

## Data model / entities

- Notes:
  - The Notes and Chunks entities contain the info on the notes and chunks, such as the noteStatus, chunkStatus, etc, which will be in a blob store
  - The checkSum field is a hash value verifying the integrity	of the data, and detecting if errors exist in the file
  
    - noteID
    - parentNoteID
    - userID
    - noteName
    - s3URLs
    - noteStatus: enum UPLOADING / UPLOADED
    - checkSum
    - fingerprint
    - createdAt

- Chunks:
  
  - chunkID
  - noteID
  - fingerprint
  - chunkStatus: enum UPLOADED / NOT_UPLOADED / FAILED

- Devices (Optional - only for supporting different types of devices like mobile and laptop):
  - Since a user could have multiple devices, this entity will store all deviceIDs		belonging to a userID
    
    - deviceID
    - userID

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Listing notes

- Because notes can be nested inside other notes, this endpoint will be used to list the notes which are either at the root of the hierarchy, or nested inside another noteID

Request:
```bash
GET /nested-notes (listing notes at the root of the hierarchy)
GET /nested-notes/:noteID (listing nested notes inside the noteID)
```

- Note that because we're only listing the notes, we can return a partial view of the Notes entity. This partial view can be used to render the notes path on the UI, ie note1/nested_note2/note3

Response:
```bash
{
  notes: [ { noteID, parentNoteID, noteName } ]
}
```

### View note

- This endpoint will be used to view and download a note's data (binary data)

#### Downloading a note

- When downloading binary content using HTTP, application/octet-stream can be		used to receive binary data

- The application/octet-stream MIME type is used for unknown binary files. It		preserves the file contents, but requires the receiver to determine file type, for		example, from the filename extension. The Internet media type for an arbitrary byte	stream is application/octet-stream.

- The * / * means that the client can accept any type of content in the response -		which could also be used for sending / receiving binary data

- Note that to download files, we could use either a pre-signed URL or a URL the		client can request to download from the CDN (let’s call it CDN URL). The process is	similar to uploading files, where the client first requests the servers for a pre-signed	URL OR CDN URL, then the client will download the file from the pre-signed URL /	CDN URL.

#### Request for a pre-signed URL / CDN URL

- Note that this endpoint is /notes, and is used for retrieving the actual note data, not the list of nested notes

Request:
```bash
GET /notes/:noteID/pre-signed-url OR cdn-url
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
  note’s binary data used to generate the note on the client side
}
```

### Creating and uploading note data

- This endpoint will be used to create and upload note data (binary data) to the backend servers. It's already assumed that a empty noteID was created using an endpoint like 'POST /notes'

#### Uploading a note

- Note that there could likely be 2 types of uploads supported depending on the note's size. A simple upload could be used when the size is small, and can be uploaded in one go. A resumable upload could be used when the size is large, as discussed in the DD.

- When uploading binary data, multipart/form-data / multipart/mixed or another MIME	type such as image/png is usually used

- The content type is set to multipart/mixed which means that the request contains	different inputs and each input can have a different encoding type (JSON or binary).	The metadata sent will be in JSON, while the note data itself will be in binary. 

- The placeholder {---xxBOUNDARYxx—} will contain a text string for the boundary	that differentiates one part of the body from another. For example				“__the_boundary__” could be used as the string. Boundaries must also start with		double hyphens and end with double hyphens too.

- Note that since this design is using a pre-signed URL to upload the note data, the client will	first request for a pre-signed URL from the servers, then make a HTTP PUT request	with the note (binary data) data in the request body to the pre-signed URL

- When the client requests for a pre-signed URL, the client will also send in the note	metadata in the request body, and the API servers will update the note metadata into	the database.

#### Request for a pre-signed URL

Request:
```bash
POST /notes/:noteID/pre-signed-url?uploadType={ SIMPLE / RESUMABLE }
{
	noteName
	parentNoteID
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

We’ll put the note's binary data in this boundary:

<note’s binary data goes here>

—xxBOUNDARYxx–
}
```

Response:
```bash
Content-Type: application/json
{
	noteID
	metadata: { createdAt, noteStatus }
}
```

## HLD

### Client

The client will be both uploading and downloading note data, thus there will be separate sections in	the client code for an “uploader” and “downloader”:

#### Uploader

- The uploader will receive local changes in the note data from the watcher, and then upload the note			changes in chunks via a pre-signed URL

#### Downloader

- The downloader will be used to download the note changes via a pre-signed URL or CDN URL

<br/>
<br/>

Additionally, the client will contain the following internal components which will communicate with	the uploader and downloader. This is also shown in ‘Client components’:

#### Chunker

- The client will also have a chunker functionality that splits the note binary data when uploading to			the blob store, and also reconstructs the note (in textual form) from the downloaded chunks

#### Watcher (client-side sync agent)

- The Watcher will monitor the local note data for any updates, and use the Uploader to upload the note changes to the servers via the pre-signed URL

- The Watcher will likely use a chunk difference algorithm that compares the calculated		local fingerprint to the fingerprint in the DB to find the note's differences to upload

- The Watcher may also batch the changes into chunks and request for upload every few seconds or so via a continuously running process, instead of uploading everytime a change happens

#### Client database

- To maintain the metadata for the files, chunks and folders on the local side, we’ll			store it in a client database. The watcher will frequently use the client database to			store local fingerprints, file / chunk metadata, and compare it against the remote Metadata DB.

Client components:

<img width="300" alt="image" src="https://github.com/user-attachments/assets/5b5263b0-e2f8-414d-9a63-e167053fa15f" />

#### Creating and uploading note workflow

The workflow for creating and uploading a note will look like:

<br/>

1. It's assumed that an empty noteID was already created using an endpoint like 'POST /notes'. This endpoint will also create an entry for the nodeID in the Metadata DB.

2. The Watcher will then detect local note changes, and send the chunk differences retrieved from the Chunker to the Uploader for upload: 
    - To upload local note changes, the Watcher will monitor the local storage (either in the desktop, web app or mobile) for changes using OS-based file system APIs like FileSystemWatcher on Windows or FSEvents on macOS.
  
    - When the Watcher detects changes, it will locally queue (maintains a local queue of changes) the modified note changes for upload. The Watcher will then dequeue the changes, then request for a pre-signed URL via the endpoint 'POST /notes/:noteID/pre-signed-url'.
  
    - The Watcher will then send the note changes to the Uploader, then the Uploader will upload the note changes via the pre-signed URL using the endpoint 'PUT /<pre-signed URL>'

3. As the note's chunks are being uploaded by the Uploader, the nodeID's noteStatus will be set as UPLOADING via S3 event notifications to the Metadata DB, and the chunkStatus of the chunks will go from NOT_UPLOADED to UPLOADED.

4. Once all the chunkStatuses are UPLOADED, via S3 event notifications, the noteStatus will change to UPLOADED for the noteID.

#### Listing then downloading note workflow

The workflow for listing then downloading a note will look like:

<br/>

1. The client could initially request the endpoint 'GET /nested-notes/:noteID' to list the nested noteIDs inside the noteID

2. When the client wants to view a note and download the note's data from the backend, the Downloader will request the endpoint 'GET /notes/:noteID/pre-signed-url' to get back a pre-signed URL.

3. The Downloader will then request the endpoint 'GET /<pre-signed URL' to get back the note's binary data (chunks)

4. After the note's chunks are retrieved, the Downloader will use the Chunker to reconstruct the note in a textual format in the UI

### API servers

- The API servers will handle generic CRUD based requests which don’t directly involve uploading and downloading of the notes' binary data. The API servers will handle requests for sending pre-signed URLs / CDN URLs to clients for uploading / downloading note data, and also handle requests for listing nested notes.

- The API servers will also handle requests for updating the metadata database during uploads / downloads.

### SQL Metadata database / cache

- The Metadata database will store the metadata for notes, chunks, etc.

- The database could either be a SQL or NoSQL database such as DynamoDB or MongoDB.		Either one could potentially do the job, however, relations and transactions may be easier to		maintain within a SQL database. The tables do have relations among them and transactions may	still need to be performed on the note metadata (when a note's chunks are being uploaded, and we need to have data consistency via the noteStatus / chunkStatus), thus a DB such as PostgreSQL will be suitable,	which also provides functionality for custom types incase we need to grow the schema. However,	a NoSQL database could perform just as well - but it may not be as easy to maintain relations or	transactions.

#### Cache

- The recently updated metadata could also be cached to reduce the load on the database and improve read latencies. Because there is a note hierarchy (using the noteID and parentNoteID), we can use Redis lists to store the different levels of the hierarchy, where a noteID in a Redis list could point to a parentNoteID in another Redis list.

Note: A high-end memory optimized server can have 144GB of RAM, which should be able to easily	cache 10s of thousands of metadata entries.

### Blob store

- The blob store will store the note's chunks. The note data itself can be uploaded in the below ways and in	‘Uploading note / file to storage solutions’ (taken from the SDI 'Dropbox'):
  - Upload note / file to a single server
  - Store note / file in blob storage:
    - A lot of the times, having the client upload the note / file to the API servers, then having the			API servers upload to the blob store is redundant and slow especially for large note data			because the uploading process has to be done twice. Clients could directly upload to			the blob store via a pre-signed URL, and any security or validation checks can be				performed via the blob store client interfacing the blob store after the user has			 	uploaded to the pre-signed URL.

    - However, in some applications, such as YouTube, where the videos will need				additional transformation, having intermediary API servers may be suitable.

  - Upload note / file directly to blob storage:
    - We can use pre-signed URLs to upload notes / files directly to the blob store. Pre-signed			URLs can be sent via the servers to the clients. Clients can then use the pre-signed			URL, which may have a TTL to upload / download their files. Pre-signed URLs are			explained in ‘Pre-signed URLs’ (taken from the SDI 'Dropbox').

- The blob store client could also handle conflicts from concurrent updates by using S3 Object	Locks at the chunk level, instead of locks for the whole file. Additionally, vector clocks and		versioning could be used to detect conflicts within chunks - if two users updated the same chunk	at the same time

### CDN

CDNs will support in downloading notes / files, as explained below and in ‘Downloading note / file solutions’ (taken from the SDI 'Dropbox'):
- Download through note / file server:
  - In this approach the note / file is downloaded twice, once from the blob store to the servers,			then another time from the servers to the client. This will be both slow and expensive

- Download from blob storage:
  - This approach will work for small to moderate scale apps, however, for large scale			apps such as Dropbox, the files may need to be downloaded from CDN POPs spread			across globally

- Download from CDN:
  - In this approach, servers can send a CDN URL to the client, similar to a pre-signed			URL of a blob store. The client will request the CDN URL, and download the note / file. This			CDN URL will give the user the permission to download the note / file from a specific CDN			POP for a limited time.

  - CDNs are usually expensive, thus the notes / files can be strategically cached using a TTL			and invalidation techniques to remove less frequently accessed notes / files

<img width="900" alt="image" src="https://github.com/user-attachments/assets/b4ea6777-a7b3-4a28-8714-55109c7f98f5" />

## DD

### Maintaining note hierarchy

- Rather than storing the entire note hierarchy all within a single entry in the Notes table, it's much more efficient to store the individual nested notes themselves as separate entries. We're also linking which noteIDs are parent to which other noteIDs via the parentNoteID field.

### Supporting large note data

Two main design choices can be implemented to support uploading / downloading large note data:

#### Progress / saving indicator
  
- Users should be able to see the progress / saving indicator on the UI so that they could resume or			retry uploads / downloads if needed
		
#### Resumable uploads

- Users should be able to pause and resume uploads. If they lose internet connection,		they should be able to pick up where they left off rather than re-uploading the entire		note again

<br/>
<br/>

Uploading a large note via a single POST request has the following limitations:

#### Timeouts

- Servers and clients usually have timeout settings, which prevents long running				processes. A single POST request for a 50 GB note could easily exceed these				timeouts.

- If we have a 50 GB note, an an internet connection of 100 Mbps, it will take 					(50 GB * 8 bits / byte) / 100 Mbps = 4000 seconds = 1.11 hours to upload a file
		
#### Browser and server limitation

- Usually browsers and servers will also impose limits on the size of a request or data	being transferred. The default is usually less than 2 GB for web servers like Apache /	NGINX, but can be configured. AWS services also have default limits, which		sometimes cannot be increased.		

#### Network interruptions

- Large notes are more prone to network interruptions. If a user is uploading a 50 GB note			and their internet connection drops, they may have to restart the entire upload.

#### User experience

- Users are also blind on the “actual progress” of saving a large note to the backend, as they have no			idea how long it will take

<br/>
<br/>

#### We can perform chunking for large note data transfers

- To address the limitations of large note data, we can use chunking to break the note data into smaller		fixed size pieces, and upload them in parallel (or one at a time if network quality is bad).		Chunking will need to be done on the client side, so that the client can split the note into			chunks, and send them to the blob store.

- The client can calculate the optimal chunk size based on the client device being used, the		client’s network connection, average file size in the blob store, etc. The average chunk size		is usually 5-10 MB.

- Chunking can also be used to show a progress / saving indicator, where the uploaded chunks			updates the progress bar.
	
#### Resumable uploads using chunking

- To handle resumable uploads, we need to keep track of which chunks have been uploaded		and which haven’t. The status of the chunk can be maintained in the Chunks table, which		will contain the chunkStatus.

- If a user resumes the upload, we can check the Chunks table to check which chunkIDs for		the noteID have been UPLOADED / NOT_UPLOADED, and then resume uploading the				NOT_UPLOADED chunkIDs.
<br/>
<br/>

Because we need to update the chunkStatus fields of the Chunks table after the chunks have	been successfully UPLOADED / FAILED to upload, we can do the following or in ‘Updating Chunks	table upon chunkID upload success / failure’ (taken from the SDI 'Dropbox'):

##### Update based on client PATCH request
- In this approach, the client will send a PATCH request to the servers to update the			Chunks table entries after a chunk has UPLOADED / FAILED, and the client has received			the response from the blob store client. This may not be secure,	 since malicious				actors could potentially send the PATCH request to update the Chunks table.

##### Rely on S3 Event Notifications

- We could instead use S3 event notifications to keep the Chunks table updated when			chunkIDs uploaded successfully / failed. This is done on the server side as opposed to			the client side using a PATCH request, thus it will be more secure. S3 event					notifications could be sent to a Lambda function, which will update the DB.

<br/>
<br/>

#### Fingerprint of note to check which parts of the note have been uploaded

- A fingerprint is a mathematical calculation that generates a unique hash value based on		the content of a file / note. The hash value can be created using SHA-256 or other cryptographic		hash functions. The hash value can be used as a unique ID for the note. Using the fingerprint,		we can check if any part of the note has already been uploaded before, since the fingerprint		will change on each upload depending on the content of the note / chunk.

- The uploader on the client side will fingerprint the entire local note and also the chunks. The		uploader will then send a request to the servers to check if the local note’s and chunks’			fingerprints exist for the noteID and chunkIDs in the Notes and Chunks tables. If the local			fingerprints don’t exist in the tables, the client will then use a pre-signed URL from the			servers to upload the local note / chunks. After the servers have sent the pre-signed URL to		the client, the servers will also update the noteID’s and chunkID’s noteStatus and chunkStatus		values respectively to UPLOADING (for the noteID) / NOT_UPLOADED (for the chunkIDs). After the blob		store client receives the uploaded chunks, it will send S3 event notifications to a Lambda		function to update the noteID and chunkIDs to UPLOADED.
		
- Throughout this process, the uploader will also track the chunks uploading progress and	update the UI

- This upload process with fingerprints is not unusual, it is actually used via S3 multipart		upload as explained in ‘S3 multipart upload’ (taken from the SDI 'Dropbox').

### Making uploads / downloads as fast as possible

#### Making uploads fast

- Chunking will already speed up uploading, as only necessary chunks via the calculated		fingerprints will need to be uploaded. Chunks can also be uploaded and downloaded in			parallel, and chunks can be adjusted depending on the network quality, which will maximize		the use of available bandwidth.

- When a note changes, only the chunks with		different local fingerprints and remote fingerprints (in DB) will need to be uploaded.

#### Making downloads fast

- Downloads will also become faster if using chunking and a CDN to store the notes and chunks closer to the	user	

#### Compression

- Compression can also speed up both uploads / downloads, where the note size is reduced		while preserving the content via a lossless compression algorithm. Fewer bytes will also		need to be transferred. The compression algorithm can be located in both the client and		server side. We can compress a note on the client before uploads, and compress the note on		the server before downloads. The recipient will then decompress the note. ‘Compression			algorithms’ (taken from the SDI 'Dropbox') explains some suitable compression algorithms.

- Usually, media files like images, videos and audio have very low compression ratios which		makes compression not worth it. However, for text files, the compression ratio is much			higher and can be compressed much more. The compression can be done based on a		fileType field and size of the file.

### Support for user's device synchronization

- To ensure support for different types of devices, we can have a Devices table where a single userID could have multiple deviceIDs. When file changes occur remotely, these changes can be fetched via the websocket connections / polling for all the deviceIDs belonging to a userID. This way, when changes are being uploaded to the backend from a client, we'll download the changes to all the deviceIDs of a userID - instead of only relying on the userID, we'll use the deviceID to differentiate between devices belonging to a user. A device limit can also be introduced for a single user.

### File / note security

Security can be improved via the following approaches:

#### Encryption in transit

- We will of course use HTTPS to encrypt the data as it’s transferred between the				client and server.

#### Encryption at rest

- We should also encrypt the files stored in S3. S3 has an encryption at rest feature			that is easy to enable. S3 will then encrypt the file using a unique key and store the			key separately from the file. Users cannot decrypt the file without this unique key.
		
#### Pre-signed URL / CDN URL prevents unauthorized users

- Pre-signed URLs and CDN URLs will also prevent unauthorized users from				uploading / downloading to the blob store / CDN. Even if unauthorized users have the			URL, because there is a TTL on the URLs, they won’t be able to use expired URLs.

- These URLs work for modern CDNs like CloudFront, and are a feature of S3. They			work as shown in ‘Workings of pre-signed URL / CDN URL’ (taken from the SDI 'Dropbox')

### Saving blob store storage space

- Because note data is variable and can become large very quickly over time, we can include the following techniques to reduce storage space:
  - Deduplicate chunks:
    - We can remove duplicate chunks in the blob store, and determine if the chunks are duplicates by using their fingerprint values
  - Move infrequently used chunks to cold storage:
    - If a note's chunks have not been accessed for months or years, we could move them to a cold storage like the Standard-IA tier within S3, which should be cheaper to store data.

### Partitioning / sharding database

- Because we want to group the chunkIDs together for a specific noteID - we can partition / shard the Chunks table using the noteID. This way, chunk data for a specific note will reside on a single shard / partition, which will mean only a single shard / partition needs to be read.

- Likewise, because we want to efficiently retrieve a specific userID's noteIDs, we can shard / partition the Notes table using the userID, so that only a single shard / partition needs to be read.












