# Client server communication

## World wide web

There are many technologies that one might use for client-server communication, but we’ll focus on the HTTP, RPC, and WebSocket protocols in this chapter. We’ll start with WWW because that is the primary use case for an HTTP protocol. The other two (RPC and WebSockets) are used extensively in different use cases. We believe these three collectively cover the major concepts of client-server communications abstractions.

The World Wide Web (WWW) is a hypertext-based information system that interlinks documents spread and stored across millions of machines all over the Internet. It’s commonly known as the web or w3.

What is the difference between the Internet and the web?

The Internet is a network of networks with a series of interconnected nodes (computers, laptops, mobile phones, etc) that can communicate with each other. In contrast, the web is one of the applications built on the Internet.

In a broad aspect, the web is a combination of the following four basic ideas:

- Client-server model: The client-server model is the principal concept behind the web. The client and server are two different entities connected together via the Internet. The client requests a resource while the server provides the requested resource to the client. An example of the client-server can be a web browser (client) and Domain Name System (DNS) server. When a user types a URL in the browser—for example, www.educative.io—the DNS returns the web server's IP address. In this case, it’s 104.18.3.119.

- Resource identifiers: This is a unique identifier to locate a resource such as files, documents, or other sources over the Internet. For example, https://www.educative.io/courses/grokking-modern-system-design-software-engineers-managers/g7EwEyNnR6D redirects us to a lesson (resource) in Educative’s course on system design.

- Hypertext and hypermedia: Hypertext is a text that is not linear, like with printed books or pages, but instead contains links to other documents where a reader can float freely from one document to another. Similarly, hypermedia is an extension of the hypertext, where along with the text (hypertext), the documents contain multimedia content such as graphics, animations, images, videos, audio, and interactive elements (such as embedded programs). For example, some websites may have images—when a user clicks on that image, the website directs the user to another web page.

- Markup language: The markup language includes a set of symbols inserted in a text document to configure and style its structure, formatting, or connection between its parts.

Note: Browsers render web pages by parsing markup languages

### Web protocols

Since the web follows the client-server model, there should be well-defined protocols to make their communication interoperable. On the web, the client requests some data that is provided by the server in a proper format. The client application, usually a browser, displays the data received from the server in a specific format—a web page. This information flow between clients and servers is directed by a protocol called Hypertext Transfer Protocol (HTTP).

Application layer protocols such as the File Transfer Protocol (FTP), Simple Message Transport Protocol (SMTP), HTTP, and so on, use lower layer protocols like Transmission Control Protocol (TCP), User Datagram Protocol (UDP), and Internet Protocol (IP) to provide services to end users. This course discusses all the protocols that are deemed essential.

### How does the web work?

From the users' perspective, the web is a collection of web pages that contain links to hundreds of other objects (text, images, audio, videos, advertisements, and tracking scripts.) stored across the Internet on different machines. A computing machine can either be a client, server, or both. Clients run a web browser software while the servers run a special software known as a web server software, which they can use to respond to a request from the client.

Web server software runs on clusters of commodity machines or a few high-end machines, giving every user the illusion that these servers only serve that client.

### What happens on the client side?

A client accesses different resources on the World Wide Web. Let’s first understand the structure of a web resource before describing the steps needed to get that resource.

Resources over the Internet are identified using a Uniform Resource Identifier (URI). The URI consists of three parts, as shown below.

<img width="776" alt="image" src="https://github.com/user-attachments/assets/f016812c-8a02-41de-bf59-fc38ea5cf6dd">

- Protocol: The HTTPS protocol is used to fetch the web page.

- Domain name: The DNS name shows where the web page is located.

- Unique path: The unique path determines the web page that needs to be accessed within a domain.

### What happens when we click a link like google.com?

The browser performs the following sequence of steps while fetching a web page or a resource:

1. When a user clicks on a link, the browser determines the web page URL, for example, www.educative.io. In some cases, the IP address for the URL will be stored in the browser's cache.

2. In the next step, the browser asks the DNS server for the IP address of www.educative.io. The DNS servers will be composed of the DNS resolvers (root DNS servers), top level DNS servers and authoritative DNS servers. The DNS server provides the web server's IP address where the web page resides.

3. The browser makes a TCP connection with the server that has the specified IP address provided by the DNS server. This is known as a TCP handshake to establish the HTTPS connection for the request. The server will accept or deny the TCP connection request in the TCP handshake from the client.

