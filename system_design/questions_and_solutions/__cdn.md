# CDN

## Requirements

### Functional

- Retrieve from origin servers:
  - Depending on the type of CDN models, the CDN proxy servers should be able to retrieve content from the origin servers
- Request proxy servers:
  - Clients should be able to for request data from the proxy servers

- Deliver from origin to proxy servers:
  - If the model is push based, the origin servers should be able to send the content to the CDN proxy servers
- Search for data in CDN infrastructure:
  - The CDN should be able to execute a search against a user query for cached or otherwise stored content within the CDN infrastructure

- Update CDN content:
  - The CDN should be able to update the content within CDN proxy servers in a PoP through scripting
- Delete / Invalidation:
  - Depending on the type of content (static / dynamic), the CDN should be able to delete or invalidate records

### Non-functional

- Availability / scalability
- Low latency
- Throughput

## CDN 101

- CDNs are intermediate servers between a client and the origin server, and are placed on the network edge (location where a device or local network interfaces with the internet)
- A CDN stores two types of data:
  - Static
  - Dynamic

- It is assumed CDNs are located at the ISP or IXP (internet exchange points) to handle high request traffic

**Note: Various streaming protocols are used to deliver dynamic content by the CDN providers. For example, CDNsun uses the Real-time Messaging Protocol (RTMP), HTTP Live Streaming (HLS), Real-time Streaming Protocol (RTSP), and many more to deliver dynamic content.**

## HLD

**We'll do the HLD before the API design because we need to know the CDN components first**

### Routing system

- The routing system directs clients to the nearest CDN. To do this, this component receives input		from various systems to understand where the content is placed, how many requests are made for a	particular content and the URI for various contents

### Scrubber servers

- Scrubber servers are used to separate the good traffic from malicious traffic and protect against		attacks.

### Proxy servers
  
- Proxy servers serve the actual content (from RAM to the users) and receive content from the		distribution system
- A PoP (group of proxy servers) will contain a control core which maintains information / location on	all the proxy servers in the PoP

### Distribution system

- Is responsible for distributing content to all edge proxy servers

### Origin servers

- Receives content from the edge proxy servers and also serves content to the proxy servers. The		origin servers will use appropriate stores to keep content mappings and other metadata

### Monitoring system

- Monitoring system will measure and collect metrics from edge proxy servers and origin servers

## API design

### CDN proxy server to receive content from origin server

Request:
```bash
GET /origin/:originServerID/content/:proxyServerID?filterOptions={}
{
	originServerID
	proxyServerID
	filterOptions: { contentType, contentVersion }
}
```

Response: 
```bash
{[
	{
		contentID
		contentType
		contentVersion
		contentMetadata
		content
	}
]}
```

### CDN origin server uses this endpoint to send content to multiple proxy servers - without the proxy server requesting for the content

Request:
```bash
POST /origin/:originServerID/content
{
	originServerID
	proxyServerList: [ proxyServerID ]
	filterOptions: { contentType, contentVersion }
}
```

Response (to a single proxy server): 
```bash
{
	proxyServerID
	contentID
	contentType
	contentVersion
	contentMetadata
	content
}
```

### Clients will use this endpoint to request content from proxy servers

Request:
```bash
GET /proxy/:proxyServerID/content?filterOptions={}
{
	proxyServerID
	filterOptions: { contentType, contentVersion }
}
```

Response: 
```bash
{
		contentID
		contentType
		contentVersion
		contentMetadata
		content
}
```

### CDN proxy servers can use this to search content from peer proxy servers in the PoP

Request:
```bash
GET /proxy/content?filterOptions={}
{
	filterOptions: { contentType, contentVersion }
}
```

Response: 
```bash
[
	{
		contentID
		contentType
		contentVersion
		contentMetadata
		content
	}
]
```

### CDN proxy servers can use this to update content in peer proxy servers in the PoP

Request: 
```bash
PUT /proxy/content
{
	proxyServerID
	content: [
			{
				contentID
				contentType
				contentVersion
				contentMetadata
				content
			}
	]

}
```

Response: 
```bash
{
	contentUpdated: True
}
```

## CDN workflow

The workflow for the design is given below:

1. The origin servers provide the URI namespace delegation of all objects cached in the CDN to the request routing system.

