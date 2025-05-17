# Important API concepts

## API versioning

API versioning is the practice of developers improving their APIs while still leaving the prior iterations functional for clients. It gives users the freedom to upgrade to new versions at their own pace, rather than forcing the update onto them, which might break their existing application.

### API versioning principles

Since API versioning is an essential part of API design, here are some best practices that should be followed while versioning:

<img width="279" alt="image" src="https://github.com/user-attachments/assets/286f0711-4e97-4d90-b241-cdf834df8549">

- A new API version should not break any existing clients. If several developers have adopted an API, introducing new versions could cause their applications to break. Therefore, it’s important to create new versions that don’t break the applications that are still dependent on the old versions. This may be done by simultaneously supporting the older version of the API after a newer version has been released.

- The frequency of API versions should be low. A release of another version is a huge investment and commitment on both the side of the provider and the developers who use the API. The developers need to evaluate the new API and see how it will affect their current applications. At the same time, the provider's side has to supply support across multiple versions so that there can be a smooth transition to the latest version.

- Backward compatible changes. If changes in an API are compatible, then we can avoid making new versions altogether (remember that backward compatibility means newer code can read what an older software version has already written). Minor changes such as adding additional query parameters do not necessarily require any changes to the client application and will continue to function in the same manner, so it doesn’t require a new API version. For instance, if a change is made to our API that still allows dependent applications to function in the same way, rolling out a new version for the change would be unnecessary and a waste of resources.

To illustrate this, let’s take a look at the slides below, which illustrate an instanceof a client making an API call to the server with mismatching versions:

1. Both the client and server are on the old version:

Both the client and server are operating on the old version, so there shouldn’t be an issue because the versions are compatible with each other.

<img width="305" alt="image" src="https://github.com/user-attachments/assets/6d3ca105-04c7-4c6d-82d8-f8ea9685b36f">

<br/>
<br/>

2. The client is on the old version and the server is on the new version:

In this scenario, the server has updated to the new version. However, if the changes are backward compatible, there shouldn’t be an issue because there will be a contingency to handle calls from clients on older versions.

<img width="305" alt="image" src="https://github.com/user-attachments/assets/b0c01145-0f17-4bbf-ac4d-fc6ce29533e0">

<br/>
<br/>

3. Both the client and the server are on the new version:

With both the client and the server on the new versions, there shouldn’t be any issues, as long as the changes made in the new version don’t break the client’s application in any way.

<img width="304" alt="image" src="https://github.com/user-attachments/assets/50ee6055-e121-42cd-a896-0c48a6642e03">

<br/>
<br/>

4. The client is on the new version and the server is on the old version:

Here, the server most likely won’t be able to handle the new API calls unless the server is forward-compatible, but this isn’t always the case.

Note: Forward-compatible refers to versions which are still functional with newer versions.

<img width="305" alt="image" src="https://github.com/user-attachments/assets/06eb889d-a4a3-48a1-b334-6d89a81e7c9c">

So, servers are backward compatible with older versions of clients, but the opposite is not true.

### When to version

Versioning is important, but what are some cases where versioning is not required? This lesson discusses scenarios when versioning is required and when it should be avoided.

Let's start with an example of a mobile phone API, where the developers are now tasked with delivering the phone's model and price in its information. This restructure changes the phone's mobileinfo from a string to an object, containing both its model and its current price. If this change is implemented without versioning, the API will repeatedly crash as it tries to parse the mobileinfo, because it’s expecting a string but getting an object in return. This situation can be visualized through the illustration below:

<img width="551" alt="image" src="https://github.com/user-attachments/assets/b5c17586-f6a6-4233-a800-d06681d5b97c">

To resolve these breaking changes, a new version has to be rolled out, or else every consumer utilizing the API in their applications will encounter these problems. While incorporating these changes, the version of the API should be embedded in the requests so that it can be routed to the correct entity, through which the users will receive the correct response.

The scenario above is just one situation where we implement versioning. The table below examines numerous scenarios and illustrates if versioning should occur in each situation.

<img width="686" alt="image" src="https://github.com/user-attachments/assets/c8826437-402c-4a82-a43a-8c5a75962361">

### API versioning semantic

Versioning semantics is a convention used to assign meaningful numbers to the released API, referred to as major, minor, and patch numbers. The semantic indicates backward compatibility/incompatibility and bug fixes of an API as listed below:

- Major: The significant changes in an API that can cause incompatibility with the older version are referred to as major versioning of an API, for example, replacing the authentication method. The structural and behavioral changes in the existing features are considered major revisions of an API.

- Minor: Adding new functionalities in an API is a minor revision. For example, adding sign-up with Google functionality in an API, keeping the existing options as it is, does not break the API functionalities and is also backward compatible with the older version.

- Patch: Fixing bugs or making small updates in the functionality of an API is referred to as patch versioning and such fixes are also backward compatible. For example, an API returning a user’s data twice is a bug and can be fixed without altering an API’s functionality.

The number semantic can be seen in the following illustration:

<img width="211" alt="image" src="https://github.com/user-attachments/assets/c3ab7107-1ebf-455f-963a-b74a5acc4ca5">

In the illustration above, five indicates the 5th major version of an API in which one new functionality was added as a minor update, and ten bugs were fixed in this new minor update.

Note: Some organizations may override the guidelines mentioned above. For this reason, the guidelines are subjective (what should be a minor revision might be treated as a major release for someone else). For example, when iOS is released each year to go with a new version of the iPhone, it usually has a new major number. If we compare the number of features from one year to the next, they may differ in number and applicability.

### Different versioning approaches

There are several API versioning approaches that various companies across the world employ. We’ll take a look at three of the most popular approaches below:

- Versioning with URLs: This is the most common method of versioning because it’s simple and effective. In this approach, the version information of the API is included within the URL in the form of an identifier, such as /v1. The URL follows a strict template so that parsing the version from the URL is achievable. When the identifier changes, it’s assumed that all the resources change as well. If a new version is introduced, a different identifier would have to be used, such as /v2. This method has the most maintenance cost compared to the rest of the procedures.

- Versioning with HTTP headers: In this approach, the HTTP header is used to specify the version of the API to be invoked. The preferred header for this approach is the HTTP `Accept` header. This approach is favorable because it keeps the API version outside of the URL, which prevents it from being cluttered.

- Versioning using host name: Another approach for versioning is to use a new host name for each version. Let's assume that we have an API at the api.example.com endpoint. We could implement a new version with a different host name, such as graph.example.com. This approach is only used when we have an extensive rework of an API, and we want to reroute the client requests onto a new server.

Versioning in a URL:

<img width="379" alt="image" src="https://github.com/user-attachments/assets/861b42f9-c6fd-4a37-84b9-3873297836a7">

Versioning in an HTTP header:

<img width="378" alt="image" src="https://github.com/user-attachments/assets/302d3434-939b-42f5-b88f-1fe45935ef9d">

Versioning in a host name:

<img width="380" alt="image" src="https://github.com/user-attachments/assets/5eef70e2-1b51-4c35-ae37-0ed0036317ac">

### API version lifecycle management

Making changes to an API requires extensive planning and testing. The consumers of our API need to be notified of any changes we might want to introduce. Here are some of the ways this can be achieved:

- Announce the new version and versioning schedules.

- Send emails to registered users about the changes coming soon.

- Introduce warning alerts in older versions that are to be deprecated.

- Define a migration period and end date for support of older versions.

- Release a new API version as a beta release for a small sample of developers to get feedback and find bugs.

- Launch the API while maintaining the old versions so that developers have time to migrate their code to the new version before the deprecation date.

## Evolving an API design (Optional)

Refer to Educative: https://www.educative.io/courses/grokking-the-api-design-interview/evolving-an-api-design

## Rate limiter

The API rate limiter throttles clients' requests that exceed the predefined limit in a unit time instead of disconnecting them. Throttling refers to controlling the flow by discarding some of the requests. It can also be considered a security feature to prevent bot and DoS attacks that can overwhelm a server by sending a burst of requests. Overall, rate limiting provides a protective layer when a large number of requests per unit of time (a spike or thundering herds) is directed via an API.

### Rate limiter responsibilities

In addition to a security feature, a rate limiter should also provide the following capabilities to manage API traffic:

- Consumption quota: Specifies the maximum number of API calls to the backend that a certain application is permitted to make in a particular time frame. API calls that go beyond the allotted quota may be throttled.

- Spike arrest: Recognizes and prevents an unexpected rise in API traffic. It also protects the back-end system and reduces performance lags and downtime.

- Usage throttling: This slows down an enormous number of API calls from a specific user within a specified time frame. Usage throttling improves the overall performance, leading to reduced impacts—especially during peak hours.

- Traffic prioritizations: Prioritizes incoming requests depending on their criticality, ensuring a balanced and stable API service. For example, an API can be used by both freemium and premium users. Both types of users should have different amounts of API usage quotas.

### Rate limiter workflow

Whenever a rate limiter receives an API request, it looks for the client's information in the database or cache, including the number of requests allowed to the users. If the count of requests already made is less than the maximum number of requests allowed, the current request is forwarded to the servers, and the count is incremented. For example, as shown in the following illustration, a client with “ID: 101” is making a request for a service. The rate limiter allows this request because the “Count” for the incoming request is “3,” which is less than the maximum number of allowed requests per unit of time (“5”).

