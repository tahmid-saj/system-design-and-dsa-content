# API architecture styles

## Architecture styles overview

We’ll consider three commonly used architectural styles. Keep in mind that each style has its pros and cons, and even if the majority of developers adopt REST, it may not be suited for our API.

### REST

Representational state transfer (REST) is by far the most popular architectural style. The industrial practices for REST API rely heavily on the HTTP protocol and are considered easy to understand, use, and manage. Its familiarity and simplicity are its greatest strengths, but it may struggle in event-driven environments. It performs well when scalability and modifiability are our API's desired characteristics. We'll expand on REST in the upcoming lessons.

### RPC

The remote procedure call (RPC) is the earliest form of API (developed in the 1980s). It mostly deals with databases and widely works on JSON and XML formats. The most vital concept in RPC is the procedure because it doesn't have to function locally and can be handled remotely in the system.

There are two types of RPCs in regard to architectural style:

- gRPC: In 2015, Google designed a general-purpose RPC, known as gRPC. It's a framework that implements RPC-based APIs using protocol buffers for serialization. It’s constantly being upgraded with new features and has reduced latency due to its compression methods.

- SOAP: Simple object access protocol (SOAP) was developed in 1999 by Microsoft. It uses XML, and to implement it, we have to stick to strict rules about encoding, structuring messages, and handling requests. It has built-in error handling, and each error will be accompanied by the relevant information to resolve it. Due to the strict and inflexible nature of SOAP, the requests can get large, which can carry overheads. Few major real-world services still use SOAP, and it’s largely considered an obsolete technology today.

### GraphQL

GraphQL serves as the query language specification for APIs. It's a newer technology developed by Facebook in 2012. It was developed to overcome the shortcomings of REST, providing an alternative to developers. Applications like GitHub and Yelp have opted to use GraphQL over REST, even though its release was fairly recent.

## REST

REST was developed to scale the internet, and adopts an approach to follow the below constraints:

- Client-server

- Cache

- Stateless

- Uniform interface

- Layered system

- Code-on-demand

We explain each constraint in detail below.

### Client-server

Client-server is the most commonly employed architectural style for network-based applications. A server component that provides several services listens for a request for those services. The client communicates with the server via the Internet (connector), waiting for a request to be processed by the service. The client's request is either rejected or fulfilled by the server, which is communicated back to the client via a response.

Separation of concerns is the core principle that focuses on client-server constraints. In order to increase scalability, the server component should be made simpler through adequate functional separation. This simplification involves consolidating all user interface features into a single client component. Both of these components can be developed (evolved) separately as long as the interface stays the same.

### Cache

A cache is an intermediate component between the client and server that contains the response to the earlier requests. These cached responses are used for equivalent and identical requests instead of directing requests to the server. The network efficiency and user's perceived performance can be improved using cache on the client's side.

Note: The response data can be cached on the client's side and utilized for similar/equivalent requests.

This constraint requires that the response data be explicitly or implicitly marked cacheable or non-cacheable. If the data in the response is marked cacheable, the client's cache can reuse them later for similar requests.

The major tradeoff with the cache constraint is that it can reduce reliability and consistency if stale data in the cache varies considerably from the data received in the direct request to the server.

What could be the approach to check the validity of the data (or a web page) in the cache?

There are a few ways to check whether the page needs to be fetched again.

- One method is to use the Expires HTTP header in the response that would determine when the page needs to be fetched again.

- Another approach is to use some heuristics. For example, if a page is not modified in the last year—indicated by the Last-Modified HTTP header—it is improbable that it will change in the next hour. However, such heuristics should be used with extra care.

- Another helpful approach is to use conditional GET. Through this request, the server returns a short reply if the cached page is still valid; otherwise, the server sends the complete response.

Let’s look at the conditional GET request as given below.

<img width="688" alt="image" src="https://github.com/user-attachments/assets/d5f3918d-11cf-431f-a1a3-904be61d027f">

In the GET request above, the If-Modified-Since HTTP header makes the GET request conditional. The If-Modified-Since statement is self-explanatory, asking for a page from the server modified after Fri, 14 Aug, 2022 15:35:47 GMT.

### Stateless

This constraint refers to the fact that no session state is allowed on the server; it should be entirely kept on the client. Moreover, each request from the client should contain all the necessary information for the server to process the request.

Note: The server should not store any data from the previous requests.

The stateless constraint improves the following performance measures:

- Reliability is increased because it allows the server to recover from partial failures easily, and no data loss occurs for the users. For example, if there is no data kept on the server, then server failure wouldn't disturb the client's side activity or any previous requests from the client.

- Scalability is improved because no user data is stored on the server, so the data is immediately removed after processing a request, which frees the resources for other incoming requests. For example, in this case, the server can handle more requests than it could have handled while keeping the limited users' data.

- Visibility is improved because the server does not have to look for extra information rather than the data in a single request to determine its entire nature. For example, if a request needs to retrieve data from the database, it will contain all the necessary information to initiate database queries. So a monitoring system can easily determine the purpose of a request.

Like other architectural options, this constraint also has a tradeoff. By sending repeating data in a succession of requests (since the data/information can’t be kept on the server), it might reduce the network’s performance.

### Uniform interface

Since a system is composed of several components, for a system to work in the desired way, the components' interaction should be directed by a uniform interface. By applying the software engineering concept of generality to the component interface, the overall system design may be made simpler and the visibility of how these components interact can be enhanced. Independent development of the components can be increased by decoupling their services from their implementation.

Note: The exchange of data should be standardized between the components.

The disadvantage of the uniform interface is that it might degrade efficiency since the information has to be transferred in a standardized form rather than the format required by the application. On the other hand, if any of the components will not follow the standards, the web's communication system will break.