4. During the TCP handshake step, a firewall check will also happen on both the client and server side. The firewall will approve the TCP handshake requests if the transmission is logical and was not tampered.

5. The browser asks for the web page using the HTTPS protocol.

6. The request will go to a load balancer if appropriate, and be routed to an internal server.

7. The server sends the page in response to HTTPS requests. If the fetched web page consists of URLs of other objects or HTML, CSS, JS files that are needed, the browser fetches all of them using the same process. Dynamic content such as data from a database will also be provided by the server here. The full response will be done via HTTP.

8. The HTML, CSS, JS are then rendered on the client side, or it will be rendered on the server side if the system is using server side rendering.

9. After fetching all the required web pages and the relevant objects, the TCP connection is terminated.

What’s the difference between static and dynamic web pages?

Static web pages are based on Web 1.0, where content stored on the server is delivered to the client as is. On the other hand, dynamic web pages emerged because of Web 2.0, where the end users interact with the page, and dynamic content gets rendered on the client-side. Dynamic content is generated by a server-side script or application and can change automatically. Furthermore, dynamic web pages are generated by server-side scripts (such as PHP, JSP, and so on), which are interpreted by the server, and the result is given to the user.

## HTTP

The Hypertext Transfer Protocol (HTTP) is a stateless, application-layer protocol for distributed and hypermedia information systems. It's the foundation of data communication for the World Wide Web and is considered the de facto standard for client-server resource sharing. Web servers and client applications (browsers) must adhere to the message formats and transmission methods provided in the HTTP specifications. For instance, when we type a URL into a browser, the web server receives an HTTP request directing it to fetch and deliver the specified web page.

HTTP is based on the concepts of request and response, where one program (the client) requests another program (the server), and the server returns a response. The client usually makes requests in the form of HTTP commands, and the server responds with data in the form of documents. These commands are structured by different API architecture styles that we'll discuss in the coming chapters. Because it’s a driving force for APIs, HTTP is an essential protocol to understand.

HTTP communication is initiated by the clients sending a request to the server, and the server responds. This section discusses the request and response message structure. The server parses each request to interpret the request and generate the response. In the same way, the client parses the received response from the server and collects the desired application data from the response message.

### HTTP request structure

An HTTP request message is composed of the following four components:

- Method: HTTP provides built-in methods that determine what kind of action a client wants to request/perform.

- The request-target and version: It can be a URL or URI, which is a unique address or identifier that determines a resource's location uniquely over the Internet. For example, the URL https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers uniquely identifies an Educative course titled "Grokking Modern System Design Interview for Engineers & Managers." It also shows which version of HTTP is being used. The version part contains the HTTP version used for the request, for example, HTTP/1.1 or HTTP/2.0.

- Headers: HTTP headers allow clients to pass additional information between the communicating entities. These headers come in as a series of key-value pairs containing important information about each request. The request headers mainly contain the following information:

  - Server information from where data is requested.

  - Information about the browser being used by the user.

  - The kind of data formats a client can accept.

- Body: The body part of the HTTP request is used to communicate any application data a client wants to communicate to the server. The format of data should be mentioned in the header so that the server clearly understands the data.

<img width="422" alt="image" src="https://github.com/user-attachments/assets/bfb9ef8b-69fe-48f2-9692-e4385d048161">

### HTTP response structure

The HTTP response has the same format as the request with the following modifications:

- The method in the request is replaced with the HTTP version in response.

- The URL in the request is replaced with a status code in response.

- The HTTP version in the request is replaced with the phrase in response.

<img width="358" alt="image" src="https://github.com/user-attachments/assets/624fa4c9-0588-4dfd-b6b7-b925e19f2685">

- Status code and phrase: The status code is a three-digit number that conveys what happened with the client’s request on the server-side. The phrase part is a group of words that convey some meaning along with the status codes, for example, some of the phrases are OK, Moved Permanently, Bad Request, Not Found, and HTTP Version Not Supported.

  The status codes are divided into the following five different categories.
  
  - The status codes at one hundred levels (100-199) are informational status codes. For example, the 100 shows that the initial part of the request by the client is received, and the client should continue.
  - The status code at the two hundred level (200-299) represents that the client’s request was accepted successfully.
  - The status code at the three hundred level (300-399) shows redirections. In other words, the clients must take some other actions to fulfill their requests successfully.
  - The status code at the four hundred level (400-499) shows an error on the client-side.
  - The status code at the five hundred level (500-599) represents an error on the server-side.
- Headers: The headers in response provide extra information about the server and the response itself.