<img width="552" alt="image" src="https://github.com/user-attachments/assets/0dc80ba9-d355-4428-9185-d761dc4b7f2f">

If each request goes out of the rate limiter, then that means the rate limiter is on the critical path and can add latency to the user. How can we manage this problem?

For a rate limiter to avoid causing latency, we should design it in a way to utilize a high-speed cache and do some work offline (not on the client’s critical path).

### Rate limiter location

A rate limiter can be placed in three different locations:

- On the client side: The simplest way is to put a rate limiter on the client-side. However, this way, the rate limiter becomes vulnerable to malicious activity, and the service provider configuration can't be easily applied. Additionally, clients may intervene in the rate-limiting value and send as many requests as they want, eradicating its actual role.

- On the server-side: A rate limiter can be placed on the server-side within the API server. This way, the same server that provides API services can also handle rate-limiting complexities.

- As a middleware: Another approach to place a rate limiter is to isolate it from front-end and back-end servers and place it as a middleware. This way, the rate-limiting services are isolated from the rest of the activities taking place in the system.

### Rate limiter characteristics

The primary goal of the rate limiter is to protect the infrastructure and product. While implementing a rate-limiting system, we should provide the following characteristics to make consumers' lives easier:

- Return the appropriate HTTP status code: Whenever a request is throttled, the system should return an HTTP 429 status code showing that the number of incoming requests has reached a predefined limit for a given amount of time. It’s also standard practice to let the developers know when they can try the request again by setting the retry-after header. Developers can use this header to retry the request.X-RateLimit-Resource: This header indicates the resource name for which the rate limit status is returned.

- Rate-limit custom response HTTP headers: Apart from the status code, we should include some other custom response headers about the rate limit. These headers help developers when they need to retry their requests. These headers include the following:

  - X-RateLimit-Limit: This header represents the maximum rate limit for calling a particular endpoint within a specific amount of time.

  - X-RateLimit-Remaining: This header represents the number of remaining requests available to developers in the current time frame.

  - X-RateLimit-Reset: This header indicates the time at which the time window is reset in UTC epoch seconds.

As shown below, the output X-RateLimit-Limit shows the number of requests a user can make to the server. The X-RateLimit-Remaining is the number of requests that we can make in an hour. This value is decremented each time we execute the given command (in other words, when we access the server). This quota is reset after X-RateLimit-Reset, which represents a timestamp in the future. Additionally, the value of X-RateLimit-Resource is core. This represents the core GitHub resource.

<img width="554" alt="image" src="https://github.com/user-attachments/assets/24afe484-0e58-42b7-9f0a-0f8391611420">

- Rate-limit status API: If there are different APIs for different endpoints, there should be a way for clients to query the limit status of various API endpoints.

- Documenting rate limits: Documenting rate-limit values can help users make the right architectural choices. This will allow them to learn about the APIs before getting trapped in the rate-limit errors.

### Rate limiter best practices

- Appropriate rate-limiting algorithms: One good practice is that the server should pick rate-limiting algorithms based on the traffic pattern that it supports. There are various rate-limiting algorithms that we can choose, for example:

  - Token bucket
  - Leaking bucket
  - Fixed window counter
  - Sliding window log
  - Sliding window counter

- Rate limiting threshold: The rate-limit threshold should be chosen carefully depending on the number of users of an API and the average behavior of a typical customer. For example, for social media applications, the number of users can be several million. So, the rate limit value should be kept relatively higher. These thresholds might need to update over time as workload patterns change.

- Documentation for developers: We should offer clear guidance to developers about the rate-limit thresholds and how they can request additional quotas so that they can continue their work without any hurdles.

- Smooth rate-limit thresholds: Starting with lower rate-limit quotas is helpful because they can be increased gradually instead of initially allowing a large amount of quotas and then decreasing it later due to a large number of users. Reducing rate-limit values later might negatively impact the client as they become used to a certain number of requests in a certain period.

- Exponential back-off mechanism: Simultaneous requests in a time window can overburden a server, which may result in failures of requests. Therefore, to avoid the rejection of incoming requests, we can progressively increase the wait time between retries for consecutive error responses. One of the techniques used to add delays is called an exponential backoff. So, another good practice is to implement exponential backoffs in our client software development kits (SDKs) and provide sample code to developers on how to do that.

Exponential backoffs can cause an increase in latency. Why should we still use them?

At the individual level, it might cause latency, but this approach is collectively better for everyone because it decreases the request failure rate.

## Client adapting APIs

API generating the same response for every client request may not be suitable for all end devices. In essence, a flexible API response refers to the flexibility in terms of the response generated and resources provided by servers to clients—mainly depending on the user and client (such as its type, version, and so on).

### Approaches

Adaptive responses can be achieved in the following ways:

<img width="358" alt="image" src="https://github.com/user-attachments/assets/d73215ec-6bc6-4803-b54a-fc8bf02c3e53">

### Client side flexibility

Client-side flexibility makes the responses flexible on the client-side before displaying the results on the screen. We get the same response for all user scenarios or different client types, and the client tailors this response according to the requirements. All the clients receive the same number of fixed fields as a response from the server.

For example, Educative’s Careers page uses four images for small devices and eight images for large devices, as depicted in the following illustrations:

<img width="569" alt="image" src="https://github.com/user-attachments/assets/d6457638-7b8c-412c-a38a-280b3c6008fb">

Although the response from the server remains the same (eight images are received for both device types), the frontend displays four images to make it look more suitable for the device’s smaller screen. Generally, if we use a large number of fixed fields in the response, then some of the fields might not be necessary for some clients. On the other hand, if we use very few fields in the response, these fields might not fulfill the client's requirements. Although the number of fields can be changed over time, it remains the same for all the clients.

### Server side flexibility

Server-side flexibility makes the responses flexible on the server-side based on the client or user scenarios. We discuss the three approaches for achieving flexibility on the server-side, as given below:

- Intermediate adaption code
- Expanded fields
- GraphQL

#### IAC (Intermediate adaption code)

Intermediate adaption code (IAC) is a technique used to obtain server-side flexibility. The adaption code acts as an intermediate layer between the client and the API. Apart from determining the client type, this code is responsible for either forwarding the client's request to the relevant API gateway or tailoring the response based on the client type.

To handle the different devices, Netflix uses the extra layer between the client-side code and the API where the client adaption code is written. This layer uses the customize endpoint for the specific device and tailors the data according to the client. Netflix uses different IACs for tablets and mobile phones to reflect device-to-device differences.

<img width="445" alt="image" src="https://github.com/user-attachments/assets/41096e6f-ae15-426f-8989-5deee6fc4d2a">

What are the two main responsibilities of IAC?

Following are the two main responsibilities of IAC:

- Client device identification: IAC identifies the client in various ways, such as using HTTP headers.

- Forward the request to the appropriate API gateway to generate a flexible response or tailor the response based on the client type.

#### Expanded fields

Expandable fields are used to request the expanded version of certain objects from an endpoint. Depending on the client type or any user-related scenario, we can request additional information through conditional parameters in the URL.

Let’s understand this by using the following hypothetical example of a restaurant finder application. There are two different devices accessing the same endpoint of this application. The devices exercise conditional parameters to request the following expanded objects.

- Mobile phone: When the GET /finder/location endpoint is called via a mobile phone, the following response is obtained:

<img width="554" alt="image" src="https://github.com/user-attachments/assets/4e09ee2b-8a8e-4ead-b556-c3d1c2a877cf">

- Web browser: Next, we need to expand the images field for the web browser. The endpoint is GET /finder/location?expand=images, which gives the following response:

<img width="554" alt="image" src="https://github.com/user-attachments/assets/ef867e15-a7a5-4013-a063-d9907875c58d">

The API generates the response according to the expand parameter. Any client desiring to receive expanded objects will need to add the expand parameter depending on the type of end device or user-specific requirements. On the server-side, we achieve flexibility using the single endpoint.

#### GraphQL

GraphQL is another great technique for generating flexible API responses. Using this approach, the client defines their requirements as a query, and the API generates a flexible response according to the client's requirements. This approach requires the server to share a schema with the client beforehand. The schema defines the structure of available resources and the client's request format. Upon receiving the client's query, the API makes a single call to fetch the data from different services to meet the query's needs. Take the example above of the restaurant finder application. If we want to know additional information about the peak times to visit a restaurant, GraphQL is useful here. Instead of making a separate call to get the peak times, we send the query to the server in the following way:

<img width="556" alt="image" src="https://github.com/user-attachments/assets/6127a374-3999-44fa-a468-db9d2eb84972">

The following response is obtained from the query:

<img width="554" alt="image" src="https://github.com/user-attachments/assets/4731d9c6-54d8-488b-bdef-9c09caef63a5">

We can conclude that by using GraphQL, we don’t need to send multiple calls to retrieve the required data from different APIs. GraphQL provides flexibility using a single request to receive data, such as location and popular timings, from different services.

### Client Identification

