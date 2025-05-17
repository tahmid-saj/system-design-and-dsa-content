# Notification system

## Requirements

### Questions

- What types of notifications does the system support?
  - Push notifications, SMS and email

- Is it a real-time system?
  - It is a soft-real time, we want users to receive 			notifications as soon as possible

- What are the supported devices?
  - iOS, android and laptop / desktop

- What triggers notifications?
  - Notifications can be triggered by client applications or on		the server side by a notification provider

- How many notifications are sent out each day?
  - 10 million push notifications, 1 million SMS, 5 million		emails

### Functional

- The system should support push, SMS, email notifications
- The system is a soft real-time system
- The supported devices include iOS, android and laptop / desktop

### Non-functional

- Low latency:
  - Low latency in notification delivery (<1 s)
- Throughput:
  - Multiple notifications will likely be sent by the notification providers to our notification system

## Notifications 101

The three types of notification formats are:
- Mobile push notifications
- SMS messages
- Emails

<br/>

Below are info on different types of notifications:

### iOS push notifications

We typically have these main parts in iOS push notifications:

#### Provider

- Builds and sends notification requests to Apple Push Notification Service (APNS). For constructing a push	notification, the provider uses the device token (unique ID for the device) and the payload (JSON format of	the notification details). An example of the payload is shown below. We usually need these 3 components to send an iOS push notification: provider, device token, and payload.

```bash
{
   "aps":{
      "alert":{
         "title":"Game Request",
         "body":"Bob wants to play chess",
         "action-loc-key":"PLAY"
      },
      "badge":5
   }
}
```

#### APNS

- This is a remote service provided by Apple to route push notifications to iOS devices

#### iOS device

- It is the end client receiving the push notification

iOS push notification:

<img width="450" alt="image" src="https://github.com/user-attachments/assets/905a9726-cc2f-472c-8155-601833b28be2" />

<br/>

### Android push notifications

- Android adopts a similar notification flow to iOS. Instead of using APNs, Firebase Cloud Messaging (FCM) is commonly used to send push notifications to android devices.

Android push notification:

<img width="450" alt="image" src="https://github.com/user-attachments/assets/e4ac5241-2f8d-4a21-a8f9-977025c99865" />

<br/>

### SMS messages

- For SMS messages, a third party SMS service like Twilio is used instead of APNS or FCM

SMS messages:

<img width="450" alt="image" src="https://github.com/user-attachments/assets/c8575f5a-a1d6-471d-a107-4f047ec6a538" />

<br/>

### Emails

- Although companies can set up their own email servers, many of them opt for commercial email services. Sendgrid and Mailchimp are among the most popular email services, which offer a better delivery rate and data analytics. For emails, email services like Mailchimp or SES are used instead of APNS

Email notifications:

<img width="450" alt="image" src="https://github.com/user-attachments/assets/e9f2a109-420f-4902-bfd5-23d007fc0769" />

The above services used as substitute for APNS are all third party services

### Notification sending / receiving flow

The very high level design of the system is shown under 'Initial high level design'. The design has the below components:

<br/>

Initial high level design:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/7ba68b6d-e3f1-4b5f-a6e5-498532e5178a" />

#### Service 1 to N

- A service can be a microservice, a cron job or a distributed system that triggers notification sending events. For example, a shipment service can remind customers that their package will be delivered tomorrow

#### Notification system

- The notification system is the centerpiece of sending / receiving notifications. The notification system itself will be operated by us, and will communicate with other external components of the design. The notification system will provide APIs for "Service 1 to N" (which will be the providers in our design), and builds notification content for 3rd party services to use.

#### 3rd party services

- 3rd party services are responsible for delivering notifications to users. Our Notification system component will communicate frequently with these 3rd party services, and thus we need to have the Notification system be compatible with these 3rd party services.

#### iOS, Android, SMS, email notification on devices

- Users will receive iOS, Android, SMS, email notifications on their devices. 

## Data model / entities

- Users:
  - We'll use the phoneNumber to send SMS messages as notifications, and use the userEmail to send email based notifications
    - userID
    - userName
    - userEmail
    - phoneNumber
    - userSettings

- Devices:
  - This entity will contain all the devices belonging to a specific userID. We'll also store the deviceToken to send both iOS and Android push notifications to devices.
  - Device tokens — sometimes known as push tokens in other products or push services—are unique, anonymous identifiers for the app-device combination that are issued by push notification services: they're basically device addresses, so you can send push notifications to your app's users.

    - deviceID
    - deviceToken
    - userID

- Notification:
  - This entity will store all the notifications which were sent to our API servers, from the providers
    - notificationID
    - userID
    - notificationTypeID
    - subject, content
    - notificationStatus: PENDING / SENT

- Notification template:
  - The notification template can also optionally be stored in the database, and will be used by the system's components to construct the notification

    - notificationTypeID
    - template

## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed messages quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

### Send notification

- This endpoint is used by the providers to send a notification

Request:
```bash
POST /notifications
{	
	from: { userEmail / phoneNumber / deviceToken }
	to: { userEmail / phoneNumber / deviceToken }
	subject, content
}
```

## HLD

### Providers

- The providers establishes the notification. For example a billing service sends emails to customers about their billing info. These providers will be different services where the notification originates from - and will use the API servers to send the notification.

### API servers

- To first send notifications, we need to gather mobile device tokens, phone numbers or email addresses - when the user installs the app or signs up for the first time. We’ll use the API servers to gather device tokens, phone numbers, email addresses and user profile info to store in the Database. The API servers will also perform basic validations to verify emails, phone numbers, etc of users when gathering info.