- Body: The response body consists of the data from the server that a client has requested.

Note: Headers allow the exchange of extended control information between the client and server. There are a large number of headers available in the HTTP specification and they're extensively used.

In HTTP, why are the control (headers) and application data included in the same request/response message?

There are several reasons that the control data should be unified with the application data in the same message, as discussed below:

- The HTTP is a stateless protocol that implies that the server should not keep any data relevant to a request. If we send control data in a separate message and application data in another message, the server should have to store the control data until the application data arrives. This approach diminishes the statelessness behavior of the HTTP protocol.
- Another reason is that it avoids sending too many requests, reducing the network’s resource consumption and data processing complexity on the client- and server-sides. Otherwise, we would be required to keep additional information both on the server- and client-sides.

### HTTP methods

- The GET method: This method is used to read data from a web source, for example, reading a page from the server.

- The POST method: This method sends user-generated data to the server in order to create or update a data source. We can understand how the POST method works through the following command.

- The PUT method: This method creates a new source or updates the existing one. It completely replaces whatever is present on the target URL.

- The DELETE method: This method deletes a resource from the server, for example, if we want to delete a user having a specific ID or name.

- The TRACE method: This method echos the content of an incoming HTTP request. This method is used for debugging purposes. The HTTP TRACE method is a special type of HTTP request that performs a message loop-back test along the path to the target resource. It allows you to see the exact message that was received by the final recipient, excluding any sensitive data, such as cookies or credentials.

- The CONNECT method: The connect method makes a two-way connection with a web server. It can be used to access a website using SSL or to open a tunnel. For instance, when a client wants to tunnel a TCP connection with a specific server (resource), they can ask the HTTP proxy server via the CONNECT method. The HTTP proxy server then establishes the connection for the client.

- The OPTIONS method: This method queries options for a page supported by a web server. For example, we use the OPTIONS method if we want to see what HTTP methods a domain can support.

- The HEAD method: This method asks for information about the document. It’s faster than the other methods because significantly less amount of information is being transferred.

The following table summarizes all the HTTP methods:

<img width="523" alt="image" src="https://github.com/user-attachments/assets/ec53efaa-4325-4e34-9eba-7da107df6fee">

Note: HTTP also supports custom methods, which extend its functionality. For instance, WebDav provides a set of extensions to the HTTP protocol via custom methods such as PRPFIND, PRPPATCH, MOVE, LOCK, UNLOCK, and so on. These custom methods are used for distributed authoring and versioning of documents.

### HTTP headers

As discussed earlier, the request to a server may contain additional lines specifying extra information, which are called request headers. For example, Authorization is a request header that represents a list of a client's credentials. Similarly, a response can also contain headers from the server-side, for example, Server is a header that shows information about the server in response. The nature of the headers in the request and response may vary, but in some cases, these may be applicable to both request and response. For example, the header Content-Type can be a part of both request and response. Following are some HTTP headers that can be used in requests, responses, or both.

<img width="622" alt="image" src="https://github.com/user-attachments/assets/df766db4-fc9f-4343-bc92-a28881860ad7">

### HTTP in APIs

The communication ecosystem was already present in the form of HTTP, and APIs used that ecosystem to their advantage instead of inventing something new. The adaptation of HTTP by APIs brings the following advantages:

- The HTTP protocol is well-known to many developers, so it’s simple to use, upgrade, and scale.

- It allows cross-platform and cross-language communication to support interoperability.

- It provides a uniform interface for communication between entities in the form of request and response messages.

- It’s a fast protocol because it requires minimal processing.

- Due to its adaptability, APIs based on it can achieve a wide range of goals. For example, making custom requests based on the use case and utilizing different built-in methods provided by HTTP.

- Repeat requests can be handled more quickly because responses can be cached.

- HTTP supports various types of encoding techniques that are helpful in various types of communication with the server via APIs. The encoding techniques are carefully opted to make an API efficient.

Which parts of the request and response messages are encrypted while using HTTPS?

HTTPS is HTTP over the Secure Sockets Layer (SSL); therefore, the entire HTTP request and response, including the headers and body, are encrypted while using HTTPS. Other details, such as the full domain or subdomain and the originating IP address, can be revealed via the DNS resolution and connection setup.

### HTTP evolution

HTTP is a widely used protocol, which directs the communication between clients and servers. This protocol was proposed and developed by Tim Berners-Lee in 1991. Over the years, this protocol has undergone many modifications that have made it feature-rich, flexible, and simple. In this lesson, we’ll compare different HTTP versions that enable us to choose a specific version for designing an API for a particular service. We discuss the following HTTP versions in the table below.

