# Location based search

Note: The below explanations will use the design for Yelp, where there will be businesses (with a long / lat) within a search radius

## Location based search approaches

- There are many ways to efficiently perform location based searching:
  - 2D search using long / lat
  - PostgreSQL's PostGIS
 
  - The below approaches divides the map into smaller areas and then builds indexes for a fast search:
    - Evenly divided grid
    - Geohash
    - Quadtree
    - Google S2

### 2D search using long / lat

- In a 2D search, we use a simple query to retrieve results using the long / lat, such as the SQL query below.
- In this case, once we have the businessIDs from the below query, we can then join this result to another table which contains additional data about the businesses such as reviews, ratings, bookings, etc.
- This approach is not efficient because we need to do a full table scan and search for all businessIDs within the search radius.

2D search using long / lat:
```sql
select businessID, lat, long from businessTable
where (lat between (${searchLat} - ${searchRadius}) and (${searchLat} + ${searchRadius})
and long between (${searchLong} - ${searchRadius}) and (${searchLong} - ${searchRadius}))
```

### Evenly divided grid

- This approach evenly divides the world into small grids, where a single grid can have multiple businesses, and each business belongs to one grid. This way, we'll query only a few grids to find businesses. Based on a given search location and radius, we can also find all the neighboring grids and then query those grids to find the businesses.
- A grid size could be equal to the distance we would like to query since we also want to reduce the number of grids. If the grid size is equal to the distance we want to query, then we only need to search within the grid which contains the given location, and also query the neighboring eight grids. Since our grids are statically defined (each grid has the same size), we can easily find the gridID of any location and it's neighboring grids.
- The downside of this approach is that the distribution of businesses will not be even, let's say for a city like New York. Thus, we'll have uneven grids, where some grids will be more populated than others. Ideally, we would want to use more smaller grids for dense areas, and large grids in sparse areas.

### Geohash

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

An example of a table containing geohash strings is given below:

<img width="426" alt="image" src="https://github.com/user-attachments/assets/9a0ba001-c665-4d7a-89f3-0c1e087b4ef5" />

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

<br/>

Geohash recursively dividing grids:

<img width="800" alt="image" src="https://github.com/user-attachments/assets/e181471d-207b-47b3-9c26-6c26b4c72042" />

### PostgreSQL's PostGIS

- While PostGIS provide's geohash functionality, PostGIS doesn't necessarily use geohash strings for a lot of it's location based searching operations. PostGIS uses it's built-in geometries which can be created using a location's long / lat value. These geometries are then used to perform spatial operations.

- PostgreSQL's PostGIS extension can significantly optimize geospatial queries. Instead of using geohash strings, PostGIS uses built-in geometries (it's GEOMETRY type, and additional types to represent points, polygons, radius, etc) to perform location based searches which will be more accurate than approximations performed using a geohash. We can first convert a location's long / lat into PostGIS-compatible geometries and use PostGIS functions to efficiently perform spatial operations. This provides faster and more efficient results than just using a LIKE query on the geohash strings in 'Using LIKE to filter geohash strings', or using a 2D search using long / lat in '2D search using long / lat'.

- PostGIS performs true geospatial calculations on the sphere using it's own built-in algorithms, avoiding errors from geohash approximations. It also provides radius-based queries for precision when we need locations within a specific search radius. For faster searches, we can also index on the location column which is of the GEOMETRY type, where GEOMETRY specifies a specific point using long / lat values.

We can store geometries by using PostGIS, and then query using PostGIS spatial functions using the below steps:

#### 1. Store geometries in table:
  
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

#### 2. We can then query using PostGIS spatial functions:

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

### Quadtree

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

#### Quadtree table / cache

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

#### Building a quadtree

- We will start with one node that will represent the whole world in one quad. Since it will have more than 100 businesses, which may be our criteria, we will break it down into four nodes and distribute locations among them. We will keep repeating this process with each child node until there are no nodes left with more than 100 businesses.

#### Dynamic quads

- We can use dynamic quads in our quadtree where if the number of businesses exceed a threshold in a quad, we'll further split the quad into 4 more quads. In the quadtree, nodes will contain the businessIDs such that the businessID can be used to query the business info from a table containing the business data.

#### Searching in a quadtree

- In the quad tree, child nodes will be connected to sibling nodes with a DLL. Using the DLL, we can move left / right / up / down to sibling or child quads to find businesses. An alternative to a DLL is to use parent pointers from the child nodes to the parent node.

- When searching in the quadtree, we start searching from the root node and visit child nodes which are in the search radius. If a child node is in the search radius, we can traverse through it’s own child nodes and sibling nodes using the DLL and return them if they are also in the search radius.

- If we don't have enough businesses to return after searching a specific node, we can search the node's siblings and also it's parent node to retrieve surrounding businesses as well.

