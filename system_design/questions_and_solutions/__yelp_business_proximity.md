# Yelp - Business proximity system

Yelp is an online platform that allows users to search for and review local businesses, restaurants, and services.

## Requirement

### Questions

- Are we designing the system for both the business host, and other users?
  - Yes

- In this system, business hosts can add businesses, users can search for businesses in a search radius, users can leave reviews, and can view a business and it's reviews. Are we designing all of this?
  - Yes
  
- Can the user change the search radius?
	- Yes

- Should users be able to view businesses on a map, or just as a simple paginated result?
  - A simple paginated result is fine

- Does the business info need to be updated in real-time by business owners?
	- No, it can be done within the next day

- How many businesses are we storing?
  - 10M businesses

### Functional

- The system can be used by both business hosts and other users:
  - Business hosts can add businesses
  - Users can search for businesses by name, location (long / lat), search radius and category
  - Users can leave reviews of businesses using a rating and description
  - Users can view a business, and it's reviews

### Non-functional

- Availability > consistency:
  - Eventual consistency in updating the businesses is fine
- Low latency:
  - Search results should be returned with low latency (10 - 500 ms)
- Efficiently returning location based search results

### Constraints

- A common constraint with Yelp is that each user can only leave one review per business

## Data model / entities

- In our data, we have high read volume / low write volume

<br/>

