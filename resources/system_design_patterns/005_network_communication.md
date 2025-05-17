# Network communication

## SSE vs WebSockets

### SSE

#### Use cases

- Unidirectional communication
  - SSE is usually best for real-time notifications, live updates such as stock prices, news feeds, etc, or progress updates
- Low communication frequency
  - It is usually used when updates are infrequent, ie once every few seconds or minutes
- Ease of implementation
  - SSE works over a standard HTTP connection, which makes it simple to set up compared to websockets
- Compatibility
  - SSEs also work natively in most browsers using the EventSource API
  - It's also ideal for applications where HTTP/2.0 is used since it efficiently multiplexes multiple SSE streams
  
#### Advantages

- SSE has a built-in reconnection logic if the connection is down
- SSE is also easy to debug since it uses HTTP, and also should be compatible with most infrastructure
- SSE is also efficient in broadcasting updates to multiple clients in a one-to-many relationship, ie live comments being sent by the server to multiple clients

#### Disadvantages

- Uni-directional communication:
  - SSE is uni-directional, where the client will first establish the long-lived HTTP connection with the server, and then only the server can send messages to the client. The client cannot directly send a message to the server via this connection.
- Bi-directional communication:
  - SSE is uni-directional, and thus only the server will send messages to the client. It is not a bi-directional communication like websockets.
- Latency:
  - SSEs also tend to have slighly higher latency compared to websockets, because it is communicating via HTTP

### Websockets

#### Use cases

- Bidirectional communication
  - Websockets are often used in chat applications, online gaming, collaborative editing, or any other use case where both the client and server frequently exchange messages
- High frequency messaging
  - Use websockets if frequent updates are required in both directions
- Real-time, low latency requirements
  - Websockets provide lower latency compared to SSE because of a persistent connection, and because it uses a lightweight TCP connection

#### Advantages

- Bi-directional communication
- Efficient for frequent or high-volume data transfer
- Persistent TCP connection reduces overhead for real-time interactions
- Works well with non-browser clients, ie IoT devices

#### Disadvantages

- Websockets may sometimes be more complex to implement and manage due to the connection upgrades, reconnections, and ensuring scalability of the connections
- Websockets may also require additional fallback solutions, ie if websockets cannot be used, then the client can instead use polling
- Websockets also use slightly higher bandwidth and resources compared to SSE, because it persists the connection

### Conclusion

#### Use SSE if:

- You only need server-to-client communication.
- The updates are relatively infrequent (e.g., news, weather updates).
- You want simplicity and compatibility with HTTP infrastructure.
- You’re using HTTP/2 and can take advantage of its multiplexing.

#### Use WebSockets if:

- You need bidirectional communication.
- The updates are frequent and require low latency.
- The application is complex (e.g., multiplayer gaming, real-time trading platforms).
- You're building a system where both the client and server frequently send messages.

#### Some hybrid applications can benefit from both:

- Use WebSockets for real-time collaboration (e.g., editing).
- Use SSE for broadcasting low-frequency updates (e.g., system-wide notifications).

## WebSockets vs WebRTC

## Unicast vs Multicast vs peer-to-peer network