#### Adding / updating / removing an entry (business) in a quadtree

- To add / update a business in the quad tree, we can search the nodes for the businessID and add / update the business in the node, and also update any neighboring siblings if needed. If after adding the business, the leaf node reaches the threshold on the number of businesses a node can have, we'll need to split this leaf node further into 4 leaf nodes and allocate these 4 leaf nodes with the businesses from the original leaf node.
- To remove a business in the quad tree, we can search the nodes for the businessID and remove the business from the node, and update the neighboring nodes accordingly

#### Quadtree sharding / partitioning

- We can shard the quadtree based on regions on the basis of zip or postal codes, such that all the businesses and nodes that belong to a specific region are stored in a single shard. A region in this case will be a branch within a quadtree - therefore, a shard could contain a separate part of a single quadtree (the branch). Some regions could also be combined into a single shard to prevent uneven distributions.
- We can do this since the user’s queries will be based on the location, so sharding this way will cause less inter-shard communication and speed up queries.
- However, this approach will result in slow responses when numerous queries are on the server for a single shard possibly during a tourist season. To prevent hotspots, we can apply replication to the quadtree, as the data is not at all large or updates frequently, making replication very easy to do.
- There could also likely be a mapping maintained within ZooKeeper that keeps track of the mapping between regionID : shardID. regionID or shardID will rarely change (it may change only when a new region or shard is updated), thus this mapping will rarely change.

#### Quadtree replication

- We can replicate both the quadtree table and cache on multiple servers to ensure high availability. This also allows us to distribute the read traffic and decrease the response times.
- Quadtrees should take up relatively little storage, and thus can be backed up easily. In case we may lose the quadtree data, we can use checkpointings at set intervals to backup the data.

#### Fault tolerance of quadtree

- Because the quadtree will likely have both a table and cache, it will be highly available. However, if a single cache server dies, we won't have a way of knowing which quadtree branch or nodes the cache server stored.
- To ensure we know which cache server stores which quadtree branch / nodes, we can store a reverse mapping of cacheServerID: [ quadtreeBranch, nodeIDs ] in a configuration service such as ZooKeeper, or within the Quadtree table itself. This way, if the cacheServerID died, we can rebuild the quadtree branch / nodes using this reverse mapping.

### Google S2

- Google S2 is similar to a quadtree data structure in that it is also an in-memory solution. It maps a sphere or long / lat value to a 1D index using the Hilbert curve (a sphere-filling curve). In the Hilbert curve, 2 points that are close to each other are also close in the 1D space according to it's 1D index values. Searching on a 1D space is also much faster than searching on a 2D space.

- S2 is great for looking at nearby businesses using a 1D index. Another advantage is it's Region Cover Algorithm, where instead of having a fixed level precision (fixed level precision being the maximum number of businesses in a grid, such as with geohash), we can specify the minimum level, maximum level, and maximum cells in S2. This way, results are more granular and the grid size is more flexible.

- The downside of S2 is that it is complex, and takes a SME to understand the internals.

### Geohash vs quadtree

#### Geohash

- Geohash is easy to implement and supports returning a business within a specified search radius, since a location will have a similar prefix to the prefix of the radius' geohash string.
- Removing a business from a geohash string is also easy since we just need to remove it from a geohash database, instead of removing it from a leaf node within the quadtree, and then updating the quadtree if the leaf node no longer contains any businesses after it's last business has been removed.
- The precision level of geohash is also fixed, thus the grid cannot be dynamically adjusted based on business density like with a quadtree. More complex logic may be needed to support adding dynamically adjusted grids to a geohash based approach.

#### Quadtree

- A quadtree is sometimes harder to implement because we need to build the tree first.
- A quadtree provides dynamic adjustments where we can dynamically adjust the precision level for dense cities like New York by dividing the grid further.
- It can also return the K businesses within a search radius by only traversing the child nodes and sibling nodes which are within the radius. We can also return the K-nearest businesses to a specific point using this approach by comparing the distance between the point to the business's location when we're traversing the tree - then we'll return the smallest K distances, which will be the K-nearest businesses.
- A downside to a quadtree is that updating the tree when adding or removing businesses may be a bit complex. Thus if there is a high frequency of updates, then a quadtree may not be the best, and a geohashing approach may be more simpler since the geohash value only needs to be changed for a single entry, as opposed to updating the sibling nodes and leaf node in a quadtree.
- To remove a business, we need to traverse from the root to the leaf node, and remove the businessID from that leaf node, then delete the node if there are no other businessIDs. This operation will take O(logn) time since we're going down the tree. Likewise, when we add a business, we'll traverse down the tree to look for the leaf node that meets the criteria (criteria may be if the leaf node's radius contains the business we will add) for the new business we will add. We'll then add the businessID to that specific leaf node.