- Businesses:
	- businessID
	- name, description
	- location
	- long / lat / geohash (if the system is using geohash) / location (if the system is using PostGIS, then location will be of PostGIS's GEOMETRY type)
	- category
	- rating, numReviews (numReviews will be used to efficiently calculate the rating for a business as discussed in the DD)
	
- User:
	- userID
	- userName
  - userEmail

- Reviews:
	- reviewID
	- userID
	- businessID
	- review
	- rating
  - metadata: { createdAt }

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### User's endpoints

#### Search for businesses

- This endpoint will return a list of businesses within a search radius, using the long / lat and some location based search functionality (like geohash, PostGIS, quadtree, etc) to efficiently find businesses within the radius
- Note that we'll likely return the results in sorted order based on the distance from the radius's center location to the businesses within the search radius. Thus, we can use cursor based pagination, where the nextCursor points to the businessesID of the results in sorted order (by distance), and returns the paginated results

Request:
```bash
GET /businesses?query&location={LONG AND LAT}&radius&category&nextCursor={ businessID }&limit
```

```Response
{
  businesses: [ { businessID, name, location, category } ],
  nextCursor, limit
}
```

#### View business info and reviews

- Note that the reviews returned via pagination could be sorted by the createdAt field, or some other likes / dislikes field. We can also apply cursor based pagination, where the cursor points to the viewport's oldest review's createdAt value

Request:
```bash
GET /businesses/:businessID (View business info)
GET /businesses/:businessID/reviews?nextCursor={ viewport's oldest review's createdAt }&limit (View business reviews)
```

Response:
```bash
Business info:
{
  businessID, name, location, category
}

Reviews:
{
  reviews: [ { reviewID, userName, review, rating } ],
  nextCursor, limit
}
```

#### Add review

Request:
```bash
POST /businesses/:businessID/reviews
{
  rating, review
}
```

### Host's endpoints

#### Add business

Request:
```bash
POST /businesses
{
  name, description, location, category
}
```

## HLD

### Microservice architecture

- A microservice architecture is suitable for this system, as the system requires independent services such as searching businesses, adding reviews, etc. These are all independent operations which could potentially be managed by separate services.

- Microservices can benefit from a gRPC communication as there will be multiple channels of requests	being sent / received in inter-service communication between microservices. Thus, gRPC could be the	communication style between microservices, as it supports a higher throughput, and is able to handle multiple channels of requests as opposed to REST, which uses HTTP, that is not optimized for		multi-channel communication between services.

### API gateway

- The API gateway will provide rate limiting, authentication, and route requests to the specific services.	For example, for searching businesses, the Business service can handle the requests.
- The API gateway will also allow combining 2 requests into 1, ie if a user wants to view business details along with the reviews, then the API gateway could compile the results from both the Business and Reviews services.

### Business service

- The Business service will handle search requests to find businesses using a category and a search radius of a location. It will also handle requests for adding businesses and viewing business details.

#### Business service using Geohash service vs PostGIS service vs Quadtree service

- The Business service will also use either the Geohash service or the PostGIS service or the quadtree service to efficiently search businesses using geohash strings, PostGIS, or a quadtree respectively, and return the paginated results of the businesses within a search radius. The specifics of the approaches, and additional approaches which can be used are discussed in the DD.

### Database / cache

- The database will store business and reviews tables. The data will be more ready heavy, as businesses and reviews won't update as frequently. We can use either a SQL based DB such as PostgreSQL, or a KV store such as DynamoDB since the data is relatively simple excluding the geocode data. PostgreSQL will provide a higher consistency, but may not be as optimal when scaling horizontally compared to DynamoDB. However, at the same time maintaining relationships in DynamoDB may be a bit more complex than doing it in PostgreSQL.
- Because the data isn't very large where it requires optimal horizontal scalability - and also because we may need to handle complex queries for searching businesses, we'll use PostgreSQL.
- Additionally, PostgreSQL provides PostGIS which can be used to index and query geocoded data - which will be helpful for searching businesses. PostgreSQL also has a full text search extension called pg_trgm which uses inverted indexes, that can be used to index and query text data. We can create these extensions using the below, as discussed in the DD.
```sql
create extension if not exists postgis;
create extension if not exists pg_trgm;
```

#### Cache

- Because the system is read heavy and needs very little storage for the business and reviews data, we could also cache the frequently accessed business and reviews with an appropriate TTL. This will further support hotkeys for businesses that may be tourist attractions.
- We can use Redis since the businesses within a specific location will likely need to be contained within a Redis list. Also, a Redis sorted set can be used to keep the reviews for a specific businessID sorted by the createdAt field.

#### Separated or single database for microservices

- It's usually assumed that we need to have separate databases for different microservices. However, the choice depends on multiple factors. In many systems, using the same database for multiple purposes is usually much simpler, and easier to maintain.

<br/>

- If we assume that there are 10M businesses, and each business has 100 reviews or so, where a single review is 500 bytes, then 10M businesses * 100 reviews * 500 bytes = 500 GB. A modern database can handle both the business info + reviews data easily, so sharding may not even be a requirement. Joining operations may also take less time if the tables are within one database, because there may be fewer network calls being made to join data.
- However, fault tolerance may be a counter argument to having separated databases for different microservices. With separated databases, we'll make sure that if a single database goes offline, the other database can still function. However, if the data is relatively small such as this case, then it could also be partitioned and replicated for fault tolerance.

<br/>

- At the end of the day, it's still a discussion of trade-offs with no single correct answer. For simplicity and ease of use, a single database is better, however if data needs to be separated to support scalability, different read / write ratios, fault tolerance, etc, then having separate databases may be better.

### Geohash service (if using geohash)

- The Geohash service will search for businesses within a search radius using a geohash based approach, and return them to the Business service. The Geohash service will take a geohash of the search radius (using a geohash converter) and find businesses within the specified radius by comparing their geohash strings.
- The geohash converter, which could be PostgreSQL's PostGIS geohash conversion functionality shown in 'PostGIS geohash conversion function', will take a long / lat coordinate of either a radius or business, and then convert it to a geohash string. This geohash string will be compared against the geohash strings in the Businesses table / cache to find relevant businesses.
- Because we're using geohash, the Geohash service will compare the prefixes of the search radius' geohash string with the prefixes of the businesses' geohash string. If the prefixes are the same, then this means the business is within the search radius. A query such as the one below can be used to find businesses with the same prefix as the search radius' geohash.

```sql
select businessID, lat, long, geohash from businessTable
where geohash like '${radiusGeohash}'
```

PostGIS geohash conversion function:
```sql
select ST_GeoHash(ST_Point(${long}, ${lat}))
```

- When new businesses are added, we'll also use the Geohash service to generate a geohash string for the new business, and then store it in the Businesses table.

- Geohash can sometimes be slower than a typical quadtree. It can also be slower than PostGIS's built-in location based search functionalities. This will be discussed more in the DD.

#### Geohash cache

- Because the querying the geohash data on disk may be slow, we can store a geohash cache in Redis. Redis provides support for geohashing to encode and index geospatial data, allowing for fast querying. The key advantage of Redis is that it stores data in memory, resulting in high-speed data access and manipulation. Additionally, we can periodically save the in-memory data to the Businesses table using CDC (change data capture).

### Quadtree service (if using quadtree)

- The Quadtree service will recursively build and update the Quadtree table and cache. The Quadtree service will also be used to search the quadtree efficiently by traversing down the tree from the root node to the leaf nodes. The search within a quadtree will be discussed more in the DD.
- A quadtree may be more suitable for this design than a geohashing approach, since there are many high density areas such as NYC, and a quadtree will account for these dense areas by splitting up the quads further.

#### Quadtree table / cache

- Because a quadtree is an in-memory data structure, we can keep both a quadtree table within PostgreSQL as well as a cache using Redis. PostgreSQL provides SP-GiST, which provides functionality for storing and querying a quadtree data structure.
- Although Redis doesn't directly provide quadtree support, we'll use Redis as the quadtree cache since it provides complex data structures such as lists and sorted sets which will be helpful in storing nodes of the quadtree. For example, the leaf node of a quadtree can be a Redis sorted set, where the businesses are sorted based on their distances to the leaf node's radius's center point. A leaf node can also contain a Redis list which contains businesses from the Business table which fall within the leaf node's radius.
- Additionally, a quadtree data structure is not as complex to build, and could be implemented within a memory optimized EC2 instance.

### PostGIS service (if using PostGIS)

- We could also use a PostGIS service which will convert the business long / lat values in the Businesses table to a PostGIS GEOMETRY type. We'll then add a new column of this GEOMETRY type (we'll call it the location column) to the Businesses table. This PostGIS service will then be used to query the Businesses table using PostGIS search functions like ST_Intersects (to find if a long / lat value intersects with another point) and ST_DWithin (to find if a long / lat value is within a radius).
- The DD will discuss more on PostGIS and it's usage in efficiently searching for businesses.

