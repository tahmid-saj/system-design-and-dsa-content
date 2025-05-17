# Chess game

Note that this design is similar to the SDI 'Meeting transcription system'

## Requirements

### Questions

- Users can play against other users, and users can also choose to be matched to a random user based on rank, or send a challenge request to another user. Are we designing all of this?
  - Yes
 
- Can users can also view their past games, such as games they won / tied / lost, and their previous games' moves?
  - Yes

- Are we also maintaining a leaderboard?
  - For simplicity, let's ignore this
 
- Can we assume that a player could send a challenge request to another player, only if they're online?
  - Sure

- How many users can we expect?
  - Chess.com has around 150M users in total, and 11M DAU

### Functional

- Matching players:
  - Players will come from around the world, and they can request to be matched to randomly selected players based on rank. We could also let a player send a challenge request to another player
  - We also want to temporarily store challenge requests, which will help to		efficiently search for players mainly based on their rank.

- Game:
  - 2 matched players can start a game, and should take turns in making their moves. Both of these players should see the move's results and be informed when the game ends due to a check mate / tie.

- Previous games analysis:
  - We want to send players statistics on games they’ve played, such as their games won / tied / lost, and previous game's moves, etc

### Non-functional

- Low latency:
  - We want moves to be notified to both players simultaneously, however the player’s	network is a factor in latency - thus we want to minimize the time a move is			processed in a server

- Consistency in game state during the game
- Matching between 2 players should be based on the rank

## Data model / entities

- User:
  - This entity will contain all the users, and their rank, and game performance info which will help in matching players
	- userID
 	- userName
	- rank
	- wons / losses / ties

- Game state:
  - This entity will contain the game state data, whether the game is currently being played or is a past game. This entity will also help us in generating the analysis of past games
  - Note that we can add the moves data to the game state entity, because realistically there can be a maximum of 6000 moves in a game - but this is very unlikely, since on average there are about 40 moves in a game.
	- gameID
	- whiteID, blackID (userIDs of white and black)
	- moves: [ { time, piece: BLACK_HORSE, beforePosition, afterPosition } ]
	- chessBoard: [ 8 x 8 matrix of current chessBoard state with pieces as the elements, such as { row, col, piece: BLACK_HORSE } ]
	- capturedPieces: { [ capturedWhitePieces ], [ capturedBlackPieces ] }

- Matching cache (temporary):
  - This entity will temporarily store matching requests when a player wants to be matched to another random player (that is of a similar rank as them). The player can specify a min and max rank that they want to be matched with - the min / max ranks can be restricted to a specific range depending on the player's rank.
  - There could likely also be a TTL on this entry, since it is temporarily being stored
	- userID
 	- rank
	- min / maxRank (for the matching request)


## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
  - Authentication: Bearer

- The below caching header could also be applied to fetch frequently accessed messages quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
  - Cache-Control: no-cache max-age Private/Public

### Send a request to be matched OR challenge another player

- Players can request to be matched using a min / maxRank OR they can challenge another player. We'll use webhooks for managing the communication between the client to server for both of these endpoints. As soon as clients enter the "matching page", they'll likely send a callbackURL for which webhook based events from the servers could be sent to. This callbackURL will be located on the client-side.
- Note that because the client has a callbackURL, the client will also have a small server, likely using Express, where it will listen for events sent at the callbackURL.

#### Subscribe for matching

Request:
```bash
POST /match
{
  callbackURL: http://localhost:3000/matching-webhook-callback
}
```

#### Send a request to be matched OR challenge another player


Random matching:

