# HTTP vs HTTPS

HTTP (Hypertext Transfer Protocol) and HTTPS (Hypertext Transfer Protocol Secure) are both protocols used for transmitting data over the internet, primarily used for loading webpages. While they are similar in many ways, the key difference lies in the security aspect provided by HTTPS.

## HTTP

HTTP stands for HyperText Transfer Protocol. It's the foundational protocol used for transmitting data on the World Wide Web. When you enter a website address in your browser, HTTP is responsible for fetching and displaying that site.

### Features

- Stateless Protocol
  - Each request from a client to a server is independent. The server doesn't retain any session information between requests.
- Text-Based
  - Data is transmitted in plain text, making it readable by both humans and machines.
- Port 80
  - By default, HTTP uses port 80 for communication.

### Use cases

Imagine you're browsing a public blog without entering any personal information. HTTP suffices here because the data exchanged isn't sensitive. The speed of HTTP can be advantageous in such scenarios where security isn't a primary concern.

## HTTPS

HTTPS stands for HyperText Transfer Protocol Secure. It's an extension of HTTP with added security measures to protect data during transmission.

- Security
  - In an age where cyber threats are prevalent, HTTPS provides a necessary shield against data breaches and cyber-attacks.
- Trust
  - Users are more likely to trust and engage with websites that display security indicators (like the padlock icon in browsers).
- SEO Benefits
  - Search engines prioritize secure websites, meaning HTTPS can improve your site's visibility and ranking.
- Compliance
  - Many regulations require the protection of user data, making HTTPS a necessity for compliance.

### Features

- Encryption
  - Uses protocols like SSL/TLS to encrypt data, ensuring that any intercepted information remains unreadable.
- Authentication
  - Verifies that the website you're connecting to is legitimate, preventing man-in-the-middle attacks.
- Data Integrity
  - Ensures that data isn't tampered with during transmission.
- Port 443
  - HTTPS operates over port 443.

### Use cases

When you're shopping online, entering personal details, or accessing your bank account, HTTPS is essential. It safeguards your sensitive information from potential eavesdroppers and ensures that your data reaches the intended server securely.

## HTTP vs HTTPS

<img width="769" alt="image" src="https://github.com/user-attachments/assets/18409fd4-92b7-4080-ae19-120f4babb760" />

## TCP vs UDP

TCP (Transmission Control Protocol) and UDP (User Datagram Protocol) are two of the main protocols used for transmitting data over the internet. Each has its characteristics, advantages, and disadvantages, making them suitable for different types of applications.

### TCP (Transmission control protocol)

TCP is a connection-oriented protocol that ensures reliable, ordered, and error-checked delivery of a stream of bytes between applications.

#### Characteristics

- Reliability
  - TCP ensures that data is delivered accurately and in order, retransmitting lost or corrupted packets.
- Connection-Oriented
  - Establishes a connection between sender and receiver before transmitting data.
- Flow Control
  - Manages data transmission rate to prevent network congestion.
- Congestion Control
  - Adjusts the transmission rate based on network traffic conditions.
- Acknowledgements and Retransmissions
  - Uses acknowledgments to confirm receipt of data and retransmits if necessary.

#### Use cases

Applications where reliability and order are critical, like web browsing (HTTP/HTTPS), email (SMTP, POP3, IMAP), and file transfers (FTP).

Example:

Loading a webpage: TCP is used to ensure all web content is loaded correctly and in the right order.

### UDP (User datagram protocol)

UDP is a connectionless protocol that sends messages, called datagrams, without establishing a prior connection and without guaranteeing reliability or order.

#### Characteristics

- Low Overhead
  - Does not establish a connection, leading to lower overhead and latency.
- Unreliable Delivery
  - Does not guarantee message delivery, order, or error checking.
- Speed
  - Faster than TCP due to its simplicity and lack of retransmission mechanisms.
- No Congestion Control
  - Does not reduce transmission rates under network congestion.

#### Use cases

Applications that require speed and can tolerate some loss of data, like streaming video or audio, online gaming, or VoIP (Voice over Internet Protocol).

Example:

Streaming a live sports event: UDP is used for faster transmission, even if it means occasional pixelation or minor video artifacts.

### TCP vs UDP

- Reliability

  - TCP: Reliable transmission, ensuring data is delivered accurately and in order.
  - UDP: Unreliable transmission; data may be lost or arrive out of order.

- Connection

  - TCP: Connection-oriented; establishes a connection before transmitting data.
  - UDP: Connectionless; sends data without establishing a connection.

- Speed and Overhead

  - TCP: Slower due to handshaking, acknowledgments, and congestion control.
  - UDP: Faster with minimal overhead, suitable for real-time applications.

- Data Integrity

  - TCP: High data integrity, suitable for applications like file transfers and web browsing.
  - UDP: Lower data integrity, acceptable for applications like streaming where perfect accuracy is less critical.

- Use Case Suitability

  - TCP: Used when data accuracy is more critical than speed.
  - UDP: Used when speed is more critical than accuracy.

TCP is used for applications where reliable and accurate data transmission is crucial, whereas UDP is chosen for applications where speed is more important than reliability, and some loss of data is acceptable.

## HTTP: 1.0 vs 1.1 vs 2.0 vs 3.0

### HTTP 1.0

#### Features

- Simple Request-Response Model
  - Each request opens a new TCP connection, and the connection is closed after the response.
- Stateless Protocol
  - Does not retain session information between requests.
- Basic Headers
  - Supports essential headers for content negotiation and caching.

#### Improvements over previous protocols

- Introduced the concept of persistent connections, albeit limited.
- Allowed for more structured and standardized requests and responses compared to earlier, more primitive protocols.

#### Use cases

In the early days of the web, HTTP/1.0 was sufficient for serving simple web pages with minimal resources. For example, static websites or early blogs that didn’t require dynamic content benefited from HTTP/1.0’s straightforward approach.

### HTTP 1.1

#### Features

- Persistent Connections
  - Keeps the TCP connection open for multiple requests/responses, reducing latency.
- Chunked Transfer Encoding
  - Allows data to be sent in chunks, enabling the server to start sending a response before knowing its total size.
- Enhanced Caching Mechanisms
  - Improved headers for better caching strategies.
- Host Header
  - Supports virtual hosting by allowing multiple domains to share the same IP address.

#### Improvements over HTTP/1.0

- Reduced Latency
  - Persistent connections minimize the overhead of establishing new connections for each request.
- Better Resource Management
  - More efficient use of network resources through pipelining (though limited in practice).
- Support for Virtual Hosting
  - Enables hosting multiple websites on a single server/IP address.

#### Use cases

Modern websites rely heavily on HTTP/1.1 for handling multiple simultaneous requests efficiently. For instance, an e-commerce site serving product images, scripts, and stylesheets benefits from persistent connections to load resources faster.

### HTTP 2.0

#### Features

- Binary Protocol
  - Translates HTTP into a binary format, making it more efficient to parse and less error-prone.
- Multiplexing
  - Allows multiple requests and responses to be in flight simultaneously over a single connection, eliminating head-of-line blocking.
- Header Compression (HPACK)
  - Reduces the size of HTTP headers, decreasing bandwidth usage.
- Server Push
  - Enables servers to send resources to clients proactively, anticipating future requests.

#### Improvements over HTTP/1.1

- Performance Boost
  - Significant reductions in page load times due to multiplexing and header compression.
- Efficient Resource Utilization
  - Better management of network resources with a single connection handling multiple streams.
- Enhanced User Experience
  - Faster interactions and smoother performance for users accessing complex web applications.

#### Use cases

High-traffic websites like social media platforms, streaming services, and large e-commerce sites leverage HTTP/2.0 to deliver rich, interactive content swiftly. For example, streaming a high-definition video on a platform like YouTube benefits from HTTP/2.0’s ability to handle multiple data streams efficiently.

### HTTP 3.0

#### Features

- Built on QUIC Protocol
  - Utilizes QUIC (Quick UDP Internet Connections) instead of TCP, enhancing speed and reliability.
- Improved Latency
  - Faster connection establishment with 0-RTT (Zero Round Trip Time) handshake.