Identification of the client is important because it helps the API gateway decide which downstream services to call. We describe the fields of the HTTP request header below in order to get the client information. Client identification is mainly done through the HTTP headers. Generally, two types of HTTP headers serve this purpose.

- HTTP User-Agent
- HTTP client hints (Accept-CH)

#### HTTP User-Agent

The HTTP User-Agent header is a string that allows servers to identify the client, OS, vendor, and version. This header is defined in the following way:

<img width="527" alt="image" src="https://github.com/user-attachments/assets/ac0b0cb4-d031-498e-a6ca-846ce109aa8b">

- product: Identifies the name of the client, such as Mozilla.
- product-version: Provides the version of the client.
- comment: This is optional, we can use it to add details related to the operating system, and more.

For example, the macOS User-Agent string looks like this:

<img width="524" alt="image" src="https://github.com/user-attachments/assets/4dfe0fda-9da5-4df9-9712-74764929dfeb">

As we can see, the string above is long and unstructured, which makes it difficult to parse from a developer’s perspective. Also, sharing detailed information about the client in the HTTP request creates privacy issues, because we need to prevent users from covert tracking (such as digital fingerprints). To overcome these issues, HTTP introduced client hints.

#### HTTP client hints

HTTP client hints are used when a server might want specific information about the client for subsequent requests. In response to the initial request, the server passes the HTTP header Accept-CH to inform the client about the fields the server is interested in.

The server indicates the client by sending the Accept-CH header in the response. For example, the Accept-CH header may contain the following information:

<img width="526" alt="image" src="https://github.com/user-attachments/assets/88ada0db-77f5-4f01-a66e-c5b5f99e586c">

The client then sends information to the server in the subsequent requests. This information includes:

- RTT: Round trip time
- Width: The device’s width
- Sec-CH-UA-Platform: A platform such as Windows, Linux, or macOS

### Client adapting APIs advantages

- Improved design of the application is achieved by choosing the optimal end (client or server) to perform the processing.

- Enhanced performance of the overall application is achieved, which leads to a better user experience.

- May result in the efficient usage of bandwidth and other client- or server-side resources (memory, processing power, and so on) because only the required data is communicated between the two ends.

### Client adapting APIs disadvantages

- Adding flexibility to API responses leads to added complexity. For example, an IAC layer requires extensive and optimized coding solutions that should handle all types of devices or different user scenarios.

- Achieving flexibility in API responses introduces an additional financial cost for the service provider. For example, an additional number of endpoints management will multiply the expense.

## Data fetching patterns

This lesson will discuss data polling techniques to send and fetch data to and from the server. The main polling methods are given below:

- Short polling
- Long polling

Additionally, this lesson also discusses WebSocket, a full-duplex protocol used to address the limitations of polling techniques and provide real-time communication between the client and server. It also enables clients and servers to avoid polling of data.

### Short polling

With short polling, the client initiates a request to the server for a particular kind of data at regular intervals (usually < 1 minute). When the server gets the request, it must respond with either the updated data or an empty message. Even though the small polling interval is nearly real-time, deciding the polling frequency is crucial. Short polling is viable if we know the exact time frame when the information will be available on the server. The illustration below represents the short polling procedure between the client and server:

<img width="398" alt="image" src="https://github.com/user-attachments/assets/6a5106c7-86be-4f43-b5cc-3823208881da">

Problems with the short polling approach are the following:

- Needless requests when there are no frequent updates on the server-side. In this case, clients will mostly get empty responses as a result.

- When the server has an update, it can’t send it to the client until the client’s request comes.

Let’s take a look at the following illustration to understand the problems mentioned above better:

<img width="340" alt="image" src="https://github.com/user-attachments/assets/f912038c-2bae-42e8-8f1a-de9d9d3b9fb4">

The illustration shows that the server has new data to send immediately after the first response. But the client has to wait for a predetermined interval until the next request to receive the data arrives.

### Long polling

Long polling operates the same way as short polling, but the client stays connected and waits for the response from the server until it has new updates. This approach is also referred to as hanging get. In long polling, the server does not give an empty response; there is an acceptable waiting time after which the client has to request again. However, this strategy is appropriate when data is processed in real-time to minimize long waiting intervals for a response. But it does not deliver significant performance because the client may have to reconnect to the server multiple times after a timeout to get new data. Let’s see the illustration below to understand how the client faces idle time and places a new request if there is no server-side update after an interval.

<img width="389" alt="image" src="https://github.com/user-attachments/assets/0cdf6494-7ad7-42fc-93f9-fa52fe234ef7">

Problems that come with long polling include:

- The delays while waiting for the occurrence of an update or timeouts.

- The server has to manage the unresolved states of numerous connections and their timeout details.

- The client’s need to establish multiple concurrent connections to send new information by sending another request. Otherwise, it needs to wait for a response or timeout of the already established connection.

Note: The TCP connection between the client and server used by the  approaches discussed above can be persistent or non-persistent. The client or server opens a TCP connection once to establish a persistent connection. However, for non-persistent, it regularly initiates TCP/IP connections for each request.

### WebSocket

WebSocket is a persistent full-duplex communication protocol that runs on a single TCP connection. In real-time applications, clients sometimes need to send requests frequently to the server. For instance, if a request is initiated by the client and receives part of the response instead of a complete response, the client can send another request over the same TCP connection. This is achieved by requesting to upgrade the connection from TCP to WebSocket. At the same time, we need low latency and efficient resource utilization. For this, WebSocket is an ideal choice, allowing full-duplex communication over a single TCP connection. Let’s understand the discussed example with the following illustration, where clients send two requests over a single TCP connection:

<img width="372" alt="image" src="https://github.com/user-attachments/assets/ea5ffff3-6fe0-49f2-a87b-8c1caf206147">

In the illustration above, the client and server can communicate data whenever needed, and such scenarios are important for many real-time applications. The stateful attribute of the WebSocket also gives an advantage by allowing for the reuse of the same open TCP connection. This approach is suitable for multimedia chat, multiplayer games, notification systems, and so on.

A WebSocket connection has to be upgraded from a typical HTTP connection.

### Data fetching comparison

Now, we’ll compare each approach considering a real-time application. The table below compares the data polling approaches based on the principal factors that help decide which approach is suitable in a given scenario.

<img width="682" alt="image" src="https://github.com/user-attachments/assets/d517ee60-880d-43df-843a-e7550b176697">

## Event driven architecture

The HTTP protocol is suitable for transferring data between client and server. However, for real-time communication, such as instant messaging, live streaming, gaming, and so on, HTTP falls short due to the connection terminating after a response from the server. The HTTP-based techniques to fetch updated data also have limitations. For example, short polling sends too many unnecessary requests, long polling uses two separate connections for sending and receiving data, and HTTP streaming allows only half-duplex communication. Event-driven architecture addresses all these limitations of HTTP-based techniques.

Event-driven architecture (EDA) is an approach that centers around events for data and applications. The event-driven architecture enables applications to act or react to those events. A client gets the data whenever an event is triggered in the application without requesting the server. The problems associated with short and long polling are eliminated by using an event-driven approach. This is very much in contrast with the traditional REST API approach to request the updated data after a certain interval or when needed. The illustration below explains the concept.

<img width="398" alt="image" src="https://github.com/user-attachments/assets/5a0c5420-85bd-4765-b315-d1fbd1c49788">

Note: The event-driven protocols require the client to subscribe to a particular topic for receiving event updates, often specifying the endpoint (a callBack URL) to post the updates. The callBack method via link allows connecting directly with the host even if it is not accessible via IP address. This URL is unique for each subscription. The pub-sub uses functionality of capability URLs to define callback URLs.

Note: Capability URL restricts access only to the owner of that URL. It allows the user of that URL to access resources associated with it.

In these cases, the client wants to be informed that something has happened. In this case, there is no request or asking paradigm (which explains that the client wants to be informed about the events without sending a request (request/asking) to the server); therefore, no response is expected.

The event-driven architecture provides an asynchronous environment. For example, when an event triggers, the system performs the intended action immediately and doesn’t wait for the synchronous delivery of other events. In other words, it doesn’t wait for a response from event listeners. This is an ideal architecture to use when clients need to be notified about the changes occurring in the backend.

### Event driven protocols

This lesson will discuss the primary event-driven protocols that are used to push data from the server. Furthermore, we’ll elaborate on how APIs based on event-driven architecture perform well in different real-time scenarios. The following is a list of event-driven protocols we’ll discuss in this lesson:

- WebHooks
- Server-Sent Events (SSE)
- WebSub
- WebSocket

### Webhooks

Webhook is a one-way event-driven communication protocol based on HTTP. It enables applications to send real-time information when a particular event gets triggered. In a webhook, the server (consumer) must first subscribe to a particular topic through a specified HTTP/HTTPS endpoint with another application's server (producer). After the subscription, any new events are automatically notified by the server. The webhook protocol is used when two servers or applications have to communicate with each other. Let’s consider the example of the Slack application where a user wants to receive a notification for meetings scheduled on Google Calendar. If this communication were to take place using the request-response architecture, it would look something like the diagram depicted below:

<img width="544" alt="image" src="https://github.com/user-attachments/assets/20e80b34-6413-435e-aadc-872f6ed04edd">