- If they request to be matched, their request will likely be in a cache temporarily (let's say for 5 mins) for the servers to find other players that also want to be matched. We can likely use an event-driven communication approach like a webhook where the client will subscribe to the server after they request this endpoint.
- Within the 5 mins, if the server finds a matched player, it will send an event to the callbackURL (server will temporarily store the callbackURL in memory). The event will let both clients know about the matching, and let them accept or deny. We'll talk more about webhooks in the HLD and DD, and how it might be more preferred than polling or websockets or SSE.

Challenging another player:

- When a player challenges another player, the client will also send a callbackURL to the servers, and subscribe to the server temporarily for about 30 secs. Within this 30 secs, the server will send an event to the other player's callbackURL, letting them know that another player wants to challenge them, and they can accept or deny within 30 secs. If the player accepts, then they will be redirected to the game endpoint hosting the actual game page. Likewise, the other player will also be requested via the callbackURL to accept (after the other player already accepted), and be redirected to the game page.

Request:
```bash
POST /match?op={ RANDOM_MATCHING } ( Random matching )
{
  rank
  min / maxRank
}

POST /match?op={ CHALLENGE } ( Challenge another player )
{
  userID
}
```

Response:
```bash
{
  userName1,
  rank
}
```

#### Accept the match

- After both of the randomly matched players receive events sent at their callbackURLs, containing info about the other user (such as their rank), the players can accept or deny

Request:
```bash
PATCH /match?op={ ACCEPT or DENY}
```

- After both of the players accept, they'll be redirected to the game endpoint / page

```bash
HTTP/1.1 301 Redirection
Location: /games/:gameID
```

### Make move

- We'll likely use a websocket to communicate moves between clients. We'll discuss more in the HLD and DD on this.

#### Establish a websocket connection

- This endpoint will be used to establish the websocket connection. The Sec-WebSocket-Key header will be a value that the server will use to generate a response key to send websocket requests. The Sec-WebSocket-Version will be the websocket protocol version, usually 13.

Request:
```bash
GET /games/:gameID/connect
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: xyz
Sec-WebSocket-Version: 13
```

- In the response, the Sec-WebSocket-Accept header will usually be generated by combining the Sec-WebSocket-Key from the client with another hashed value. This resulting value will be returned to the client

Response:
```bash
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: xyz + hash value
```

#### Make move

- Note that we're not sending the current player's color here, because the server should have access to the current player's color by using the database / cache, and the color is already attached to the piece we're moving

Request:
```bash
WS /games/:gameID
SEND {
  { piece: BLACK_HORSE, beforePosition, afterPosition }
}
```

Response:
```bash
RECV {
  movedPiece: BLACK_HORSE,
  beforePosition, afterPosition,
  isCaptureMove,
  isCheckMate
}
```

### Get previous game data

Request:
```bash
GET /games/:gameID
```

Response:
```bash
{
  whiteID, blackID
  moves
  chessBoard (the final chessboard state)
  capturedPieces
}
```

## HLD

### Microservice vs monolithic

- Majority of large scale systems with multiple required services and entities may be better managed using a microservice architecture. However, a monolithic architecture might be more appropriate for a chess website because it will likely be a small to moderate scale app, and it might be simpler to manage the resources within the codebase, rather than separating them out.

### Client

- The client and server will both use webhooks to communicate during the matching process. The client will be a frontend, which will also contain a small server, likely using Express, which will allow the servers to send back webhook events to a specified callbackURL in the client-side. See the resource note for 'Webhooks' for the webhook code implementation on both the client and server side.
- Chess.com, Uber and additional apps which need to send web based notifications actually also use webhooks, and we'll use it too, but either of the following could be used as well, but it might be more difficult:
  - Polling:
    - Clients can first request to be randomly matched, or request the server to challenge another user. At the same time, clients will poll for any matching / challenge requests every few seconds.
    - Polling can lead to bandwidth issues on the server-side, since connections will need to be opened and closed frequently when there are no new updates - making unnecessary network requests.
  - Websockets:
    - Since the communication during the matching process is not necessarily bidirectional, and doesn't have frequent client-server communication after the client sends a random matching / challenge request, websockets are not optimal here.
  - SSE:
    - SSEs are also no optimal here, because they are a unidirectional communication approach, initiated by the server. After the server sends a SSE to the client, the client will still need to accept / deny, which means there still needs to be some bidirectional communication here.
  - Webhooks:
    - Webhooks are within the sweet spot of the type of communication we're looking for. Webhooks are a one-way event-driven communication, where the client can subscribe to a server's topic and get events at a specific callbackURL. The communication for the matching process will likely not be as frequent, where websockets or SSE is needed, however, it will also not be as infrequent where polling is needed. We can build a simple express based server on the frontend, and listen on the callbackURL which will receive events during the matching process.

### API servers

- The API servers will handle requests for randomly matching / challenging users, redirecting to the game endpoint in the Game servers, and retrieving past games data.

Reiterating from the API design, the random matching process will be as follows:

1. When a client requests to be randomly matched, the API servers will check the cache to see if there is a similarly ranked player. If the API server is not able to find a matching within a second, it can store the match request in the cache with a TTL of about 5 mins, so that other match requests can potentially be matched to this player.
2. Once the API servers find 2 matched players, they will then send the other player's info at their callbackURLs, for them to accept / deny the match.
3. If both players accepts the match, the clients will send a request to the API servers, such that the API servers can redirect the 2 clients to the Game server's game endpoint.

<br/>

Reiterating from the API design, challenging other users will look like:

1. When a client requests the API servers to send a challenge request to another player, the API servers will send a request at the other player's callbackURL.
2. The other player can accept / deny the challenge. If the player accepts, they'll send a request to the API servers, such that the API servers can redirect this player to the Game server's game endpoint
3. Once the other player accepts the challenge, the API servers will at the same time send a request to the requesting client's callbackURL (the client who first challenged the other user), so that they can also accept and be redirected to the game endpoint / page.

### Database / cache

- The database will store all the game state data for both past and current games. We'll store the game state for current games, because we'll still potentially want to recover the game state if either clients lose network connection. When the game is being played, the database will be updated by the Game servers.

- We could use either use a NoSQL DB like DynamoDB or a SQL DB like PostgreSQL. Either one will likely work equally well, with a few tweaks such as partitioning and indexing. However, because we don't have as many relationships, and the game state data will be very write heavy as well as unstructured to some degree, we could use DynamoDB. We can also set a GSI on the Game state table, where the partition key is the gameID, and the sort key can be gameID's "endTime". This will help in querying the game state data.

<br/>

We can also use Redis sorted sets (and lists) for storing the game state and matching requests in-memory for fast access and updates:

#### Redis sorted set / list for game state

- Using Redis sorted sets and lists, we can store the current game's state. A game state entry will look as follows:

```bash
- gameID
- whiteID, blackID (userIDs of white and black)
- moves: [ { time, piece: BLACK_HORSE, beforePosition, afterPosition } ]
- chessBoard: [ 8 x 8 matrix of current chessBoard state with pieces as the elements, such as { row, col, piece: BLACK_HORSE } ]
- capturedPieces: { [ capturedWhitePieces ], [ capturedBlackPieces ] }
```

- We can easily store the moves in a Redis sorted set, and set the score as the time field. The chessBoard and capturedPieces could also be stored in lists. Storing the game state in Redis will allow the Game servers to frequently update in-memory, and also update the game state asynchronously to the Game state table. The cached game state data will also have a TTL, according to the total game time.

- When players make game moves, the move will also be sent to the other client via the Game servers.

- This game state cache could also be stored within the Game servers hosting the game, to prevent network calls being made. It will actually be better for the game state cache to be tightly coupled with the Game servers, since then the Game servers doesn't have to look up via service discovery or consistent hashing where the game state cache instance is, which will further increase latency in the game. And if consistent hashing is being used, during scaling events, the Game server could be routed to a completely different game state cache instance than before, where this game state cache won't store the Game server's current game state.

#### Redis sorted set for storing match requests

- We can also store the player's match requests in a Redis sorted set (only for random match requests). We'll set the score as the rank, and have the API servers perform a binary search between the min / maxRank in the sorted set, looking for another player with a similar rank in this range. If a matched player is found and they accept the match, that player can be removed from the sorted set.

### Game servers

- The Game servers maintain a websocket connection with the clients for the duration of the game. The Game servers will maintain a timer for the game, and allow each player to take turns in sending move requests via the websocket.

- If the client makes a move, they'll use this websocket connection. However, it's likely that we'll have users connected to different Game servers, and to deliver moves from one Game server to another, we'll likely need a short-lived lightweight bidirectional communication solution, likely using Redis PubSub.

#### Redis PubSub servers communicating game moves between Game servers

- Redis PubSub can maintain a lightweight hashmap of websocket connections. With Redis PubSub, a subscription can be created for a gameID's topic, and moves can be published to that topic which will be received at-most-once by the subscribers.

- Redis PubSub is lightweight and has an at-most-once delivery, which means that it doesn’t guarantee message delivery. If there’s no subscribers listening, then the message will be lost, and stored in the Game state table / cache.

- Redis PubSub is appropriate for this design because it sends messages only when there are currently subscribed Game servers, and if there are no subscribed Game servers, then the message is not received. This is a mock of how a chat app operates as well.

- One issue with this approach is that there is an all-to-all relationship between Game servers and Redis PubSub servers, where we’ll need connections for all those relationships. However, Redis PubSub is much more lightweight than Kafka, and will not take up as much bandwidth. We'll still discuss in the DD how we can route a game to the same Game server, which will ensure that we don't have as many connections between Game servers and Redis PubSub servers.

- Receiving moves from other clients:
  - When recipient clients connect to the Game server, the Game server will subscribe to the gameID's topic via a Redis PubSub server. Any moves published to this topic will be forwarded to the recipient client by the recipient's Game server (since the Game servers are currently subscribed).

- Sending moves to other clients:
  - When sending moves, the sender Game server will publish a move to the gameID's topic. Any currently subscribed recipient Game servers will receive this move as well. The recipient Game servers can then deliver the move to the connected client.

#### Containers in Game servers maintaining timer and handling game

- As mentioned earlier, the Game servers will likely need to have a timer to handle the game. The Game servers can have multiple containers which each handles a game and a timer. Everytime a move is sent to the Game servers, the Game server will send the move to the appropriate container.

- The container will likely also perform the updates to the database / cache and communicate with the Game servers. And once the timer is over or a player wins, the container will let the corresponding Game server (maintaining the websocket with the client that made the move / last checkmate move) know that the game has ended via the websocket connection between the containers and the Game server.

- The Game server will then publish the game / move update to Redis PubSub, and the subscribed Game server of the opponent will receive the message from the Redis PubSub channel. The opponent's Game server will then send back the game / move update to the opponent's client. The container will also update the users' profiles on the wons / losses / ties, rank, etc, once the game ends.

### L4 load balancer

- We’ll need an L4 load balancer to support traffic at the TCP level. L4 load balancers, let’s say using ELB in TCP mode can load balance websockets. When client’s need to connect to a Game server, the L4 load balancer will route them to the Game server they previously connected to or to a Game server using the load balancing algorithm. However, if a Game server goes down, the L4 load balancer can route the client to connect to another Game server instead.

- When a client needs to connect to the Game server, the request will first go to the L4 load balancer, then to the Game server. There will actually be a symmetric websocket connection between both the client to the L4 load balancer, and between the L4 load balancer to the Game server.

- L4 load balancers can be stateful and use sticky sessions to persist the server the client previously connected to. The sticky session can be implemented by identifying the user, usually with cookies or their IP address, and storing the user’s connected server for handling future requests.

- If clients disconnect from a Game server, they can automatically reconnect to the same Game server or another one via the L4 load balancer. Reconnecting to the same Game server may be easier, as the session data in the L4 load balancer doesn’t have to be updated.

<img width="1003" alt="image" src="https://github.com/user-attachments/assets/d60704a3-b0d9-40c5-80c1-2f22d1d0d35d" />

## DD

### Efficiently fetching game state data from Redis sorted sets and lists

- We will use Redis sorted sets and lists to efficiently fetch the cached game state, however we can do the following and in 'Efficiently fetching from Redis / live leaderboard' (taken from the SDI 'Leetcode'):

- Polling with database queries

- Caching with periodic updates:
  - Using this approach, we will still cache majority of the queries, but when there are cache misses,			the API servers will run the query on the database, which may still be expensive. To make sure			there are more cache hits using this approach, we could still use a cron job which runs every 10-20			secs or so and updates the cache. Thus, only the cron job will be running the expensive query on			the database, and clients will have reduced cache misses.

  - The issue with using a cron job is that if it is down, then the cache will not be updated, and it will			cause multiple cache misses OR a thundering herd due to the clients requesting the API servers to			run the expensive database query

  - If using another cache such as Memcached, it may cause race conditions if the same entry on			the cache is being updated by multiple processes, however Redis is single threaded, and thus will			likely not have this issue within a single instance

- Redis sorted set / lists with websockets / periodic polling: 
  - There may be inconsistencies between the database and cache, thus we could add CDC			(change data capture). For different databases like DynamoDB, there is DynamoDB streams, and		for PostgreSQL, there is PostgreSQL CDC. CDC is used to capture updates on the database in		the form of WAL or another operations log, and replay any missed operations on other services. Usually CDC functionalities for various databases will store the operations in the WAL, and push		it to a queue such as Kafka - then there will be workers within the other service which will pull			operations from the queue and perform the operations on the other service
  - In		this case, we can use CDC to replay operations on the DynamoDB database to the cache using		DynamoDB streams to ensure the cache and database have the same consistent data

- Note that since these approaches are taken from the SDI 'Leetcode', it's using polling. However, in our design, we're using websockets - so just substitute it with websockets. Also, we'll use Redis lists in addition to sorted sets.

Efficiently fetching from Redis / live leaderboard:

<img width="750" alt="image" src="https://github.com/user-attachments/assets/d5e1c28a-6bce-4801-b146-f55688d3e78b" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/a44ce39d-b012-4e50-957e-14b8baec10af" />

<img width="750" alt="image" src="https://github.com/user-attachments/assets/7a420fec-d6be-4908-87db-e28c8e384fde" />


**The Redis Sorted Set with websockets solution offers real-time updates and is more appropriate for this bidirectional communication. The containers within the Game servers will update this cache when game moves are sent by clients. The game move will also be sent to the other client via Redis PubSub**

### Handling multiple match requests

- Depending on the number of match requests being made, we can introduce a message queue like Kafka or SQS between the L7 load balancer and API servers. The queue acts as a buffer during traffic spikes, allowing the API servers to process match requests at a sustainable rate rather than being overwhelmed.
- The message queue also allows us to horizontally scale the API servers to consume the match requests, while providing durability to ensure no request is dropped if the API servers experiences issues.

**Adding a message queue between the L7 load balancer and API servers is likely overcomplicating the design. The API servers and cache storing the match requests should be able to handle the write throughput directly, and we'll always need some service in front of it that can scale horizontally. Unless there's expensive business logic in the API servers that we want to isolate, it's better to keep the architecture simpler and just scale the servers themselves.**

**In an interview setting, while this pattern might impress some interviewers, it's worth noting that simpler solutions are often better. Focus on properly scaling your database and API servers before adding additional components.**

### Scaling the websockets and Game servers to support millions of concurrent game moves

- Since we're using websockets, we'll need to maintain a connection with each client. A modern cloud based server can handle 100k - 1M concurrent long-lived websocket connections. However, usually hardware and OS limits like CPU, memory management, and file management becomes the bottleneck first.

**Contrary to a common misconception, the capacity isn’t limited to 65,535 connections. That number refers to the range of port numbers, not the number of connections a single server port can handle. Each TCP connection is identified by a unique combination of source IP, source port, destination IP, and destination port. With proper OS tuning and resource allocation, a single listening port can handle hundreds of thousands or even millions of concurrent SSE connections.
In practice, however, the server’s hardware and OS limits—rather than the theoretical port limit—determine the maximum number of simultaneous connections.**

- By using Redis PubSub servers, there will be all-to-all connections between the Game servers to the Redis PubSub servers as mentioned in the HLD. We can solve this issue by doing the following:
  - Ultimately, we want to reduce the all-to-all connections as much as possible. This means that we want a single Game server to subscribe to as few topics in the PubSub servers as possible, so that it doesn't lead to an all-to-all connection issue between the Game servers to the PubSub servers.
  - The all-to-all connections can be reduced by using a L7 load balancer OR a dynamic lookup via a configuration service (ZooKeeper) to always route 2 players for a gameID to the same Game server using the gameID parameter in the HTTP request when the client first requests to establish a websocket. This way, clients will first be redirected to the gameID's endpoint in the Game server hosting the actual game page, then they'll request to establish a websocket connection with the same Game server using an HTTP request containing the gameID. This way, the 2 players will be connected to the same Game server via websockets. We're using L7 load balancers instead of L4 because HTTP requests are what establishes the websocket, and L4 LBs can't route requests using any parameters - it can only use IP, ports, etc.
  - Making sure that the 2 players are connected to the same Game server will mean that there's no longer a need for a Redis PubSub server, since the same Game server can send the game state and move updates to both 2 players. However, some servers are far away from users, and thus it's still necessary to have PubSub servers between them because the websocket connections are not on the same Game server. By making sure that there's still a good portion of gameIDs being held on the same Game server, we'll greatly reduce the number of all-to-all connections.

### Fairness in latency

- Let’s assume 2 different players have differing internet latencies of 300 ms vs 50 ms. We can first ping the clients 2-3	times to get the round trip time and evaluate their internet latency. After comparing the 2 player’s internet latencies, we	can introduce fairness in latency if the latencies differ too much. We can give much slower clients up to 500 ms of extra	time, or the delay time that is introduced from the internet latency calculation via the round trip. For clients with faster	internet latencies, we don’t need to give them extra time.

### WebRTC

- It is possible to connect clients directly via a peer-to-peer connection like WebRTC, which will reduce the load on the	servers. However, without a mediator such as a server in between the clients, clients have an easier way of cheating		as there are no servers handling the security or validation of the move.

### Reverse proxies

- Clients can also be connected to reverse proxies which route requests to the backend services such as Game servers.

- A peer-to-peer bidirectional connection such as websockets can be used to allow communication between clients to	the reverse proxies. A websocket is preferable as opposed to HTTP or polling due to it’s bidirectional nature, and it’s		ability to maintain a TCP connection for two-way communication, whereas HTTP needs to create a connection for		every request.
  
- To maintain a mapping of the reverse proxies the clients are connected to, we can store the mappings in a service		discovery service which utilizes Zookeeper. Thus, all the reverse proxies could connect to the service discovery		service.

<br/>
<br/>

Additional deep dives:

### Thundering herds
  
- When we have to restart the gateway or connection to the clients, and the existing connected clients try to reconnect	to the restarted servers, it will cause a thundering herd problem as a massive number of clients will try to reconnect all	at once to the same gateway. This is further shown in ‘Thundering herd during server restarts’
	
- A solution to the thundering herd issue is to use a separate connection service that connects to the service discovery	service and the backend services such as game engine and matching service. The connection service doesn’t connect	to the clients directly, but only connects to the gateways. The gateways are positioned to be directly connected to all		the clients. Therefore, any restarts on the connections could be made on the connections service without causing a		thundering herd.

- The connection service is essentially a mapper or mediator between the gateways and the backend services, so that	the gateway doesn’t only maintain the connection - the connection service maintains it as well. Thus, any changes or	restarts on	the connections can be made to the connection service, without the change affecting all the client			connections. This is shown in ‘Connection service’

Thundering herd during server restarts:

<img width="850" alt="image" src="https://github.com/user-attachments/assets/59b708f6-8887-404f-8ff4-2d2255123469" />

<br/>
<br/>

Connection service:

<img width="850" alt="image" src="https://github.com/user-attachments/assets/ee47a208-403b-4c59-90b5-16e282b8d686" />