### Reviews service

- The Reviews service will handle viewing and writing reviews to the Reviews table.

#### Separate services vs combined services

- Sometimes it may be appropriate to have separate services, however there is no hard and fast rule. Depending on the below, we may need separate services for different aspects of the system:
  - Whether the functionaliity is closely related
  - Whether the services need to scale independently due to vastly different read / write patterns
  - A single service may have a very different implementation than another service - then we might want separate services
- In this case, the Business service will have a different implementation in that it'll use an efficient location based search functionality to perform searches. Also the location based data stores may be very different in that it also needs to be scaled different, for example a quadtree may also require a cache which needs to be scaled differently. Also, users will search for businesses a lot using the Business service as opposed to leaving a review via the Reviews service which will be in-frequent - which means that the read / write ratio will be different and it's better to scale them separately.

<img width="750" alt="image" src="https://github.com/user-attachments/assets/38d0a25a-27fc-494f-bbf3-4fd84d58161d" />

## DD

### Efficiently storing the location data for fast searches

Efficiently storing location data for fast searches can be done using multiple approaches. The resource notes in 'Location based search' goes over all of the main approaches. However, in this DD, we'll use either geohash, quadtree or PostGIS.

#### Geohash service

- Refer to the "Geohash" section in the resource note 'Location based search' for the background on geohash.

<br/>