In the illustration above, Slack periodically requests Google Calendar for an update using the request-response architecture. As shown in the diagram above, Google Calendar didn’t have an update for the first couple of requests, but provided an update to Slack on the third request. For organizations, there can be hundreds of customers and dozens of meetings or other scheduled events. If Slack starts polling each user from the Google Calendar application, it becomes wasteful for both parties involved. Therefore, using the request-response architecture is not ideal for these kinds of scenarios. This situation requires the use of event-driven architecture. Let's see how we can improve this experience using webhooks. Take a look at the illustration below:

<img width="356" alt="image" src="https://github.com/user-attachments/assets/4cb17670-d99b-419d-9a87-c49f141135e4">

In the illustration above, the Slack application first subscribes to a particular event with the Google Calendar application. After a successful subscription, Google Calendar notifies Slack when there is an update for the subscribed event. Therefore, we can see how webhooks reduce the overall communication required for event updates between two applications. Another advantage of this approach is to avoid reaching the application's rate limit.

Despite the advantages, webhooks also have the following drawbacks:

- Not every application supports webhook integrations.
- It isn’t suitable in situations where an application wants to know only the final result instead of an update of each event.
- It only pushes the events to the consumers; if a server cannot receive them, there is no mechanism to explicitly request that event from the server.
- A consumer doesn’t know when the server is down or if it fails to send events. This can result in an assumption that the events are not occurring at all.

Applications that provide different services to other applications through the webhook architecture include:

- Google uses webhooks for Google Assistant and Google Calendar services.
- Meta uses webhooks for payments, messengers, and social graph services.

Other webhook applications are Twilio, Slack, Shopify, Stripe, and many more.

### SSE (Server sent events)

Server-Sent Events (SSE) are a unidirectional (server-to-client) server push approach and a component of the HTML5 specification. Here, a server push means that the specified client automatically gets data from the server after the initial connection has been set up. In SSE, the client requests the URL through a standard EventSource interface to enable an event stream from the server. Additionally, the client defines the text/event-stream under the Accept header in the request. Here, the event-stream represents a media type known as Multipurpose Internet Mail Extensions (MIME). Before initiating the request, the client-side application also checks the server-sent event support on the client (browser).

This approach is mainly used for the notification system, where clients get notified by the server upon update. Let's see the illustration below to understand the SSE approach:

<img width="484" alt="image" src="https://github.com/user-attachments/assets/6de72137-ada3-4196-857e-b7dc4e8b71c8">

In the illustration above, the client automatically gets notifications until the client or server terminates the connection. Both the SSE and webhook protocols are similar in functionality; the only difference is that webhooks send events to servers, and SSE sends events to clients.

The drawbacks that come with the SSE approach are as follows:

- When we use SSE over HTTP/1.1, the browsers allow a limited number of connections per domain because each requested resource requires a separate TCP connection. However, HTTP/2 has resolved this issue by multiplexing all requests and responses over a single TCP connection, but most applications still use HTTP/1.1.

- Another major problem with SSE is that it only allows text-based streaming due to data format limitations, such as not supporting binary data. So, we can’t use it for other streaming data such as video, audio, and so on.

Applications use SSE for different purposes. For example, Twitter, Instagram, and Meta use SSE for newsfeed updates. Stock applications use SSE for real-time stock updates. Sports applications use SSE for live score updates.

Assuming that a network is flaky between the client and the server, it isn’t easy to guarantee consistent connections in real-world applications. How will SSE recuperate when the connection drops?

SSE mitigates this issue by sending the last event ID to the specified client. The last event ID is specified in the HTTP header Last-Event-ID through a new HTTP request. When the server receives this request, it sends the event from that provided ID.

Why is SSE preferred over HTTP streaming for live streaming of an event?

With HTTP streaming, the intermediate network gateways or proxies might wait for all chunks and then aggregate them to deliver to the requested client. In contrast, SSE delivers messages to clients as soon as they’re available, making SSE the optimal choice for real-time updates. Therefore, HTTP streaming is not suitable for real-time updates, such as notification services and live sports updates.

### WebSub (Pub-Sub)

WebSub is another event-driven architecture for distributed publish-subscribe communication, also known as pub-sub, and PuSH. WebSub has three main components, which is one of the reasons why it is unique compared to other event-driven architectures. 

- Publisher: The content producer publishes the specified topic event information to the defined Hubs.

- Hub: A middleman that decouples publishers and subscribers. It serves as a content distributor who takes the specified content from the publisher and pushes it toward the subscriber.

- Subscriber: A consumer who receives the update for particular content (known as a topic) from the subscribed Hubs publicized by the publisher. Whenever a publisher produces new content related to a specific topic, the Hub pushes them to the subscriber(s).

Let's see the illustration below to understand how the above three components work together.

<img width="497" alt="image" src="https://github.com/user-attachments/assets/e9c5ca58-eacb-4b02-865b-f85ffba40540">

In the illustration above, the subscriber first asks for the defined Hubs from a publisher. After getting the Hub details, subscribers send the subscription request for a specific topic in the resource URL to a particular Hub. The Hub uses this topic resource URL to send updates delivered by the publisher. The structure of the subscription/unsubscription request is defined below:

<img width="558" alt="image" src="https://github.com/user-attachments/assets/3bcdd404-d83e-4866-ac8b-a4675c8cdbf0">

- hub.mode: A string containing subscribe or unsubscribe to define the request.

- hub.topic: The resource URL of the topic to which the subscriber wants to subscribe or unsubscribe.

- hub.callback: A callback URL where the Hub responds with subscription details.

Note: The callback URL allows connecting directly with the host, even if it isn’t accessible via IP address (it isn’t dependent on the IP address of the host). This URL is unique for each subscription.

The Hub verifies the subscription request by sending a separate GET request to the subscriber. After that, the subscriber responds with a 200 status code to confirm the subscription. Upon successful subscription, the Hub sends notifications to all subscribers for the specific topic when it receives updates from the defined publisher.

WebSub is ideal when multiple clients require updates from the same producers. Another unique thing that comes with WebSub is the built-in security feature known as verification of intent. As shown in the illustration above, verification of intent is a kind of handshake that takes place before receiving content in the subscription request from the subscriber. The intent is verified by the Hub as an extra security layer to avoid subscription requests from attackers posing.

#### Verification of intent

Verification of intent is a process where a Hub verifies the subscriber. It gets performed in two steps:

- Request: The Hub generates a challenge string (a unique random string) and sends it to the callback URL of the subscriber.
- Response: The subscriber verifies the request by echoing the challenge string in response to the verification request.

The structure of the verification request is given below:

<img width="524" alt="image" src="https://github.com/user-attachments/assets/b356aa1a-77af-4d79-a962-03e0c74b5b26">

The response message from the subscriber should contain a confirmation of the request made earlier. An example of such a response message is given below:

<img width="526" alt="image" src="https://github.com/user-attachments/assets/acf40ff0-0ceb-4520-b456-23e7d67fbe49">

As shown above, the subscriber needs to echo back the hub.challenge apart from the HTTP status code and phrase (200 OK). The subscriber can also decline the request by responding with a failure response (3xx, 4xx, 5xx). On the other hand, the subscriber must include the hub.challenge to confirm its subscription to a request. Otherwise, the verification is considered to have failed.

Note: The WebSub network stops working when the Hub goes down.

### WebSocket

WebSocket is an event-driven protocol that enables bidirectional communication between the client and servers. It differs from the protocols mentioned above because they target sending events only from the server side (unidirectional). Whereas in WebSockets protocols, communicating parties can exchange data whenever needed and without any restrictions.

### Summary

SSE is suitable if an application wants to send events to clients with textual payloads only. Similarly, if targeted consumers are clients and servers, and there is no limitation of data formats, then the WebSub protocol is more ideal.

<img width="604" alt="image" src="https://github.com/user-attachments/assets/282cb63a-e84b-4e2a-8cc1-712b6c69e635">

## Cookies and sessions

### Cookies

A cookie is a small amount of data stored by a specific website (server) on the user's computer. The data stored in the cookies is labeled with a unique ID. It’s exchanged between a client's browser and the server, where the server reads the cookies and decides what information needs to be provided to the user.

Cookies contain information about the user's activity on the website. This includes the user's IP address, web browser type, version, operating system, and the pages the user has visited. Some other relevant information stored in a cookie includes clicks on different items or objects and the actions performed by the client—for example, views, time spent, items added to a cart, and so on.

When a user sends a request to a web server to visit a website, a response from the server contains the Set-Cookie header representing details about the cookies, as shown below. The client sends this cookie in response to future requests to the web server.

<img width="779" alt="image" src="https://github.com/user-attachments/assets/1eb3825b-2f1e-4813-a22c-0568c6e6c1ad">

Below are the parameters in the Set-Cookie header:

- Name: This is the name of the cookie.
- Value: The information that is stored on the user’s computer by the website.
- Expires: When the cookie will expire.
- Domain: This indicates the server to which the cookie is sent in future requests.
- Path: Represents an entity on the server that will receive the cookie.

#### How are cookies created?

