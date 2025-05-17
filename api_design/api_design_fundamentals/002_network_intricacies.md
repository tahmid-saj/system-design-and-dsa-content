# Network intricacies

## OSI model

Open system interconnection (OSI) consists of seven layers, each with a header containing information about the protocol in use, addresses, sequence number, and so on. The OSI model defines how communication is carried out between a sender and receiver. Let's understand the OSI model with the example of email, shown in the slides below:

<img width="509" alt="image" src="https://github.com/user-attachments/assets/4682014e-3ef9-4d72-9c5d-7110cf1f7e3d">

1. When a user sends an email, it first interacts with the application layer, which is responsible for data manipulation.
2. Next, the email's data is forwarded to the presentation layer, which adds the presentation layer header (PH) to it.
3. The session layer adds the session layer header (SH) and manages the session during the communication.
4. The transport layer adds the transport layer header (TH), divides the data into segments, and adds the sender and receiver port numbers.
5. The network layer converts the segments into packets and adds the IP addresses of the sender and receiver.
6. The data link layer converts the packets into frames, adds the MAC address of the immediate next hop in the path and passes them to the physical layer. This layer adds a data layer header (DH) and a data trailer (DT) to define the boundaries of a frame on the wire.
7. The physical layer converts the frames into the bitstreams and sends it to the receiver side.

<img width="508" alt="image" src="https://github.com/user-attachments/assets/5b8f93fa-2265-4dc7-b704-795a8d080e91">

8. The bit stream propagates to the physical layer of the receiving machine through the transmission medium.
9. The physical medium sends the data to the data link layer, which reads the header of the frame at the data link layer.
10. The data link layer hands over the packet to the appropriate network layer protocol after removing the data link layer header (DH) and trailer (DT).
11. The network layer forwards the packets to the transport layer after reading the network layer header (NH).
12. The transport layer header (TH) is used to forward data to the session layer.
13. The session layer header (SH) contains information that is used to forward the packet to the correct presentation layer protocol.
14. The presentation layer header (PH) forwards the data to the email client running on the application layer.

- Application layer: The sender interacts with the application layer, and it includes different protocols, for example, HTTP and SMTP protocols.

- Presentation layer: It takes care of the data's format on the sender and receiver sides. It ensures the data is understandable at the receiver end. Also, it may perform encryption, decryption, and compression of the data.

- Session layer: It creates, manages, and terminates the sessions between end-to-end devices. It’s also responsible for authentication and reconnections.

- Transport layer: It’s responsible for data ordering, reliability, and error checking.

Note: The application, presentation, session, and transport layers are only present on the end hosts, and not on the routers (the intermediate nodes that only use the network, datalink, and physical layers).

- Network layer: IP addressing and routing is the responsibility of the network layer. A node connected to the internet needs to have an IP address for communication with peers.

- Data link layer: This layer is responsible for frame transmission, address for local area network (LAN), and logical link control. In OSI models, the data unit is considered to be a packet in the network layer and a frame in the data link layer.

- Physical layer: It handles the transmission of bitstreams on the physical link between the sender and the immediate next hop receiver. The physical link can be Ethernet, DSL, and so forth.

The OSI model is always considered as a reference model and is not implemented because of many technical and nontechnical reasons. At first, nobody understood what session and presentation layers do, because these layers were more specific to the applications, not the network. These two layers could have been merged into the application layer (something that the TCP/IP model did).

Note: Historically, TCP/IP was introduced prior to the OSI model and does not contain the session, presentation, and physical layer.  We can think of this change in the following way: the concerns of the session and application layer are the responsibility of the application layer, and the data link layer also takes care of the concerns of the physical layer. The contribution of the OSI model was a clear separation of concerns into different layers and their service interfaces. OSI was lacking in terms of protocols. That is where the TCP/IP model came in.

## TCP / IP model

The Transmission Control Protocol/Internet Protocol (TCP/IP) model is mainly based on internet protocols (IP and TCP). The collection of protocols creates an hourglass shape, and the internet protocol uses the IP layer as its narrow waist, where the protocols above and underneath can flourish independently. We can add new protocols related to the application, transport, and network layers of the architecture according to the application's requirements.