2. The origin server publishes the content to the distribution system responsible for data distribution across the active edge proxy servers.

3. The distribution system distributes the content among the proxy servers and provides feedback to the request routing system. This feedback is helpful in optimizing the selection of the nearest proxy server for a requesting client. This feedback contains information about which content is cached on which proxy server to route traffic to relevant proxy servers.

4. The client requests the routing system for a suitable proxy server from the request routing system.

5. The request routing system returns the IP address of an appropriate proxy server.

6. The client request routes through the scrubber servers for security reasons.

7. The scrubber server forwards good traffic to the edge proxy server.

8. The edge proxy server serves the client request and periodically forwards accounting information to the management system. The management system updates the origin servers and sends feedback to the routing system about the statistics and detail of the content. However, the request is routed to the origin servers if the content isn’t available in the proxy servers. It’s also possible to have a hierarchy of proxy servers if the content isn’t found in the edge proxy servers. For such cases, the request gets forwarded to the parent proxy servers.

## DD

### CDN model types
- Push:
  - Content gets sent automatically to the CDN proxy servers from the origin server. The content delivery to the CDN proxy			servers is the content provider’s responsibility. Push CDN is appropriate for static content delivery, where the origin server			decides which content to deliver to users. If the content is dynamic, the origin servers in the push model may struggle to			keep up to date with the changing content.

- Pull:
  - Requests for content is sent to the origin servers from the proxy servers. The requested content is then delivered to the			proxy servers from the origin servers. This model is better for dynamic content. The pull model may also contain less			replicas of proxy servers since dynamic content is served to a smaller range of users, rather than static content (for push		         model).

- Most CDN providers use both the push and pull model to get benefits of both

### Multi-tier CDN architecture

- Content from origin servers distribute content to parent proxy servers which distribute to child proxy servers in a tree like			structure. Multi-tiering allows us to scale the CDN for increasing number of users, and reduces the burden of delivering content		from the origin server to the proxy servers - parent proxy servers can delivery content instead of the origin servers.

- If one child proxy server is down, the request can be routed to the parent proxy servers which will contain the content for the		request.

### Handling failures

- If one proxy server is down, another proxy server in the PoP can resume the work and provide the cached content

- If a origin server is down, the cached content in the proxy servers can still be delivered to end users while the origin server is		being recovered

- Checkpointing of cached operations could be maintained in proxy servers and origin servers (however checkpointing is 			preferred for non-volatile data)

- Hearbeat protocol can be used to monitor the health of proxy servers in a PoP

### Periodic polling
  
- If going with a pull model, proxy servers can request the origin server periodically and update the content in the cache			accordingly. It can use a TTR (time to refresh) for requesting updated data from the origin servers.

### Content invalidation

- The content could have a TTL assigned to it by the origin server, so that the content expires after a time

### Lease

- The origin servers could also assign a lease value to the content, which is the time interval for which the origin server agrees		to notify the proxy servers of any changes for the content

<br/>

Facts:

### Anycast

- Anycast is a routing methodology where all servers located in multiple locations share the same IP address. It uses Border		Gateway Protocol (BGP) (where every node in a network is aware of the location and status of other nearby nodes in the			network) to route clients to nearby servers.

### Client multiplexing
  
- Client multiplexing involves sending a list of candidate servers to the client, and the client then chooses one server from the 		list to send the request to.

### HTTP redirection

- HTTP redirection is the simplest of all approaches, where the client requests content from the origin server. The origin server		responds with an HTTP protocol to redirect the user via a URL.

### Predictive push

- Predictive push is a research where we decide what to push near the clients

### ProxyTeller

- ProxyTeller can decide where to place the proxy servers and how many proxy servers are required to achieve high				performance

CDN design:

<img width="800" alt="image" src="https://github.com/user-attachments/assets/84197ff5-2a30-45af-af23-4ee17a0bba2a" />

<br/>
<br/>

Multi-tier CDN architecture:

<img width="680" alt="image" src="https://github.com/user-attachments/assets/d90c338e-a775-4fc3-b7c0-2890201d8ab8" />

<br/>
<br/>

HTTP redirection of CDN entry:

<img width="660" alt="image" src="https://github.com/user-attachments/assets/e5e207c6-f0f1-4541-9ae7-24997be4a021" />