Let's understand cookie creation with an example. Let’s assume that Alice connects with the web using a newly installed browser and contacts the website www.example.com. When they visit the website for the first time, the server sends cookie data in response to Alice’s browser consisting of the unique ID. The cookies are stored locally and are sent in the requests to the same website, as shown in the figure below.

<img width="433" alt="image" src="https://github.com/user-attachments/assets/7acfe3a0-4c2b-4c3c-aa6a-0f42fdb0e503">

Note: A browser usually has an upper limit on the number of cookies that it can store per domain. For example, few browsers allow storing up to 50 cookies per domain, and the amount of information a server sends to the client is small (usually no more than 4 KB).

The following table shows different attributes of a cookie object while visiting www.google.com.

<img width="574" alt="image" src="https://github.com/user-attachments/assets/3cbd4401-4f13-4cbc-b662-659f39c784cd">

Note: In the table above, the tick (✓) symbol means the values have been provided. Whereas "–" means the values have not been provided.

The cookies table in our browser contains the following fields:

- Name: The name of the cookie.
- Value: The information that’s stored on the user’s computer by the website. This information can include the user’s name, password, and preferences.
- Domain: This represents the domain that is allowed to receive the cookie.
- Path: This shows a specific path or URL on the website for which the cookie is valid.
- Expires/Max-Age: This is the expiration date or the maximum age of the cookie.
- Size: The cookie size in bytes.
- HTTPOnly: This indicates whether the cookie should only be used over HTTP or can be modified through JavaScript.
- Secure: It indicates that the cookie can be sent to the server over HTTPS, if true.
- SameSite: This field contains values lax, strict, or None. The lax value shows that the cookies can be sent on some cross-site requests, whereas the strict value doesn’t allow cookies on cross-site requests. The None value shows that the cookies can be sent to both cross-site and same-site requests.
- SameParty: This field indicates whether the party from which the user accessed the site is the same as the party that set the cookie.
- Partition Key: The partition key is used in the case when we have a site embedding content from another site. For example, https://abc.com embeds content from https://xyz.com. The partition key is used to provide support for cross-site cookies. This key represents the top-level URL we are accessing—for example, https://abc.com. The partition key in our case would be ("https", "abc.com").
- Priority: The cookie priority field is used to indicate the priority of a given cookie. The field can take on one of three values: Low, Medium, or High. The higher-priority cookies remain longer on the client than the low-priority cookies (the expiration date of these cookies are set by the server).

Note: Although cookies do not change the behavior of HTTP in any way, they do function as application-specific data storage that help maintain the state within an application according to different users.

#### What are cookies used for?

- Session management: Cookies can be used for session management. Upon exchanging cookies, the website recognizes users and their preferences. For example, whether  a specific user likes to see news related to sports or politics.

- Personalization: Cookies help the server-side maintain client-specific information. This helps in providing an experience that has been tailor-made for a particular user.

- Tracking: Cookies are used to track users across websites. For example, when a user visits a website, a cookie is stored on their computer. The cookie contains information about the user, such as the pages they visited, the time they visited, and the time they spent on a specific page. This allows businesses to show targeted ads to users based on their interests. Cookies can also be used to track users' browsing history and activity. This information can be used to personalize the user's experience on a website or application.

What is the lifetime of a cookie?

There are two ways to define the lifetime of a cookie:

- Some cookies are deleted immediately when a session ends, or when the browser is closed.
- Other cookies are deleted after the date specified by the Expires or the Max-age attributes set by the server.

Can the client tamper with the cookie’s attributes?

Yes, a client can tamper with the cookie’s attributes. This can be done by changing the values of the cookie’s attributes or by adding and removing attributes. It is important to use secure methods of storing and transmitting cookie data.

Servers often use measures to catch such tampering, for example, by including secure hashes of the cookies data. As a result, the client will not be able to change the cookie data and the hash value. When presented with such a cookie to a server, a hash of the new data won’t match with the one stored as part of the cookie, and the server will reject the cookie as a result.

What happens if a cookie is stolen?

If a cookie is stolen, it can be used to gain access to the user’s account. This is because the cookie contains information about the user, such as their preferences and authentication credentials. An attacker can use this information to access the user’s account and potentially steal sensitive data. It’s crucial to ensure that cookies are stored securely and are not accessible to attackers.

Note: Cookies can be deleted in your browser settings. You can find the settings in the “Options” or “Preferences” menu of your browser.

### Sessions

Sessions refer to the time users spend browsing a website. It represents the time between the user's arrival on a website's page and when they finish surfing it. A web session is a series of network activities that takes place between a web server and a web browser. During a session, the server and browser exchange a series of messages and information to establish a connection and start interacting with each other.

The interaction and the data exchanged between a web server and a web browser can include our search engine history, form data, added items to a shopping cart, ticket booking, the amount of time consumed on a page of a website, and so on. This data is exchanged via different kinds of cookies between the web server and the browser. To sum up, any interaction that we have with any website is recorded as a web session.

While sessions are often conflated and confused with cookies, they have some key differences from each other, as shown in the following table.

<img width="638" alt="image" src="https://github.com/user-attachments/assets/80e12ea9-a74f-44d9-81b8-5ba48e0bbd24">

What are some disadvantages of sessions?

Some of the disadvantages of sessions include the following:

- Because the session data is stored on the server memory, it may cause performance overhead if there is a large number of users, hindering the system’s scalability.
- Sessions can be vulnerable to session hijacking, a technique in which hackers gain access to the session ID and disguise themselves as authorized users.

What are some of the advantages of adding sessions to our applications instead of just using cookies?

There are several advantages of using sessions with cookies:

- Sessions are more secure than cookies because they’re stored on the server rather than on the user’s computer.
- Sessions are more reliable because they aren’t susceptible to browser cookies being accidentally deleted or turned off.
- Sessions allow for a greater amount of data to be stored because they aren’t limited by the size of a cookie.

Are session IDs secure?

The data between the client and server are exchanged after establishing a secure connection. This secure connection helps to deliver the session ID securely to the user.

Note: A single session between a web browser and the web server lasts for a certain duration. Depending on the use case, this session can be as short as a few minutes or as long as an entire day (or more).

#### Why is a web session used?

Instead of storing a huge amount of data in the browser, developers use session IDs to save information on the server-side while preserving user privacy. Both sessions and cookies have unique IDs; therefore, a web application sends the session ID and cookie ID back to the server each time a user performs an action or submits a request, along with a description of the activity.

Note: Session IDs and cookie IDs are sometimes confused. They both are closely related but aren’t the same. Cookie IDs identify a specific computer or visitor and can be used for authentication, storing website preferences and server session identification. On the other hand, session IDs are used to identify a specific session. A client has only one cookie ID but may have several session IDs, these two can be used together to better track the preferences of the user and give them a better experience.

#### Sessions in APIs

As discussed earlier, a session is a stateful connection between a client and a server. In the context of APIs, a session is typically used to store information about the state of a user's interaction with an API, such as authentication details, preferences, and progress. This information can then be used to customize the API experience for the user and provide a more seamless interaction.

Note: There’s plenty more stuff about cookies that we can talk about, but for the purpose of this course, this information will suffice. To conclude, cookies either benefit businesses or evade privacy. Therefore, some organizations support cookies while others oppose them. For example, Apple and Google clamped down on cookies (especially those that help track user activity), which hurt many advertisement businesses for big tech giants like Meta. On the other hand, Amazon supports and uses cookies for various purposes.

## Idempotency in APIs

Refer to the Educative module: https://www.educative.io/courses/grokking-the-product-architecture-interview/the-role-of-idempotency-in-api-design

## SSR vs CSR

In terms of APIs, one of our goals is to make the applications perform better. Let’s take an example of a video hosting site. We might notice that it takes a while for the thumbnails of the videos to load, as shown in the illustration on the right. Suppose this video hosting site utilizes an optimized API gateway. However, the content may still be displayed after a significant delay. There are multiple reasons for having higher latency, with rendering being the most common. Rendering is described as the process of utilizing HTML, CSS, and JavaScript code into an interactive web page or depicting the web page in the browser.

There are multiple reasons for having higher latency, with rendering being the most common. Rendering is described as the process of utilizing HTML, CSS, and JavaScript code into an interactive web page or depicting the web page in the browser.

### SSR (Server side rendering)

Server-side rendering (SSR) is a technique that generates a complete HTML document on the server and sends it to the client as a response to a request. The browser parses the HTML document and starts displaying it. On the initial load, the page is static and noninteractive. However, once the JavaScript file has been downloaded from the server, it modifies the DOM, and the page becomes interactive. DOM stands for Document Object Model. It's a programming interface used to represent an HTML document's content as a tree. The DOM provides structure to the HTML elements so we can easily access and manage them. Let's understand how server-side rendering works:

<img width="474" alt="image" src="https://github.com/user-attachments/assets/b27849b3-f9c6-4118-b2b3-8b74cf5adfc8">

Note: The term "Paint" means when a pixel is visible to the user.

Let’s assume the following HTML document is received from the server. The document contains some content with a link:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Example</title>
  </head>
  <body>
    <h1>Educative</h1>
    <p>This is a website of Educative. Here is the career page</p>
    <a href="https://www.educative.io/careers">Link</a>
  </body>
