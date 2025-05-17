# API gateway 101

## What is an API gateway

There's a good chance you've interacted with an API Gateway today, even if you didn't realize it. They're a core component in modern architectures, especially with the rise of microservices.

Think of it as the front desk at a luxury hotel. Just as hotel guests don't need to know where the housekeeping office or maintenance room is located, clients shouldn't need to know about the internal structure of your microservices.

An API Gateway serves as a single entry point for all client requests, managing and routing them to appropriate backend services. Just as a hotel front desk handles check-ins, room assignments, and guest requests, an API Gateway manages centralized middleware like authentication, routing, and request handling.

The evolution of API Gateways parallels the rise of microservices architecture. As monolithic applications were broken down into smaller, specialized services, the need for a centralized point of control became evident. Without an API Gateway, clients would need to know about and communicate with multiple services directly – imagine hotel guests having to track down individual staff members for each request.

API gateways are thin, relatively simple components that serve a clear purpose. In this deep dive, we'll focus on what you need to know for system design interviews without overcomplicating things.

## Core responsibilities

The gateway's primary function is request routing – determining which backend service should handle each incoming request. But this isn't all they do.

Hellointerview.com note: Funny enough, I'll often have candidates introduce a gateway in a system design interview and emphasize that it will do all this middleware stuff but never mention the core reason they need it -- request routing.

Nowadays, API gateways are also used to handle cross-cutting concerns or middleware like authentication, rate limiting, caching, SSL termination, and more.

### Tracing a request

Let's walk through a request from start to finish. Incoming requests come into the API Gateway from clients, usually via HTTP but they can be gRPC or any other protocol. From there, the gateway will apply any middleware you've configured and then route the request to the appropriate backend service.

1. Request validation
2. API Gateway applies middleware (auth, rate limiting, etc.)
3. API Gateway routes the request to the appropriate backend service
4. Backend service processes the request and returns a response
5. API Gateway transforms the response and returns it to the client
6. Optionally cache the response for future requests

<img width="643" alt="image" src="https://github.com/user-attachments/assets/057fcce7-7800-4851-b63d-1395285c0284">
<br/>
<br/>

1. Request Validation

Before doing anything else, the API Gateway checks if incoming requests are properly formatted and contain all the required information. This validation includes checking that the request URL is valid, required headers are present, and the request body (if any) matches the expected format.
This early validation is important because it helps catch obvious issues before they reach your backend services. For example, if a mobile app sends a malformed JSON payload or forgets to include a required API key, there's no point in routing that request further into your system. The gateway can quickly reject it and send back a helpful error message, saving your backend services from wasting time and resources on requests that were never going to succeed.

2. Middleware

API Gateways can be configured to handle various middleware tasks. For example, you might want to:

- Authenticate requests using JWT tokens
- Limit request rates to prevent abuse
- Terminate SSL connections
- Log and monitor traffic
- Compress responses
- Handle CORS headers
- Whitelist/blacklist IPs
- Validate request sizes
- Handle response timeouts
- Version APIs
- Throttle traffic
- Integrate with service discovery

Of these, the most popular and relevant to system design interviews are authentication, rate limiting, and ip whitelisting/blacklisting. If you do opt to mention middleware, just make sure it's with a purpose and that you don't spend too much time here.

My suggestion when introducing a API Gateway to your design is to simply mention, "I'll add a API Gateway to handle routing and basic middleware" and move on.

3. Routing

The gateway maintains a routing table that maps incoming requests to backend services. This mapping is typically based on a combination of:

- URL paths (e.g., /users/* routes to the user service)
- HTTP methods (e.g., GET, POST, etc.)
- Query parameters
- Request headers

For example, a simple routing configuration might look like:

```yml
routes:
  - path: /users/*
    service: user-service
    port: 8080
  - path: /orders/*
    service: order-service
    port: 8081
  - path: /payments/*
    service: payment-service
    port: 8082
```

The gateway will quickly look up which backend service to send the request to based on the path, method, query parameters, and headers and send the request onward accordingly.

4. Backend communication

While most services communicate via HTTP, in some cases your backend services might use a different protocol like gRPC for internal communication. When this happens, the API Gateway can handle translating between protocols, though this is relatively uncommon in practice.

The gateway would, thus, transform the request into the appropriate protocol before sending it to the backend service. This is nice because it allows your services to use whatever protocol or format is most efficient without clients needing to know about it.

5. Response Transformation

The gateway will transform the response from the backend service into the format requested by the client. This transformation layer allows your internal services to use whatever protocol or format is most efficient, while presenting a clean, consistent API to clients.

For example:

```yml
// Client sends a HTTP GET request
GET /users/123/profile

// API Gateway transforms this into an internal gRPC call
userService.getProfile({ userId: "123" })

// Gateway transforms the gRPC response into JSON and returns it to the client over HTTP
{
  "userId": "123",
  "name": "John Doe",
  "email": "john@example.com"
}
```

6. Caching

Before sending the response back to the client, the gateway can optionally cache the response. This is useful for frequently accessed data that doesn't change often and, importantly, is not user specific. If your expectation is that a given API request will return the same result for a given input, caching it makes sense.

The API Gateway can implement various caching strategies too. For example:
- Full Response Caching: Cache entire responses for frequently accessed endpoints
- Partial Caching: Cache specific parts of responses that change infrequently
- Cache Invalidation: Use TTL or event-based invalidation

In each case, you can either cache the response in memory or in a distributed cache like Redis.

## Scaling an API gateway

When discussing API Gateway scaling in interviews, there are two main dimensions to consider: handling increased load and managing global distribution.

### Horizontal scaling

The most straightforward approach to handling increased load is horizontal scaling. API Gateways are typically stateless, making them ideal candidates for horizontal scaling. You can add more gateway instances behind a load balancer to distribute incoming requests.

While API Gateways are primarily known for routing and middleware functionality, they often include load balancing capabilities. However, it's important to understand the distinction:

- Client-to-Gateway Load Balancing: This is typically handled by a dedicated load balancer in front of your API Gateway instances (like AWS ELB or NGINX).
- Gateway-to-Service Load Balancing: The API Gateway itself can perform load balancing across multiple instances of backend services.

This can typically be abstracted away during an interview. Drawing a single box to handle "API Gateway and Load Balancer" is usually sufficient. You don't want to get bogged down in the details of your entry points as they're more likely to be a distraction from the core functionality of your system.

### Global distribution

Another option that works well particularly for large applications with users spread across the globe is to deploy API Gateways closer to your users, similar to how you would deploy a CDN. This typically involves:

- Regional Deployments: Deploy gateway instances in multiple geographic regions
- DNS-based Routing: Use GeoDNS to route users to the nearest gateway
- Configuration Synchronization: Ensure routing rules and policies are consistent across regions

Let's take a look at some of the most popular API Gateways:

<img width="610" alt="image" src="https://github.com/user-attachments/assets/b9b06904-4145-41d6-9136-4175c6e14576">

<img width="475" alt="image" src="https://github.com/user-attachments/assets/e48b0029-98df-4cd6-8810-0614b6265e7f">

## When to propose an API gateway

Ok cool, but when should you use an API Gateway in your interview?

The TLDR is: use it when you have a microservices architecture and don't use it when you have a simple client-server architecture.

With a microservices architecture, an API Gateway becomes almost essential. Without one, clients would need to know about and communicate with multiple services directly, leading to tighter coupling and more complex client code. The gateway provides a clean separation between your internal service architecture and your external API surface.

However, it's equally important to recognize when an API Gateway might be overkill. For simple monolithic applications or systems with a single client type, introducing an API Gateway adds unnecessary complexity.

I've mentioned this throughout, but I want it to be super clear. While it's important to understand every component you introduce into your design, the API Gateway is not the most interesting. There is a far greater chance that you are making a mistake by spending too much time on it than not enough.
Get it down, say it will handle routing and middleware, and move on.

# AWS API gateway

## What is AWS API gateway?

AWS API Gateway is a fully managed service that enables developers to create, publish, monitor, and secure APIs at any scale. It serves as a gateway for applications to access backend services, such as AWS Lambda, Amazon EC2, or any HTTP endpoint. API Gateway handles the entire API lifecycle, including deployment, versioning, and security.

## How does it work

API Creation:
- Developers define API endpoints, request/response models, and integrations with backend services using the API Gateway console, AWS CLI, or AWS SDKs.

Routing:
- API Gateway routes incoming HTTP or WebSocket requests to the appropriate backend service based on the configured routes.

Request Transformation:
- Incoming requests can be transformed (e.g., JSON to XML) or validated against a schema before reaching the backend.

Security:
- API Gateway enforces security using authentication mechanisms such as AWS Identity and Access Management (IAM), API keys, or third-party OAuth 2.0 providers.

Throttling and Rate Limiting:
- Automatically throttles requests to prevent backend overload and ensures compliance with usage plans.

Monitoring:
- Provides detailed metrics, logs, and tracing data for monitoring API usage and diagnosing issues.

## Advantages

Fully Managed:
- Simplifies API deployment and management, allowing developers to focus on application logic.

Scalability:
- Automatically scales to handle high traffic volumes.

Security:
- Built-in support for AWS IAM, API keys, Lambda authorizers, and OAuth 2.0 for authentication and authorization.

Flexibility:
- Supports RESTful APIs, WebSocket APIs, and HTTP APIs.

Integration with AWS Services:
- Seamlessly integrates with AWS Lambda, DynamoDB, S3, Step Functions, and more.

Throttling and Quotas:
- Allows fine-grained control over API usage and prevents abuse by throttling or setting usage quotas.

Monitoring and Logging:
- Integrates with Amazon CloudWatch to provide detailed metrics and logs.

Cost-Effectiveness:
- Pay-as-you-go pricing model with no upfront costs.

## Disadvantages

Cost for High Traffic:
- Can become expensive with very high request volumes compared to alternatives like Application Load Balancer (ALB) for simple use cases.

Latency:
- Adds a slight overhead to API requests due to processing and routing.

Learning Curve:
- Configuring API Gateway effectively requires understanding multiple AWS concepts and services.

Cold Starts with Lambda:
- When used with AWS Lambda, cold starts can introduce latency for the first request.

Complexity for Simple Use Cases:
- API Gateway can be overkill for simple applications requiring basic routing.

## Features of AWS API gateway

Multi-Protocol Support:
- RESTful APIs: For traditional HTTP-based APIs.
- WebSocket APIs: For real-time, two-way communication.
- HTTP APIs: Lightweight APIs optimized for performance.

Authentication and Authorization:
- AWS IAM roles.
- API keys for usage plans.
- Lambda authorizers for custom authentication.
- Integration with third-party OAuth 2.0 providers.

Request Transformation and Validation:
- Transform incoming requests and outgoing responses.
- Validate request payloads against JSON schemas.

Throttling and Rate Limiting:
- Protect backend services by limiting the number of requests.

CORS (Cross-Origin Resource Sharing):
- Simplifies integration with front-end applications by managing CORS headers.

Monitoring and Analytics:
- Provides metrics such as request count, latency, and error rates.
- Logs requests and responses in Amazon CloudWatch.

Caching:
- Reduces latency and backend load by enabling response caching at the API Gateway level.

API Versioning:
- Supports deploying multiple versions of the same API.

Deployment Stages:
- Manage APIs across stages like development, staging, and production.

Custom Domain Names:
- Allows APIs to be accessed using custom domains with SSL/TLS.

## Use cases of AWS API gateway

Building Serverless Applications:
- Use API Gateway with AWS Lambda to create scalable and cost-efficient serverless APIs.

Microservices Architecture:
- Acts as a single entry point for multiple microservices.

Real-Time Applications:
- Enable WebSocket APIs for real-time communication in chat apps, notifications, or gaming.

API Monetization:
- Create usage plans and API keys to offer tiered access to APIs for monetization.

Backend for Mobile or Web Apps:
- Serve as a backend for front-end applications, handling business logic and data transformation.

IoT Applications:
- Provide APIs for IoT devices to communicate with backend services.

Modernizing Legacy Systems:
- Wrap legacy systems with an API to make them accessible via modern interfaces.
