# Local delivery like Gopuff

Gopuff delivers goods typically found in a convenience store via rapid delivery and 500+ micro-fulfillment centers. Note that this SDI is similar to the SDI 'E-commerce service like Amazon' and 'Uber'

## Requirements

### Questions

We'll start by asking our interviewer about the extent of the functionality we need to build. Our goal for this section is to produce a concise set of functionalities that the system needs to support. In this case, we need to be able to query availability of items and place orders.

- What part of Gopuff should we focus on, should we focus on the inventory and ordering design, the location based search, delivery, etc?
  - Focus on the system that will query the inventory and can be used to view order updates. Also, focus on the location based search for finding stores which contains the items and user's delivery address. Talk about the delivery process of the system as well, but don't focus purely on it.

- Should location based search to see delivery time and ETA (as well as if the delivery can be made within an hour or so) be incorporated?
  - Yes, include location based search

- Should we design the "delivery" part of the system, where the person making the delivery will provide their ETA periodically?
  - Talk about the design behind delivery, but let's not focus too much on it

### Functional

- Customers should be able to query availability of items, deliverable in 1 hour, by location (i.e. the effective availability is the union of all inventory nearby DCs)
- Customers should be able to order multiple items at the same time

#### Out of scope

- Handling payments / purchases
- Handling driver routing and deliveries
- Search functionality and catalog APIs (the system is strictly concerned with availability and ordering)
- Cancellations and returns

### Non-functional

- Low latency of inventory availability requests:
  - Inventory availability requests should fast (<100ms) to support use-cases like search
- Consistency in ordering:
  - Ordering should be strongly consistent: 2 customers should not be able to purchase the same physical product
- Scalability in order requests:
  - System should be able to support 10k DCs and 100k items in the catalog across DCs
  - Order volume will be O(10M orders / day)

## Data model / entities

- Items:
  - The Item entity will represent a specific item that customers will actually care about
    - itemID
    - name, description

- Inventory:
  - The Inventory entity will represent a physical instance of an item, located at a DC. We'll sum up inventory to determine the quantity available to a specific user for a specific itemID. Note that the Inventory entity is different from the Item entity in that the Item entity is like a class, while the Inventory entity contains objects of the class. While our API consumers are strictly concerned with items that they might see in a catalog (e.g. Cheetohs), we need to keep track of where the physical items are actually located at different DCs using this Inventory entity. Our Inventory entity is a physical item at a specific location.
    - itemID
    - dcID
    - stock

- DCs:
  - This represents a physical location where items are stored. We'll use these to determine which items are available to a user
    - dcID
    - long / lat

- Order:
  - This represents a collection of Inventory entries which have been ordered by a userID (we could also store shipping / billing info here)
    - orderID
    - userID
    - itemID
    - dcID
    - shipping / billing
    - metadata: { createdAt }

