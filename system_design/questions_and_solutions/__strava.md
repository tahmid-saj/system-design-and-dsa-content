# Strava (fitness tracking app)

Strava is a fitness tracking application that allows users to record and share their physical activities, primarily focusing on running and cycling, with their network. It provides detailed analytics on performance, routes, and allows social interactions among users.

While Strava supports a wide variety of activities, we'll focus on running and cycling for this question.

## Requirements

### Questions

- How many concurrent activities will the system be tracking for users?
  - 10M concurrent activities

### Functional

- Users should be able to start, pause, stop and save their runs and rides
- While running or cycling, users should be able to track / view activity data, including route, distance and time
- Users should be able to view details about their own past completed activities as well as the activities of their friends

#### Out of scope:

- Adding or deleting friends (friend management)
- Authentication and authorization
- Commenting or liking runs

### Non-functional

- Availability > consistency:
  - The system should be highly available
- Consistency of up-to-date fitness statics:
  - The app should provide the athlete with accurate and up-to-date local statistics during the run / ride
- The app should function in remote areas with low network connectivity or without network connectivity
- The system should scale to support 10M concurrent activities

## Data model / entities

- User:
  - This entity represents a person using the app, and contains profile info and settings
    - userID
    - userName

- Activity:
  - This represents an individual running or cycling activity, and including the activityType (run / ride), startTime, endTime and route data (GPS coordinates), distance and duration
    - activityID
    - activity, activityType: RUN / BIKE
    - startTime, endTime
    - routeID
    - distance
    - duration
    - activityStatus: STARTED / PAUSED / COMPLETED
    - statusUpdateEvents: JSON
   
- Route:
  - Note that this Route entity could be on the Activity entity instead, but we'll separate them out because the route can change over time
  - routeID
  - route: Route object (potentially containing a list of the route steps with GPS coordinates (long / lat) and timestamps)

- Friend:
  - This represents a connection between users for sharing activities (note: friend management is out of scope, but the concept is necessary for sharing). We'll assume the friend relationships are bi-directional, and thus we'll record the friendship using the userID and friendID fields, where friendID is a friend of userID.
  - When we add a friend relationship to this Friend entity, we'll add 2 entries to the table: one with the userID and friendID, and the other with the userID and friendID reversed. By making the first column the primary key, we can ensure querying for a userID's friendIDs is efficient.
    - userID (PK)
    - friendID

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed data quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Create activity

- This endpoint will be used to create a new activity

Request:
```bash
POST /activities
{
  activityType: RUN / RIDE
}
```

Response:
```bash
{
  Activity object
}
```

### Update activity

- This endpoint will be used to update the status of an activity

Request:
```bash
PATCH /activities/:activityID
{
  activityStatus: STARTED / PAUSED / COMPLETED
}
```

<img width="690" alt="image" src="https://github.com/user-attachments/assets/bd8b79da-42b2-46ab-8e13-954b66b8cdef" />

### Add a new location to activity's route

- When it comes to tracking activity data, we'll use the following endpoint to update the activity's route and distance.

Request:
```bash
POST /activities/:activityID/routes
{
  location: GPS coordinate (long / lat)
}
```

### Set an activity as COMPLETE

- When it comes to sharing activities with friends, we'll say that this happens automatically when an activity is saved, so instead of a endpoint for sharing, we can just update our existing endpoint that updates the activityStatus to COMPLETE.
- We'll mark an activity as COMPLETE using the same endpoint we use to update the activityStatus

Request:
```bash
PATCH /activities/:activityID
{
  activityStatus: COMPLETE
}
```

### Get list of activities for a user

- To view activities, we'll need a list view that shows either our activities or the activities of our friends. This list will just show basic information about the activity, such as the distance, duration, and date (hence the Partial<> type from TS). We'll also use offset based pagination because it's not likely that we'll get back a large number of results.
- This initial GET request returns a list of activities with just the basic information and the activityID for each activity. When the user clicks on an activity, we can make a second, more detailed GET request using the activityID to get the full activity details.

Request:
```bash
GET /activities/mode={ USER / FRIENDS }&offset&limit -> Partial<Activity>[]
```

<img width="750" alt="image" src="https://github.com/user-attachments/assets/5b150048-0b4f-45af-b5f9-8640909b5474" />

### Get an activity by activityID

- When we click on an activity, we'll want to see more details about like the maps with the route and any additional metrics or details (that are out of scope for this question).

Request:
```bash
GET /activities/:activityID -> Activity
```

## HLD

<img width="750" alt="image" src="https://github.com/user-attachments/assets/fd185e9c-3f76-493b-a077-c8f002b3f642" />

### Client

- The client app will allow users to interact with the system through a mobile app. The client will likely also have GPS capabilities built-in the smartphone. The app will make use of these built-in GPS capabilities.

