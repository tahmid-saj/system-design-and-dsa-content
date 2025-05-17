# Event scheduling system like Google Calendar

Google Calendar is like a special calendar that we can use on our computer or phone. We can use it to remember important things, like birthdays, appointments, and events. We can also set reminders to help us remember when something is coming up soon. We can also share our calendars with our family or friends. It’s like having our own special schedule that helps us keep track of everything that we need to do.

With Google Calendar, we can quickly schedule meetings and events and get reminders about upcoming activities, so we always know what’s next.

## Requirements

### Questions

- How many DAU can we expect? And on average how many events will a user book per day?
  - Assume the DAU is 100M, and on average a user will book 3 events per day

### Functional

- Users can lookup all events in the calendar - they should be able to lookup events in a monthly, weekly or daily format
- Users can book an event (either with multiple people or a single user)
- Users can check availability of users when booking an event
- Users can invite users to the event (either one or multiple users)

- Request RSVP: When users initiate an event for other users, they can request RSVP so that they can confirm if the other users are attending or not
- Users will also get notifications before the time for an event
- Users should also be able to make changes to an existing event (either updating it or cancelling it)

### Non-functional

- Availability > consistency:
  - Users should be able to use Google Calendar whenever they need it
- Eventual consistency of event updates:
  - Updates make to events might not show up for everyone right away, but eventually the changes will be applied to everyone's calendar shortly
- Low latency for viewing availability:
  - When users are scheduling an event, they should be able to view other users' availability with low latency

## Data model / entities

- Users:
  - userID
  - userName
  - email
 
- Events:
  - This entity will contain the events (and their details) which are booked by users
    - eventID (PK)
    - userID
    - startTime, endTime
    - location
    - metadata: { createdAt }

- Event users:
  - This entity will contain events and their invited users (including the host user which will have a default rsvpStatus of ACCEPTED)
    - eventID (CPK)
    - userID (CPK)
    - rsvpStatus: PENDING / ACCEPTED / DECLINED

## API design

- Note that we’ll use userID if the user is authenticated. The userID could be placed in a session token or JWT in the Authentication header as such:
  - Authentication: Bearer

- The below caching header could also be applied to fetch frequently accessed entries quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
  - Cache-Control: no-cache max-age Private/Public

### View all events in calendar (default view is weekly)

Request:
```bash
GET /events?view={ WEEKLY }&date
```

Response:
```bash
{
  events: [ { eventID, userID, startTime, endTime, location } ]
}
```

### Book an event

- Users can book an event by providing the eventName, startTime / endTime, location, invitedUsers, etc. Once the user books the event, the backend servers will also send out invitations to those attendees using their email addresses - the users will then be requested to response (RSVP)

Request:
```bash
POST /events
{
  startTime, endTime,
  location,
  invitedUserIDs
}
```

### Check availability of users when booking an event

- When the user is scheduling an event, they can check if another userID is available at a specific startTime and endTime. Note that we don't want to provide userIDs in the query parameters at all, thus it's much more safe to send a PATCH request (even if no resource is created) to check the userID's availability. We also would need to use a valid SSL certificate within the frontend to encrypt the connection with the backend servers, thus sending userIDs within the request body would have less risk.

Request:
```bash
PATCH /events/availability -> true / false
{
  userID,
  startTime, endTime
}
```

### Invite users to event

- After an event is booked, the host user can also invite non-invited users to the event using this endpoint where they provide their email addresses - the users will then be requested to response (RSVP). Note that because we're creating a new entry in the Event users table using this endpoint, we'll use POST here

Request:
```bash
POST /events/:eventID/invitations
{
  userIDs
}
```

### Users send RSVP response

- After a user books an event, the backend servers can request the invited users to respond to the invitation. The invited users will receive the invitation in their emails and will then have the option to ACCEPT / DECLINE the invitation using this endpoint, where their responses will be stored in the storage in the Event users entity

Request:
```bash
PATCH /events/:eventID/invitations
{
  response: ACCEPT / DECLINE
}
```

### Update event

- Users can also make updates to an existing event, and this update will be sent as an email to all invited users and will also be synchronized across all their devices

Request:
```bash
PUT /events/:eventID
{
  startTime, endTime,
  location,
  invitedUserIDs
}
```

### Cancel event

- Users can also delete an existing event, and an email notification will be sent to all invited users

```bash
DELETE /events/:eventID
```

## HLD

### API gateway

- As the system will likely use multiple services via a microservice architecture, the API gateway will route requests to the appropriate service, handle rate limiting and authentication