- Geohash works by converting the long / lat to a string of letters and digits. We first divide the map into 4 grids recursively until the grid size is small enough such that it can contain a relatively small number of businesses. As the map gets recursively divided, we'll assign a generated Base-32 geohash string to the grid. Geohash also operates with a fixed precision, where the smallest grids cannot be further divided, and all the smallest grids will have the same size. However, custom dynamic behavior can be added to a geohashing approach, but adding dynamic behavior may be more complex to do.
- Since geohashes represent hierarchical spatial data, shorter geohash strings cover larger areas, and longer geohash strings cover smaller areas with more precision. Therefore, if we keep removing the last character from a geohash string, the new geohash string will be for a larger area. To make geohash filtering more efficient, we can index the geohash column (like in 'Index on geohash') so that queries with the LIKE or WHERE operators will optimize it's prefix based searches.
- An example of using LIKE with a geohash string is given below:

Index on geohash:
```sql
CREATE INDEX idx_geohash ON Businesses USING geohash
```

Using LIKE to filter geohash strings:
```sql
select businessID, lat, long, geohash from businessTable
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

- Geohash works well for majority of the cases, but boundary issues may come up when one business covers 2 geohash strings. Additionally, in some cases, there could be businesses within the border of 2 geohash strings, and so that business doesn't belong to any geohash string. In these cases, the geohash generation algorithm can be modified to account for such edge cases.
- Also, another issue may be when too few businesses appear in the search result. In this case, we can increase the search radius by removing the last digit of the geohash string, and we can continue to increase the radius by removing another digit from the end.

##### Geohash sharding / partitioning

- If we have a table containing the businessIDs and geohash strings, we can easily shard the database and partition the tables based on prefixes of the geohash strings. We'll shard by the prefixes of the geohash strings because businesses which are within the same geohash search radius will also be within the same shard. This will make searches faster, since we'll have to look through fewer shards or entries of the table.
- In general, tables containing location data for businesses take up very little storage, thus sharding or partitioning may not even be needed, but will help to support the read load and fault tolerance.

#### Quadtree service

- Refer to the "Quadtree" section in the resource note 'Location based search' for the background on quadtrees.

<br/>

- A quadtree also recursively divides the map into 4 grids until the contents of the grids meet a certain criteria, like not having more than 100 businesses. A quadtree is an in-memory data structure that helps with location based searching.
- The data on a leaf node (leaf node represents the most granular grid) in a quadtree can contain long / lat and a list of businessIDs in the grid. The data on a parent node (parent node represents the parent grid of leaf nodes) contains the parent grid's long / lat values and pointers to the 4 child nodes.
- Assuming a leaf node has at most 100 businesses, then to build a quad tree for N businesses:
  - It will take (N * 100) * log(N / 100) time complexity, since we're parsing through (N / 100) leaf nodes which contains at max 100 businesses each, and we'll also be parsing the height of the tree which will be log(N / 100), where N / 100 is the number of leaf nodes.

- Below is an example of a quadtree quad:
<img width="750" alt="image" src="https://github.com/user-attachments/assets/23144928-0519-46eb-8b49-4dd0cd8c45b5" />

<br/>

- To search in a quadtree, we'll start from the root node and traverse down the tree until we find a node within the search radius. If we find a node within the search radius, we'll traverse the node's child nodes and siblings to see if they're also in the search radius. We'll keep a list of businesses in the leaf nodes which are within the search radius, and then return the list of businesses. The downside to a quadtree is that searches can be a bit complex to implement.
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
businesses: [ { businessID, name, location, long / lat, category } ],
nodeQuad: { maxLong, maxLat, minLong, minLat },
leafNode: TRUE / FALSE,
childNodePtrs: { childNode_1, childNode_2, childNode_3, childNode_4 }
}
```
- In this entry, the nodeID can represent the node of the quadtree. If a node is a leaf node, we'll set the leafNode to TRUE. Also, if it is a leaf node, then there will be businesses populated within this node. The nodeQuad field will also be the quad's max /  min long / lat values.
- When searching for businesses within a search radius, we'll first check if the nodeQuad's long / lat values are intersecting with the search radius. If the quad is intersecting, then we'll traverse down the tree to find the leaf nodes. In the leaf nodes, we'll search for businessIDs which have long / lat values within the search radius.