<img width="445" alt="image" src="https://github.com/user-attachments/assets/c8e53f9e-3021-4764-a7f4-b16c26e87d90">

![image](https://github.com/user-attachments/assets/08b6558c-81c9-4f0d-acb6-39e46abdb52f)

Each layer performs particular services and communicates with its upper and lower layers. The physical layer and data link layer are combined in the network access layer. It consists of multiple network technologies such as Ethernet. The internet layer is responsible for logical data transmission over the network. Next, the transport layer determines the application using the port number and sends the data to the relevant application on the remote peer. In the application layer, we have multiple protocols—such as HTTP, SMTP, FTP, and so on—to interpret and display the data on the screen. The TCP/IP model is the open-protocol suite, and anyone can use it.

Ethernet: Ethernet is a set of standards, protocols, and related hardware and software implementations that establishes a connection between devices over a wired medium.

#### Transport layer

The transport layer is responsible for ensuring reliable communication between two hosts by managing network traffic and delivering data: 

- Establishing and terminating sessions: The transport layer establishes and ends IP communication sessions. 
- Data transfer: The transport layer ensures that data is completely transferred, and that it is delivered to the correct protocol and destination. 
- Error recovery: The transport layer uses error detection and correction mechanisms to ensure data is reliable. 
- Flow control: The transport layer controls the rate at which data is sent. 
- Port numbers: The transport layer uses standardized port numbers to facilitate communication for well-known applications. 
- Protocols: The transport layer uses protocols such as Transmission Control Protocol (TCP) and - - User Datagram Protocol (UDP) to control the volume of data and where it is sent.

### The narrow waist of the internet

The Internet Protocol (IP) has mainly dominated the network layer. This is especially because it maximizes interoperability, makes addressing universal, and provides best-effort service. Due to this reason, the internet was said to have a narrow waist architecture because the IP extends its support to many upper-layer transport and application protocols and many bottom-layer communication technologies. The concept is depicted in the illustration below:

<img width="284" alt="image" src="https://github.com/user-attachments/assets/7a9f7480-c06e-43e2-82cd-505765a5c847">

However, the Internet's progression in multiple aspects (such as real-time responsiveness, security, and so on) coupled with the explosive growth of HTTP-based applications led to the logical conclusion that HTTP is the new narrow waist of the Internet.

Some of the reasons for this insight are as follows:

- Existing infrastructure like proxies, caches, and content delivery networks (CDNs) facilitate HTTP evolution.

- HTTP easily penetrates enterprise firewalls, making it the obvious choice for nearly any application.

- The evolution of HTTP, especially for streaming applications.

Although the web was dominated by HTTP traffic in the 1990s, HTTP-based applications also increased in the early 2000s due to the overtake of REST architecture. However, an increasing number of applications across the web depended on streaming media, which posed a challenge for HTTP. But in the past decade, HTTP overcame this limitation by introducing HTTP streaming.

With the usage of APIs over the web, businesses depend on HTTP to exchange data, make development faster, and add functionalities in little to no time, without rewriting code. With such a level of reliance on HTTP, it’s safe to deduce that the new narrow waist of the Internet is HTTP. This means that the majority of traffic on the web runs over the HTTP protocol.

HTTP is super important for the continued growth of businesses due to its content-centric and versatile nature. For data transfer between companies, HTTP is used as the engine to run REST APIs. Consequently, the usage of HTTP over the years will only intensify. Nonetheless, HTTP requires transmission (TCP) and security protocols (TLS) for safe communication. This means that the narrow waist of the Internet can be expanded to include IP, TCP, TLS, and HTTP.

<img width="187" alt="image" src="https://github.com/user-attachments/assets/9c90d89c-1c84-456a-8bcd-710b85194ff4">

## Sockets

APIs provide services by exchanging information between client and server processes. The underlying network stack usually abstracts this interprocess communication, but how is it done? Popular API technologies such as RESTful, GraphQL, and gRPC work differently, but at the most basic level, they all use socket interfaces for process identification, connection establishment, and interprocess communication.

Let’s see the basic requirements for successful communication between two processes or services that operate on separate networked devices:

- Identification of devices on the internet.

- Identification of processes on the communicating devices.

- Steps or procedures to exchange data between those processes.

Let’s understand how sockets play an important role in maintaining these three requirements.

A socket is an interface that creates a two-way channel between processes communicating on different devices. Processes running on the application layer use sockets as an interface to take services from the transport layer to establish communication. Further, the interfacing requires an IP address and a port number to uniquely identify a process or application globally. The interface (IP address + port) is referred to as a socket address.

Two different sockets (endpoints) are required for any two processes to communicate. Each process in a connection is recognized by its respective socket address. The diagram below shows how “Process A" from a machine with "IP 1" can communicate with the “Process X" on another machine with "IP 2."

<img width="772" alt="image" src="https://github.com/user-attachments/assets/df803259-d52f-4cae-a279-915e637bb8e1">

Note: The ports used to run services on different devices can be different or the same. We can also assign the same port to different services on different devices connected to the internet. Port numbers ranging between 1–1024 are well-known ports because they’re mostly used as a standard for a particular service. For example, port 80 and 443 are used for HTTP and HTTPS, respectively.

Finally, the transport protocol (TCP or UDP) specified in the transport layer of the network stack is responsible for successfully exchanging data between these processes. All this information is present in the network stack, and we can access it using a single interface from the network socket.

## Multiple concurrent connections

Sockets enable the simultaneous creation of multiple communication channels on a single machine. The diagram below shows an example of multiple processes/services running on one machine (in this case, with an IP address of 104.18.2.119) and communicating with different processes running on different machines that are connected via a network in the following way:

- SMTP service with socket 104.18.2.119:587 talking to socket 10.1.y.z:50625

- HTTPS service with socket 104.18.2.119:443 talking to socket 10.2.y.z:54043

- FTP service with socket 104.18.2.119:21 talking to socket 10.3.y.z:52134

- PostgreSQL service with socket 104.18.2.119:5432 talking to socket 10.4.y.z:56432

The IP address 10.x.y.z used above is a private address range and is for illustration purposes only.

<img width="519" alt="image" src="https://github.com/user-attachments/assets/8cacc363-9e48-40a9-abf8-3cbb9b2a92db">

What is the maximum number of possible connections that can be established simultaneously on one machine?

Because the size of the port number is 16 bits, the maximum number of ports on a machine is limited to 65,536. However, the answer to this question is tricky. The 5-tuple information on a machine that identifies a typical connection is as follows:

- Source IP
- Source port
- Destination IP
- Destination port
- Transport layer protocol

Any combination of the information above can increase the maximum number. For example, a machine may have multiple IPs so that it can open more connections. Typically, both the available memory and computing power limit the number of simultaneous connections a machine can handle.

## Categories of network sockets

Network sockets can be categorized into two general types based on the transport protocol.

### Stream sockets

A stream socket creates a reliable end-to-end connection between the two endpoints using transport protocols like TCP and SCTP to transmit data between processes. It also utilizes the recovery facility of the underlying protocol (for example, TCP) to retransmit the lost data during the data propagation phase.

SCTP, or Stream Control Transmission Protocol, is a transport layer protocol in the Internet protocol suite that ensures reliable, in-sequence data transmission:

- SCTP guarantees that data units arrive at the endpoint in the correct sequence and completely
- SCTP requires a connection between endpoints to be established before data can be transmitted.
- SCTP allows for multiple streams of messages to be maintained for each endpoint. This allows for applications to deliver messages of different priorities and strict message order.

A stream socket is established using 3 tuples of information containing the IP, port and transport protocol.

SCTP is similar to UDP (User Datagram Protocol) and TCP (Transmission Control Protocol). It's also sometimes known as next-generation Transmission Control Protocol or TCPng.

A stream socket created on TCP can be in different states, as shown by the diagram below. A brief description of the different flags used in the illustration below is as follows:

- The SYN represents that the synchronization flag is set, while the number in front of SYN is the sequence number of the packet being sent.

- The ACK represents that the acknowledgment flag is set, while the number in front of ACK is a sequence number indicating the last successfully received byte by the remote peer. TCP numbers each byte of the connection in each direction.

- The FIN represents that the finish flag is set, while the number in front of FIN is a sequence number indicating the last successfully received byte by the remote peer.

The FIN represents that the finish flag is set, while the number in front of FIN is a sequence number indicating the last successfully received byte by the remote peer.

<img width="776" alt="image" src="https://github.com/user-attachments/assets/8af023d8-b617-4445-a434-fb6c56713db6">

Note: "Stream Socket 2" in the figure above is a server socket, which we’ll introduce separately in the later section. Also, note that the notation for <flag> = <number> is just for writing convenience, while these values have separately defined locations in the TCP header.

For a TCP connection, if the sender doesn’t receive an acknowledgment of the sequence after a defined period, the data is considered lost, and a retransmission request is initiated. The initiator of the connection doesn’t necessarily have to close it. Any connected partner can request termination and enter a receive-only mode where it can receive but not send data on the channel. After the other party finishes sending, the connection is closed completely.

### Datagram sockets

Unlike stream sockets, datagram sockets don’t create an end-to-end channel between two endpoints to transfer data between processes. It just sends data and expects it to reach the receiver end. It’s used in scenarios where data loss is not significant. It usually operates on a UDP-like protocol for data transfer.

<img width="703" alt="image" src="https://github.com/user-attachments/assets/c3143a1b-e799-40b6-9f83-5789b2f4089b">

Note: "Datagram Socket 2" in the figure above is a server socket, introduced later in this lesson.

Since the communication is stateless and doesn’t even contain packet sequence numbers, it’s nearly impossible to identify data lost during the propagation phase because there is no built-in mechanism in the UDP protocol to recover lost data. However, there are protocols that work on top of UDP and use application-level sequencing to make the communication reliable. While data flows in only one direction in the diagram above, the receiver can also send data in the other direction using the sender IP and port defined in the datagram socket.

### Raw sockets

Raw sockets are another type of network socket that doesn’t specify any transport protocol. It’s used to directly access the protocol stack of a network suite, typically for testing or developing transport protocols.

## Sockets in API development

We can divide sockets into two main types based on their role in modern APIs.

- Client: A process that requests or accesses information from another process or service through a communication channel.

- Server: A process that provides a service or responds to a request from another process through a communication channel.

A typical client-server model is illustrated in the diagram below:

<img width="565" alt="image" src="https://github.com/user-attachments/assets/6d7eab5f-a57a-4f74-900a-7a71db2fe9dc">

### Server socket

The server socket is configured to remain open and passively listen for incoming traffic by binding to a socket address. The server socket passively listens to incoming connection requests from clients and adds them to a connection queue. The server accepts the connections from the connection queue in a FIFO (first in, first out) manner and processes requests by creating separate process threads.

### Client socket

The client socket is created to get data or services from the server socket. The port and IP defined by the server socket must be known before a client socket can establish a connection with a server process. Typically, browsers automatically identify and populate well-known ports for commonly used services.

## Network socket interface

The socket API has different methods that can be used when communicating. The syntax of these methods may vary, and depend on the platform. Here, we only discuss these methods in general terms, without focusing on the syntax. A list of commonly used functions, along with brief descriptions, is given below.

Note: The socket API in UNIX code is a collection of calls that allow applications to communicate with each other by establishing connections, sending and receiving data, and closing connections. The API is implemented as system calls, such as connect, read, write, and close. A system call is a way for a computer program to request services from the operating system (OS) it's running on. System calls are used for a variety of tasks, including: Creating and executing new processes, Communicating with kernel services, and Performing network and file IO. There are separate frameworks in C and C++ that provides the implementation of the socket API.

<img width="656" alt="image" src="https://github.com/user-attachments/assets/4b7c81e5-76c4-496c-8916-26c872fd7826">

## Summary

We can conclude from this lesson that we have many abstraction layers to help developers develop portable applications without worrying about network details. The network sockets are one of the basic abstractions, the only interface responsible for creating connections at a core level.

In our API designs, we’ll only discuss concepts at a higher-level of abstraction instead of basic concepts like network sockets. Because all higher-level communication abstractions are based on sockets, we now understand how communication happens.