<img width="416" alt="image" src="https://github.com/user-attachments/assets/ee8081a7-9ad6-47f0-90df-f103f867dcb3">

### HTTP/0.9

HTTP/0.9 was the initial version of HTTP. It was the simplest client-server and request-response protocol. This version of HTTP only had the support of the GET request method, and similarly, the response would consist of hypertext only. This version had no support for HTTP headers; as a result, this version couldn't transfer other content-type files. The connection would also terminate immediately after sending the response.

### HTTP/1.0

HTTP/1.0 was a browser-friendly protocol that supported HTTP header fields—including rich metadata—for requests and responses. As a result, the response was not limited to just hypertext, but could transfer other types of files, such as scripts, stylesheets, and media. HTTP/1.0 brought a number of changes to its infant version of HTTP/0.9. The HTTP/0.9 version's specification was about a page long; however, the HTTP/1.0 RFC came in at 60 pages. In comparison to HTTP/0.9, HTTP/1.0 had the support of three HTTP methods: HEAD, GET, and POST. Apart from the support of various HTTP methods, HTTP/1.0 used some ideas that we’re familiar with, for example, headers, response status codes, errors, redirection, conditional requests, and encoding.

#### Drawbacks of HTTP/1.0

In HTTP/1.0, the notable flaws highlighted below had to be addressed:

- Non-persistent: An issue with HTTP/1.0 is its inability to keep the connection open between requests. The TCP connection would terminate after the client received the response to a single HTTP request. This approach is called non-persistent HTTP and it worked well in a world when a web page was typically just HTML text. The number of embedded links for resources like icons and other media content has increased significantly over time on the average web page. Non-persistence adds latency for the client, and in our world, many use cases need little to no latency for a better user experience. Let's understand this issue in detail, as given below.The following illustration shows the TCP three-way handshake required before the HTTP request is made. If a connection establishes and terminates after a request, the three-way handshake is repeated before making the next request. Therefore, HTTP/1.0 was not an efficient protocol for subsequent requests.

- Lack of host header: HTTP/1.0 had no mandatory host header in the request message. The host header identifies the target domain name to whom the request is made. If more than one website is hosted on the same server (virtual hosting), this header enables the server to identify the website easily.

- Limited caching headers: HTTP/1.0 performs cache revalidation using the If-Modified-Since header.

<img width="424" alt="image" src="https://github.com/user-attachments/assets/ed1ce01a-e5cd-4a0a-a17c-04f70c8e69fe">

### HTTP/1.1

HTTP/1.1 came with a tremendous amount of features and options that overcame the drawbacks of the previous versions—HTTP/0.9 and HTTP/1.0. Due to the flaws mentioned above, there was a need for a major revision in HTTP/1.0. In this regard, HTTP/1.1 was proposed, which came with many features that are defined in RFC 2616. The following notable changes are made to the HTTP/1.1 to overcome the drawbacks of the HTTP/1.0 protocol.

- Persistent connection: Unlike HTTP/1.0, HTTP/1.1 now enables persistent connection. In HTTP/1.1, we may create a TCP connection, submit a request, receive a response, and then send more requests, all while receiving more responses. Another name for this strategy is connection reuse. The relative overhead caused by TCP is decreased per request by spreading out the setup cost, startup, and release over many requests.
The process of connection reuse is demonstrated in the following figure:

<img width="342" alt="image" src="https://github.com/user-attachments/assets/cc116ac4-082c-42cf-a353-cb6d788c6671">

HTTP/1.1 connections are persistent by default, meaning they remain open until either the client or server closes them. This allows multiple requests to be sent over a single connection, instead of opening a new connection for each request. 

However, the client or server can close a connection at any time by sending a Connection header with the connection-token "close". 

Persistent connections improve the performance of HTTP/1.1 over HTTP/1.0, which closed connections after each request. However, there are some issues with persistent connections, such as head-of-line (HOL) blocking, where a request at the head of the queue can block all requests behind it.

HTTP keep-alive, a.k.a., HTTP persistent connection, is an instruction that allows a single TCP connection to remain open for multiple HTTP requests/responses. By default, HTTP connections close after each request.

- Pipelining: It’s also possible to pipeline requests, which enables sending multiple (inflight) requests before the arrival of the responses of earlier requests. This approach decreases the client's perceived latency and increases the system's performance.