<img width="446" alt="image" src="https://github.com/user-attachments/assets/2021e7fa-da36-4c38-95cd-f3d10c2cbc2b">

In addition, the following architectural constraints are proposed to guide the behavior of the components:

- Identification of resources: In REST, the abstraction of information is a resource. Any information that can be named is a resource—for example, a document, image, video, or a collection of other resources or objects. These resources are addressed by a unique identifier called a Uniform Resource Identifier (URI). For example, the URI uniquely identifies a specific website's root resource.

- Manipulation of resources through representations: Representation of data is the sequence of bytes and the relevant metadata. In this constraint, the clients have the liberty to manipulate the representation of resources. In other words, the same exact source (documents and objects) can be represented to different clients in different ways. For example, a web page can be rendered as an HTML page in a browser while it is shown in XML or JSON format in a console program.

- Self-descriptive messages: This is another constraint that ensures a uniform interface between different components. A self-descriptive (response) message contains all the information the client needs to understand—for example, 200 OK indicates the successful execution of the client's request. There should be no need for extra information—documents or any other data— to understand the message.

- Hypermedia as the engine of application state (HATEOAS): A client can request information dynamically through hypermedia. Hypermedia is a nonlinear media of information containing different types of resources, including images, videos, hyperlinks, etc. The resources requested from the server should also contain links to other related resources. Links are the components that allow users to traverse information in a relevant and directed way.

### Layered system

The layered system constraints imposed an organized hierarchy of an intermediate set of components (referred to as a layer) between the client and the server. This constraint enables client-server communication to be intercepted by other essential components to make the communication easier, secure, and properly directed to the intended servers.

Note: Adding more components between client and server assists and directs the communication between them.

The layered approach enhances the decoupling across multiple layers by making it visible to only the adjacent layers and hiding it from the other layers. For example, in the figure below, only proxy and downstream servers know that the request goes through the load balancers, but the clients might be unaware of it.

The layered system constraint improves the following:

- Evolvability because each layer can be modified or added with advanced functionality without affecting other layers.

- Reusability because the existing components that can be reused in one form or the other instead of reinventing or creating from scratch.

An example of a layered system is adding a proxy as well as load balancing and security checking components between client-server communication.

One of the major drawbacks of the layered system is that the requests (or responses) might need to traverse more hops, which usually adds latency.

<img width="554" alt="image" src="https://github.com/user-attachments/assets/4389b886-c7fc-45b6-a159-0945d67b22d2">

### Code-on-demand

This constraint enables web servers to send executable programs (code) to clients, such as plug-ins, scripts, applets, and so on. Code-on-demand establishes a technological coupling between clients and servers. The client application must understand the code it downloads from the servers; therefore, this constraint is the only one in the web's architectural style that is considered optional. For example, certain applications require additional plug-ins to be installed on the client side. Therefore, such constraints can't be made compulsory in the REST architecture.

Note: A client application can request servers for codes (scripts, applets, plug-ins) that can be executed on the client side.

The major advantages of the code-on-demand are:

- Extensibility: The client's extensibility is improved because it has the independence of how certain things can be done.

- Performance: The user's perceived performance is improved because certain things happen locally on the client's side instead of regular interaction with the server.

One drawback of this constraint is that scripts sent from the server may contain malicious code that could interfere with the client's processes and might interrupt other activities. For this purpose, a sandbox on the client side is used to avoid the potentially harmful activities of the script. In the sandbox, the code is executed in an isolated and safe environment where it’s being observed for harmful activity, which can be blocked on the spot, and the user is notified accordingly.

Another drawback is that the monitoring system may be unable to track the request's full nature due to the server sending code instead of simple data.

Note: Adhering to all six constraints is only possible in an ideal scenario. As we have seen, some of the constraints are conflicting—for example, if we conform to the stateless constraint, we can achieve visibility; however, at the same time, using the code-on-demand constraint reduces the visibility of the full nature of the request. Therefore, API designers should follow the maximum possible constraints while designing a RESTful web API.

### REST constraints summary

<img width="670" alt="image" src="https://github.com/user-attachments/assets/f9893e5b-4103-4a1c-9778-02cef819a361">

What is the difference between REST and HTTP?

REST is a web architecture style that proposes some constraints that should be used to design web or mobile applications. However, HTTP is the protocol, or, in simple words, a method that enables us to achieve the constraints proposed by REST. Although HTTP was designed earlier than REST, fortunately, it has all the features that can be utilized to make the World Wide Web conform to the REST constraints. Therefore, HTTP is widely adopted in this regard.

## REST APIs

Many programming languages and protocols use CRUD operations for manipulating data. For example, in the SQL database, we use insert, select, update, and delete. Similarly, interacting with the REST application often involves CRUD operations because the REST-based applications are built around resources that need to be created, read, updated, and deleted. REST APIs are protocol agnostics; however, the underlying protocol they use widely for communication is HTTP. Therefore, the CRUD operations can be easily mapped to major HTTP methods, as shown in the following table.

<img width="680" alt="image" src="https://github.com/user-attachments/assets/aa172e34-ca78-42eb-9b73-2a4cc08ede47">

### What makes a REST API?

The following are constraints which help make the API RESTful:

- Client-server: In the client-server setup, communication is initiated by the client via HTTP protocol by calling different HTTP methods. Since client and server are considered independent of each other, applications on both sides can evolve independently without affecting each other.

- Cache: Caching responses on the client side helps to respond to similar requests, which reduces the client’s perceived latency. The cache header in the HTTP response is set if there is a need to keep the response data on the client. Similarly, it can also have the information about the time after which the data is marked invalidated.