</html>
```

The browser starts parsing the above document and displays the corresponding content. When a user clicks the “Careers” page link, the browser sends another request to the server and reloads the complete web page. We assume that both pages (current and “Careers”) have the same header and footer. So only the inner content needs to be updated. However, SSR reloads the complete page, which incurs the load on the server and the usage of unnecessary bandwidth. Therefore, developers mostly use SSR for when the web page initially loads.

<img width="760" alt="image" src="https://github.com/user-attachments/assets/dc9b9579-b9b3-495a-9bc3-d663b4da0f74">

#### When should SSR be used?

- SSR works well when we need the initial load of the web page to be fast.
- If a web page consists of static content, then SSR is suitable for rendering the content quickly.
- SSR favors SEO because the browser populates the page without waiting for the JavaScript to render.

Static SSR is used to generate a static HTML document on the server. The server sends a lightweight HTML document to the client. Mostly, portfolio websites contain the same content for all users. Static SSR performs better because the server sends the static content to every user.

Dynamic SSR is used to generate the dynamic HTML document on the server. It sends heavy-weight HTML documents to the client. For example, a social media website dynamically generates a different profile page for each user. Dynamic SSR does not perform well because the server has to populate a complete HTML document for each user.

### CSR (Client side rendering)

Client-side rendering (CSR) generates the complete web page in the browser instead of on the server. All the content, whether it is static or dynamic, is handled on the client side. The server sends the empty HTML file (which means no HTML content is populated except the basic structure of the HTML file) with JavaScript code or a link to it. The browser executes this JavaScript code to generate the web page.

Let's understand how CSR updates or renders the content in the browser:

<img width="421" alt="image" src="https://github.com/user-attachments/assets/61d3cba6-f72d-4601-b9a0-db5962fbb079">

Let’s assume the following HTML document is received from the server. The document contains only the div tags with the main ID. The content is populated after the script tag on the client-side.

```html
<!DOCTYPE html>
<html>
<head>
  <title>Example</title>
</head>
<body>
  <div id="main"> </div>

<script>
  function loadpage() {
    const element = (
     <div>
        <h1>Educative</h1>
        <p> This is a website of Educative. Here is the career page </p>
        <a href="https://www.educative.io/careers">Link</a>
      </div>
    );
    ReactDOM.render(element,document.getElementById('main'));
  }
  setInterval(loadpage, 1000);
</script>

</body>
</html>
```

The content creation on the client-side can be handled using multiple frameworks such as React, Vue, Angular, and so on. These frameworks allow rerendering of specific DOM elements to update the data or user interface.

<img width="664" alt="image" src="https://github.com/user-attachments/assets/5d4d0e72-d5dd-4baf-87bd-c6d9c19e6d44">

#### When should CSR be used?

- It is preferable to use it for websites that update their content frequently.
- If the web page consists of dynamic content, then CSR is good for rendering the dynamic content quickly.
- If SEO (search engine optimization) is not a goal of the website, then we can use CSR.

Additional rendering techniques:

AJAX stands for Asynchronous JavaScript and XML. This approach allows the browser to fetch specific data from the server and renders the new content without refreshing the page. For more information about AJAX, see this article.

Prerendering is another technique where the HTML of a page is pregenerated on the server. When the user navigates to this page, the prepopulated HTML document is fetched from the server and starts painting the document on the screen. Once the browser executes the client-side JavaScript, the web page becomes interactive.

A company has hired you to develop a new social media platform that will compete with tech giants like Facebook and Twitter. You need to meet the following requirements for this new social media application:

- It should be optimized for SEO and should be easily discoverable by web crawlers.

- Users should not have to wait long for the initial loading of the website.

- The platform should quickly show updated data on the web page.

- The website should be able to effectively display and handle dynamic data.

Given this information, what type of rendering should be used for the platform?

For the new social media platform you’re developing, the best approach is to use both server-side rendering (SSR) and client-side rendering (CSR) at different stages. Initially, use SSR to optimize for SEO and ensure the website loads quickly for users, meeting the first two requirements. Then, incorporate CSR, utilizing libraries like React or Vue, to efficiently display and handle dynamic data, ensuring the platform quickly shows updated data on the web page. This combination leverages the strengths of both rendering methods to meet all the specified requirements.

### SSR vs CSR summary

From the details mentioned above, we can see that both SSR and CSR have their pros and cons, and there is no clear winner. Today's websites and applications are also full of rich features and require both the advantages of SSR and CSR at different levels and hierarchies. Using just SSR for the entire application may degrade the application's performance and further depreciate over time because we might add additional load onto the server. However, If we use CSR to bypass the load on the server, the initial load of the page might increase. A suitable option is to use a mixture of both techniques to utilize the advantages of both approaches and improve user experience.

We can take the example of a social media application that primarily uses SSR with minimal CSR to render its website pages. In contrast, others may do the complete opposite depending on their requirements. For example, YouTube uses a combination of both approaches. To achieve this, YouTube uses SPF (structured page fragments) for static and dynamic loading of the web page's content.

<img width="560" alt="image" src="https://github.com/user-attachments/assets/e5a66a6c-d3eb-4a89-b46d-8c74deb5b928">

## Speeding up web page loading (Optional)

Refer to the Educative module: https://www.educative.io/courses/grokking-the-product-architecture-interview/speeding-up-web-page-loading

## Resource hints and debouncing

### Resource hints

Resource hints are hints or instructions that instruct the browser on managing specific resources—such as web pages, images, and so on—as well as which resources need priority in being fetched and rendered. They’re implemented using the rel attribute of the link element in HTML, as shown in the code snippet below. These hints are implemented by the front-end developers in their HTML pages.

```html
<!--prefetch-->
<link rel="prefetch" href="/pages/next-page.html">
<link rel="prefetch" href="<API endpoint>/newsstory1/newsvideo.mp4">

<!--preload-->
<link rel="preload" as="image" href="header-logo.svg">

