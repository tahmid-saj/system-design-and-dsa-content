# Proxy servers

## Proxy servers introduction

A proxy server is an intermediate piece of software or hardware that sits between the client and the server. Clients connect to a proxy to make a request for a service like a web page, file, or connection from the server. Essentially, a proxy server (aka the forward proxy) is a piece of software or hardware that facilitates the request for resources from other servers on behalf of clients, thus anonymizing the client from the server.

A forward proxy, also known as a "proxy server," or simply "proxy," is a server that sits in front of one or more client machines and acts as an intermediary between the clients and the internet. When a client machine makes a request to a resource (like a web page or file) on the internet, the request is first sent to the forward proxy. The forward proxy then forwards the request to the internet on behalf of the client machine and returns the response to the client machine.

![image](https://github.com/user-attachments/assets/0e2824f9-e7b3-4ae7-acf1-5bdd49466bd2)

Typically, forward proxies are used to cache data, filter requests, log requests, or transform requests (by adding/removing headers, encrypting/decrypting, or compressing a resource).

A forward proxy can hide the identity of the client from the server by sending requests on behalf of the client.

In addition to coordinating requests from multiple servers, proxies can also optimize request traffic from a system-wide perspective. Proxies can combine the same data access requests into one request and then return the result to the user; this technique is called collapsed forwarding. Consider a request for the same data across several nodes, but the data is not in cache. By routing these requests through the proxy, they can be consolidated into one so that we will only read data from the disk once.

### Reverse proxy

A reverse proxy retrieves resources from one or more servers on behalf of a client. These resources are then returned to the client, appearing as if they originated from the proxy server itself, thus anonymizing the server. Contrary to the forward proxy, which hides the client's identity, a reverse proxy hides the server's identity.

A reverse proxy is a server that sits in front of one or more web servers and acts as an intermediary between the web servers and the Internet. When a client makes a request to a resource on the internet, the request is first sent to the reverse proxy. The reverse proxy then forwards the request to one of the web servers, which returns the response to the reverse proxy. The reverse proxy then returns the response to the client.

Contrary to the forward proxy, which hides the client's identity, a reverse proxy hides the server's identity.

![image](https://github.com/user-attachments/assets/8be2eeb5-7784-447b-bab0-8c4e48205502)

In the above diagram, the reverse proxy hides the final server that served the request from the client. The client makes a request for some content from facebook.com; this request is served by facebook’s reverse proxy server, which gets the response from one of the backend servers and returns it to the client.

A reverse proxy, just like a forward proxy, can be used for caching, load balancing, or routing requests to the appropriate servers.

![image](https://github.com/user-attachments/assets/be27e385-1f2e-4bb9-8e22-e7217ba405b9)

### Summary

A proxy is a piece of software or hardware that sits between a client and a server to facilitate traffic. A forward proxy hides the identity of the client, whereas a reverse proxy conceals the identity of the server. So, when you want to protect your clients on your internal network, you should put them behind a forward proxy; on the other hand, when you want to protect your servers, you should put them behind a reverse proxy.

## Proxy server use cases

Proxy servers serve a variety of purposes in networked environments, often enhancing performance, security, and privacy. The following are some common uses of proxy servers:

### Performance enhancement

Proxy servers can cache frequently accessed content, reducing the need for repeated requests to the target server. This caching mechanism can improve response times, reduce bandwidth usage, and decrease the load on target servers.

### Security enhancement

Proxy servers can act as a protective barrier between clients and target servers, enforcing access control policies and filtering malicious or harmful content. By monitoring and filtering network traffic, proxy servers can help protect internal networks from external threats and prevent unauthorized access to sensitive resources.

### Anonymity and privacy

Proxy servers can mask the client's IP address and other identifying information, providing a level of anonymity and privacy when accessing the internet or other network resources. This is particularly useful for clients who wish to access content that is restricted based on geographic location or to avoid tracking and surveillance.

### Load balancing

Reverse proxy servers can distribute client requests across multiple target servers, preventing individual servers from becoming overburdened and ensuring high availability and performance. Load balancing can be particularly beneficial for large-scale applications and services with high levels of concurrent users or requests.

### Centralized control and monitoring

Proxy servers enable centralized control and monitoring of network traffic, facilitating easier administration and management of network resources. Administrators can implement policies, filters, and other configurations on the proxy server to manage traffic and optimize network performance.

### Content filtering

Proxy servers can be configured to block or filter specific content types, websites, or services based on predetermined policies. This functionality is often used in educational and corporate environments to enforce acceptable use policies or comply with regulatory requirements.

### Content adaptation and transformation

Proxy servers can modify and adapt content to suit specific client requirements, such as altering image formats, compressing data, or adjusting content for mobile or low-bandwidth devices. This capability enhances the user experience by ensuring that content is optimized for the client's device and network conditions.

### Logging and auditing

Proxy servers can log and record network traffic, providing a valuable source of information for auditing, troubleshooting, and monitoring purposes. Detailed logs can help administrators identify performance issues, security vulnerabilities, or policy violations and take appropriate corrective action.

### SSL termination

Reverse proxy servers can handle SSL/TLS encryption and decryption, offloading this task from the target servers. This process, known as SSL termination, can improve the performance of target servers by reducing the computational overhead associated with encryption and decryption.

### Application-level gateway

Proxy servers can act as an application-level gateway, processing and forwarding application-specific requests and responses between clients and servers. This capability allows proxy servers to provide added functionality, such as authentication, content filtering, or protocol translation, at the application level.

Proxy servers play a crucial role in enhancing the performance, security, and privacy of networked environments, providing numerous benefits to both clients and target servers.

## VPN vs proxy servers

VPN (Virtual Private Network) and Proxy Servers are both tools used for privacy and security online, but they function differently and serve distinct purposes. Understanding their differences is essential in determining which one to use based on your needs.

### VPN (Virtual private network)

A VPN creates a secure, encrypted tunnel between your device and a remote server operated by the VPN service. All your internet traffic is routed through this tunnel, meaning that your data is secure from external observation.

#### Characteristics

- Encryption
  - Offers end-to-end encryption for all data transmitted.
- Traffic Routing
  - Routes all internet traffic through the VPN server.
- IP Masking
  - Hides your IP address and makes it appear as if your traffic is coming from the VPN - server’s location.
- Security and Privacy
  - Provides a high level of security and privacy.

#### Use cases

- Securing data while using public Wi-Fi networks.
- Bypassing geographical restrictions and censorship.
- Protecting sensitive transactions (like online banking).

#### Example

Using a VPN service while connecting to a public Wi-Fi network at a coffee shop to securely access your personal and work accounts.

### Proxy server

A Proxy Server acts as an intermediary between your device and the internet. It receives your requests, forwards them to the internet, and then relays the response back to you.

#### Characteristics

- IP Masking
  - Hides your IP address, making it appear as if the requests are coming from the proxy’s location.
- Limited Scope
  - Usually, only browser traffic or traffic from specific applications is rerouted.
- No Encryption
  - Does not inherently encrypt data (except for secure proxy servers like HTTPS proxies).
- Caching
  - Some proxies cache data, which can speed up subsequent requests to the same sites.

### VPN vs proxy servers

#### Encryption

- VPN
  - Encrypts all data between your device and the VPN server.
- Proxy Server
  - Does not encrypt data (unless it’s a special type of proxy like an HTTPS proxy).

#### Traffic Routing

- VPN
  - Reroutes and encrypts all internet traffic from your device.
- Proxy Server
  - Only reroutes traffic from your browser or specific apps, not necessarily encrypting it.

#### Privacy and Security

- VPN
  - Offers more privacy and security due to encryption and comprehensive traffic routing.
- Proxy Server
  - Provides IP masking but limited security features.

#### Performance

- VPN
  - Can be slower due to encryption overhead.
- Proxy Server
  - Usually faster than VPN as there’s no encryption, but can be slower if many users access the same proxy.

#### Use Case Suitability

- VPN
  - Suitable for users concerned with privacy and security, especially when using public Wi-Fi networks.
- Proxy Server
  - Good for bypassing content restrictions or simple IP masking without the need for encryption.

The choice between a VPN and a proxy server depends on your specific needs. If you prioritize privacy and security, especially when handling sensitive data, a VPN is the better choice. If you simply need to bypass geo-restrictions or internet filters for browsing purposes, a proxy server might suffice. For the best security, a VPN is recommended due to its encryption capabilities and comprehensive coverage of all internet traffic.