- Location updates:
  - Note that this entity will likely be only stored within a cache, since the drivers location data is very short lived and frequently updated - it doesn't make sense to store it in a DB. Also, there are likely nowhere near as many drivers as there are users, thus, it makes sense to store a single entry (or the past 2-3 location updates) for a driver's current location in-memory.
    - driverID
    - long / lat / geohash (if using a geohashing approach) / location (if the system is using PostGIS, then location will be of PostGIS's GEOMETRY type)
    - updatedAt 

One important thing to note for this problem is the distinction between Item and Inventory. You might think of this like the difference between a Class and an Instance in object-oriented programming. While our API consumers are strictly concerned with items that they might see in a catalog (e.g. Cheetohs), we need to keep track of where the physical items are actually located. Our Inventory entity is a physical item at a specific location.

The remaining entities should be more obvious: we need DistributionCenter (from here after: DC) to keep up with where our inventory is physically located and and Order entity to keep track of the items being ordered.

<img width="750" alt="image" src="https://github.com/user-attachments/assets/5693cf10-2837-4a66-a223-1aeceafd6eff" />

## API design

- Note that we’ll use userID if the user is authenticated and will be booking tickets. The userID could be placed in a session token or JWT in the Authentication header as such:
  - Authentication: Bearer

- The below caching header could also be applied to fetch frequently accessed entries quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
  - Cache-Control: no-cache max-age Private/Public

Next, we can start with the APIs we need to satisfy, which should track closely to our functional requirements. There are a lot of extraneous details we could shove into these APIs, but we're going to start simple to avoid burning unnecessary time in the interview (a common mistake in practice!).

To meet our requirements we'll need 2 main APIs: the first API allows us to get availability of items given a location (and maybe a keyword), and the second API allows us to place an order. We'll include cursor based pagination in our availability API to avoid overwhelming the client with more data than it needs.

### View item availability

Request:
```bash
GET /items/:itemID/availability?lat&long&nextCursor&limit (if viewing availability of itemID)
GET /availability?searchQuery&lat&long&nextCursor&limit (if viewing availability of itemIDs corresponding to the searchQuery)
```

Response:
```bash
{
  items: { [ name, stock ] },
  nextCursor, limit
}
```

### Place order on item

Request:
```bash
POST /order -> Partial<Order> | Failure (will return a partial view of the Order object, or a Failure object)
{
  lat, long,
  items: Item[] (could simply also contain a partial view of the Item object, which includes itemID)
}
```

<img width="750" alt="image" src="https://github.com/user-attachments/assets/340fc426-fd04-4377-bfce-6fa303ca4932" />

Delivery person based APIs:

### Location updates from delivery person

- The delivery person could also provide location updates to the backend servers so that the location and ETA can be periodically captured and notified to the client

Request:
```bash
PATCH /location-updates
{
  long / lat
}
```

The person making the order will also receive location updates and ETA after these updates are sent to the backend servers:

```bash
{
  location, ETA
}
```

## HLD

### API gateway

- As the system will likely use multiple services via a microservice architecture, the API gateway will route requests to the appropriate service, handle rate limiting and authentication

### Nearby service

- Customers should be able to query availability of items by providing a long / lat, and possibly a searchQuery to the endpoints 'GET /items/:itemID/availability' or 'GET /availability'. To do this, we have two steps. First, we need to find the DCs that are close enough to deliver in 1 hour. All of our inventory lives in a DC, so we can shortcut having to check every item in our system. Once we have the list of serviceable DCs (from the DC table), we can check the inventory of them (from the Inventory and Items table) and return the union to the user. Note that the Nearby service will only be used to find nearby dcIDs using a provided long / lat.

- Thus, this Nearby service will be used to find nearby DCs from the DC table (DCs which are deliverable within an hour) using the long / lat provided by the client. We can measure the distance to the user's input with some simple math. A very basic version might use Euclidean distance while a more sophisticated example might use the Haversine formula to take into account the curvature of the Earth. We'll optimize on this approach in the DD since it might take too long to retrieve the nearby DCs and the available items in those DCs.

- The Nearby service will also use an external Travel time service (3rd party Mapping API - Google's Maps API) and Location based search to calculate the travel times from DCs (potentially including traffic) to users.

### Availability service

- Clients will directly request the endpoints 'GET /items/:itemID/availability' or 'GET /availability' to get the availability of the items in any nearby DCs. The Availability service will join the nearby dcIDs, provided by the Nearby service, with the itemIDs in the Inventory and Item tables, to return the available stock to the user.

When a user makes a request to get availability for items A, B, and C from latitude X and longitude Y (to the endpoints 'GET /items/:itemID/availability' or 'GET /availability'), here's what happens:

1. We make a request to the Availability Service with the user's location X and Y and any relevant filters.

2. The availability service fires a request to the Nearby service with the user's location X and Y.

3. The Nearby service returns us a list of DCs that can deliver to the user's location.

4. With the DCs available, the availability service will query the Inventory and Items tables with those dcIDs. We'll then sum up the results and return them to our client.

### Database

- The database will contain the Items, Inventory, DCs and Orders entities. We can most likely use a SQL DB like PostgreSQL to store these entities because it will allow us to easily perform join operations and maintain consistency during stock updates in DCs. Also, because a lot of the Inventory, DCs and Orders entries will be region based, we can shard the database by region, where users in the same region will send requests to the same shard for their region.

#### DC table

- The DC table will contain the DC entity, which includes the dcID, long / lat of the DC and possibly other DC info.

#### Inventory table

- The Inventory table will contain the inventory of the itemIDs (the Inventory entity) and their corresponding dcIDs. The Nearby service will use this table to find the inventory of items of the nearby dcIDs it gathered using the long / lat provided by the user.

#### Items table

- The Items table will contain the Items entity, which will contain additional info of the itemID which can be retrieved by the Nearby service.

<img width="750" alt="image" src="https://github.com/user-attachments/assets/6dd2b9d3-6963-480c-8469-e1e1b8f688b6" />

### Orders service

- The last thing we need to complete our requirements is for us to enable placing orders. For this, we require strong consistency to make sure two users aren't ordering the same item. To do this we need to check the inventory, record the order, and update the inventory together atomically.

- While latency is not a big concern here (our users will tolerate more latency here than they will on the reads), we definitely want to make sure we're not promising the same inventory to two users. How do we do this?

- This idea of ensuring we're not "double booking" is a common one across system design problems. To ensure we don't allow two users to order the same inventory, we need some form of locking. The idea being that we need to "lock" the inventory while we're checking it and recording the order in a such a way that only one user can hold the lock at a time. We can accomplish this by doing the following (discussed in 'Ensuring consistency for orders'):
  - Two data stores with a distributed lock
  - Singular Postgres transaction

<img width="750" alt="image" src="https://github.com/user-attachments/assets/37a274fd-0749-4304-9885-00855a8819c7" />

#### Process for ordering items

- By choosing the "great" option and leaning in to our existing Postgres database we can keep our system simple and still meet our requirements. For an order, the process looks like this:

1. The user makes a request to the Orders service to place an order for items A, B, and C.

2. The Orders service creates a singular transaction which we submit to our Postgres leader. This transaction:
    1. Checks the inventory for itemIDs A, B, and C and validates that the stock > 0.
    2. If any of the itemIDs are out of stock, the transaction fails.
    3. If all itemIDs are in stock, the transaction records the order and updates the status for inventory itemIDs A, B, and C to ORDERED OR decrements the stock field for the itemIDs in the Inventory table.
    4. A new row is created in the Orders table recording the order for A, B, and C.
    5. The transaction is committed.
3. If the transaction succeeds, we return the order to the user.

- There are some downsides to this setup. In particular, if any of the items become unavailable in the order, then the entire order fails. We'll want to return a more meaningful error message to the user in this case, but this is preferable to succeeding in an order that might not make sense (when the item is not in-stock).

- Thus far, we have three services, one for Availability requests, one for Orders, and a shared service for Nearby DCs. Both our Availability and Orders service use the Nearby service to look up DCs that are close enough to the user. The Orders service will use the Nearby service to validate if the nearest dcID is close enough to the user when creating an order. We have a singular Postgres database for inventory and orders, partitioned by region. Our Availability service reads via read replicas, our Orders service writes to the leader using atomic transactions to avoid double writes.

### Location service

(Refer to Uber's Location service)

### Location updates cache

- We'll store the location updates from the driver into this Location updates cache. Because the location updates are frequently changing and are short lived, it makes more sense to store it in a cache instead of persisting it. The entries in this cache could also be given an appropriate TTL, because location updates older than 10-20 mins won't be valuable.

### 3rd party Mapping API (Google's Maps API)

- We'll use a 3rd party mapping API such as Google's Maps API to provide the mapping and routing functionality. It will be used by the Nearby service and potentially Location service to calculate the distance and ETA between locations.

## DD

### Ensuring availability lookups incorporate traffic and drive time

So far our system is only determining nearby DCs based on a simple distance calculation. But if our DC is over a river, or a border, it may be close in miles but not close in drive time. Further, traffic might influence the travel times. Since our functional requirements mandate 1 hour of drive time, we'll need something more sophisticated. What can we do? We'll do the following (discussed in 'Ensuring availability lookups incorporate traffic and drive time'):
- Simple SQL database
- Use the travel time estimation service against all DCs
- Use the travel time estimation service against nearby DCs 

### Ensuring low latency and scalability for availability lookups

We'll need to trigger availability lookups everytime a user lands on an itemID's page to check the stock. Currently, once we have nearby DCs we use those DCs to look up availability directly from our database. This introduces a lot of load onto our database. Let's briefly detour into some estimates to figure out how much throughput we might expect.

<img width="750" alt="image" src="https://github.com/user-attachments/assets/26005f20-843b-460c-a580-41db64f1466c" />

To figure out how many queries for availability we might have, we'll back in from our orders / day requirement which we set at 10M orders per day. All-in, we might estimate that each user will look at 10 pages across search, the homepage, etc. before purchasing 1 item. In addition, maybe only 5% of these users will end up buying where the rest are just shopping:

```bash
Availability lookup queries issued: (((10M orders / day) / (100k seconds / day)) * 10) / 0.05 = 20k queries / second
```

This is a manageable number of queries per second, but for scalability and latency purposes, we'll need to think about how we can scale this to handle peaks. What do we do? We can do the following (discussed in 'Ensuring low latency and scalability for availability lookups'):
- Query inventory through cache
- Postgres read replicas and partitioning



