- Uniform interface: This constraint enables different components to exchange data in a standard way. Therefore, there is a need to have a protocol that provides a standard way of communication. Fortunately, HTTP provides us with the standard way of communication in the form of HTTP methods. Every method has some essential components that should be there to send a request. Similarly, the response also has some standard format that a server sends to the client. For example, in the following HTTP method, we have name, URI, HTTP version, hostname, and data sections. These sections are common in every POST request.

<img width="748" alt="image" src="https://github.com/user-attachments/assets/2b6f5e9c-75f3-411b-834e-1a0c4bfecf04">

Note: The HTTP protocol was created from 1989–1991, while the REST architecture style was proposed in 2000. This shows that HTTP was not created for REST, but REST APIs adopted HTTP as a standard protocol. It indicates that REST can be implemented via any protocol conforming to all the constraints of REST, where HTTP is the best choice. This is because HTTP fulfills most of the constraints that the REST architecture styles proposed.

- Stateless: REST APIs use HTTP requests that are, by default, stateless. Each request is processed independently without a need for prior data or information.

- Layered system: This constraint allows a user to deploy different services on different servers. For example, deploying APIs on server I, storing authentication information on server II, storing data on server III, and so on. For this purpose, when using an HTTP request, a client doesn’t know whether it is connected with the end server or any intermediate server. Developers that adhere to this rule can change server systems without affecting the fundamental request-response process.

- Code-on-demand: This constraint is optional; however, a client can request the server for some scripts. When a client requests a base object to a server via the HTTP protocol, all the script files and other objects are downloaded and rendered on the client side upon a user’s or client’s event.

<br/>
<br/>

What does the RESTful API client’s request contain?

In order for a request to follow the RESTful paradigm, it should include the following:

- Unique resource identifier: A server uses unique resource identification to access a resource requested by a client. For this purpose, the server uses a URL to specify a path to the resource.

- HTTP methods: Since there is a close resemblance of the HTTP methods with the CRUD operations, developers prefer to use HTTP to implement RESTful APIs. These methods are used to tell the server what to do with the resources.

- HTTP headers: HTTP headers are used to exchange the metadata with the server. For example, some headers are used to exchange the client’s information, rate limiting details, request status, data formats, data, parameters required for processing a request, and so on.

Note: Another field is the request body that should be included in a RESTful API request. However, this is optional because some requests don’t need the request body.

What does a RESTful API response contain?

In response to a request from the client, the following data should be included in the response in order to conform to the RESTful API paradigm.

- HTTP status code: The response from the server should contain a status code to give a clear picture to the client about the request status.

- Response/message body: The response from the server also contains the message body that includes the resource representation. Based on the information in the request headers, the server chooses an appropriate representation format. Clients may request data in XML or JSON formats, which specify the format of the data’s plain text representation. For example, if we request a specific book title, Grokking the API Design, the response may contain the following representation of the data:

<img width="722" alt="image" src="https://github.com/user-attachments/assets/6c2494f4-c0a4-4cee-a3e5-c95fbe257bc8">

- HTTP headers: The response also contains headers that provide more context about the response, server, encoding technique, data, content type, number of requests made by the client, and so on.

### REST API best practices

Now that we understand what makes an API RESTful, let's discuss some best practices when developing RESTful APIs.

- Exchange of data via JSON: The REST APIs should use JSON format for sending and receiving data. The other formats—like XML and YAML— lack some common procedures for encoding and decoding the data. On the other hand, a wide range of server-side technologies offer built-in methods to parse and manipulate JSON data. For example, JSON.parse() and JSON.stringify() are used to convert a JSON string to a JSON object and convert a JSON object to JSON string, respectively.

- Nesting on endpoints: Different endpoints containing the associated information should be interlinked to make them easier to understand. For example, imagine a platform where multiple users can post their articles. A nesting like https://www.example.com/posts/user seems logical. Similarly, if we need to get comments for a post, we should add /postId/comments at the end of the /posts path. The resultant endpoint will become https://www.example.com/posts/postId/comments. This is a good practice through which we can avoid mirroring database structure in our endpoints, keeping the data safe from attackers.

- Use nouns instead of verbs in the paths: We should strictly avoid using verbs instead of nouns in the endpoints. The verbs represent methods (the HTTP already has such methods), while the noun represents entities. Using verbs in the endpoints is not useful and makes the endpoints unnecessarily long. For example, instead of the https://www.example.com/posts/getUser endpoint, which has the verb get, we should use https://www.example.com/posts/user.

- Error management and standard error codes: We should use HTTP status codes regularly when an error occurs to indicate the nature of the error. This helps the API consumers to understand the problem and handle it on their end if needed. Moreover, we should also add an error message with the status code to help users to take some corrective measures.

- Filtering and pagination: Sometimes, the database gets incredibly large. Fetching data from such a database becomes time-consuming and reduces performance. Filtering reduces the requested information from the server and thus the end-to-end query latency. For example, the https://www.example.com/posts?author=fahim endpoint will fetch the posts authored by fahim instead of listing all the posts. Similarly, there is a need to paginate data to fetch partial results at a time to minimize page loading time and reduce the burden on the client for loading a bulk of data all at once. Filtering and pagination reduce the usage of server resources and increase performance.

- Adopting standard security practices: Another best practice we should adopt is making our API invulnerable to malicious attacks. In addition, the communication between the client and server should also be private. More importantly, we should also ensure that the server doesn't send unrelated information to unrelated users. This way, we can restrict users to the data intended for them rather than allow them to access other users' data. For this purpose, we can use HTTPS running on top of SSL/TLS. For example, https://www.example.com/ runs on TLS, while the http://www.example.com/ doesn't use any TLS features.