#### Client-side GPS coordinate updates

- When the activity is in progress we need to both update the status and display the activity data to the user.

- The first, and most important, part of this is to accurately track the distance and route of the activity. We can do this by recording the user's GPS coordinates at a constant interval. We make the assumption that they are using a modern smartphone with GPS capabilities, so we can use the GPS coordinates to calculate the distance using the Haversine formula.

Note: The Haversine formula calculates the great-circle distance between two points on a sphere (like Earth) given their longitudes and latitudes, using the haversine function, which is sin²(θ/2).

Here is how the GPS coordinate updates would work:

1. The client app will record the user's GPS coordinates at a constant interval, let's say 2 seconds for a BIKE ride and 5 seconds for a RUN. To do this, we'll utilize the built-in location services provided by both iOS and Android:
    - For iOS: We'll use the **Core Location framework**, specifically the **CLLocationManager** class. We can set up location updates using the frameworks's **startUpdatingLocation()** method and implement the **locationManager(_:didUpdateLocations:)** delegate method on the mobile app to receive location updates via the method **startUpdatingLocation()**.
    - For Android: We'll use the **Google Location Services API**, part of Google Play Services. We can use the **FusedLocationProviderClient** class and call the **requestLocationUpdates()** method to receive periodic location updates in the mobile app.

2. The client app will then send these new GPS coordinates to our 'POST /activities/:activityID/routes' endpoint.

3. The Activity service will update the Route table in the database for this activity with the new GPS coordinates and the time the coordinates were recorded. Note that the server-side will always be responsible for creating timestamps (unless the client-side needs to be the one to create timestamps).

4. The Activity service will also update the distance field by calculating the distance between the new GPS coordinate and the previous one using the Haversine formula.

<img width="750" alt="image" src="https://github.com/user-attachments/assets/4c32012e-5252-48eb-afde-7b34e4517431" />

Note: Astute readers are likely already yelling at their screen as they've realized that we don't need to send these updates to the server, instead handling the logic locally on the client. You're right. We'll get into this in the DD. The reality is most of the time I ask this question, candidates overlook this optimization and we get to it later in the interview.

### Activity service

- We need to design a system that correctly handles both our create activity endpoint and our update activity state endpoint. The Activity service will allow users to create and update their activities, which include starting, pausing, stoping and saving their runs and rides. 

A user is going to start by opening the app and clicking the "Start Activity" button:

1. The client app will make a POST request to '/activities' to create a new activity, specifying whether it's a RUN or a BIKE ride.
2. The Activity service will create the activity in the database and return the activity object to the client.
3. If the user opts to PAUSE or resume their activity, they'll make a PATCH request to '/activities/:activityId' with the updated state and the Activity service will update the activity in the database accordingly.
4. When the activity is over, the user will click the "Save Activity" button. This will trigger a PATCH request to '/activities/:activityId' with the state set to COMPLETE.

#### Handling activity time elapsed when activityStatus = PAUSE

- One interesting part of the design is how to handle the activity time when a user pauses their activity. A naive approach to handling the amount of time elapsed in an activity would be to manage time based on a startTime and then, when an activity is ended, calculate the elapsed time by subtracting the startTime from the current time.

- However, this approach would be problematic if a user pauses their activity. The startTime would remain unchanged and the elapsed time would continue to increment, which would be inaccurate.

- One common way we could handle this, we can maintain time via a log of status update and timestamp pairs. The Activity service can then update the statusUpdateEvents (JSON field) in the Activity table on each activityStatus change. For example, we could have the following log:

```bash
[
    { status: "STARTED", timestamp: "2021-01-01T00:00:00Z" },
    { status: "PAUSED", timestamp: "2021-01-01T00:10:00Z" },
    { status: "RESUMED", timestamp: "2021-01-01T00:15:00Z" },
    { status: "STOPPED", timestamp: "2021-01-01T00:20:00Z" }
]
```

- When the user clicks "Stop Activity", we can calculate the elapsed time by summing the durations between each pair of timestamps, excluding pauses. In the example above, the elapsed time would be 15 minutes (10 minutes + 5 minutes).

- This may seem like overkill for our simple requirement, but it would allow for natural expansions into a feature that shows athletes when they were paused and for how long, as well as a breakdown of "total time" vs "active time."

### Database

- The database will store info about activities, including route, distance, time and friend management data.
- What database should we choose? It doesn't really matter - we can choose either DynamoDB or PostgreSQL, and implement basic indexing via GSIs / LSIs on the tables to help with the queries on activityStatus, startTime / endTime, activityType, etc. This is a large but totally manageable amount of data; there is no crazy read or write throughput, and data is relational but not heavily so. Realistically, all popular major database technologies would work great here.
- For the Activity Service, given both read and write throughput should be pretty low (mainly because we can store route and activity updates locally in the client then send updates every now and then, rather than periodically sending updates to the backend servers every second), there is no reason to break this into microservices that scale independently. Instead, when we run into issues with memory, CPU, or network limitation we can just scale the Activity service horizontally.