<img width="671" alt="image" src="https://github.com/user-attachments/assets/11a081fb-99cc-4570-a0bf-f3d165518205">

- More HTTP methods: HTTP/1.1 is the most commonly used version that supports multiple HTTP methods, including HEAD, GET, POST, PUT, DELETE, TRACE, and OPTIONS .

- The Host header: HTTP/1.1 has made the Host header mandatory, which is included by default in the request.

- Virtual hosting: Virtual hosting enables a web server to host multiple websites using a single web server. It wasn't available in HTTP/1.0 because the marketplace would be simpler with static web pages. But as the demand to economically serve many websites from a single server grew, HTTP/1.1 added the needed support. This feature is now provided in HTTP/1.1 via the Host HTTP header, allowing the server to determine the website a request is intended for.
The advantage of virtual hosting is that it enables web hosting companies to offer services at a lower cost by hosting multiple websites on a single server.

- The Upgrade header: HTTP/1.1 has the ability to upgrade the already established client-server connection to a new protocol via the Upgrade header. For example, the protocol can be upgraded to HTTP/2.0 or HTTPS after making a connection with the server.

- Transfer-Encoding: HTTP/1.1 provides a way to send specific commands to any proxies between the client and the server via a mechanism called transfer encoding. However, we won’t be relying on it in this course because this mechanism can be taken advantage of by a malicious or buggy proxy and can make debugging of any occurring issues difficult.

- Additional cache headers: HTTP/1.1 has advanced headers to control cache revalidation (for example, "If-Unmodified-Since", "If-None-Match", "Cache-Control", and so on.).

### HTTP/2.0

The Web has used HTTP/0.9 and HTTP/1.0 from the beginning; however, HTTP/1.1 was developed in 2007 and became a little outdated in terms of its services by 2012.

The primary focus of HTTP/2.0 was to maintain backward compatibility; therefore, the headers, URLs, and general semantics didn't change much. Any new application could use HTTP/2.0 to benefit from the latest features, while the existing applications could still operate on HTTP/2.0 using limited features because of backward compatibility. The main features of HTTP/2.0 are the following:

- Prioritized responses: In the older HTTP/1.1, multiple requests over a TCP connection are sent in a pipeline where the responses from the server are received in the order the requests were sent. On the other side, in HTTP/2.0, many requests can be sent, and the server responds in any order based on the priorities of the requests. For example, if there are requests for two different images, the server sends the small image first. When the browser starts displaying the small image, the second image is sent to the client. This feature of HTTP/2.0 is called multiplexing, in which the responses can arrive in any order.

- Server push: In HTTP/2.0, a server can send resources to the client that might be needed on the client-side prior to the client's request for the resources. This mechanism is called a server push. For example, if a client requests a web page and the server knows that it needs other resources, such as style sheets and script files, the server sends these resources prior to the request from the client.

One of the advantages of HTTP/2.0 is that it can send responses out of order. How can we determine which response corresponds to which request?

In HTTP/2.0, each request is marked with a unique identifier before sending it to the server. The responses coming back from the server include the identifier of the requests they belong to; therefore, a browser can quickly determine which response corresponds to which request.

What is the difference between HTTP pipelining and multiplexing?

There’s a subtle difference between HTTP pipelining and multiplexing, that is, the order of arrival of responses.

Pipelining: In pipelining, multiple HTTP requests over a single TCP connection can be made without waiting for the earlier request’s responses. The responses arrive in order.

Multiplexing: On the other hand, in multiplexing, we can make multiple requests over the same TCP connection without waiting for the earlier requests’ responses. The responses arrive in any order.

### HTTP/3.0

HTTP/3.0 was a major revision in HTTP that was created by complementing the commonly used HTTP/1.1 and HTTP/2.0. The primary difference between HTTP/2.0 and HTTP/3.0 is the transport protocol that is used to support HTTP messages. The previous version relied on the Transmission Control Protocol (TCP). However, HTTP/3.0 utilizes QUIC (Quick UDP Internet Connections) on top of User Datagram Protocol (UDP). The main features of HTTP/3.0 are:

- Adoption of QUIC protocol: Multiplexing of streams and per-stream flow control is provided by QUIC, a transport protocol. It has the capacity to enhance HTTP performance in comparison to TCP mapping by offering stream-level reliability and congestion control throughout the connection.

- TLS 1.3: HTTP/3.0 also implements TLS 1.3 at the transport layer, providing similar security and integrity to running TLS over TCP.