##### Building a quadtree

- We will start with one node that will represent the whole world in one quad. Since it will have more than 100 businesses, which may be our criteria, we will break it down into four nodes and distribute locations among them. We will keep repeating this process with each child node until there are no nodes left with more than 100 businesses.

##### Dynamic quads

- We can use dynamic quads in our quadtree where if the number of businesses exceed a threshold in a quad, we'll further split the quad into 4 more quads. In the quadtree, nodes will contain the businessIDs such that the businessID can be used to query the business info from a table containing the business data.

##### Searching in a quadtree

- In the quad tree, child nodes will be connected to sibling nodes with a DLL. Using the DLL, we can move left / right / up / down to sibling or child quads to find businesses. An alternative to a DLL is to use parent pointers from the child nodes to the parent node.

- When searching in the quadtree, we start searching from the root node and visit child nodes which are in the search radius. If a child node is in the search radius, we can traverse through it’s own child nodes and sibling nodes using the DLL and return them if they are also in the search radius.

- If we don't have enough businesses to return after searching a specific node, we can search the node's siblings and also it's parent node to retrieve surrounding businesses as well.

##### Adding / updating / removing an entry (business) in a quadtree

- To add / update a business in the quad tree, we can search the nodes for the businessID and add / update the business in the node, and also update any neighboring siblings if needed. If after adding the business, the leaf node reaches the threshold on the number of businesses a node can have, we'll need to split this leaf node further into 4 leaf nodes and allocate these 4 leaf nodes with the businesses from the original leaf node.
- To remove a business in the quad tree, we can search the nodes for the businessID and remove the business from the node, and update the neighboring nodes accordingly

##### Quadtree sharding / partitioning

- We can shard the quadtree based on regions on the basis of zip or postal codes, such that all the businesses and nodes that belong to a specific region are stored in a single shard. A region in this case will be a branch within a quadtree - therefore, a shard could contain a separate part of a single quadtree (the branch). Some regions could also be combined into a single shard to prevent uneven distributions.
- We can do this since the user’s queries will be based on the location, so sharding this way will cause less inter-shard communication and speed up queries.
- However, this approach will result in slow responses when numerous queries are on the server for a single shard possibly during a tourist season. To prevent hotspots, we can apply replication to the quadtree, as the data is not at all large or updates frequently, making replication very easy to do.
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
- For example, we'll first add a location column of type GEOMETRY to the businesses table as shown below. In here, POINT is a PostGIS type which represents the long / lat, and SRID 4326 specifies the WGS84 coordinates format.

```sql
alter table businesses
add column location GEOMETRY(POINT, 4326)
```

- To populate the location column using a specific long / lat value, we can do the following. ST_MakePoint will return a POINT type using the long / lat values we provide.

```sql
update businesses
set location = ST_SetSRID(ST_MakePoint(long, lat), 4326)
```  

##### 2. We can then query using PostGIS spatial functions:

**If we want to find locations using a specific point, we can do the following:**

- For example, we can use the ST_Intersects function to check if a business's location (location is PostGIS's GEOMETRY type) intersects with a specific polygon as shown below. For example, we'll input the polygon's max / min long / lat values into the ST_MakeEnvelope function which will create a rectangular polygon. Other polygon based functions are also available in PostGIS. We'll then use the ST_Intersects function, and input the business's location field (which will be of a PostGIS GEOMETRY type) and also input this polygon.

```sql
select * from businesses
where ST_Intersects(location, ST_MakeEnvelope(${minLong}, ${minLat}, ${maxLong}, ${maxLat}, 4326)
```

**If we want to find locations within a specific search radius, we can do the following:**

- We can also use the ST_DWithin PostGIS function to find businesses within a specific search radius as shown below. We'll use ST_MakePoint to create a point using a long / lat value of the center of the search radius. In here, the centerLong and centerLat values will be center's long / lat values. The radiusInMeters value will be the actual search radius in meters. ST_DWithin will check if the business's location is within the specified radius's center point.