### Events search service

- Users will use the Events search service for viewing events in their calendar via the endpoint 'GET /events', which will retrieve the events from the DB. This service will be a read heavy service, thus it makes sense to separate it from the other Bookings and invitations service which is dedicated to booking and invitations of events.
- Users will very frequently open their calendars only to view events for the current week, day, etc, and will infrequently book an event. Thus, it also makes sense to separate this read heavy functionality from the write functionality, where they can be scaled differently.

### Bookings and invitations service

- The Bookings and invitations service will handle the all other endpoints for booking and invitations of events, which don't include directly viewing events in a user's calendar.

When users book events, the process will look as follows:

1. The API gateway will first request the endpoint 'PATCH /events/availability' in the Bookings and invitations service to check if the invited user is available at the startTime / endTime planned for the event.
2. The Bookings and invitations service will then look into the Event users table to check if the invited userID is available for the planned startTime / endTime, and then let the client know
3. The client can then request the endpoint 'POST /events' in the Bookings and invitations service to book the event with the invited userIDs.
4. The Bookings and invitations service will then create an entry in the Events table for the booked event
5. During this book request, the API gateway will also request the endpoint 'POST /events/:eventID/invitations' to send email invitations to invited userIDs
6. The Bookings and invitations service will then create entries in the Event users table for the invited userIDs

<br/>

When users want to send an RSVP response, the process will look as follows:

1. The client will send a request to the endpoint 'PATCH /events/:eventID/invitations' in the Bookings and invitations service to confirm their attendance
2. The Bookings and invitations service will then update the rsvpStatus for the userID sending the RSVP

### Database

- The DB will contain the Events and Event users entities. The entites are relational in nature, mainly via the eventID and userID fields. For our writes, we can likely expect 100M users * 3 new booked events = 300M daily booked events / 100k seconds (86400 seconds in a day rounded up) = 3k writes per second. Modern SQL DBs like PostgreSQL can definitely handle this write load, however for the Event users table, we could expect that we'll need multiple new entries for all the invited users for a new booked event - thus, we might need 3k * 5 = 15k writes per second on the Event users table to add new invited users. This is still a write load PostgreSQL (specifically a AWS Aurora or RDS instance) can handle with indexing and partitioning.

- We can likely partition the Events table on the userID, because we'll be frequently looking for calendar events for a specific userID from a single partition. We can also partition the Event users table on the eventID, because we'll be frequently looking for invited userIDs for a specific eventID from a single partition.

- We could use a cache to provide low latency reads on calendar events from the Events table, but there are multiple things to consider when implementing this cache as explained in the DD. Also, if we have 100M DAU, and they'll likely view their calendars 10 times a day, then we'll have 1B reads per day / 100k seconds (86400 seconds in a day rounded up) = 10k reads per second on the Events table. This is still a read load a PostgreSQL based AWS Aurora or RDS instance can handle with indexing and partitioning.

### Notification service

- The Notification service will send optional email / push notifications to invited users when new events are booked. The Bookings and invitations service can asynchronously request the Notification service to send an email / push notification to the userID's email address or phone number

## DD

### Caching the calendar events

Users will very frequently look at their calendar events multiple times a day, thus to support low latency reads of calendar events, we can cache the frequently accessed calendar views (monthly, weekly, daily) for users. This can be a read-through cache, which will populate popular calendar views for users. We can likely use Redis sorted sets for caching calendar events using the startTime of the eventID. Thus, a userID can likely have at maximum 3 different keys for sorted sets containing different views (monthly, weekly, daily), where the member will be only the necessary details of the event (eventID, startTime, endTime, etc), and the score will be event's startTime.

However, when using a cache to improve read latencies, there's still some things to consider:

#### Caching calendar events to handle reads on "user's availability" endpoint 'PATCH /events/availability' faster

Using a cache to store the Events table data will allow the Bookings and invitations service to handle reads on the user's availability faster. This will help if multiple users are being invited to an event, and the host would need to check the availability for all of those users. However, data on the cache can become stale quickly if updates for new booked events are not also pushed into the cache. We'll discuss this next:

#### Data inconsistency between the cache and database

