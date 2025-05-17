# Reverse proxy

![image](https://github.com/user-attachments/assets/1ff41b41-a9ef-4ec2-a60b-d798844765f7)

A reverse proxy is a web server that centralizes internal services and provides unified interfaces to the public. Requests from clients are forwarded to a server that can fulfill it before the reverse proxy returns the server's response to the client.

Additional benefits include:

- Increased security - Hide information about backend servers, blacklist IPs, limit number of connections per client

- Increased scalability and flexibility - Clients only see the reverse proxy's IP, allowing you to scale servers or change their configuration

- SSL termination - Decrypt incoming requests and encrypt server responses so backend servers do not have to perform these potentially expensive operations
  - Removes the need to install X.509 certificates on each server

- Compression - Compress server responses

- Caching - Return the response for cached requests

- Static content - Serve static content directly
  - HTML/CSS/JS
  - Photos
  - Videos
  - Etc
 
## Load balancer vs reverse proxy

- Deploying a load balancer is useful when you have multiple servers. Often, load balancers route traffic to a set of servers serving the same function.

- Reverse proxies can be useful even with just one web server or application server, opening up the benefits described in the previous section.

- Solutions such as NGINX and HAProxy can support both layer 7 reverse proxying and load balancing.

## Reverse proxy disadvantages

- Introducing a reverse proxy results in increased complexity.
- A single reverse proxy is a single point of failure, configuring multiple reverse proxies (ie a failover) further increases complexity.