#### Users should be able to view COMPLETED activities and activities from their friends

- Once activities are COMPLETED, we should have them already saved in the database and all we needed to do was update their status to COMPLETEED using the same endpoint we used to update the activityStatus.

- When it comes to viewing activities, we only need to query the DB for the activities with this COMPLETED activityStatus, while also filtering on the mode query param to either show the user's activities or their friends' activities which can be done with a simple WHERE clause:

```sql
SELECT * FROM activities 
WHERE state = "COMPLETED"
AND userID === :userID -- if mode is USER
AND userID IN (SELECT friendID FROM friends WHERE userID = :userID) -- if mode is FRIENDS
LIMIT :pageSize OFFSET (:page - 1) * :pageSize
```

The full flow of a user getting a list of activities (activities that they completed OR their friends completed), and then viewing an activity from the list is thus:

1. User navigates to the activities list page on the app.
2. Client makes a GET request to '/activities?mode={ USER / FRIENDS }&offset&limit' to get the list of activities.
3. The list of activities is rendered in the UI and the user clicks on an activity to view details.
4. Client makes a GET request to '/activities/:activityID' to get the full activity details to render on a new details page.

Note: For showing the map, we can use a combination of the route data and the Google Maps API. We can pass the array of coordinates to the Google Maps API and it will draw a line connecting all the points.

## DD

### Tracking activities when users are offline (in low network connectivity areas)

Many athletes will opt to workout in remote areas with no network connectivity, but they still want to be able to track their activities. This brings us to an impactful realization that re-shapes the entire system.

The key insight is that, so long as we don't support realtime-sharing of activities, we can record activity data locally, directly on the clients device and only sync activity data back to the server when the activity completes and/or the user is back online.

Importantly, this actually solves several problems for us:
- We can track activities without worrying about network reliability on the client side.
- Even when the client has a fine network connection, we save network bandwidth by avoiding pinging location updates to the server every few seconds (instead, only sending the updates when the activityStatus is COMPLETED or on PAUSE).
- Showing accurate and up-to-date activity data to the user is easy as it all happens only when the user chooses to be back online. 

<img width="750" alt="image" src="https://github.com/user-attachments/assets/c61883e6-929e-4991-ab3e-369b201fd159" />

How do we track the activity and route data when users are offline?

1. Just like in our high-level design, we use on-device location services to record the user's GPS coordinates at a constant interval.
2. We record this event data locally on the device in an in-memory buffer (e.g., an array of GPS coordinate and timestamp pairs).
3. To prevent data loss in case of device shutdown or battery depletion, we'll periodically persist this buffer to the device's local storage every ~10 seconds:
    - For iOS: We can use Core Data for larger, structured datasets, or UserDefaults for smaller amounts of simple key-value data.
    - For Android: We can use Room database for larger, structured datasets, or SharedPreferences for smaller amounts of simple key-value data.
4. When the app is reopened or the activity is resumed, we first check local storage for any saved data and load it into our in-memory buffer before continuing to record new data.
5. Once the activity is complete and the device is online, we send all the accumulated data to our server in a single request. For very long activities, we might need to implement a chunking strategy to handle large amounts of data efficiently.
6. We can also implement a background sync mechanism that attempts to upload data periodically when a connection becomes available, even if the activity isn't complete yet. This balances efficiency with data durability.
7. Upon confirmation that the data was saved to our remote database, we can delete the local buffer and are ready to go again.

Thus, the client will now have both the GPS update capabilities most modern mobiles have, an in-memory activity buffer (created from scratch using Java / Kotlin, or using the ByteBuffer class Java provides to work with in-memory buffers), and also a persistent storage.

This approach ensures that even if the device unexpectedly shuts down, we'll only lose a maximum of 10 seconds of activity data (or whatever interval we choose for our periodic saves to the persistent storage). However, it's important to balance the frequency of GPS tracking and data persistence with battery life considerations.

Note: 

Core Data is an object graph and persistence framework provided by Apple in the macOS and iOS operating systems. Use Core Data to save your application’s permanent data for offline use, to cache temporary data, and to add undo functionality to your app on a single device. To sync data across multiple devices in a single iCloud account, Core Data automatically mirrors your schema to a CloudKit container. Through Core Data’s Data Model editor, you define your data’s types and relationships, and generate respective class definitions. Core Data can then manage object instances at runtime to provide the following features.

In Android development, Room is a persistence library provided by the Android Jetpack framework. It is used to create and manage an abstraction(Data hiding layer) over SQLite, which is a widely used relational database engine.