```sql
select * from businesses
where ST_DWithin(location, ST_SetSRID(ST_MakePoint(${centerLong, ${centerLat}}), 4326), ${radiusInMeters})
```

### Efficiently searching for businesses using full text search

- Searching by long / lat in a traditional database without a proper indexing is very inefficient for large datasets. When using simple comparison operators to find businesses based on long / lat within a search radius or box, the database has to perform a full table scan to check every single entry which matches these conditions. This is also true when searching for terms in the name or description. This would require a wild card search across the entire database via a LIKE clause.

Inefficient way of searching for businesses:
```sql
select * from businessTable
where lat > 10 and lat < 20 and long > 10 and long < 20 and name like '%coffee%'
```

- We can efficiently search for businesses using the below approaches, and in 'Efficiently searching for businesses using full text search':
  - Basic database indexing
  - Elasticsearch
  - PostgreSQL with extensions:
    - While pg_trgm is great for full text searches, it still may not perform as well as Elasticsearch which is more optimal for searching through text.

In some cases, interviewers will ask that you don't use Elasticsearch as it simplifies the design too much. If this is the case, they're often looking for a few things in particular:

1. They want you to determine and be able to talk about the correct geospatial indexing strategy. Essentially, this usually involves weighing the tradeoffs between geohashing and quadtrees, though more complex indexes like R-trees could be mentioned as well if you have familiarity. In my opinion, between geohashing and quadtrees, I'd opt for quadtrees since our updates are incredibly infrequent and businesses are clustered into densely populated regions (like NYC).

2. Next, you'll want to talk about second pass filtering. This is the process by which you'll take the results of your geospatial query and further filter them by exact distance. This is done by calculating the distance between the user's lat/long and the business lat/long and filtering out any that are outside of the desired radius. Technically speaking, this is done with something called the Haversine formula, which is like the Pythagorean theorem but optimized for calculating distances on a sphere.

3. Lastly, interviewer will often be looking for you to articulate the sequencing of the phases. The goal here is to reduce the size of the search space as quickly as possible. Distance will typically be the most restrictive filter, so we want to apply that first. Once we have our smaller set of businesses, we can apply the other filters (name, category, etc) to that smaller set to finalize the results.

### Allow searching by predefined location names such as cities and neighborhoods

- Users usually search using natural terms like city names or neighborhood names. For example, Pizza in NYC. Sometimes these terms don't only just contain addresses, but also names of specific parts in a city, like "Downtown toronto".

- A simple radius from the center point of this city or neighborhood is insufficient. This is because city or neighborhood names are not perfectly circular and can have widely different shapes. Instead, we need a way to define a polygon for each location, and then check if any of the businesses are within that polygon.

- These polygons are just a list of points and come from a variety of sources. For example, GeoJSON is a popular format for storing geographic data and includes functionality for working with polygons. They can also just be a list of coordinates that you can represent as a series of lat/long points.

- We need to do the below to find businesses within these polygons, where the polygons represent cities / neighborhoods:
1. We need to find a way to go from a location's name (such as Toronto or NYC) to a polygon.
2. We'll then use that polygon to filter a set of businesses that exist within it.

#### Solving for (1)

- Solving 1. is relatively straightforward - we can create a new table called Locations that maps location names like cities / neighborhoods to polygons. These polygon datasets can be sourced from various publicly available datasets like Geoapify.
- We can create a Locations table, where it contains the fields name (represents the city / neighborhood name), locationType (can be city, neighborhood, etc), and polygon (contains the polygon data). We'll then populate this Locations table with the data from the sourced polygons datasets. We'll also index the name field of this Locations table for faster lookups. This way, we can now find the polygon for a specific location name such as "Toronto" or "NYC".

Below is an example of an entry of this Locations table:
```bash
{
  locationName: "Toronto",
  locationType: CITY,
  polygon: [ polygons dataset from a source like Geoapify ]
}
```

#### Solving for (2)