<!--preconnect-->
<link rel="preconnect" href="https://api.our-amazing-api.com">
```

### Prefetching

Prefetching is a resource hint that allows the browser to fetch resources that might be needed later. These resources are stored in the browser's cache. Let's imagine that a user is scrolling on the home page of a video-sharing website. It’s expected that a user will click on a video that will interest them. In this case, we would want to improve the subsequent video's load time by fetching the video in advance and storing it in the browser's cache. The prefetch directive is well suited for that. This example has been visualized in the illustration below

<img width="534" alt="image" src="https://github.com/user-attachments/assets/23e7edce-8cc2-480e-b2af-feaf54d0f007">

In the example above there are two scenarios, one with prefetching and one without. Without prefetching, the video request is only sent when the user clicks on the video. However, with prefetching, the video is fetched in advance, reducing latency.

The prefetch directive is implemented in the following way:

```html
<link rel="prefetch" href="/pages/next-page.html">
<link rel="prefetch" href="<API endpoint>/homepage/newsvideo.mp4">
```

In the HTML snippet given above, we see that the browser has been instructed to fetch the page with the news story and the cover photo from the back-end API in advance. These resources have been provided in the href. We do this because we anticipate the user will want to click on an interesting headline to know more.

The prefetch resource hint has a low download priority. This means that it doesn’t interfere with other resources and can be used to prefetch quite a few things. For this reason, it’s best used when we have to load resources later and not immediately. The example of a video site that we discussed earlier is an optimal use case of prefetching because the files needed for the videos can be fetched while the user is scrolling the landing page. Netflix has used prefetch effectively to reduce their Time to Interactive (TTI) by 30%.

Note: TTI (Time to Interactive) is a performance metric that measures the time it takes for a web page to become fully interactive for a user. This includes the time it takes for the page to load all of its critical resources, such as images, scripts, and stylesheets, as well as the time it takes for the JavaScript code on the page to be parsed and executed so that the page can respond to user interactions such as clicking buttons, links, or filling out forms.

Prefetching is not a perfect method. Despite the low download priority, this directive can still increase data consumption, which itself can cause issues for users that are on a limited data plan. Furthermore, we can end up loading extra bytes that might prove to be useless. Because of the low download priority, it isn’t recommended to be used when we need to load urgent resources. For that, we’ll use the `preload` resource hint, which we’ll discuss later.

Let's look at what we've learned so far in the summary table below:

<img width="656" alt="image" src="https://github.com/user-attachments/assets/f80c6e20-6c36-4bf7-98d2-66c9daf3b0bc">

#### DNS prefetching

DNS prefetching is another type of prefetching. This resource hint notifies the client that there are assets that may be required later on from a different URL. This tells the browser to resolve the URL quickly. Let’s suppose that we need an image from the URL example.com, this is how we’ll represent it:

```html
<link rel="dns-prefetch" href="//example.com">
```

If we don’t do this, the browser (upon realizing the need for this resource) would first have to resolve the DNS, and that can potentially cause a delay. By implementing DNS prefetching, we have eliminated the potential delay.

### Preloading

Preloading is used to force the browser to download a resource as soon as possible because we believe it to be crucial to the page. This technique can preload all the assets (images, fonts, and so on) through a certain script. It can also preload HTML pages with the JavaScript already executed and the CSS already applied. In doing so, the preloaded page will be rendered and displayed instantly. This directive is best used for resources that are imperative for the critical rendering path, such as fonts, CSS, and so on.

```html
<link rel="preload" as="image" href="header-logo.svg">
```

The preload directive also requires the as attribute in its declaration, which is used to indicate the resource type that we wish to preload. The preload resource hint has a higher priority compared to prefetch and other resource hints. The browser may ignore other directives due to priority issues or a slow internet connection, but browsers must load the resources that are mentioned in the preload directive. Due to this, preloading is a powerful and useful instruction because it can allow us to make the browser download a resource immediately. We should use preload for resources considered critical to the current page, such as the main stylesheet, JavaScript files required for initial rendering, and web fonts.

However, preloading has its own drawbacks. Overusing it can lead to it interfering with the other tasks that the browser has scheduled since preloading overrides the priorities set by the browser itself.

Let’s summarize what we’ve learned so far in the table below:

<img width="664" alt="image" src="https://github.com/user-attachments/assets/7c5364d2-f54b-4128-a747-def971921626">

What is the difference between prefetching and preloading?

The prefetch and preload resource hints are used to improve the performance of a website by allowing the browser to load resources in advance. However, they have different purposes and use cases.

Prefetching tells the browser to proactively fetch a resource and store it in the cache for future use. The goal of prefetch is to reduce the latency and loading time of a resource if it is needed later in the current or future sessions. The prefetch directive is typically used for resources that are not critical to the current page, but may be needed in the future.

Preloading tells the browser to fetch and process a resource as soon as possible. The goal of preload is to improve the loading performance of the current page by reducing the time it takes for a resource to become available. The preload directive is typically used for resources considered critical to the current page and should be loaded as soon as possible.

In summary, the main difference between prefetching and preloading is their intended use case. The prefetch directive is used to prepare the browser for future use, while preload is used to improve the performance of the current page.

### Preconnecting

Preconnecting helps the browser establish connections to a domain in advance. This is helpful when we might need to quickly download a resource from a domain, such as a website using fonts from Google Fonts or requesting a JSON response from an API.

When a browser sets up a connection to a third-party domain, it can often take hundreds of milliseconds. Setting a connection in advance can help us avoid that delay. If we are familiar with DNS prefetching, then we might think that this is very similar to preconnecting. However, the preconnect directive has a distinct advantage over the DNS prefetch. While performing the DNS lookups, preconnect performs the TLS negotiations and TCP handshakes as well while the DNS prefetch will only do the DNS lookup and will require a round trip to do the other steps.

<img width="547" alt="image" src="https://github.com/user-attachments/assets/b67c0bc3-29bf-4a86-b2dc-5fe60380f3f1">

This directive eliminates the round-trip latency and saves time. This can speed up the load times by 100–500 ms by establishing connections to third-party origins earlier. A few hundred milliseconds might seem insignificant, but they can make quite a bit of a difference in the way a user experiences the performance.

```html
<link rel="preconnect" href="https://api.our-amazing-api.com">
```

For this reason, preconnect is best used for resources that are hosted on a different domain from the main page, such as a CDN or an external API.

Preconnecting is a great tool to have in our arsenal, but setting up and maintaining a connection to stay open is a costly operation, both for the client and the server. So, while it may save time, it might cause extra CPU usage.

Let’s update what we’ve learned so far in the summary table below:

<img width="653" alt="image" src="https://github.com/user-attachments/assets/f0f39edd-02dd-4062-9fc1-a0448bfb7400">

### Debouncing

Debouncing is a technique used to make a function wait a certain amount of time before it can be called again. It’s often used in conjunction with events like scrolling, key presses, mouse movement, and other events that bring great overhead with them if they’re called every time they’re executed.

Let's revisit the example above. Here, we can add a debounce() function to our scroll event and add a delay to make sure that it can’t make too many calls to the back-end APIs. The debouncing function makes the system wait until the debounced event has not been called in a certain amount of time. Any calls prior to this time expiring are dropped. This avoids causing performance issues from the API and server. This solution can also be further improved if the client-side code keeps track of where the user is and when they have stopped scrolling so that the client only requests the data needed at that point.

```js
function debounce(func, wait) {
  let timeout;
  return function() {
    const context = this, args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      func.apply(context, args);
    }, wait);
  };
}