- Improved performance: HTTP/3.0 has lower latency and high reliability due to the adoption of the QUIC protocol. In some studies, HTTP/3.0 is faster than HTTP/2.0.

- Avoids head-of-line blocking: It also addresses a major problem in HTTP/1.1 and HTTP/2.0, known as blocking.

The following figure shows the HTTP/3.0 protocol stack:

<img width="398" alt="image" src="https://github.com/user-attachments/assets/f4014e68-fc40-4394-9398-d003bdc9e3c5">

The following table summarizes the differences between different versions of HTTP:

<img width="665" alt="image" src="https://github.com/user-attachments/assets/a59b8e04-313b-4eca-bf65-0aeb04462a94">

## Remote Procedure Calls (RPCs)

### What is an RPC?

A remote procedure call (RPC) architecture is a service or action-oriented style of creating APIs, where resources are distributed among different services running on remote machines. RPC facilitates interprocess communication by enabling clients to run remote procedures (functions) in a simple local function-call-like abstraction (for example, a simple programming function that is called to return a value after performing some operations that are hidden from the callee.). A generic RPC architecture is shown in the illustration below:

<img width="338" alt="image" src="https://github.com/user-attachments/assets/5509b04e-1dd7-411d-917b-ee0c23c9a518">

The table below elaborates the individual components of a remote procedure call:

<img width="656" alt="image" src="https://github.com/user-attachments/assets/bd82cd14-af5e-4a4b-b1ff-f4749c324fc8">

The RPC runtime is the actual software program that does the heavy lifting and glues all the components together. It communicates with the underlying operating system and network interface to transfer data over the wire. RPC uses the interface definition language (IDL) to set up templates that specify function names, parameters, and so on, to glue processes running in different development environments. The IDL compiler runs only once and generates code stubs to support data conversion between different formats understood by programs written in different languages. RPC-style APIs are easy to implement thanks to traditional function-call-like integration support provided by IDL headers.

While there are many implementations of the RPC mechanism, the following are a few modern implementations usually used in different kinds of APIs:

<img width="676" alt="image" src="https://github.com/user-attachments/assets/03145bca-33a9-420b-89a0-5fecb01c945f">

Note: The core of RPC is synchronous (blocks the client until a response is returned), and most modern frameworks also provide mechanisms to make asynchronous remote procedure (function) calls to increase throughput.

### How does RPC work?

RPC follows the request-response model, and we’ve divided each request-response cycle into the following four subsections:

1. Initiating RPC calls from the client applications

2. Packing data and forwarding to RPC runtime

3. Establishing connections across the network

4. Transmitting data to the remote end through the network

#### 1. Request and response

Before we discuss the request initialization, we must understand the two IDL header types.

- Import module: A component added to the client-side, specifying a list of functions it can call.

- Export module: A component added to the server-side, specifying a list of functions it can perform.

The import and export modules defined in the IDL headers maintain a list of remote functions provided by the API, along with the format of input parameters and returned responses. An RPC request is initiated by a client, and it must specify a function identifier and parameter list that are consistent with the signatures provided by the IDL import module.

Let's take a look at a hypothetical example of an RPC available at the example.com/rpc-demo endpoint. We’ll call the demo RPC that accepts a single string parameter of greeting. The request and response headers sent and received by a JSON-RPC client are as follows:

<img width="790" alt="image" src="https://github.com/user-attachments/assets/83d3b225-fc9c-4086-bed0-3cba74020815">

Note: For simplicity, we’ve removed unnecessary fields from the request and response headers given above. Also, we’ll learn more about data formats, for example, JSON, in the coming lessons.

#### 2. Marshalling and unmarshalling data

Before a client or server can send or receive data, it must be converted into a format they can understand. Each client and server has its own stub responsible for transforming the request and response data in a mutually convertible format using the following techniques:

- Marshalling: Packing data into a mutually convertible format.

- Unmarshalling: Unpacking data from a mutually convertible format.

Both client and server RPCs must agree on common marshalling and unmarshalling techniques during network propagation. Various values (such as caller ID, service ID, parameters list, and so on) that are required to make a successful RPC call are marshalled by code stubs and trigger RPC runtime to transfer data over the network.

The following illustration shows the overall process of communication, demonstrating a complete RPC request and response cycle:

<img width="707" alt="image" src="https://github.com/user-attachments/assets/dfafd9b5-d25f-49bb-87e6-b50869e157f5">

