# Tinder

Tinder is a mobile dating app that helps people connect by allowing users to swipe right to like or left to pass on profiles. It uses location data and user-specified filters to suggest potential matches nearby.

## Requirements

### Questions

- In this system, users can create a profile with preferences (age range, interests, etc) and specify a maximum distance. They can also view potential matches in line with their preferences and within max distance of their current location. Users can also swipe right / left on profiles one-by-one to express "yes" or "no" on other users. Users will also get a match notification if they mutually swipe on each other. Are we designing all of this?
  - Yes
 
- Should we design the uploading of pictures?
  - Yes, let's design for uploading of pictures

- Should we focus on designing for efficiently searching profiles using geohash, quadtree, PostGIS, etc?
  - Yes, also look into location based searching

- Should users be able to chat via DM after matching?
  - For simplicity, let's ignore chatting

- What is the DAU and the average number of swipes / user per day?
  - 20M DAU, and ~100 swipes / user per day on average

<img width="700" alt="image" src="https://github.com/user-attachments/assets/f9222435-321f-41d5-921b-7a636507535a" />

### Functional

- Users can create a profile with preferences (age range, interests, etc) and specify a maximum distance
- Users can view potential matches in line with their preferences and within max distance of their current location
- Users can also swipe right / left on profiles one-by-one to express "yes" or "no" on other users
- Users will also get an instant match notification if they mutually swipe on each other

- The system should avoid showing user profiles that the user previously swiped on

### Non-functional

- Consistency for swipes:
  - There should be consistency for swipes, and the system should avoid showing user profiles that the user previously swiped on
- Low latency for potential matches:
  - The system should provide potential matches and user profiles with low latency (< 300 ms)
- The system should support 20M DAU and ~100 swipes / user per day on average - and also handle 20M x 100 swipes per day

## Data model / entities