- The API servers will provide an endpoint for the Providers ("Service 1 to N" from Notifications 101) to send notifications, and also authenticates the providers to ensure only verified providers can send notifications using the API servers

- The API servers will use the user / device token / user's notification settings data from the Database, and push the provider’s notification		request to the message queues to send notifications in parallel. It will also create a new entry for the notification in the Notifications table of the database in-case users want to go back and view their notifications.

#### API servers pushing notification to message queues

- Processing and sending notifications, as well as gathering contact info all on the API servers may not be the best. Notifications will be created and sent much more frequently, and we can process it in parallel, since notification events are independent of one another.
- Therefore, the API servers can push notification requests to message queues, where individual workers (processes or workers running on servers) will pull the message from the queue and construct the notification using a notification template, to send the notification to the 3rd party services. Adding a queue also allows us to perform retries in sending notifications and to buffer between the API servers and 3rd party services.

### Database / cache

- The database will store the user profile, device and notification data. When the user enters their user profile and contact info, the data will be stored in this database. When a notification is sent by the API servers, we'll also store the notification entry in this database.

#### Notification template blob store

- Also, the database could store notification templates, such that the workers will use the notification template when constructing the notification before sending it to the 3rd party services - instead of building the notification from scratch. Because the notification template will likely contain mostly textual, HTML, and media based content, we can store it in S3 which will be optimized in storing binary based content which follows to actual structure.

- Because the data is relatively simple, and it does have some relationships, we could use either SQL or NoSQL. SQL or NoSQL DBs with appropriate indexing and partitioning should perform relatively equally. However, since the data does contain some relationships, we'll use a SQL DB like PostgreSQL.

- A notification template can be used to maintain a consistent format and also save time. An entry is shown below:

```bash
BODY:
You dreamed of it. We dared it. [ITEM NAME] is back — only until [DATE].

CTA:
Order Now. Or, Save My [ITEM NAME]
```

#### Cache

- We'll also cache the frequently accessed user, device data, and notification templates, which should be static and simple to cache. Either Memcached or Redis may be used here, however we could benefit from Memcached's lower latencies via multi-threading.

### Message queues

- The message queues decouple the API servers from the workers and third party notification services. When high volumes of notifications are sent out, we can process the notifications in parallel using both the message	queues and workers. Message queues also ensure that fewer notification requests from the providers are dropped, since they could instead be added to the message queue.

- A queue service such as SQS could be used for asynchronously sending notifications to workers. SQS also has a retry mechanism for failures, and exponential backoff via it's visibility timeout which will be useful here.

- The downside to using message queues is that it will add operational overhead to manage the partitioning and offsets	of the queues, however SQS will take care of the major partitioning, chunking, etc, whereas AZ or region-based replication may need to be configured on AWS. 

- An alternative is for the API servers to send the notification requests directly to the third party services, 	however, depending on the API servers' capabilities, this might overwhelm the API servers, and also potentially block other notifications which need to be sent.

### Workers

- The workers will pull the notification from the message queues and send it to the corresponding 3rd party notification	services. The workers will likely run as containers on an IO optimized EC2 instance, or via ECS. The workers will likely also use a notification template from the database / cache to construct the notification.

### 3rd party notification services

- Third party notification services such as APNS (apple push notification service), FCM (GCP Firebase Cloud Messaging),	SMS, Email services (Mailchimp and AWS SES) are responsible for delivering notification payloads to devices

<img width="852" alt="image" src="https://github.com/user-attachments/assets/f3d6a53d-e1bb-47b1-89c0-0488b79228a5" />

## DD

Below are some deep dives and improvements of the system:

### Notifications stored in the database to ensure retries and deduplication

- Notifications can usually be delayed or re-tried but never lost. To ensure this, the API servers can store the notifications being sent on the database, such that the workers can re-enqueue the notification back into the queue if there is an error and perform a re-try using the saved notification data.
- Because we're re-trying to send the notification, SQS provides a visibility timeout which ensures that messages are delivered exactly-once, so that no duplicate notifications are being received by the 3rd party services. We could also perform the deduplication by using the stored notification in the database, and check if the notificationStatus field has changed to SENT. If the notificationStatus is already SENT, then the worker won't send that notification.
- If a third party service also fails to send the notification, it could also be configured to retry and push	the notification back to the message queue with an appropriate visibility timeout

### Notification settings

- Notification settings can be stored in the database under the userSettings field in the Users entity, to ensure users can opt out of notifications. The API servers will first check the userSettings field to verify if the user has opted out of receiving a specific notificationType, before the API servers send the notifications.
- The userSettings field could contains info such as notificationType (push, SMS, email) and optIn (if user wants to opt in to receiving notifications)

### Scheduled notifications

- For scheduled notifications, the providers will send the notifications when the event or	task is coming up. The design for scheduled notifications is similar to the SDI 'Distributed job scheduler'

Additional deep dives:

### Monitoring service

- A key metric to monitor is the total number of queued notifications. If the number is large, the notification events are not processed fast enough by workers. To avoid delay in the notification delivery, more workers may be needed. The monitoring service can be used to allocate more workers to handle notification delivery.

- Notification metrics, such as open rate, click rate, and engagement are important in understanding customer behaviors. The monitoring service implements events tracking. Integration between the notification system and the monitoring service is usually required.


## Wrap up

- Geo-replication
- Sharding / replication / partitioning / consistent hashing of servers / database nodes