<img width="800" alt="image" src="https://github.com/user-attachments/assets/45a25a16-320e-4ef9-99d6-a30df813c27e" />

### Scaling to support 10M concurrent activities

Now that we track activities locally, scaling our backend became pretty easy! We cut down on the number of requests our backend services receive by a factor of 100x since we only send data once a RUN / RIDE completes now. Our production engineering team is going to be thrilled, so too the finance team.

We'll now focus on scaling our system to support 10M concurrent activities and 100M DAU. With ~100M DAU doing an activity each day we add up to ~100M new activities each day. Over a year, that's ~36500M activities or ~36.5B activities. To estimate the amount of storage we need for each activity, we can break it down as follows:

- Basic metadata like activityStatus, userID, startTime / endTime, etc should be pretty cheap. Let's say ~100 bytes per activity.
- The route is the most expensive part. If the average activity is 30 minutes and we take GPS coordinates, on average, every ~3 seconds, then we'll have about 600 points per activity. Each route row needs a latitude and longitude field as well as a timestamp. This is an additional (8 bytes + 8 bytes + 8 bytes) * 600 = ~15KB. 15KB * 36.5B = 547.5TB of data each year.

This is a good amount of data, but it's far from unmanageable. Here are some things we could do to handle this:

- We can shard our database to split the data across multiple database instances. We can shard by the activityID's startTime since the majority of our queries will want to see recent activities. Also, if we have different entries belonging to the same activityID in different shards, then a query to retrieve all those activityID entries will need to fetch the data from multiple shards, instead of a single shard if we shard by the startTime.

- We could introduce data tiering. The chances that someone wants to view a run from several years ago are pretty low. To reduce storage costs, we could move older data to cheaper storage tiers:
  - Hot data (recent activities) stays in fast, expensive storage
  - Warm data (3-12 months old) moves to slower, cheaper storage
  - Cold data (>1 year old) moves to archival storage like S3

- We can introduce caching if needed using a Recent activity cache. If we find that we are frequently querying the same activities, we can introduce caching to reduce the read load on our database. This would not be a priority for me, as read throughput should be pretty low. but its the first thing we would do if load times become unacceptable.

### Supporting real-time sharing of activities with friends

One common follow up question in this interview is, "what happens when you want to allow friends to follow along with activities in real-times". In this case, friends don't just see activity statistics once completed, but they can watch you mid run/bike ride -- seeing your stats and routes update in near real-time. This moves the design closer to other popular realtime systems like the SDI 'FB Live Comments' or 'Chat app like Whatsapp'.

To enable real-time sharing with friends, we'll reintroduce periodic server updates during activities. While maintaining local device logic for user-facing data, we'll send location updates to the server every 5 seconds. As the server gets these updates, they'll be persisted in the database and broadcast to all of the user's friends.

Now, I know what you're likely thinking, "Websockets!" This isn't wrong per se, you could absolutely implement this with websockets or SSE, but I'd strongly argue it's over-engineering the problem. While you could introduce a real-time tracking service which connects to friends clients via Websocket or SSE and use pub-sub to broadcast updates to friends, this introduces a lot of unecessary complexity.

Instead, there are two key insights that suggest a simpler, polling mechanism will be more effective:

1. **Updates are predictable**: Unlike with Messenger or Live Comments, we know that the next update should come in the next 2-5 seconds. This predictability allows for efficient polling intervals.

2. **Real-time precision isn't critical**: Friends don't need to see up-to-the-second information. A slight delay of a few seconds is acceptable and won't significantly impact the user experience.

Using this logic, we can implement a simple polling mechanism where friends' clients periodically request updates at the same interval that the athlete's device is sending updates to the server (offset by a few seconds to account for latency).

We can further enhance the user experience by implementing a smart buffering system. This approach involves intentionally lagging the displayed location data by one or two update intervals (e.g., 5-10 seconds). By buffering the data, we can create a smoother, more continuous animation of the athlete's movement. This eliminates the jarring effect of sudden position changes that can occur with real-time updates. To friends viewing the activity, the athlete will appear to be in constant motion, creating a more engaging, "live-stream-like" experience. While this approach sacrifices absolute real-time accuracy, it provides a significantly improved visual experience that better matches users' expectations of how a live tracking feature should look and feel. The intentional lag also helps compensate for any network latency, ensuring a more consistent experience across different network conditions.

### Incorporating a real-time leaderboard of top athletes

Another natural extension to this problem could be to expose a leader board of the top athletes by activityType and distance. We could filter by country, region, city, etc. Here are some approaches we could take (discussed in 'Incorporating a real-time leaderboard of top athletes'):
- Naive approach
- Periodic aggregation
- Real-time leaderboard with Redis