- API versioning: We should offer different versions of the API if we make any changes to it that might affect customers. Versioning can be done in line with semantic versions, like the majority of contemporary software—for example, 2.1.6, to denote major version 2, minor version 1, and the sixth patch. This allows us to gradually discontinue old endpoints rather than forcing everyone to migrate to the new API simultaneously. The v1 endpoint may still be useful for individuals who don't want to migrate, while the v2, with its eye-catching additional features, can benefit those who are ready to switch. API versioning can be done by adding /v1 or /v2 to the API path—for example, https://www.example.com/v1 and https://www.example.com/v2.

- API documentation: Another good practice is to have comprehensive API documentation to help developers and other consumers to understand the API and use it in their applications. A good API document consists of the following:

  - Detailed and clear explanation of API endpoints and all other functionality with a proper use case

  - SDK implementation provided in several state-of-the-art programming languages

  - Clear instructions related to the integration

  - Clear updates on the API lifecycle

  - Error messages and proper status codes to convey clear information about the error

<br/>
<br/>

REST APIs can support the following file formats:

- application/json: JavaScript Object Notation (JSON) is the most flexible and feature-rich format that is used for most of the resources.

- application/xml: eXtensible Markup Language (XML) is used rarely for some selected resources.

- application/x-wbe+xml: This is the Decision Server Event internal XML format. It supports importing, exporting, and deploying event projects, hosting events, and event runtime.

- application/x-www-form-urlencoded: This is sometimes used to send data to the server in a request, mostly to work around URI length limits when querying the REST API. For example, in this encoding, the variables and values are separated using the equal = symbol—for example, VariableOne=ValueOne&VariableTwo=ValueTwo. Moreover, the non-alphanumeric characters are also replaced with a percent sign and two hexadecimal digits, %HH.

- multipart/form-data: When sending a large amount of data or text containing non-ASCII characters, the x-www-form-urlencoded is inefficient because for each non-alphanumeric character, it will take three bytes instead of one. Therefore, multipart/form-data should be used to submit forms containing files, non-ASCII characters, and binary data to avoid sending extra bits of data.

Note: Whenever the data is sent in JSON format to the client, the server should set Content-Type in the HTTP header to application/json . This way, the clients look at the Content-Type header and correctly interpret JSON data.

<br/>
<br/>

Why is Hypertext Transfer Protocol (HTTP) an obvious choice for implementing REST APIs?

As we know, REST is an architectural style independent of any protocol. However, to bring it into practice, there needs to be a protocol that should follow REST constraints. Fortunately, HTTP’s logic matches some of the concepts of the REST style; therefore, developers often choose HTTP for creating REST APIs. Let’s list all of the REST constraints that are supported by default by HTTP:

- HTTP operates in a client-server model.
- HTTP includes headers that mark whether an object should be cached or not.
- HTTP includes verbs (methods) that determine the desired action of HTTP requests, providing a uniform communication interface between different entities.
- HTTP uses a stateless operational model.

<br/>
<br/>

### REST API advantages

REST architecture influences how we view, edit, and transfer material online. It’s the preferred choice of many well-known web services. Let's look at the reasons behind this choice in the list below:

- Adaptability: The REST APIs are adaptable because they are able to transfer data in a wide variety of formats and handle a wide variety of requests.

- Scalability: Regardless of size or capabilities, they are made to communicate with any two pieces of software. A web application's REST API will be able to swiftly handle the growing volume and variety of queries as it expands and adds more services.

- Compatibility: REST APIs employ existing web technologies, so they are very simple to create and operate. A REST API just requires the resource's URL to request it.

## GraphQL

### REST API drawbacks

In a REST API, we hit a URL and receive whatever data comes back. However, there are certain problems with how a REST API fetches data, as given below:

- Multiple requests problem: A REST API sends multiple requests whenever data required by the application resides on multiple endpoints. There is a need for a mechanism to fetch data from multiple endpoints in a single request.

- Overfetching and underfetching: Often, in a REST API, the data fetched in response to a single request is either a very large amount or a very small amount that does not serve the purpose of the application's request. Therefore, we need an approach to fetch the exact amount of data needed by an application.

Let's discuss these drawbacks in detail in the following sections.

Note: In this lesson, we’ll use SWAPI (Star Wars API) for demonstration purposes to convey better ideas of GraphQL to our learners.

#### Multiple requests problem

In a REST API, we fetch different types of data from different access points (URLs), which often causes us to send various requests to fetch the desired data. For example, to access the starships, planets, and films data using SWAPI, we would need to make multiple requests to the respective endpoints:

- For starships, we need to access the https://swapi.dev/api/starships/ endpoint.

- For planets, we need to access the https://swapi.dev/api/planets/ endpoint.

- For films, we need to access the https://swapi.dev/api/allFilms/ endpoint.

In the end, after the successful fetching of required data from multiple endpoints, the client starts rendering it.

<img width="376" alt="image" src="https://github.com/user-attachments/assets/c1bc5a4c-0831-4bcb-a32f-4fcde7d0789d">

#### Overfetching and underfetching

REST often suffers from two other types of problems: Overfetching and underfetching. Overfetching refers to retrieving extra information than what is needed, while underfetching is when the fetched information is not enough for an application. The problem with overfetching is that it uses extra resources and may burden a server with an additional load. Due to underfetching, the client makes more requests to the server to access the desired data.

For example, the following GET request returns a starship data having an ID equal to 10.

<img width="780" alt="image" src="https://github.com/user-attachments/assets/4f08b24b-7ddd-4f91-8fe1-b94dead75053">

The response to the above GET request receives the following data in JSON format. For example, if we require just the name, length, and cargoCapacity, the GET request will instead return all the following data consisting of other attributes of the starship having an ID equal to 10.

<img width="779" alt="image" src="https://github.com/user-attachments/assets/a13898ff-9994-4c8a-ac8d-ff5b3a4eaf08">