When a host books a new event (or updated an event), to ensure the cache does not become stale, the Bookings and invitations service will also need to update the cache with new booked events or updated events. This way, the data between the cache and the DB will rarely be inconsistent. Because the system will likely have more reads than writes on calendar events (probably a ratio of 5-10:1), we can benefit from this type of strategy. Writes may take a bit longer since writes for events now have to update both the cache and DB, however, reads will be faster (especially for viewing calendar events and users' availability).

In terms of memory, if there's 100M DAU, and each will book around 3 events per day - we can assume the cache will have an appropriate TTL of a few hours for those 100M users in a single day:
- 100M * 3 = 300M users * 500 bytes for event data = 150 GB for a single day of events
- 150 GB * 7 days = 1050 GB for a week of events

There, from our estimations, caching events at a daily and weekly level is possible with modern day cache servers (via AWS Elasticache which can cache up to 1 TB in a single server). However, we may want to only cache events for frequently logged in users (determined by our Authentication service or Bookings and invitations service).

We could also cache the monthly view, however, because users might not view their monthly schedule as often, we could simplify our design, where the Bookings and invitations service will only cache the current week (and perhaps next week's events), and use the DB to retrieve the other weeks' events to return a monthly view to the user.

### Recurring events

To support recurring events, we can use separate the recurring event instances from the actual recurring event itself. This way, we'll use the Events table to store the event instances, and store the recurring event details itself in a Recurring events table. This will allow users to modify individual event instances without impacting the entire series of events. The data model for the Recurring events table might look as follows:

- Recurring events:
  - recurringEventID
  - userID
  - startTime, endTime
  - location
  - frequency: enums indicating the frequency of the recurring event, such as MON_WED_PER_WEEK

Whenever a new recurring event entry is created in this Recurring events table via the Bookings and invitations service, multiple event instance entries between the startTime and endTime of the recurring event could also be added to the Events table. As those event instances are added to the Events table, the invited users will also be populated into the Event users table for those event instances. 

Because calculating event insrances / occurrnces of recurring events for multiple users / invited users can be CPU intensive, this process can be offloaded to background jobs via a queue like SQS, which ensures exactly once message delivery. Worker containers could be set up via AWS ECS specifically to handle these types of recurring events with multiple occurrences and entries which need to be added to the DB. The Worker contains will then pull the booked recurring events from SQS, then create the entries for the event occurrences and invited users in the Events and Event users tables respectively.

### Device synchronization

- To ensure device synchronization, where if a user is invited to a new booked event, it should also be registered on their mobile device as well - we’ll a Devices table which contains deviceIDs for each userID. We’ll use the deviceID to differentiate between devices belonging to a user.

- To ensure device synchronization, where calendar invitations on the laptop should be immediately registered on mobile - when a userID is invited to an event, the Bookings and invitations service will still store a single record for the userID in the Event users table, but it will also send notifications for the deviceIDs belonging to the userID.

### Email and push notifications

The Notification service will be similar to the SDI 'Notification service'. It will use third party notification services such as APNS (apple push notification service), FCM (GCP Firebase Cloud Messaging), SMS, Email services (Mailchimp and AWS SES) for delivering notification payloads to deviceIDs belonging to a userID

### Microservice vs monolithic

When using a microservice architecture, a service usually has it’s own database it manages. In a monolithic architecture, multiple services could manage the same database. This is shown in ‘Microservice vs monolithic’ (note that this diagram is from the SDI 'Hotel reservation system').

Our design has a hybrid approach, where a single service could still access databases or tables other services could manage or access. For example, the Bookings and invitations service accesses both the Events and Event users tables. We have a hybrid approach, because a pure microservice approach can have consistency issues when managing transactions. The Bookings and invitations service accesses multiple tables / databases, and if a transaction fails, then it will need to roll back the changes in those respective databases / tables.

If we used a pure microservice approach, the changes will need to be rolled back in all the databases BY THE SERVICES which manage them instead of by only the Booking service. We cannot only just use a single transaction (within the Bookings and invitations service) in a pure microservice approach, we’ll need multiple transactions happening within those other services as shown in ‘Microservices transactions’ (note that this diagram is from the SDI 'Hotel reservation system'). This causes an overhead and may lead to inconsistency issues.

Microservice vs monolithic:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/3ade0c8e-9ae6-48a2-9c86-97686ec1ccd1" />

<br/>
<br/>

Microservices transaction:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/2608a3b6-d161-4205-86ea-5d015a3b5f43" />

### Scaling the API to support large number of users

To scale the API for high concurrency for large events, we’ll use a combination of load balancing, horizontal scaling and caching as shown in ‘Scaling API to support high concurrency’.

Scaling API to support high concurrency - taken from the SDI 'Ticketmaster':

<img width="700" alt="image" src="https://github.com/user-attachments/assets/a187b31b-c583-4929-9894-25bdf597455a" />