- Better Handling of Packet Loss
  - Enhanced resilience to network issues, maintaining performance even in unstable conditions.
- Built-in Encryption
  - QUIC integrates TLS 1.3, ensuring secure data transmission by default.

#### Improvements over HTTP/2.0

- Faster Connections
  - QUIC’s UDP-based approach allows quicker data transfer and reduced latency.
- Enhanced Security
  - Built-in encryption simplifies secure communication without additional overhead.
- Superior Performance in Real-World Conditions
  - More robust against packet loss and varying network conditions, ensuring consistent performance.

#### Use cases

Applications requiring real-time data transmission, such as online gaming, video conferencing, and live streaming, greatly benefit from HTTP/3.0. For instance, video conferencing tools like Zoom or Microsoft Teams can achieve lower latency and smoother video streams using HTTP/3.0’s QUIC protocol.

### Why upgrade to newer HTTP versions?

- Performance Enhancements
  - Newer versions significantly reduce load times and improve user experience.
- Security Improvements
  - Enhanced encryption and secure protocols protect data better.
- Scalability
  - Efficient handling of multiple requests supports larger, more complex applications.
- Future-Proofing
  - Adopting the latest standards ensures compatibility with emerging technologies and user expectations.

### Summary

<img width="766" alt="image" src="https://github.com/user-attachments/assets/e40a7898-279d-471b-b302-dd76faa1e92d" />

The evolution of HTTP from 1.0 to 3.0 showcases the web’s ongoing quest for speed, efficiency, and security. Each version builds upon its predecessor, introducing features that address the growing demands of modern web applications. As a software engineer, leveraging the advancements in HTTP protocols can lead to more robust, performant, and secure applications.

- HTTP/1.0

  - Release Year: 1996
  - Connection: New per request
  - Use Case: Simple, static websites

- HTTP/1.1

  - Release Year: 1997
  - Connection: Persistent
  - Use Case: Dynamic websites, e-commerce

- HTTP/2.0

  - Release Year: 2015
  - Connection: Multiplexed streams
  - Use Case: High-traffic, interactive web apps

- HTTP/3.0

  - Release Year: 2020
  - Connection: QUIC (UDP-based)
  - Use Case: Real-time applications, streaming

## URL vs URI vs URN

### URL (Uniform resource locator)

- Definition
  - A URL is a specific type of URI that not only identifies a resource on the internet but also provides a method to locate it by describing its primary access mechanism, usually its network location.
- Components
  - It typically includes a protocol (such as HTTP, HTTPS, FTP), domain name, and path, optionally followed by query parameters or a fragment identifier.
- Example
  - https://www.example.com/path?query=term#section
- Key Characteristics
  - Specifies how the resource can be accessed (protocol).
  - Includes the location of the resource (like a web address).

### URI (Uniform resource identifier)

- Definition
  - A URI is a generic term used to identify a resource either by location, name, or both. It serves as a universal identifier for resources on the internet.
- Scope
  - All URLs and URNs are URIs, but not all URIs are URLs or URNs.
- Example
  - A URL https://www.example.com is also a URI, and a URN like urn:isbn:0451450523 (identifying a book by its ISBN) is also a URI.
- Key Characteristics:
  - A more general concept than both URL and URN.
  - It can be either a locator (URL), a name (URN), or both.

### URN (Uniform resource name)

- Definition
  - A URN is a type of URI that names a resource without describing how to locate it. It’s used to assign a unique and persistent identifier to a resource.
- Example
  - urn:isbn:0451450523 uniquely identifies a book using its ISBN, irrespective of where it exists.
- Key Characteristics:
  - Provides a unique and persistent identifier.
  - Does not specify a location or method to access the resource.

### Summary

- URL
  - Specifies both the identity and the location of a resource (How and Where).
- URI
  - A more comprehensive term covering both URLs (identifying and locating) and URNs (just identifying).
- URN
  - Focuses only on uniquely identifying a resource, not on where it is located or how to access it.

In practical terms, when you’re browsing the internet, you're mostly dealing with URLs. URIs and URNs come more into play in specific contexts like software development, digital libraries, and systems where unique and persistent identification of a resource is crucial.