The underfetching occurs when a specific URL doesn't provide the required information. In such cases, the clients make additional requests to fetch the required data. This can lead to the n+1 requests problem, in which the client first downloads a list of endpoints and then makes one additional request per endpoint to fetch the required data.

Can underfetching lead to issues like overburdening the server?

Yes, like overfetching, underfetching can also overburden a server due to too many requests to get the desired data.

Both underfetching and overfetching cause issues. The extra round trips to get desired data increase latency. Also, sending too much data to the client, most of which the client throws away, is a waste of data and adds client-perceived latency that makes an application feel sluggish.

### GraphQL

GraphQL is a new API standard and a query language specification developed by Facebook in 2012 to handle the problems in the REST APIs. Before making it open source in 2015, Facebook had used it internally as an alternative to the common REST architecture. GraphQL is analogous to the SQL queries in relational databases, where we can build a query to fetch the required data from multiple tables. GraphQL works in a similar way for APIs to fetch data from multiple endpoints in a single request.

Note: From a client's perspective, it will be a single request, but at the server side, we’ll probably need to make many round trips inside the data center to different components, like databases, caches, and so on. However, that isn’t bad because latency inside the data center is very low as compared to latency between client and server.

GraphQL is sometimes confused with the database, but it’s actually a query language for APIs. Therefore, it can be used in any context where an API can be used. GraphQL is also transport agnostic, just like REST, but it typically uses HTTP as the underlying protocol for its operations.

### GraphQL components

The implementation of GraphQL can be divided into two components: the GraphQL server and the GraphQL client.

#### GraphQL server

The GraphQL server takes our APIs and exposes them to the GraphQL client via an endpoint. It has two main parts:

- Schema: A schema is a model of the data and defines relationships between the data. Based on the schema, the server specifies what types of queries and data a client can request.

- Resolve functions: A schema can tell us what types of data a client can request but lacks information about where the data comes from. Here, the resolve functions specify how types and fields in the schema are connected to various backends. In other words, the resolve functions provide directions to convert GraphQL operations into data.

#### GraphQL client

The GraphQL client is the actual front-end component that allows us to accept queries, connect to the GraphQL endpoint, and issue queries to gather data. It may be a single-page application, a content management system (CMS), a mobile application, and so on.

<img width="586" alt="image" src="https://github.com/user-attachments/assets/58404442-4445-4849-b137-3a1140d1d51b">

### Data manipulation using GraphQL

GraphQL offers us two types of operations: queries and mutations. We have seen how data can be fetched using queries. However, there is also a need to have a mechanism to manipulate data on the server side. GraphQL uses operations called mutations in order to insert new data or modify the existing data on the server. We can think of GraphQL mutations as the equivalent of POST, PUT, PATCH, and DELETE methods used by REST.

#### GraphQL mutations

Mutations in GraphQL are defined in a similar way as we define functions; in other words, mutations also have names and selection criteria. There are three types of GraphQL mutation operations.

- Insert mutations: These are used to insert a new record on the server side.

- Update mutations: These are used to modify an existing record in the database.

- Delete mutations: These are used to delete a specific record from the database.

Let's insert a new record into the database using an insert mutation.

Assume that we have students' data stored in the database, including name, rollNo, and degreeProgram. The following mutation will insert a new student into the database after specifying values for name, rollNo, and degreeProgram. The AddNewStudent schema is defined on the server side, while addStudent is the function that a client can use to insert data in the database.

<img width="779" alt="image" src="https://github.com/user-attachments/assets/e5f247b4-0a99-4fbd-ab12-423284e48d62">

#### GraphQL queries, and request and response format

A GraphQL query requests only the data that is needed. A query is defined using the word query, and inside it, we mention other objects and the attributes whose values need to be fetched.

Following is a GraphQL query requesting the attributes name, length, and cargoCapacity of the object starship having an ID equal to 10.

<img width="779" alt="image" src="https://github.com/user-attachments/assets/e5935104-2689-4e44-947e-706942659ca4">

The response to the preceding GraphQL query is in JSON format that matches the shape of our query, shown below. The response consists of the data we requested and has returned the name: Millennium Falcon, length: 34.37, and cargoCapacity: 100000.

<img width="779" alt="image" src="https://github.com/user-attachments/assets/fed7ed08-adb7-4a4f-8d67-f5e18240b83f">

GraphQL queries can be nested—for example, let's modify the query above and request the name, diameter, and climates of a planet having an ID equal to 5.

<img width="780" alt="image" src="https://github.com/user-attachments/assets/a8c08861-2af5-4f21-9de6-1dc2f59e67e4">

In the query above, we are now requesting more information about another object that is a planet having an ID equal to 5. An advantage of the GraphQL query is that we can request different types of data within a single request. The following response now consists of the starship as well as the planet data.

<img width="779" alt="image" src="https://github.com/user-attachments/assets/e1354667-4372-48cc-8450-d8e77f336b30">

### How does GraphQL fill the gaps in REST?

GraphQL resolves both the shortcomings of the REST API in the following ways:

- Multiple requests problem: GraphQL allows us to access multiple endpoints in a single query, which eliminates the first problem in the REST API. The following example shows a query accessing starship, planet, and allFilms data in a single request. So instead of sending multiple requests using the REST API, GraphQL does the job in a single query.

<img width="774" alt="image" src="https://github.com/user-attachments/assets/dd4c8ec5-a552-4769-85b3-9773ac7aa4e7">

- Overfetching and underfetching: Similarly, a single GraphQL query also addresses the overfetching and the underfetching problem by accessing the exact information needed for an application. In the example above, we require some specific attribute values, and the response to the query only contains the values of the starship, planet, and allFilms, as shown below:

<img width="770" alt="image" src="https://github.com/user-attachments/assets/17f66979-1b17-42cb-b246-9ca035dda131">

<br/>
<br/>

Is it possible to imitate the behavior of GraphQL by requesting only the desired data via the REST API?

Yes, REST APIs use a partial response strategy to get the desired data. For example, GET /planets will show all the planets available on the endpoints. However, in the partial response strategy (also called filtering), we define some conditions in the request. For example, GET /planets?result=find(radius, gravity) will return the radius and gravity of all the planets.

If it is possible to fetch only the desired information using the REST API, then why is there a need for GraphQL?

The partial response strategy, or filtering, is a flexible approach to getting the required information via REST APIs from a single endpoint. However, GraphQL benefits us the most in a case when we frequently need to retrieve desired responses from multiple endpoints at the same time. Additionally, we can define which fields and it's sub-fields we need in GraphQL queries, which is more flexible than REST.

### GraphQL drawbacks

Apart from the features that GraphQL provides, there are certain areas for improvement. For instance, it’s more complicated to implement than REST and incurs extra complexities. From a maintenance perspective, there are three main drawbacks when opting for GraphQL:

- Error handling: REST provides us with a comprehensive response status that tells us about any error that occurred. In GraphQL, we need to parse the response to understand the error, which increases complexity and adds to user-perceived latency.

- File upload: GraphQL specification does not include file uploads. This functionality is left to the developers and their choice of implementation, which includes one of the following strategies. These strategies are more complicated than the features REST provides:

  - Using a mutation with the Base64 encoded blobs, which makes the request larger and more complex to encode and decode.

  - Allocating dedicated servers or REST APIs to upload the files.

  - Using third-party libraries, such as graphql-upload.

- Web caching: GraphQL can work with multiple endpoints; therefore, caching data at different levels is a bit harder.

## gRPC

API performance is highly dependent on the architecture of the back-end services. Network communication and system scalability are two important factors directly affecting the performance of web services. Technologies like Simple Object Access Protocol (SOAP), JSON-RPC, RESTful services, etc., have some limitations, such as tight coupling, additional processing, header overhead, interoperability issues, and so on. This led Google to develop the "Stubby" project in 2001 to address the problems above for its backends. The gRPC is an extended version of the Stubby project that was made public as free open-source software (F/OSS) by Google in 2015 and was accepted as an incubation project by CNCF in 2017.

gRPC is an RPC framework that achieves high performance by leveraging the multiplexing functionality introduced in HTTP/2 to create logical subchannels to support the following types of connections:

- Request-response: The client can send a single request, and the server can reply with a single response.

- Client streaming: The client can send multiple requests, and the server can reply with a single response.

- Server streaming: The client can send a single request, and the server can reply with multiple responses.

- Bidirectional streaming: The client can send multiple requests, and the server can reply with multiple responses.

Note: Subchannels are a logical management of streams created by multiplexing an HTTP/2 connection.

<img width="763" alt="image" src="https://github.com/user-attachments/assets/991723c0-dcfc-4b73-8a81-16b796d2fc7a">

gRPC internally manages these HTTP/2 streams to create subchannels and abstracts the details from the client at the application level. A generic gRPC client-server communication is illustrated in the diagram below:

<img width="466" alt="image" src="https://github.com/user-attachments/assets/b7bcac73-fd70-475c-ab52-662975d76862">

The overall workflow of gRPC is the same as the normal RPC architecture. For example, it calls a remote procedure, then the local code abstraction is handled by the gRPC code stub, and it then communicates with the server-side gRPC over an HTTP channel and executes the remote procedure, and finally returns the result. However, gRPC has added a lot of improvements by using HTTP/2 streams and other components that are discussed in the next section.

In gRPC, Protobuf is the default interface definition language (IDL), which provides a mechanism for serializing data into a cross-platform binary format that can compress headers to achieve high performance. gRPC also has a built-in method for generating client and server code stubs to speed up the development process and manage changes later. Although gRPC was released in 2016, it has quickly gained popularity, and companies such as CoreOS, Cisco, Square, Netflix, Carbon3D, Allo, Google Cloud Services, and others are using it in their production environments.

Note: The gRPC core is implemented in only three different languages: C, Java, and Go. However, it officially supports more than a dozen different languages by wrapping these supported languages in a C core, making it suitable for various development environments.

Before diving into the gRPC communication cycle, let’s look at some of its main components for a better understanding.

### gRPC components

- Channel: It’s an HTTP/2 connection associated with a specific server-side endpoint. Clients can also set default properties of gRPC, such as turning compression on or off when creating a channel.

- Subchannel: It’s the logical management of HTTP/2 streams within a channel, where each subchannel represents a connection between a client and a server when load balancing across multiple available servers. Each channel has a one-to-many relationship with subchannels.

<img width="637" alt="image" src="https://github.com/user-attachments/assets/c4fc33ed-0aca-4452-965f-75e9eb984aff">

gRPC also provides some pluggable components that can be added or removed according to business needs. Some of the pluggable components are listed below:

- DNS resolver: It’s a DNS service that resolves an endpoint URL to its IP. It can also return multiple IPs against a request based on the number of back-end servers serving that URL.

- Load balancer: It’s a scheduler that directs requests to the backend according to the load balancing policy. This enables gRPC to distribute the load of different subchannels among the pool of back-end servers and makes the system highly scalable.

- Envoy proxy: It’s an intermediate server for clients (browsers) running on HTTP/1.1, making them compatible with the HTTP/2 protocol. There are several other proxy options available, but this is the most commonly used proxy for gRPC.

Interestingly, the DNS resolver and load balancer are on the client side and decide which gRPC server to choose to create a subchannel. The client-side load balancing technique achieves high performance by avoiding extra hops when using server-side (proxy) load balancing. But it also brings up client trust issues, which may not be an appropriate option when dealing with third-party applications. Therefore, it’s a design decision to consider all the advantages and disadvantages before load balancing on the client or server side.