- Users / Profiles:
  - userID
  - userName
  - userEmail
  - userInfo: UserInfo object that contains info about the user
  - s3URLs
  - long / lat / geohash (if the system is using geohash) / location (if the system is using PostGIS, then location will be of PostGIS's GEOMETRY type)
  - preferences: { ageRange, location, gender }

- Media:
  - The media entity represents the actual bytes of the media file (photos / videos). We'll use S3 for storing the media files.

- Swipe:
  - This entity represents the expression of "yes" / "no" on a user profile, and belongs to a user (the swipingUserID field) and is about another user (targetUserID)
    - swipingUserID
    - targetUserID
    - liked: YES (swipe right) / NO (swipe left)
   
- Match:
  - This entity represents a connection / match between 2 users as a result of them both swiping "yes" to each other
    - matchID
    - swipingUserID
    - targetUserID

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Create a profile

- We'll use this endpoint for creating a profile for a user. As shown below, the user can first provide their own info and preferences (such as min / max age, distance, inferested in, etc).

Request:
```bash
POST /profile
{
  userName, userPhoneNumber,
  minAge, maxAge,
  distance,
  interestedIn: MALE / FEMALE / BOTH
}
```

### Upload images for profile

#### Request pre-signed URL for uploading profile's images

- When a user requests to upload an image, they will first request for the pre-signed URL for uploading an image. The backend servers will then link the uploaded images using the s3URLs field in the Users entity.

- When uploading binary data, multipart/form-data / multipart/mixed or another MIME type such as image/png is usually used

- The content type is set to multipart/mixed which means that the request contains different inputs and each input can have a different encoding type (JSON or binary). The metadata sent will be in JSON, while the file itself will be in binary.

- The placeholder {---xxBOUNDARYxx—} will contain a text string for the boundary that differentiates one part of the body from another. For example “the_boundary” could be used as the string. Boundaries must also start with double hyphens and end with double hyphens too.

- Note that since this design is using a pre-signed URL to upload files, the client will first request for a pre-signed URL from the servers, then make a HTTP PUT request with the file data in the request body to the pre-signed URL

Request:
```bash
POST /profile/pre-signed-url
```

Response:
```bash
{
  pre-signed URL
}
```

#### Upload profile's images to pre-signed URL

Request:
```bash
PUT /<pre-signed URL>
Content-Type: multipart/form-data; boundary={---xxBOUNDARYxx—}
{
—xxBOUNDARYxx–
<HEADERS of the boundary go here>

We’ll put the a single photo's / video's binary data in every boundary like this:

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

### Get feed of potential matched profiles

- Next we need an endpoint to get the "feed" of user profiles to swipe on, this way we have a "stack" of profiles ready for the user. The user will first request using a specific long / lat and distance, then get back a list of potentially matched profiles

- Note: we don't need to pass in other filters like age, interests, etc. because we're assuming the user has already specified these in the app settings, and we can load them server-side.

Request:
```bash
GET /feed?lat={}&long={}&distance={}
```

Response:
```bash
{
  users: [ { userID, userName, preSignedURLs / CDN URLs, userInfo object } ],
  nextCursor, limit
}
```

<img width="700" alt="image" src="https://github.com/user-attachments/assets/775b3b6a-9f87-4816-9f71-8ac0e991b146" />

### View profile's images

- Using the provided matched profiles from the servers, the client can then use the pre-signed URLs / CDN URLs to retrieve the profiles's photos / videos from the blob store or CDN.

- When downloading binary content using HTTP, application/octet-stream can be used to receive binary data

- The application/octet-stream MIME type is used for unknown binary files. It preserves the file contents, but requires the receiver to determine the file type, for example, from the filename extension. The Internet media type for an arbitrary byte stream is application/octet-stream.

- The "* / *" means that the client can accept any type of content in the response - which could also be used for sending / receiving binary data

- Note that to download files, we could use either a pre-signed URL or a URL the client can request to download from the CDN (let’s call it CDN URL). The process is similar to uploading files, where the client first requests the servers for a pre-signed URL OR CDN URL, then the client will download the file from the pre-signed URL / CDN URL.

#### Fetch profile's images using pre-signed URLs or CDN URLs

Request:
```bash
GET /<pre-signed URL or CDN URL>
Accept: application/octet-stream
```

- The response body contains the file chunks. The chunks can also be returned using multiplexing via HTTP/2.0. Multiplexing will allow the client to send requests for the chunks of a file, then the server will send the responses containing the file chunks in any order. The returned chunks can be used to reconstruct the file on the client side.

Response:
```bash
Content-Type: application/octet-stream
Content-Disposition: attachment; filename=”<FILE_NAME>”
{
	file’s binary data used to generate the file on the client side
}
```

### Swipe on a user

- Users can use this endpoint to swipe on a user

Request:
```bash
POST /swipe
{
  userID,
  decision: YES / NO
}
```

<img width="688" alt="image" src="https://github.com/user-attachments/assets/d816dfe8-c4ff-402c-a1ca-084622863b8b" />

## HLD

### Client

- The client will be both uploading and downloading files, thus there will be separate sections in the client code for an “uploader” and “downloader”:

- Both the "uploader" and "downloader" parts of the client will use a chunker functionality that splits the files when uploading to the blob store, and also reconstructs the files from the downloaded chunks

### API gateway

- The API gateway will provide rate limiting, authentication, and route requests to the specific services. For example, for a profile creation request, the API gateway could route the request to the Profile service.

### Profile service

- The Profile service will allow users to create a profile with their info and preferences (age range, gender preference, interests, etc) and specify a maximum distance. The first thing we need to do in a dating site like Tinder is allow users to tell us about their preferences. This way we can increase the probability of them finding love by only showing them profiles that match these preferences.
- The Profile service will request the endpoint 'POST /profile', which will store the user's profile in the Profile table. The Profile service will also allow users to upload their profile's images to the blob store using the endpoint 'POST /profile/pre-signed-url' after they first send a request to get the pre-signed URL to the blob store. We'll also make the initial assumption that our media is small enough to be uploaded directly via a single request.
- Overall, this service will be stateless and can be easily scaled horizontally.

When a user creates a profile:

1. The client sends a POST request to /profile with the profile information as the request body.
2. The API Gateway routes this request to the Profile Service.
3. The Profile Service updates the user's profile preferences in the database.
4. The results are returned to the client via the API Gateway.
  
### Profile table / cache

- The Profile table will store the User / Profile entity, such as their info, images and preferences. Note that the data store in this table is not the authentication data - the authentication data will be stored and managed by a different service such as Auth0.

- Because matches will occur much less frequently than swipes, we can also store the Matches entity in this Profile table. A match will occur when 2 users both swipe right on each other. If there is a match, determined by the Swipe service, then the Swipe service will store a matchID entry for this match.

- We can use either a SQL or NoSQL database such as DynamoDB here. The data doesn't necessarily contain that many relationships or strict consistency between entities, such that a SQL database would be the most optimal here, thus we'll use DynamoDB because it's more optimal for performing low latency queries using GSIs / LSIs, which will support faster reads on the profiles likely using the user's preferences like location, age, etc. Also, we may not require features of SQL, such as multi-table transactions and different isolation levels because we won't see many concurrent operations for profiles. However, SQL can also be used here.

- For faster lookups to get the data of matched profiles for a specific userID, we'll set the userID as the primary key, and we'll also use multiple GSIs which will set the partition key as the preferences (such as age, location, gender, etc). Because GSIs also require a sort key, we can use a "lastActive:userID" field as the sort key to ensure the GSI's primary key (partition key + sort key) is unique in the Profile table. Note that we'll use "lastActive:userID" because just using the lastActive timestamp + the preferences as the primary key won't make the primary key unique, thus we'll add the userID to the lastActive timestamp using the composite sort key and string "lastActive:userID".

#### Users should be able to view a stack of potential matches

- When a user enters the app, they are immediately served a stack of profiles to swipe on. These profiles abide by filters that the user specified (e.g. age, interests) as well as the user's location (e.g. < 2 miles away, < 5 miles away, < 15 miles away).

So far, when a user requests a new set of potential matches:

1. The client sends a GET request to '/feed' with the user's location as a query parameter.
2. The API Gateway routes this request to the Profile Service.
3. The Profile Service queries the Profile table for a list of users that match the user's preferences and location.
4. The results are returned to the client via the API Gateway.

- Note that if we went with a SQL DB such as PostgreSQL, then we can leverage PostGIS which can be used to index and query geocoded data - which will be helpful for searching potential matches. PostgreSQL also has a full-text search extension called pg_trgm which uses inverted indexes, that can be used to index and query text data. We can create these extensions using the below, as discussed in the DD.

```bash
create extension if not exists postgis;
create extension if not exists pg_trgm;
```

#### Profile cache

- Because the system is read heavy and doesn't need as much storage for the profiles data, we could also cache the frequently accessed profiles with an appropriate TTL. We can use Redis since the stack of potential matched profiles for a specific userID could likely be contained within a Redis list, which can be provided to the userID over time.

#### Profile service using Geohash service vs PostGIS service vs Quadtree service

- The Profile service will also use either the Geohash service or the PostGIS service (if we went with using PostgreSQL as the Profile table) or the quadtree service to efficiently retrieve the stack of potential matches using geohash strings, PostGIS, or a quadtree respectively, and return the profiles within the specific location (and according to the userID's preferences). The specifics of the approaches, and additional approaches which can be used are discussed in the DD.

### Geohash service (if using geohash)

- The Geohash service will retrieve the stack of potential matches within a search radius using a geohash based approach, and return them to the Profile service. The Geohash service will take a geohash of the search radius (using a geohash converter) and find profiles within the specified radius by comparing their geohash strings.
- The geohash converter, which could be PostgreSQL's PostGIS geohash conversion functionality shown in 'PostGIS geohash conversion function', will take a long / lat coordinate of either a radius or profile, and then convert it to a geohash string. This geohash string will be compared against the geohash strings in the Profile table / cache to find relevant profiles.
- Because we're using geohash, the Geohash service will compare the prefixes of the search radius' geohash string with the prefixes of the profile's geohash string. If the prefixes are the same, then this means the profile is within the search radius. A query such as the one below can be used to find profiles with the same prefix as the search radius' geohash.

```sql
select userID, lat, long, geohash from profileTable
where geohash like '${radiusGeohash}'
```

PostGIS geohash conversion function:
```sql
select ST_GeoHash(ST_Point(${long}, ${lat}))
```

- When new profiles are created, we'll also use the Geohash service to generate a geohash string for the new profile, and then store it in the Profile table.

- Geohash can sometimes be slower than a typical quadtree. It can also be slower than PostGIS's built-in location based search functionalities. This will be discussed more in the DD.

#### Geohash cache

- Because the querying the geohash data on disk may be slow, we can store a geohash cache in Redis. Redis provides support for geohashing to encode and index geospatial data, allowing for fast querying. The key advantage of Redis is that it stores data in memory, resulting in high-speed data access and manipulation. Additionally, we can periodically save the in-memory data to the Profile table using CDC (change data capture).

### Quadtree service (if using quadtree)

- The Quadtree service will recursively build and update the Quadtree table and cache. The Quadtree service will also be used to search the quadtree efficiently by traversing down the tree from the root node to the leaf nodes. The search within a quadtree will be discussed more in the DD.
- A quadtree may be more suitable for this design than a geohashing approach, since there are many high density areas such as NYC, and a quadtree will account for these dense areas by splitting up the quads further.

#### Quadtree table / cache

- Because a quadtree is an in-memory data structure, we can keep both a quadtree table within PostgreSQL as well as a cache using Redis. PostgreSQL provides SP-GiST, which provides functionality for storing and querying a quadtree data structure.
- Although Redis doesn't directly provide quadtree support, we'll use Redis as the quadtree cache since it provides complex data structures such as lists and sorted sets which will be helpful in storing nodes of the quadtree. For example, the leaf node of a quadtree can be a Redis sorted set, where the profiles are sorted based on their distances (or preferences match) to the leaf node's radius's center point. A leaf node can also contain a Redis list which contains profiles from the Profile table which fall within the leaf node's radius.
- Additionally, a quadtree data structure is not as complex to build, and could be implemented within a memory optimized EC2 instance.

### PostGIS service (if using PostGIS)

- We could also use a PostGIS service which will convert the profile's long / lat values in the Profile table to a PostGIS GEOMETRY type. We'll then add a new column of this GEOMETRY type (we'll call it the location column) to the Profile table. This PostGIS service will then be used to query the Profile table using PostGIS search functions like ST_Intersects (to find if a long / lat value intersects with another point) and ST_DWithin (to find if a long / lat value is within a radius).
- The DD will discuss more on PostGIS and it's usage in efficiently searching for profiles.

### Swipe service

- We need a way to persist swipes and check if there is a match, where 2 users both swiped right on each other. The Swipe service will persist swipes and check for matches from the Swipe table. If there are matches (2 users both swiped right on each other), then the Swipe service will return the matches to the client.

### Swipe table

- The Swipe table will store the swipe data for users. Given that the swipe interaction is so effortless, we can assume we're going to get a lot of writes to the DB. Additionally, there is going to be a lot of swipe data. If we assume 20M daily active users doing 200 swipes a day on average, that nets us 4B swipes a day. This certainly means we'll need to partition the data.
- Cassandra is a good fit as a database here. We can partition by swiping_user_id. This means an access pattern to see if user A swiped on user B will be fast, because we can predictably query a single partition for that data. Additionally, Cassandra is extremely capable of massive writes, due to its write-optimized storage engine (CommitLog + Memtables + SSTables). A con of using Cassandra here is the element of eventual consistency of swipe data we inherit from using it. We'll discuss ways to avoid this con later in the DD.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/80d4c886-d588-4c4d-b109-a7a1afaea1ed" />

When a user swipes:

1. The client sends a POST request to '/swipe' with the userID and the swipe direction (right or left) as parameters.
2. The API Gateway routes this request to the Swipe Service.
3. The Swipe Service updates the Swipe table with the swipe data.
4. The Swipe Service checks if there is an inverse swipe in the Swipe table and, if so, returns a match to the client.

### Notification service

- The Notification service will deliver push notifications (either APN or Firebase Cloud Messaging notifications for iOS and Android devices respectively) to users when there is a match when they mutually swipe right on each other.

- When a match occurs, both people need to be notified that there is a match. To make things clear, let's call the first person who like the other Person A. The second person will be called Person B. Notifying Person B is easy! In fact, we've already done it. Since they're the second person to swipe, immediately after they swipe right, we check to see if Person A also liked them and, if they did, we show a "You matched!" graphic on Person B's device. But what about Person A? They might have swiped on Person B weeks ago. We need to send them a push notification informing them that they have a new connection waiting for them. To do this, we're just going to rely on device native push notifications like Apple Push Notification Service (APNS) or Firebase Cloud Messaging (FCM).

<img width="700" alt="image" src="https://github.com/user-attachments/assets/86adbdef-fef3-4786-b23d-616172e37518" />

Let's quickly recap the full swipe process again, now that we've introduced push notifications into the flow:

1. Some time in the past, Person A swiped right on Person B and we persisted this swipe in our Swipe DB.
2. Person B swipes right on Person A.
3. The server checks for an inverse swipe and finds that it does, indeed, exist.
4. We display a "You Matched!" message to Person B immediately after swiping.
5. We send a push notification via APNS or FCM to Person A informing them that they have a new match.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/1f03d52b-47bf-422b-ac1a-04ab9fad6073" />

### Blob store

- The blob store will contain the photos / videos uploaded by users. The Profile service will provide pre-signed URLs to this blob store (S3), such that the user can upload the media files.

- The blob store will store the file chunks. The file itself can be uploaded in the below ways and in ‘Uploading file to storage solutions’:
  - Upload file to a single server
  - Store file in blob storage:
    - A lot of the times, having the client upload the file to the API servers, then having the API servers upload to the blob store is redundant and slow especially for large files because the uploading process has to be done twice. Clients could directly upload to the blob store via a pre-signed URL, and any security or validation checks can be performed via the blob store client interfacing the blob store after the user has uploaded to the pre-signed URL.
    - However, in some applications, such as YouTube, where the videos will need additional transformation, having intermediary API servers may be suitable.
  - Upload file directly to blob storage:
    - We can use pre-signed URLs to upload files directly to the blob store. Pre-signed URLs can be sent via the servers to the clients. Clients can then use the pre-signed URL, which may have a TTL to upload / download their files. Pre-signed URLs are explained in ‘Pre-signed URLs’.

<img width="900" alt="image" src="https://github.com/user-attachments/assets/00548003-8a50-4c68-b3ca-6788a1aad8a4" />

## DD

### Efficiently storing the location data for fast searches

Efficiently storing location data for fast searches can be done using multiple approaches. The resource notes in 'Location based search' goes over all of the main approaches. However, in this DD, we'll use either geohash, quadtree or PostGIS.

#### Geohash service

- Refer to the "Geohash" section in the resource note 'Location based search' for the background on geohash.

<br/>

- Geohash works by converting the long / lat to a string of letters and digits. We first divide the map into 4 grids recursively until the grid size is small enough such that it can contain a relatively small number of profiles. As the map gets recursively divided, we'll assign a generated Base-32 geohash string to the grid. Geohash also operates with a fixed precision, where the smallest grids cannot be further divided, and all the smallest grids will have the same size. However, custom dynamic behavior can be added to a geohashing approach, but adding dynamic behavior may be more complex to do.
- Since geohashes represent hierarchical spatial data, shorter geohash strings cover larger areas, and longer geohash strings cover smaller areas with more precision. Therefore, if we keep removing the last character from a geohash string, the new geohash string will be for a larger area. To make geohash filtering more efficient, we can index the geohash column (like in 'Index on geohash') so that queries with the LIKE or WHERE operators will optimize it's prefix based searches.
- An example of using LIKE with a geohash string is given below:

Index on geohash:
```sql
CREATE INDEX idx_geohash ON profileTable USING geohash
```

Using LIKE to filter geohash strings:
```sql
select userID, lat, long, geohash from profileTable
where geohash like '${radiusGeohash}'
```

Also, let's say we're searching for locations within the geohash redius of "dpz83" - then the query above should return the following:
- dpz83a
- dpz83b
- dpz83xyz

<br/>
<br/>

- We can also generate a geohash string using PostgreSQL's PostGIS extension as follows:

PostgreSQL geohash conversion function:
```sql
select ST_GeoHash(ST_Point(${long}, ${lat}))
```

<br/>
<br/>

- Geohash works well for majority of the cases, but boundary issues may come up when one location covers 2 geohash strings. Additionally, in some cases, there could be profiles within the border of 2 geohash strings, and so that profile doesn't belong to any geohash string. In these cases, the geohash generation algorithm can be modified to account for such edge cases.
- Also, another issue may be when too few profiles appear in the search result. In this case, we can increase the search radius by removing the last digit of the geohash string, and we can continue to increase the radius by removing another digit from the end.

##### Geohash sharding / partitioning

- If we have a table containing the userIDs and geohash strings, we can easily shard the database and partition the tables based on prefixes of the geohash strings. We'll shard by the prefixes of the geohash strings because profiles which are within the same geohash search radius will also be within the same shard. This will make searches faster, since we'll have to look through fewer shards or entries of the table.

#### Quadtree service

- Refer to the "Quadtree" section in the resource note 'Location based search' for the background on quadtrees.

<br/>

- A quadtree also recursively divides the map into 4 grids until the contents of the grids meet a certain criteria, like not having more than 100 profiles. A quadtree is an in-memory data structure that helps with location based searching.
- The data on a leaf node (leaf node represents the most granular grid) in a quadtree can contain long / lat and a list of userIDs (profiles) in the grid. The data on a parent node (parent node represents the parent grid of leaf nodes) contains the parent grid's long / lat values and pointers to the 4 child nodes.
- Assuming a leaf node has at most 100 profiles, then to build a quad tree for N profiles:
  - It will take (N * 100) * log(N / 100) time complexity, since we're parsing through (N / 100) leaf nodes which contains at max 100 profiles each, and we'll also be parsing the height of the tree which will be log(N / 100), where N / 100 is the number of leaf nodes.

- Below is an example of a quadtree quad:
<img width="750" alt="image" src="https://github.com/user-attachments/assets/23144928-0519-46eb-8b49-4dd0cd8c45b5" />

<br/>

- To search in a quadtree, we'll start from the root node and traverse down the tree until we find a node within the search radius. If we find a node within the search radius, we'll traverse the node's child nodes and siblings to see if they're also in the search radius. We'll keep a list of profiles in the leaf nodes which are within the search radius, and then return the list of profiles. The downside to a quadtree is that searches can be a bit complex to implement.
- A quadtree is also an in-memory data structure, thus it will likely be stored within a cache or in-memory database. Therefore, we'll need to invalidate any nodes within the quadtree, and frequently perform updates to it.

- Below is an example of a quadtree, along with the DLL data structure consisting of sibling nodes. The DLL will help with searching sibling nodes when traversing the quadtree and finding nodes / siblings within a search radius:
<img width="800" alt="image" src="https://github.com/user-attachments/assets/9b53efa6-5790-4a6a-97d2-961ba90a0af5" />

<br/>

##### Quadtree table / cache

- An entry in the quadtree table / cache can be as follows:

Quadtree node's entry in table / cache:
```bash
{
nodeID,
profiles: [ { userID, userName, location, long / lat } ],
nodeQuad: { maxLong, maxLat, minLong, minLat },
leafNode: TRUE / FALSE,
childNodePtrs: { childNode_1, childNode_2, childNode_3, childNode_4 }
}
```
- In this entry, the nodeID can represent the node of the quadtree. If a node is a leaf node, we'll set the leafNode to TRUE. Also, if it is a leaf node, then there will be profiles populated within this node. The nodeQuad field will also be the quad's max /  min long / lat values.
- When searching for profiles within a search radius, we'll first check if the nodeQuad's long / lat values are intersecting with the search radius. If the quad is intersecting, then we'll traverse down the tree to find the leaf nodes. In the leaf nodes, we'll search for userIDs (profiles) which have long / lat values within the search radius.

##### Building a quadtree

- We will start with one node that will represent the whole world in one quad. Since it will have more than 100 profiles, which may be our criteria, we will break it down into four nodes and distribute locations among them. We will keep repeating this process with each child node until there are no nodes left with more than 100 profiles.

##### Dynamic quads

- We can use dynamic quads in our quadtree where if the number of profiles exceed a threshold in a quad, we'll further split the quad into 4 more quads. In the quadtree, nodes will contain the userIDs (profiles) such that the userID can be used to query the profile info from a table containing the profile data.

##### Searching in a quadtree

- In the quad tree, child nodes will be connected to sibling nodes with a DLL. Using the DLL, we can move left / right / up / down to sibling or child quads to find profiles. An alternative to a DLL is to use parent pointers from the child nodes to the parent node.

- When searching in the quadtree, we start searching from the root node and visit child nodes which are in the search radius. If a child node is in the search radius, we can traverse through it’s own child nodes and sibling nodes using the DLL and return them if they are also in the search radius.

- If we don't have enough profiles to return after searching a specific node, we can search the node's siblings and also it's parent node to retrieve surrounding profiles as well.

##### Adding / updating / removing an entry (profile) in a quadtree

- To add / update a profile in the quad tree, we can search the nodes for the userID and add / update the profile in the node, and also update any neighboring siblings if needed. If after adding the profile, the leaf node reaches the threshold on the number of profiles a node can have, we'll need to split this leaf node further into 4 leaf nodes and allocate these 4 leaf nodes with the profiles from the original leaf node.
- To remove a profile in the quad tree, we can search the nodes for the userID (profile) and remove the profile from the node, and update the neighboring nodes accordingly

##### Quadtree sharding / partitioning

- We can shard the quadtree based on regions on the basis of zip or postal codes, such that all the profiles and nodes that belong to a specific region are stored in a single shard. A region in this case will be a branch within a quadtree - therefore, a shard could contain a separate part of a single quadtree (the branch). Some regions could also be combined into a single shard to prevent uneven distributions.
- We can do this since the user’s queries will be based on the location, so sharding this way will cause less inter-shard communication and speed up queries.
- There could also likely be a mapping maintained within ZooKeeper that keeps track of the mapping between regionID : shardID. regionID or shardID will rarely change (it may change only when a new region or shard is updated), thus this mapping will rarely change.

##### Quadtree replication

- We can replicate both the quadtree table and cache on multiple servers to ensure high availability. This also allows us to distribute the read traffic and decrease the response times.
- Quadtrees should take up relatively little storage, and thus can be backed up easily. In case we may lose the quadtree data, we can use checkpointings at set intervals to backup the data.

##### Fault tolerance of quadtree

- Because the quadtree will likely have both a table and cache, it will be highly available. However, if a single cache server dies, we won't have a way of knowing which quadtree branch or nodes the cache server stored.
- To ensure we know which cache server stores which quadtree branch / nodes, we can store a reverse mapping of cacheServerID: [ quadtreeBranch, nodeIDs ] in a configuration service such as ZooKeeper, or within the Quadtree table itself. This way, if the cacheServerID died, we can rebuild the quadtree branch / nodes using this reverse mapping.

#### PostGIS service

- Refer to the "PostGIS" section in the resource note 'Location based search' for the background on PostGIS.

<br/>

- While PostGIS provide's geohash functionality, PostGIS doesn't necessarily use geohash strings for a lot of it's location based searching operations. PostGIS uses it's built-in geometries which can be created using a location's long / lat value. These geometries are then used to perform spatial operations.

- PostgreSQL's PostGIS extension can significantly optimize geospatial queries. Instead of using geohash strings, PostGIS uses built-in geometries (it's GEOMETRY type, and additional types to represent points, polygons, radius, etc) to perform location based searches which will be more accurate than approximations performed using a geohash. We can first convert a location's long / lat into PostGIS-compatible geometries and use PostGIS functions to efficiently perform spatial operations. This provides faster and more efficient results than just using a LIKE query on the geohash strings in 'Using LIKE to filter geohash strings' (in resource notes), or using a 2D search using long / lat in '2D search using long / lat' (in resource notes).

- PostGIS performs true geospatial calculations on the sphere using it's own built-in algorithms, avoiding errors from geohash approximations. It also provides radius-based queries for precision when we need locations within a specific search radius. For faster searches, we can also index on the location column which is of the GEOMETRY type, where GEOMETRY specifies a specific point using long / lat values.

We can store geometries by using PostGIS, and then query using PostGIS spatial functions using the below steps:

##### 1. Store geometries in table:
  
- We can first convert the geohash into a PostGIS GEOMETRY or bounding box and store it in a GEOMETRY column in a specific table
- For example, we'll first add a location column of type GEOMETRY to the Profile table as shown below. In here, POINT is a PostGIS type which represents the long / lat, and SRID 4326 specifies the WGS84 coordinates format.

```sql
alter table profileTable
add column location GEOMETRY(POINT, 4326)
```

- To populate the location column using a specific long / lat value, we can do the following. ST_MakePoint will return a POINT type using the long / lat values we provide.

```sql
update profileTable
set location = ST_SetSRID(ST_MakePoint(long, lat), 4326)
```  

##### 2. We can then query using PostGIS spatial functions:

**If we want to find locations using a specific point, we can do the following:**

- For example, we can use the ST_Intersects function to check if a profile's location (location is PostGIS's GEOMETRY type) intersects with a specific polygon as shown below. For example, we'll input the polygon's max / min long / lat values into the ST_MakeEnvelope function which will create a rectangular polygon. Other polygon based functions are also available in PostGIS. We'll then use the ST_Intersects function, and input the profile's location field (which will be of a PostGIS GEOMETRY type) and also input this polygon.

```sql
select * from profileTable
where ST_Intersects(location, ST_MakeEnvelope(${minLong}, ${minLat}, ${maxLong}, ${maxLat}, 4326)
```

**If we want to find locations within a specific search radius, we can do the following:**

- We can also use the ST_DWithin PostGIS function to find profiles within a specific search radius as shown below. We'll use ST_MakePoint to create a point using a long / lat value of the center of the search radius. In here, the centerLong and centerLat values will be center's long / lat values. The radiusInMeters value will be the actual search radius in meters. ST_DWithin will check if the profile's location is within the specified radius's center point.

```sql
select * from profileTable
where ST_DWithin(location, ST_SetSRID(ST_MakePoint(${centerLong, ${centerLat}}), 4326), ${radiusInMeters})
```

## Ensuring swiping is consistent and has low latency

Let's start by considering the failure scenario. Imagine Person A and Person B both swipe right (like) on each other at roughly the same time. Our order of operations could feasibly look something like this:

1. Person A swipe hits the server and we check for inverse swipe. Nothing.
2. Person B swipe hits the server and we check for inverse swipe. Nothing.
3. We save Person A swipe on Person B.
4. We save Person B swipe on Person A.

Now, we've saved the swipe to our database, but we've lost the opportunity to notify Person A and Person B that they have a new match. They will both go on forever not knowing that they matched and true love may never be discovered.

<img width="800" alt="image" src="https://github.com/user-attachments/assets/95de65ee-259f-40fe-8fb2-58333b5de0c4" />

Given that we need to notify the last swiper of the match immediately, we need to ensure the system is consistent. Here are a few approaches we could take to ensure this consistency (discussed in 'Ensuring swiping is consistent and has low latency'):
- Database polling for matches
- Transactions
- Sharded cassandra with single-partition transactions
- Redis for atomic operations:
  - Note that we won't need to use a Redis distributed lock because it's not technically possible for multiple users to swipe right on the same user, and for the same user to also swipe right on all those users at the same time. Simply using a Redis hash to perform atomic operations (due to Redis's single-threaded nature) works better. This means that the operations made in the Redis hash will be serialized, thus the ordering of the 2 "swipe rights" don't matter, they will always happen in-serial.
  - The main challenge with this approach is managing the Redis cluster effectively. While Redis provides excellent performance for atomic operations, we need to carefully handle node failures and rebalancing of the consistent hashing ring. However, these operational challenges are more manageable than trying to achieve consistency in Cassandra. Also, it's very rare for 2 different users to swipe right on each other at the same time, thus it's unlikely that the Redis servers managing these atomic operations will crash due to request intensity.

## Ensuring low latency for feed / stack generation

When a user opens the app, they want to immediately start swiping. They don't want to have to wait for us to generate a feed for them. We can ensure low latency for feed / stack generation by doing the following and in 'Ensuring latency for feed / stack generation':
- Use of indexed databases for real-time querying
- Pre-computation and caching
- Combination of pre-computation and indexed database

Astute readers may realize that by pre-computing and caching a feed, we just introduced a new issue: stale feeds. How do we avoid stale feeds?

Caching feeds of users might result in us suggesting "stale" profiles. A stale profile is defined as one that no longer fits the filter criteria for a user. Below are some examples of the ways a profile in a feed might become stale:

1. A user suggested in the feed might have changed locations and is no longer close enough to fit the feed filter criteria.
2. A user suggested in the feed might change their profile (e.g. changed interests) and no longer fits the feed filter criteria.

To solve this issue of stale potential matches, we might consider having a strict TTL for cached feeds (< 1h) and re-compute the feed via a background job on a schedule. We also might pre-computing feeds only for truly active users, vs. for all users. Doing upfront work for a user feed several times a day will be expensive at scale, so we might "warm" these caches only for users we know will eventually use the cached profiles. A benefit of this approach is that several parameters are tunable: the TTL for cached profiles, the number of profiles cached, the set of users we are caching feeds for, etc.

<img width="800" alt="image" src="https://github.com/user-attachments/assets/d3901fcc-97e7-4654-925e-5e89b40a0755" />

A few user-triggered actions might also lead to stale profiles in the feed:

1. The user being served the feed changes their filter criteria, resulting in profiles in the cached feed becoming stale.
2. The user being served the feed changes their location significantly (e.g. they go to a different neighborhood or city), resulting in profiles in the cached feed becoming stale.

All of the above are interactions that could trigger a feed refresh in the background, so that the feed is ready for the user if they choose to start swiping shortly after.

## Avoid showing user profiles that a user previously swiped on

It would be a pretty poor experience if users were re-shown profiles they had swiped on. It could give the user the impression that their "yes" swipes were not recorded, or it could annoy users to see people they previously said "no" to as suggestions again. We should design a solution to prevent this bad user experience (discussed in 'Avoid showing user profiles that a user previously swiped on'):
- DB query + contains check
- Cache + DB query + contains check
- Cache + contains check + bloom filter

