1. First the IDL import and export modules are added to the client and servers respectively. These IDL modules define a list of functions the client can call, and functions the server can perform
2. A request is initiated using the IDL import module via the client
3. The request data is then marshalled via the client stub
4. The client RPC establishes a connection via some network protocol (TCP, UDP or HTTP) with the server RPC
5. The client RPC then creates and sends data packets (chunks) for the request to the server RPC
6. The server RPC invokes the server side function defined in the IDL export module on the server
7. When the function is invoked, the request data is unmarshalled via the server stub
8. A response is returned after the function is completed by the server
9. The response is marshalled using the server stub
10. The data packets (chunks) for the response are then created via the server RPC
11. The response is transmitted over the network protocol from the server RPC to the client RPC

#### 3. Binding connection

Client and server communication starts by establishing a connection via a method called bind. There are two types of binding in RPC:

- Static binding: The server endpoint (IP address and port) is dedicated and already known by the client.

- Dynamic binding: The server endpoint is decided and assigned by the RPC dynamically using a DNS resolver.

Each client and server has its own runtime RPC responsible for reliable communication between them. It packs data into chunks that can be transmitted over the network. It also specifies the network protocol used for communication and handles network-related problems reported by the network protocol, such as network failures, timeouts, and so on.

#### 4. Network protocol

Most RPC protocols come with rules that exhibit high performance by fine-tuning transport and application layers. Additionally, RPC can work with the transport protocols TCP and UDP. Although popular RPC standards—such as gRPC, JSON-RPC, SOAP, and so on—use HTTP as the underlying application layer protocol that works on TCP (or UDP in case of HTTP/3.0) for data transmission.

### RPC advantages

The RPC architecture has the following key properties that make it a desirable choice for working with distributed systems such as microservices:

- RPC is an operation-oriented architecture, and we can easily add endpoints when the API has new requirements.

- RPC provides significant network abstraction, making it easy to implement without worrying about network details.

- RPC-based architectures, such as gRPC, lead to better performance and are easier to integrate because IDL modules allow automatic code generation for popular languages.

- RPC architectures also allow faster development with libraries supporting most of the popular languages

### RPC disadvantages

Although RPC has unique capabilities, it also has the following limitations:

- Changes must be reflected on both the client- and server-sides, making it harder to update.

- Custom stub libraries may have to be created for some languages, and if a language of our choice is not supported by a specific IDL compiler, we might need to change the strategy.

What is the difference between an API call and an RPC?

RPC is the primitive form of an API. Modern APIs share their origins in RPC-style architectures but are much more complex than just calling code snippets remotely and having additional capabilities. In other words, RPC is one of the possible mechanisms to implement APIs, but we can say that the most basic form of an API is a simple RPC call.

## WebSockets

Most web APIs use HTTP as their underlying protocol to transfer data, and HTTP is often considered as one of the best options for executing batch tasks asynchronously. But when it comes to two-way and real-time communication such as chat, live streaming, gaming, and so on, HTTP falls short because it is a request-response protocol, where usually a server closes the connection after sending the response. We describe some HTTP-based techniques and their corresponding limitations in achieving bidirectional communication in the table below:

<img width="571" alt="image" src="https://github.com/user-attachments/assets/c9494418-fabf-448c-8785-956c606de334">

Note: The table above focuses on HTTP/1.1 because the other versions were not introduced when WebSocket was first developed.

We conclude from the above discussion that we need a different approach to achieve two-way data transfer between the server and client without waiting for clients' requests. We need an approach that has low latency and avoids TCP handshake by keeping the connection open indefinitely.

WebSocket was introduced in 2011 to enable full-duplex asynchronous communication over a single TCP connection to use resources efficiently. HTTP connection restricts TCP to a one-sided communication, where the client always starts the communication due to the request-response model. In other words, the client first sends requests, then the server responds to them, which is a half-duplex communication. In contrast, WebSockets take full advantage of the TCP connection allowing clients and servers to send or receive data on demand.

<img width="575" alt="image" src="https://github.com/user-attachments/assets/26aacdd2-bc65-4959-8757-0fb3da582b0b">

WebSocket leverages the core TCP channel utilizing its full-duplex nature. Data can be sent and received simultaneously by the client and the server. Websocket is a stateful protocol that performs relatively faster than HTTP because it’s lightweight and carries the overhead of large headers with each request. WebSocket is stateful because it stores connection related information on the participating machines.