### gRPC communication cycle

The gRPC framework focuses on managing network connections and RPC calls. Let's start with connection management. We divide the gRPC connection lifecycle into the following 10 major steps:

1. The client initiates a request to execute a remote procedure call according to the IDL contract specified in the gRPC generated code.

2. The generated code marshals the data and sends it to the gRPC framework requesting to establish a connection.

3. The gRPC sends the endpoint URL specified in the metadata of the request to the DNS resolver, which returns the IP addresses of all the back-end servers running on this URL.

4. The gRPC then sends the received list of IP addresses to the load balancer, which selects one of the back-end servers based on its configuration or load balancing policy.

5. Once a backend is selected, the gRPC initiates a connection request to the gRPC transport and returns a reference to a gRPC code stub that can be used later to send messages.

6. The gRPC transport sends an HTTP/2 stream over the wire, which reaches the listener on the server side.

7. The listener notifies server-gRPC of incoming connection requests to accept or reject the connection.

8. The server-gRPC accepts the connection, creates a subchannel for it, and returns the reference to the subchannel. A transport stream is created against each subchannel, maintaining separate read and write buffers for sending and receiving data.

9. Communication takes place over this subchannel by sending RPC calls. A subchannel can send multiple RPC calls, creating a separate stream for each call.

10. The packets received at the server gRPC are sent to the server stub to unmarshal the data. The server stub performs type conversions and calls the procedure on the server machine.

<img width="779" alt="image" src="https://github.com/user-attachments/assets/e621cfab-3b21-495f-88fd-29add1c41e72">

Each subchannel is associated with a client and a server. Whereas, each stream corresponds to each RPC call. When a new connection request is initiated, a new subchannel might be created with a different backend, making the system highly scalable.

<img width="647" alt="image" src="https://github.com/user-attachments/assets/52f7ef94-385c-4ea7-8863-9f983392eab4">

### gRPC operations in a remote call

Now that we know how subchannels are created in gRPC, let's go over the basic types of operations supported by gRPC.

- Headers: The client shares metadata, such as back-end IP, status, type of connection, and so on, by sending gRPC headers to the server. The server accepts the incoming request and sends back its header containing the reference to the newly created subchannel.

- Messages: The client sends a message with an RPC request, then the server receives the request and does the necessary processing, returning a message with a response. The number of messages exchanged between the client and server may vary depending on the connection type.

- Half-close: The client sends a half-close status at the end of its message, indicating that the client is now in receive-only mode and can close the connection when the server has finished sending the response.

- Trailer: The server sends a trailer at the end of its response with information, such as server load or any errors that occurred during the execution of the code on the server side.

The basic operations are the same for all types of connections, except that they’re batched in unary calls, i.e., the server receives headers, messages, and half-close before sending back its headers, messages, and trailers. The operation flow in the unary call is shown in the following illustrations:

<img width="740" alt="image" src="https://github.com/user-attachments/assets/c603d1f6-6b01-41a2-9458-f5cd3875a69e">

### gRPC advantages

gRPC is evolving rapidly, and new features are added frequently. A list of added benefits is given below:

- gRPC is fast and efficient due to the use of binary transport formats and the ability to fine-tune low-level features of the transport protocol. The graph below shows that when used for asynchronous communication between different services, gRPC can produce three times more throughput than most
JSON/HTTP implementations.

- It uses machine-readable contracts, allowing it to automatically generate client and server code with a single compiler.

- It can support all four types of communication and abstracts out details like timeouts, retries, request cancellations, and so on.

- Since the Internet of Things (IoT) devices are resource constrained (limited bandwidth, buffer storage, and so on), gRPC provides data flow control (transfer rate) through intimate control over HTTP.

- Pluggable components, such as a resolver, balancer, compressor, and so on, allow developers to precisely set the environment according to business logic.

Note: The compressor component allows compression in multiple encoding formats to reduce the number of bytes on the wire.

<img width="523" alt="image" src="https://github.com/user-attachments/assets/e0e74408-faa8-4bb5-b8b6-0eb88d1461b1">

### gRPC disadvantages

Since gRPC is in a mature state, it also has some limitations:

- It lacks native support for browsers and JavaScript applications running in HTTP/1.1, and it requires setting up additional layers to make it work.

- Using the default binary format makes debugging and viewing error details more difficult. However, some pluggable components might help in this regard.

- Additional software layers can increase complexity and development costs.

### gRPC summary

gRPC is one of the most sophisticated forms of modern RPC frameworks. It abstracts RPC details from client and server and manages connections internally. It also adds flexibility through pluggable components, like load balancers and resolvers. While it claims to be universally adopted, it may not be the best choice for all use cases. For example, when the API is more resource oriented or deals directly with clients implemented in JavaScript, instead of considering gRPC, other options like REST may be more suitable for our needs. Also, it’s a newer technology with more room for improvement compared to REST/HTTP-style architectures.

<br/>
<br/>

What is the difference between a gRPC channel and a subchannel?

A channel is the actual TCP connection created between a gRPC client and a gRPC server. A subchannel is the logical management of HTTP/2 streams inside this channel.

Why is gRPC considered to be a better choice for resource-constrained devices?

The gRPC framework provides more control over the HTTP protocol, allowing it to adjust data transfer rates based on client capabilities, which is why it can be considered a better choice when dealing with resource-constrained devices.

## Comparing API architecture styles

### REST

REST defines a set of constraints due that every API conforming to the REST style should abide by. All HTTP methods can be used in REST API calls to perform CRUD operations—for instance, `POST` to create a resource, `GET` request to read a resource, `PUT` to update the resource, and `DELETE` to remove a resource. 

