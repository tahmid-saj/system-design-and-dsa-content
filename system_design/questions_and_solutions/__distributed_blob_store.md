# Distributed blob store

## Requirements

### Questions

- Should the system allow users to upload / download / delete blobs, and manage containers?
  - Yes 

- Does the system need data versioning?
	- Yes
  
- Does the system store any kind of data (blob)?
	- Yes, binary data

- Should the storage follow a flat data organization?
	- Yes, with a bucket/container and blobs inside of it

### Functional

- The blobs in the storage follow write one, read many (WORM)
	- Usually bob stores follow this approach, where instead of modifying	a blob in the storage, we upload a new version for the same blob

- The blobs in the storage must have versioning
- The system should store any kind of data (mainly binary data)

- We can create a container to group blobs
- The system should support the operations:
  - Create container
  - List containers
  - Delete container
	
  - Put blob
  - List blobs
  - Get blob
  - Delete blob

### Non-functional

- Durability / availability:
	- The system should durably persist the blobs

- Blob uploading / downloading throughput:
	- The system should handle throughput appropriately for uploading / downloading		large files like 50 GB

## Blob store 101

### WORM

- Blob stores usually follow WORM (write once, read many times)

### Chunking

- Files can be stored as fixed size chunks. This can help		when uploading large files, and also ensures that if the		chunk failed to be uploaded, then only that chunk needs to	be re-tried in uploading, instead of re-trying all the chunks		for the file.

- We can also reduce the amount of data uploaded by		comparing and uploading only the modified chunks when a	file is being updated

### Client-side caching

- Caching at the client side a copy of the metadata can		prevent multiple requests being made to	the databases

### Data model / entities

- Users:
	- userID
	- userName

- Containers:
	- containerID
	- userID
	- containerName

- Blobs:
  - The blobs and chunks tables contains info on the blobs and chunks, such as blobName, chunkStatus, etc, which will be in the blob store

  - The checkSum field is a hash value verifying the integrity of the data, and detecting if errors exist in the file
  
    - blobID
    - containerID
    - userID
    - blobName
    - s3URLs (the s3URLs will allow clients to upload / download the blobs directly from the blob store storage, instead of uploading / downloading the blobs from the API servers)
    - blobStatus: UPLOADING / UPLOADED
 
    - checkSum
    - metadata: { fileSize, fileType, createdTime, updatedAt }
 
    - fingerprint

- Chunks:
  - This entity will contain the chunkID : nodeID mappings the node manager service will use
    - chunkID
    - blobID
    - nodeID
    - chunkStatus: UPLOADED / NOT_UPLOADED / FAILED
   
    - fingerprint

- Blob versions:
  - This entity will contain the versionIDs for a blobID. New entries will be added when a new version of the blobID is uploaded
  - This table is only necessary if blob versioning is in scope
 
    - versionID
    - blobID
    - createdAt

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Container endpoints

#### Create container

Request:
```bash
POST /containers
{
	containerName
}
```

#### List containers

Request:
```bash
GET /containers?nextCursor&limit
```


Response:
```bash
{
  containers: [ { containerID, containerName } ],
  nextCursor, limit
}
```

#### Delete container

- Note that the container and any blobs in it are deleted during garbage collection asynchronously

Request:
```bash
DELETE /containers/:containerID
```

### Blob endpoints

#### Put blob

- When uploading binary data, multipart/form-data / multipart/mixed or another MIME	type such as image/png is usually used

- The content type is set to multipart/mixed which means that the request contains	different inputs and each input can have a different encoding type (JSON or binary).	The metadata sent will be in JSON, while the file itself will be in binary. 

- The placeholder {---xxBOUNDARYxx—} will contain a text string for the boundary	that differentiates one part of the body from another. For example				“__the_boundary__” could be used as the string. Boundaries must also start with		double hyphens and end with double hyphens too.

- Note that since this design is using a pre-signed URL to upload files, the client will	first request for a pre-signed URL from the servers, then make a HTTP PUT request	with the file data in the request body to the pre-signed URL

- When the client requests for a pre-signed URL, the client will also send in the file	metadata in the request body, and the API servers will update the file metadata into	the database.

##### Request for a pre-signed URL