A WebSocket establishes an HTTP connection and then upgrades it to the WebSocket protocol. All the transmission happens directly on the TCP channel. The URLs for connections using WebSocket begin with ws:// and wss:// for non-TLS and TLS-based connections, respectively. Transport layer security (TLS) is a protocol that provides security for data communication over the network.

<img width="475" alt="image" src="https://github.com/user-attachments/assets/648af132-10ed-40a3-96e8-9e2caf44cc54">

The illustration above depicts the conversion from HTTP to a WebSocket connection. We can see that the transmission layer connection (TCP) is the same while the application layer protocol is updated from HTTP to WebSocket.

### How do WebSockets work?

A WebSocket connection starts with an HTTP connection established through a three-way TCP handshake. Afterward, an HTTP GET request is initiated to switch the protocol to WebSocket. The connection upgrade request can be accepted or rejected by the HTTP server. If the server is compatible with the WebSocket protocol and the upgrade request is valid, the connection is upgraded to a WebSocket connection. The response contains the status code 101 (Switching Protocols) and the value for the field, Sec-WebSocket-Accept.

The headers of the initial switching protocol request are shown below:

<img width="718" alt="image" src="https://github.com/user-attachments/assets/58f3792e-67ce-4ed8-baf2-06ee3dbd2857">

For simplicity, we have removed some fields from the headers above.

The headers above contain the following noticeable fields:

- Status code 101 shows that the protocol is successfully upgraded and can send WebSocket frames (frames are the number of bytes, defined and used in different network protocols - it is the unit of transmission.).

- The Sec-WebSocket-Key is a base64-encoded 16-byte value that the server uses to verify that the upgrade request is coming from a legitimate client that understands the WebSocket protocol, and not a malformed HTTP request. This value is then encrypted using a hashing algorithm like SHA, MD5, and so on.

- The server decrypts the value of the Sec-WebSocket-Key and generates the Sec-WebSocket-Accept field by prepending a Globally Unique Identifier (GUID) value to the client-provided Sec-WebSocket-Key. The value of Sec-WebSocket-Accept is also encrypted and sent back to the client, indicating that the server has accepted the connection upgrade.

Are WebSockets and network sockets the same?

No, network sockets provide APIs access to the underlying transport layer which can be TCP, UDP, SCTP, and so on, with aided abstraction. Whereas, WebSocket is a protocol that allows web applications to communicate bidirectionally over a single TCP connection.

Once the connection is established and successfully upgraded to WebSocket protocol, initial control frames are exchanged. WebSocket has two types of frames, control and data frames. Each frame is identified by a 4-bit opcode. Control frames are used to know the status of the connection and can carry a maximum of 125 bytes of payload. Although, these frames can also be packaged with application data called data frames. A data frame is identified by an opcode whose most significant bit is zero. A list of common frames and their brief descriptions are given below:

<img width="557" alt="image" src="https://github.com/user-attachments/assets/603daeaf-18f1-462a-8e47-2650ae26f083">

When closing a WebSocket connection, close frames are exchanged between endpoints. After an endpoint receives a close frame, it must not send more data. Any metadata stored to maintain the TCP connection information must also be cleaned up during the connection teardown process by the endpoints. Finally, under normal circumstances, the server raises the FIN flag, and both endpoints close the TCP connection when the close sequence is complete.

<img width="551" alt="image" src="https://github.com/user-attachments/assets/523880d1-37a8-4204-a364-e9a47d69712a">

Why is it difficult to scale WebSockets horizontally?

Due to the stateful nature of WebSocket, both endpoints are bound to the channel, and we cannot add more machines to reroute requests and distribute the workload among different servers.

While horizontally scaling a single WebSocket connection is difficult, distributing different WebSocket connections to different servers can be achieved by an appropriate intermediary, such as a load balancer or an API gateway.

### WebSocket advantages

WebSockets perform well for real-time applications and provide the following benefits:

- Bidirectional communication channel

- Both server and client can send and receive data on demand

- Higher frequency of data exchange

- Faster data transmission with a header size of 2—10 bytes

- Compatibility with existing infrastructure

- Bypasses firewall using the default ports 80 and 443

### WebSocket disadvantages

WebSockets is a relatively new concept and not be as mature as HTTP-style architectures. While it's great for specific scenarios, such as multiplayer gaming, live streaming, and video conferencing, it also has some limitations.

- Horizontal scaling is complex, because we can’t load balance and reroute requests coming from a client once the connection is upgraded to WebSocket.

- Greatly affected by connection failures, as the connection is stateful and the request headers carry no information about the sending and receiving ends, it’s difficult to recover the lost connection.