#### REST advantages

REST APIs turn out to be a more suitable option in the following cases:Flexibility: REST also provides flexibility due to its lesser burden on the server side than GraphQL.

- CRUD operations on resources: REST is resource oriented and used to perform CRUD operations on data sources.

- Stateless behavior: When we need to maintain a stateless behavior in our requests and response paradigm—for example, if the servers don't need to store any data from the prior requests to execute the current request. The data in the request is enough to execute it successfully.

- Targeting a couple of resources/endpoints at a time: When the number of resources to operate on is few.

- REST as a wrapper: The RESTful interface can also be used around the gRPC channel internally to route the requests to other APIs or services.

- Flexibility: REST also provides flexibility due to its lesser burden on the server side than GraphQL.

#### REST disadvantages

The heavy event-driven paradigm is getting popular in today's world. Some use cases that are bound to be operated asynchronously can be modeled via REST APIs. However, there remains a room for improvement that can be optimized through asynchronous protocols. For example, with the help of distributed computing, we have to handle a large amount of data in the big data processing and analytics world. There are use cases where we need to connect things (applications and services) with large-scale data. A lot of data processing and communication between applications creates a bottleneck and becomes impractical when handled with a messages-oriented RESTful interface.

To conclude, you have to look for alternative APIs you’re a distributed system engineer and have entered the world of analytics and big data. This is because for big data analytics, data is often on the cloud on some blob store or file system. It might be the case that results go to some files, and the response contains only the URI of that result. APIs are just a conduit to that data, but they need to be an efficient facilitator for achieving application objectives.

<img width="745" alt="image" src="https://github.com/user-attachments/assets/2438ebf8-0263-411d-976f-fa3cf729656a">

### GraphQL

Facebook engineers have developed GraphQL to handle the issue of loading data of different API requests from different endpoints to provide a rendered view—for example, generating a newsfeed by fetching data from various resources through different API calls. The REST APIs expose data through different endpoints. On the other hand, GraphQL exposes data via a single endpoint, which is flexible. GraphQL enables consumers to select and retrieve the required data from the API and get what they've asked for. Moreover, GraphQL enables us to see the data through specific schema. Doing so helps to read/write data in a structured way. Such structured ways are important for large operations and to quickly understand any data trail.

#### GraphQL advantages

Primarily, the following two use cases are where GraphQL is beneficial:

- When there is a client application gathering data from multiple data sources. GraphQL aggregates data from multiple data sources and sends a consolidated response to the client. For example, in the case of a Stripe payment gateway, the data is retrieved from various endpoints, including customers, invoices, charges, and so on.

- When many client applications share one data source, but their view is different. GraphQL allows the applications to access the shared data where they can use it in a way that makes sense. Via GraphQL, applications can ask for the specific fields they want to present to the user instead of requesting all the fields.

#### GraphQL disadvantages

GraphQL is not the right option for server-to-server communication. For example, if we want to build a way for some back-end services to speak to each other, GraphQL might not be a good choice here. Instead, we need to look for other suitable options.

<img width="745" alt="image" src="https://github.com/user-attachments/assets/13f3382e-f273-4d1b-be08-d2b98bc1774c">

Why is graphQL not the right option for server-to-server communication?

GraphQL can be used for server-to-server communication, but there are certain drawbacks associated with it, such as the following:

- Parsing and validating queries adds extra overhead compared to simple REST APIs.

- Server-to-server communication may involve simple data communication; GraphQL increases the complexity of implementing it.

- GraphQL promotes strong coupling—a server acting as the client will need to implement the exact structure provided by the server.

- The performance of a server can be compromised when multiple services are involved and query different data.

The suitability of GraphQL for server-to-server communication relies on factors such as the requirements, complexity level, performance considerations, and trade-offs associated with that communication.

### gRPC

The gRPC API framework combines all the performance improvement and capabilities of HTTP/2 as a single package. It can be utilized in several cases that require high throughput backends to communicate with limited CPU and memory devices. In connection with this, gRPC is a framework with built-in features required to run a system and efficient serialization and deserialization capabilities.

#### gRPC advantages

As mentioned in the previous section, if we have to design a low-latency, highly scalable distributed system, we should consider gRPC. In this case, by default, we can consider the protocol buffers (ProtoBufs) as a better serialization mechanism.

gRPC is also a better choice if we aim to build a back-end system including an enormous number of interconnected microservices. In such a case, gRPC can provide efficiency and speed. It will also offer built-in features, such as deadline propagation, cascading cancellation, retries, request hedging, etc.

Note: Deadline is defining how long we should wait before the RPC is completed before terminating it with an error. And propagation means the deadline will propagate to all nested RPC calls.

Note: Request hedging is an alternative for retries. It means multiple gRPC calls are sent, and the first successful response is considered.

#### gRPC disadvantages

The gRPC framework supports only a few languages; therefore, we can't utilize it if our language isn’t in the supported language list. Another important downside is that even if our language is supported, the consumer might want to use another language that is not on the list. Then we’ll need to opt for another choice or look for more workarounds. So, if an enormous number of consumers are not able to utilize the native gRPC libraries, then it isn’t a useful tool to use in this case.

Moreover, if we’re building a system that calls a limited number of back-end services and only communicates with a web browser, then gRPC is not the right option. It doesn't mean we can't use gRPC, but other technologies, such as REST and GraphQL, will benefit us the most.

<img width="778" alt="image" src="https://github.com/user-attachments/assets/0308c904-657b-47f8-ae04-a0880670e016">

### Summary

<img width="680" alt="image" src="https://github.com/user-attachments/assets/09440158-13a9-4b93-9a69-409a228b3ad1">