Request:
```bash
POST /containers/:containerID/pre-signed-url
{
  blobName
  blobMetadata
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
  
  <file’s binary data goes here>
  
  —xxBOUNDARYxx–
}
```

Response:
```bash
Content-Type: application/json
{
	blobID
	containerID
	metadata: { createdTime, blobStatus }
}
```

#### List blobs

Request:
```bash
GET /containers/:containerID/blobs?nextCursor&limit
```

Response:
```bash
{
  blobs: [ { blobID, blobName, blobMetadata } ],
  nextCursor, limit
}
```

#### Get / download blob

- When downloading binary content using HTTP, application/octet-stream can be		used to receive binary data

- The application/octet-stream MIME type is used for unknown binary files. It		preserves the file contents, but requires the receiver to determine file type, for		example, from the filename extension. The Internet media type for an arbitrary byte	stream is application/octet-stream.

- The */* means that the client can accept any type of content in the response -		which could also be used for sending / receiving binary data

- Note that to download files, the client will first request for a pre-signed URL to download the blob chunks from the blob store. They will also specify a specific versionID to download if necessary.

##### Request for a pre-signed URL

Request:
```bash
GET /containers/:containerID/blobs/:blobID/:versionID/pre-signed-url
```

Response:
```bash
{
  pre-signed URL
}
````

##### Download from pre-signed URL

Request:
```bash
GET /<pre-signed URL>
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

#### Delete blob

- Note that the actual blob will be deleted during garbage collection asynchronously

Request:
```bash
DELETE /containers/:containerID/blobs/:blobID/:versionID
```

## HLD

### Client

- The client will be both uploading and downloading files, thus there will be separate sections in	the client code for an “uploader” and “downloader”, most likely provided with this blob store's SDK / CDK
  - Uploader:
    - The uploader will upload chunks of the local blob to the blob store via a pre-signed URL
  - Downloader:
    - The downloader will download the chunks of the blob (in the blob store) via a pre-signed URL

- Additionally, the client will contain the following internal components which communicate with the uploader and downloader. This is also shown in 'Client components'
  - Chunker:
    - The client will also have a chunker functionality that splits the files when uploading to the blob store, and also reconstructs the files from the downloaded chunks
  - Client database:
    - To maintain the metadata for the local blob and chunks, we'll store it in a client database. The uploader and downloader will use the client database to store local fingerprints, blob / chunk metadata, and compare it against the remote Metadata DB.

Client components:

<img width="400" alt="image" src="https://github.com/user-attachments/assets/f866587d-6312-40a0-a02d-96ed432990e3" />

### API servers

- The API servers handles CRUD based requests for the containers or blobs and communicates with the Node manager		service to find the appropriate data nodes containing the chunks for the blob the request is for. The API servers don't directly upload or download the blobs to the storage disks - they'll provide the pre-signed URLs to the client, such that the client can directly upload / download from the storage disks.

- The API servers will also handle requests for updating the metadata database during uploads / downloads.

### Data nodes

- The data nodes hold the actual blob data. Blobs are chunked and split into fixed size pieces, and a data node	will contain a set of chunks for different blobs. A single data node will also be replicated.

- The blob itself can be uploaded in the below ways and in 'Uploading files / blobs to storage solutions':
  - Upload file / blob to a single server
  - Store file / blob in blob storage:
    - A lot of the times, having the client upload the file to the API servers, then having the			API servers upload to the blob store is redundant and slow especially for large files			because the uploading process has to be done twice. Clients could directly upload to			the blob store via a pre-signed URL, and any security or validation checks can be				performed via the data node's client interfacing the data node after the user has			 	uploaded to the pre-signed URL.

    - However, in some applications, such as YouTube, where the videos will need				additional transformation, having intermediary API servers may be suitable.
  - Upload file / blob directly to blob storage:
    - We can use pre-signed URLs to upload files directly to the blob store. Pre-signed			URLs can be sent via the servers to the clients. Clients can then use the pre-signed			URL, which may have a TTL to upload / download their files. Pre-signed URLs are			explained in ‘Pre-signed URLs’.

### Node manager service

- The node manager manages all the information about status, replication and chunk mappings for data nodes

- Nodes use heartbeat / gossip protocol within a replica set. If a node fails to send a heartbeat, a node will notify	the node manager service and the node manager will consider that node down and processes the requests on	to	the replica nodes instead in that replica set. 

- The blobs will be split into chunks, where chunks of a single blob will be stored on different data nodes. The 		manager node will manage the chunkID : nodeID mapping in the Metadata database so that the clients can fetch the chunks at the		nodeID. A chunk is the minimum size for reads / writes.	

- As different chunks are spread across different nodes, the chunks a single blob can be fetched from the nodes	in a parallel	 fashion as shown to the bottom in ‘Chunks mapped to nodes’.

- The nodes within a cluster may perform leader election during failures and use hinted handoff for temporary		failures, where if there is a crashed node, the interim node will maintain a log of the operations it has done, and	replay it to the crashed node once it recovers, so that it has the updated data.

- The node manager will also allocate space depending on requests from the monitoring system (which will 		check if additional space is needed for a node)

- The node manager may seem like a SPOF, so we will use checkpointing where we take snapshots of the data	at different time intervals. The snapshot will capture the state, data, hardware configuration of the node			manager. 

- The node manager will also maintain an operation log defining the serialized order of concurrent operations in	an external storage. If the node manager fails, another node manager will automatically take over and use the		saved checkpoint information and operational log. 

- The node manager will be a stateless service, but as downloading the saved checkpoint information and 		operational log may take a long time, we can always keep an alternative node manager service that always has	the same saved checkpoint info and operational log, so that there are no delays from downloading.

- A client within the data node OR the node manager itself could also handle conflicts from concurrent updates by using S3 Object	Locks at the chunk level, instead of locks for the whole blob. Additionally, vector clocks and		versioning could be used to detect conflicts within chunks - if two users updated the same chunk	at the same time

### Metadata database / cache

- The metadata database will store the metadata for blobs, chunks, containers, blob versions, etc. The metadata database will be used by the node manager service to store the metadata and also mappings for the chunks.

- The database could either be a SQL or NoSQL database such as DynamoDB or MongoDB.		Either one could potentially do the job, however, relations and transactions may be easier to		maintain within a SQL database. The tables do have relations among them and transactions may	still need to be performed on the blob metadata, thus a DB such as PostgreSQL will be suitable,	which also provides functionality for custom types incase we need to grow the schema. However,	a NoSQL database could perform just as well - but it may not be as easy to maintain relations or	transactions.

#### Cache

- The metadata may likely contain hierarchical data, where a container will have a blob, and a blob will have multiple chunks, where there is a separate status and metadata for those chunks. Thus, we can use Redis's support for complex data structures, such as lists and maps to cache the metadata.

### Monitoring system

- The monitoring service will monitor the data nodes and notify the node manager service of failures within nodes

- It may also get information on the available space left on the disks, so the node manager will allocate more		space


<img width="1100" alt="image" src="https://github.com/user-attachments/assets/15063478-5392-4785-b23d-9edb983514ba" />

<br/>
<br/>

Chunks mapped to nodes:

<img width="1034" alt="image" src="https://github.com/user-attachments/assets/bfd2cd54-ca0e-422e-95ad-93e0fae0c997" />

## DD

### Chunking hierarchy
  
- The overall mappings will be as follows:
  - userID : containerID
  - containerID : blobID
  - blobID : [ list of chunkIDs maintained by the node manager ]
  - chunkID : nodeID

- Blobs will be split into chunks, where chunks of a single blob will be stored on different data nodes. The node manager will store	the chunkID : nodeID mapping in the metadata database. The blob will also be split into equal sized chunks, where a chunk is the minimum size for reads /	writes. The nodes will also be replicated as shown in ‘Chunks mapped to nodes’.

### Replication of data nodes
  
- We can perform replication of a single node as shown in ‘Chunks mapped to nodes’

- We can have synchronous replication within data center and asynchronous replication across data centers

- We could replicate using either a primary-secondary or peer-to-peer nodes approach. Since we have many reads happening and	only one write, we may choose to have a primary-secondary node approach as opposed to a leaderless replication approach

### Garbage collector
  
- If a blob delete request comes in, the blob will be marked “to be deleted” by the node manager, and deletion will take place		asynchronously by the	garbage collector, which will free up the space.

- Any requests for the “to be deleted” blob will fail as the blob will be marked as deleted.

### Versioning

- To implement blob versioning, we could maintain a separate Blob versions table which contains the	versionIDs for the same blobID.

- We can implement blob versioning using the below approaches:
  - Upload a completely new blob on each change, and add a new version to the Blob versions	table:
    - Instead of overwriting the only stored file in the blob store, we could upload a		completely	new blob when a new blob version is uploaded, and set a new version for	it by adding a new entry to the Blob versions table

  - Upload only modified chunks, and add a new version to the Blob versions table:
    - We could only upload the modified chunks and set a new version for the blob with the	modified chunks by adding a new entry to the Blob versions table

### Supporting large files
		
#### We can implement resumable uploads for large files

- Users should be able to pause and resume uploads. If they lose internet connection,		they should be able to pick up where they left off rather than re-uploading the entire		file again

#### Uploading a large file via a single POST request has the following limitations

- Timeouts:
  - Servers and clients usually have timeout settings, which prevents long running				processed. A single POST request for a 50 GB file could easily exceed these				timeouts.

  - If we have a 50 GB file, an an internet connection of 100 Mbps, it will take 					(50 GB * 8 bits / byte) / 100 Mbps = 4000 seconds = 1.11 hours to upload a file
		
- Browser and server limitation:
  - Usually browsers and servers will also impose limits on the size of a request or data	being transferred. The default is usually less than 2 GB for web servers like Apache /	NGINX, but can be configured. AWS services also have default limits, which		sometimes cannot be increased.		

- Network interruptions:
  - Large files are more prone to network interruptions. If a user is uploading a 50 GB file			and their internet connection drops, they may have to restart the entire upload.

- User experience:
  - Users are also blind on the “actual progress” of sending a large file, as they have no			idea how long it will take

#### Chunking for large file transfers

- To address the limitations of large files, we can use chunking to break the file into smaller		fixed size pieces, and upload them in parallel (or one at a time if network quality is bad).		Chunking will need to be done on the client side, so that the client can split the file into			chunks, and send them to the blob store.

- The client can calculate the optimal chunk size based on the client device being used, the		client’s network connection, average file size in the blob store, etc. The average chunk size		is usually 5-10 MB.

- Chunking can also be used to show a progress indicator, where the uploaded chunks			updates the progress bar.
	
#### Resumable uploads using chunking

- To handle resumable uploads, we need to keep track of which chunks have been uploaded		and which haven’t. The status of the chunk can be maintained in the Chunks table, which		will contain the chunkStatus.

- If a user resumes the upload, we can check the Chunks table to check which chunkIDs for		the fileID have been uploaded / not uploaded, and then resume uploading the				NOT_UPLOADED chunkIDs.

Because we need to update the chunkStatus fields of the Chunks table after the chunks have	been successfully uploaded / failed to upload, we can do the following or in ‘Updating Chunks	table upon chunkID upload success / failure’:
  - Update based on client PATCH request:
	  - In this approach, the client will send a PATCH request to the servers to update the			Chunks table entries after a chunk has uploaded / failed, and the client has received			the response from the blob store. This may not be secure,	 since malicious				actors could potentially send the PATCH request to update the Chunks table.
  - Rely on S3 Event Notifications OR another notification sent from the data nodes to the Metadata DB:
    - We could instead use S3 event notifications to keep the Chunks table updated when			chunkIDs uploaded successfully / failed. This is done on the server side as opposed to			the client side using a PATCH request, thus it will be more secure. In the case with S3, S3 event					notifications could be sent to a Lambda function, which will update the metadata DB.

#### Fingerprint of blobs to check which parts of the blob have been uploaded

- A fingerprint is a mathematical calculation that generates a unique hash value based on		the content of the file. The hash value can be created using SHA-256 or other cryptographic		hash functions. The hash value can be used as a unique ID for the file. Using the fingerprint,		we can check if any part of the file has already been uploaded before, since the fingerprint		will change on each upload depending on the content of the file / chunk.

- The uploader on the client side will fingerprint the entire local file and also the chunks. The		uploader will then send a request to the servers to check if the local file’s and chunks’			fingerprints exist for the blobID and chunkIDs in the Blobs and Chunks tables. If the local			fingerprints don’t exist in the tables, the client will then use a pre-signed URL from the			servers to upload the local blob / chunks. After the servers have sent the pre-signed URL to		the client, the servers will also update the blobID’s and chunkID’s blobStatus and chunkStatus		values respectively to UPLOADING (fileID) / NOT_UPLOADED (chunkIDs). After the data node client receives the uploaded chunks, it will send a simple notification OR a S3 event notifications to a Lambda		function to update the blobID and chunkIDs to UPLOADED in the Metadata DB.
		
- Throughout this process, the uploader will also track the chunks uploading progress

- This upload process with fingerprints is not unusual, it is actually used via S3 multipart		upload as explained in ‘S3 multipart upload’.

### Making uploads / downloads as fast as possible

#### Making uploads fast

- Chunking will already speed up blob uploading, as only necessary chunks via the calculated		fingerprints will need to be uploaded. Chunks can also be uploaded and downloaded in			parallel, and chunks can be adjusted depending on the network quality, which will maximize		the use of available bandwidth.

#### Making downloads fast

- Blob downloads will become faster if using chunking to download smaller sized data

#### Compression

- Compression can also speed up both uploads / downloads, where the blob size is reduced		while preserving the content via a lossless compression algorithm. Fewer bytes will also		need to be transferred. The compression algorithm can be located in both the client and		server side. We can compress a file on the client before uploads, and compress the file on		the server before downloads. The recipient will then decompress the file. ‘Compression			algorithms’ explains some suitable compression algorithms.

- Usually, media files like images, videos and audio have very low compression ratios which		makes compression not worth it. However, for text files, the compression ratio is much			higher and can be compressed much more. The compression can be done based on the	blobType / fileType and size of the blob.

### Partitioning of metadata database
  
- When storing the metadata in tables, we can partition based on full blob path (userID/containerID/blobID) in PostgreSQL. 

- Using this approach, there will be faster queries as the node manager will mostly be filtering the metadata based on the 			userID, containerID, blobID we’ve mentioned in our partitioning logic. PostgreSQL is also able to speed up queries by			maintaining references to those partitions for fast access

- The node manager will also be responsible for configuring the partitioning of the metadata in the tables

### Caching:
- We can cache the data at multiple places such as:
  - Cache the metadata
  - Cache at the API servers the mapping for the chunkID : nodeID, so that the API servers don’t have to request the node			manager for the mappings
  - Frequently accessed chunkIDs could also be cached at the node manager internally

<br/>
<br/>

Additional deep dives:

### File security

Security can be improved via the following approaches:

#### Encryption in transit

- We will of course use HTTPS to encrypt the data as it’s transferred between the				client and server.

#### Encryption at rest

- We should also encrypt the files stored in the data nodes by a separate encryption service / layer. Blob stores like S3 has an encryption at rest feature			that is easy to enable. S3 will then encrypt the file using a unique key and store the			key separately from the file. Users cannot decrypt the file without this unique key.

#### Access control

- Another Shared blobs table can also be used to maintain the basic ACL and can be used to validate				permissions of userIDs accessing a blobID.
		
#### Pre-signed URL / CDN URL prevents unauthorized users

- Pre-signed URLs will also prevent unauthorized users from				uploading / downloading to the blob store. Even if unauthorized users have the			URL, because there is a TTL on the URLs, they won’t be able to use expired URLs.

- These URLs work for modern CDNs like CloudFront, and are a feature of S3. They			work as shown in ‘Workings of pre-signed URL / CDN URL’

### Streaming a file

- To stream a file, the downloader within the client can use an offset value to keep track of the byte from which we need to start reading again in the chunk

### blobName indexing (Optional, and will only be used if a search system like Elasticsearch is used as well):

- To optimize searching for blobs in a container, we can index the blobs based on tags / descriptions when uploading the blobs. These tags / descriptions such as blobName, blobType and description can help find the blob faster if we’re using a	search system like Elasticsearch.

## Wrap up

- Adding additional node managers for scalability
- Geo-replication / cross-data center replication
- Quorum based approach for writes and reads in the nodes
- Security:
  - Encryption on the data
  - RBAC on storage
- We want to ensure via the API servers that the client is authorized to access the	 blob