- We'll need to be able to filter a set of businesses within a polygon. Both PostgreSQL via the PostGIS extension, and Elasticsearch have functionality for working with polygons which they call Geoshapes or Geopoints respectively.
- In the case of Elasticsearch, we can simply add a new geo_shape field to our business documents and use the geo_shape query to find businesses that exist within a polygon:

```json
{
  "query": {
    "geo_bounding_box": { 
      "location": {
        "top_left": {
          "lat": 42,
          "lon": -72
        },
        "bottom_right": {
          "lat": 40,
          "lon": -74
        }
      }
    }
  }
}
```

- Doing this bounding box search on every request isn't that efficient though. We can do better.
- Instead of filtering on bounding boxes for each request, we can pre-compute the areas for each business upon creation and store them as a list of location identifiers in our business table. These identifiers could be strings (like "san_francisco") or enums representing different areas.
- For example, a business document in Elasticsearch might look like this:
```json
{
  "id": "123",
  "name": "Pizza Place",
  "location_names": ["bay_area","san_francisco", "mission_district"],
  "category": "restaurant"
}
```

- Now all we need is an inverted index on the location_names field via a "keyword" field in ElasticSearch

- By pre-computing the encompassing areas we avoid doing them on every request and only need to do them once when the business is created.

### Efficiently calculating and updating the average rating for businesses to ensure it's available in search results

- When users search for businesses, we want to ensure the calculated and updated average rating for businesses is available. In our paginated search results, we won't show the full business details - we'll only show a partial view of the business data, such as it's name, location, category and rating.
- We can efficiently calculate and update the average rating for businesses to ensure it's available in the search results using the below approaches, and in 'Efficiently calculating and updating average rating':
  - Naive approach
  - Periodic update with cron job
  - Synchronous update with optimistic locking:
    - To solve concurrent write issues, we can use optimistic locking, where within a transaction or a write, we'll first need to confirm that the number of reviews hasn't changed in the duration of the transaction / write. If the number of reviews has changed, then the transaction / write will be rollbacked, then re-tried again.
    - Optimistic locking is actually a non-locking method that allows multiple users to attempt to update the same entry concurrently without the use of locks. However, only when the writes are being made, in optimistic locking, we'll check if the write follows certain constraints, ie in this case, the numReviews field cannot change in the duration of the transaction / write.

- We could also use a message queue, along with workers calculating and updating the ratings, however users will very infrequently leave reviews, which would make this not an optimal solution as explained in 'Downside of message queues + workers calculating and updating business rating'

### Ensuring a user can only leave one review per business

- We need to implement a constraint that allows users to leave only one review per business. We can do so using the below approaches, and in 'Ensuring a user can only leave one review per business':
  - Application-level check
  - Database constraint:
    - We can add a database constraint below to the Reviews table:

```sql
ALTER TABLE reviewsTable
ADD CONSTRAINT unique_user_per_business UNIQUE (userID, businessID)
```

- Generally speaking, whenever we have a data constraint we want to enforce that constraint as close to the persistence layer as possible. This way we can ensure our business logic is always consistent and avoid having to do extra work in the application layer.

### Returning ranked businesses

- To return ranked businesses, by let's say the rating, we can do the following for the different services we'll use:

#### Geohash

- Using the results from the Geohash service, we can sort the businesses based on the rating before applying pagination. However, this approach will be very slow, and thus a separate Redis sorted set containing the ranked businesses and their geohash strings could also be maintain to speed up searches based on ranking.

#### PostGIS
    
- Using PostGIS, it will also be similar to the geohash ranking approach, where we'll sort based on the rating before applying pagination and returning the results. However, this approach will be very slow, and thus we could also use a separate Redis sorted set here as well.

#### Quadtree

- Because a quadtree is an in-memory data structure, it will work the best when it comes to storing a Redis sorted set containing businesses sorted by the rating. To return the top K businesses based on the rating, we can just return the top K based on the quadtree node which will likely contain or reference a Redis sorted set. This approach may take up extra memory (not that much), but will be much faster than the previous approaches via geohash / PostGIS.