function scrollEvent(){
  console.log('Scrolling');
}
const showChange = debounce(() => scrollEvent());
```

In the code snippet above, we declare a function called debounce() and provide it with the function  func() and the timeout value. The timeout variable is used to keep track of the current debounce timer. We set a new debounce timer using setTimeout. The timer waits the amount of milliseconds indicated in the wait variable before calling the original function func using apply and passing along the captured context and args.

Take a look at the diagram below:

<img width="538" alt="image" src="https://github.com/user-attachments/assets/64c65c0c-778d-4dd8-8248-4023f167b60e">

In the diagram above, we see a client that is constantly requesting data from the server. As soon as the request threshold has been reached, the requests sent by the user are dropped and not entertained until the debounce time limit has been reached.

## Circuit breaker pattern

The circuit breaker pattern is straightforward and has three states in its life cycle:

- Closed: This is considered to be the normal state. In the closed state, all the calls being made to the service pass through, and the number of failures is monitored.

<img width="537" alt="image" src="https://github.com/user-attachments/assets/3b3a12ff-233c-48d4-a767-36a7d577e07c">

- Open: If the microservice experiences slowness, the circuit breaker begins getting failures for requests to that service. Once this number of failures passes a certain limit, the breaker goes into the open state and activate a timeout for the service. In this state, any requests sent to the microservice are stopped by the circuit breaker immediately. Instead, the circuit breaker can send a response to the client, informing it about the timeout of the microservice and if an alternative service is available. It also advises the clients to send the requests to that service. The client can then either choose to redirect to a different instance of the service or choose to wait until the service is back online. This gives the microservice some time to recover by eliminating the load it has to handle. Once the timeout has expired, the breaker will pass to a half-open state.

Note: When the circuit breaker is in the open state, it prevents the requests from reaching the microservice. This is not a failure of the service but rather an interception by the circuit breaker to give the downed microservice time to recover. Without this intervention, microservices can fail in a cascading fashion, and rebooting such a complex system is often time consuming. Our overall service should be designed in such a way that if few dependent services are not available temporarily, the overall service degrades slowly (instead of a total outage).

<img width="556" alt="image" src="https://github.com/user-attachments/assets/dd102d7e-e21c-46a5-a3f5-6f3a5686ea35">

- Half-open: In this state, a limited number of requests are allowed to pass through to the microservice. This is done to test if the underlying issue is still persisting. Even if a single call  allowed to the microservice fails in the half-open state, then the breaker trips and goes back to the open state. However, if all the calls sent succeed, then the breaker resets to the closed state and begins operating as normal.

<img width="559" alt="image" src="https://github.com/user-attachments/assets/c3661dce-14eb-4757-94ae-92f605ca4f9d">

<img width="559" alt="image" src="https://github.com/user-attachments/assets/6e1696f6-fdc9-49a0-810d-43f9924a4364">

Note: A request is considered failed if the microservice isn't able to respond within a specific time defined for that service. A rejection from the circuit breaker is not considered as a failed service. In the half-open state, the circuit breaker rejects some requests by itself and allows limited requests to go through to the microservice to test its functionality.

Here, we depict the lifecycle of a circuit breaker and the events that trigger its different states:

<img width="553" alt="image" src="https://github.com/user-attachments/assets/ae5fa972-0a9b-4442-8a43-4c8ad0cb55f3">

### Cascading failures

A cascading failure happens when the failure of one service affects the performance of the services dependent on it, causing multiple services in the system to fail.

<img width="558" alt="image" src="https://github.com/user-attachments/assets/08705da2-0f88-4e5b-bc6a-1bbfd2310fe0">

<img width="559" alt="image" src="https://github.com/user-attachments/assets/0e74f2a7-6881-436b-9f37-5fc07222b300">

In the slides above, we have a system with interconnected services. If one fails, then the rest are at risk of failure as well, causing a cascaded failure of the system. The failed service is not able to respond to requests, causing the dependent services to have to wait for too long and eventually fail due to not receiving any response in time.

The circuit breaker pattern can help us in this regard by adding an extra layer that the services have to go through to make a call. This allows services to fail faster if they’re being unresponsive and protects the clients from potentially failing if the target service is unresponsive.

Let's visualize how circuit breakers can help us fix or mitigate the issue of cascading failures:

<img width="560" alt="image" src="https://github.com/user-attachments/assets/aed0a30b-19c6-4030-97f5-66caa02df149">

<img width="560" alt="image" src="https://github.com/user-attachments/assets/f85953b6-ebab-4518-9aea-52c19b6c9f74">

<img width="560" alt="image" src="https://github.com/user-attachments/assets/9113b40a-fe22-4c42-bc82-8e9f5acedece">

In the slides above, we have a system of interconnected services, each of which has its own circuit breaker. If Service 6 crosses the failure rate threshold, then the circuit breaker attached to it switches to the open state. As a result, any requests to Service 6 are stopped by the circuit breaker and sends a response to the requesting clients, allowing them to either wait or to be redirected to another instance of the service. This contains the failure to one service because the other services should immediately get responses of failures and can move on to other tasks.

As mentioned in the previous section, the open-state timeout of the circuit breaker gives the service time to repair. Once the timeout is over it will go into the half-open state. In this state, a fraction of the usual requests (in our case, two out of three) are sent to the service, if all of them succeed, then the circuit breaker goes into the closed state and the service starts functioning normally again.

### Circuit breaker pattern summary

In this lesson, we learned that the circuit breaker pattern is an extremely useful technique to include in our API design strategies. The purpose of this pattern is to allow services to "fail fast and recover ASAP." This pattern will help us in building resilient systems that can protect our system from cascading failures and  protect our client processes from being blocked due to having to wait for a response from a failed service.

On the surface, it might seem like circuit breakers have a similar function to rate limiters. Why should we use one over the other?

While they may seem to be similar on the surface because they’re both used to limit calls to an API or a service, upon further exploration, we can see that they have two different use cases.

In general, rate limiters are not very complex. They restrict the calls being made to a service in a specific period of time. They do this by monitoring the number of calls being made to a service. If the number of calls in the specified time frame exceeds the limit set by the system, then the rate limiter begins a timeout, during which any calls to the service are dropped. Once the timeout is over, the service returns to normal functioning. The rate limiter essentially helps us protect the server from overloading by controlling the throughput.

One of the main differences circuit breakers have with rate limiters is that they ensure the failure remains isolated to one component and are used to keep the client service safe when the target service is unresponsive. Circuit breakers are smarter and more resilient than rate limiters. This is because they’re able to detect failures and shut off access to the failed service, while rate limiters do no such thing. Therefore, circuit breakers are preferred with more complex systems, such as one with cascading services.

Circuit breakers are also concerned with the health of the service and the half-open state of the circuit breaker is there to check if the service is healthy enough to function properly. On the other hand, the rate limiter is not concerned with the health of the service. It only limits the number of requests made to a service.

## Managing retries (Optional)

Refer to the Educative module: https://www.educative.io/courses/grokking-the-product-architecture-interview/managing-retries

## Caching at different layers

From the description above, it may seem like caching at the server end would be adequate. However, that is not always the case. We can use caching at different layers in end-to-end communication to reduce latency. Here, we’ll mainly talk about caching at three different layers: client, middleware, and server, as shown in the illustration below.

<img width="552" alt="image" src="https://github.com/user-attachments/assets/9482d57c-556d-416b-b51a-0d07f1ec858f">

Client-side layer: This layer identifies the caching types on the client-side devices.

- Web browser cache: The browser simply checks if the required resources are locally available and returns the response. These resources are related to HTML, CSS, and other multimedia files required to build a website. Also, utilizing local data is usually faster than the other choices—for example, when the client has requested the data, and it takes several seconds to respond due to a slow Internet connection. The next time, the browser utilizes the local data without going to the network and responds within milliseconds.

Middleware layer: This layer identifies caches on the network between client and server networks.

- Internet service provider (ISP): The ISP mainly maintains two cache types. The first is the Domain Name System (DNS) cache to reduce the DNS query latency. The second is the proxy server that sits in the middle of the client and origin server.

- DNS: The main job of DNS is the resolution from the domain name to the IP address. The DNS resolver takes multiple round trips to different servers in order to get an IP address for the requested domain. The DNS caching caches the top-level domains and helps the DNS resolver to return the IP address with low latency.

- CDNs: This is a large-sized cache that is used to serve numerous clients requesting the same data. CDNs mostly provide static objects to the closest clients.

Server-side layer: This layer reduces server-side burden by using in-memory caching systems.

- API gateway cache: This cache stores responses to frequently requested API calls to avoid the recomputation of the same results. On similar subsequent requests, the response is served from the cache instead of downstream calls. It can store any data that can be transmitted over HTTP. The API gateway ensures the request is the same as the previous one by analyzing its request headers and query parameters. The API gateway does not have to worry about analyzing the request payload because we cached only GET requests for the most part.

- Web server cache: The web server cache stores the most frequently requested static web pages. In case of dynamic data, the request is forwarded and handled by the application server.

- Application server cache: Normally, the data is stored on the database, and fetching the data from the disk takes much more time than the RAM. This layer stores the frequently accessed data objects in different formats, and multiple custom caching solutions can be used on the application server, such as DynaCache.

- Database cache: The database cache is used to store the responses of queries that take time to execute and are frequently called, thereby reducing the query response time.

Note: DynaCache can store and retrieve the data objects, and it has a solution to remove invalid entries from the cache and make it up to date.

What should be the optimal size of the cache?

The cache size depends on the application’s requirements. For example:

- Number of users using the application
- Size and/or type of the data in the application
- Nature of the application—for example, read heavy or write heavy
- Cache access patterns—for example, sequentially or randomly access the content

Let’s assume that you’re working on a system that allows users to log in with their credentials and then monitor the road traffic in their area, which is updated every 30 seconds. The platform has a sleek UI that consists of HTML elements, such as navbars, headers, footers, and a container that displays the API data.

Given all this, what data should you cache to reduce the system latency? Also, what data should you cache on the client-side to reduce the burden on the server-side?

To reduce system latency, you should cache the road traffic data on the server-side using in-memory caching or distributed caching solutions. This approach minimizes database queries for data that’s updated every 30 seconds. On the client-side, caching user authentication data and UI elements like navbars, headers, and footers using local storage or session storage is advisable for quick retrieval. This strategy reduces the burden on the server-side by avoiding unnecessary data transfers for elements that don’t change frequently.

### HTTP caching headers

HTTP is the core of web APIs and provides cache support. When the server sends the HTTP response to the client, it also sends the cache headers in the response. These headers indicate whether the response can be cached on any caching layer. This section will explore different HTTP cache headers to know which headers are used for what purpose.

HTTP uses headers to set caching policies for the client and intermediate/shared caching devices. When a client sends the first request to any middleware for a resource, the middleware will forward the request to the origin server in case of unavailability to fetch that resource. In return, the server responds with the resource along with caching instructions in the caching header. The illustration below indicates the process in detail.

<img width="552" alt="image" src="https://github.com/user-attachments/assets/e9d6106d-6170-4e78-aa2a-a31d9fee997f">

The illustration above shows that the origin or the web server responds with the resource along with caching instructions in the Cache-Control header. The public and max-age headers indicate that the resource can be cached by both the caching devices and the clients for a specific time period.

Primarily, the caching headers describe policies in the following disciplines:

- Cacheability: This describes whether the content can be cached or not. For example, certain content may be cached for a specified amount of time, while others cannot be cached at all.

- Scope: The scope describes the possibility of caching the content at a particular caching layer. It may be possible to store some content on the client side but not on the middleware. For example, personalized content prefers to be cached on the client side, and popular public Tweets prefer to be cached on the middleware cache, such as CDNs.

- Expiration: As the name suggests, there is a possibility of storing data for a fixed time on a caching layer. In certain cases, this expiration time may be extended.

- Validation: Since the expiration of cached content is a norm, it’s important that caching headers allow validation with the origin server and update the content with a new one before fulfilling the incoming requests.

Mainly, the Cache-Control header is used both in client requests and in server responses via some directives. We require some other headers as well to validate the content. Let's discuss headers that support the caching policies.

<img width="452" alt="image" src="https://github.com/user-attachments/assets/347568cd-b2cf-43fb-8585-ec254f239c11">

Note: Etag and Last-Modified both are useful, but Etag may provide more precise information about the resource. For example, if the resource is modified frequently within a very short interval, then Last-Modified might remain the same for the frequent changes (due to unavailability of timestamp with fine-enough granularity). On the other hand, Etag always generates a unique ID for each change made to the resource's content.

- If the max-age and public directives are given together in the Cache-Control header, then the content is cached for the number of seconds specified in the max-age directive on all the caching layers from server to client. If, however, public is replaced by private, then this content is cached only by the client for a given time.

- If max-age and s-max-age are given together, then the value of max-age is applicable to the client and the value of max-age overrides the value of s-max-age for the shared caches on any middleware or server layer.

- If both Etag and Last-Modified are provided by the server, then If-None-Match and If-Modified-Since are sent from the client’s end for validation. The expired content gets updated by the server.

As traffic grows on the Internet, the load on the servers increases day by day. Caching helps us reduce loads on servers or networks and provides low-latency responses to the clients. However, caches have some drawbacks—they are expensive, limited in size, and may contain stale data. Furthermore, caches are not generally suitable for storing dynamic content. Considering the advantages of caching, we need to implement proper cache policies to keep content updated in the cache. Also, caching at all layers might be complex, especially when we want to achieve consistency with the origin server.

Should caching be performed on every layer?

The answer depends on a number of things, including the content type. The server defines the policies through its caching headers. For instance, if the content is static, such as logos, CSS, or scripts of the sites, then the server sends a public directive in the Cache-Control header to indicate that the content can be cached on any layer. In contrast, if the content is sensitive, such as the user’s personal information, then the server sends a private directive so that only the client layer will cache the content.

## API monitoring (Optional)

Refer to the Educative module: https://www.educative.io/courses/grokking-the-product-architecture-interview/api-monitoring

