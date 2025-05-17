# AWS ELB

## What is AWS ELB

AWS Elastic Load Balancer (ELB) is a managed service provided by Amazon Web Services (AWS) that automatically distributes incoming application traffic across multiple targets, such as Amazon EC2 instances, containers, IP addresses, or Lambda functions, in one or more availability zones. ELB helps improve the availability, fault tolerance, and scalability of your applications.

## How does AWS ELB work?

Traffic Distribution:
- ELB receives incoming traffic and distributes it across registered targets (e.g., EC2 instances, containers) according to a configured load-balancing algorithm and health check status.

Health Checks:
- ELB performs health checks on registered targets to ensure they can handle requests. Unhealthy targets are removed from the rotation until they recover.

High Availability:
- ELB operates across multiple availability zones (AZs) to ensure resilience. It automatically scales to handle varying levels of traffic.

Protocol Support:
- Supports protocols like HTTP, HTTPS, WebSockets, TCP, and UDP, depending on the type of load balancer.

## Types of AWS ELB

Application Load Balancer (ALB):
- Operates at Layer 7 (HTTP/HTTPS).
- Ideal for routing traffic based on content (e.g., URL paths, host headers).
- Supports advanced features like WebSocket, server name indication (SNI), and authentication.

Network Load Balancer (NLB):
- Operates at Layer 4 (TCP/UDP).
- Best for handling high-performance, low-latency, or static IP traffic.

Gateway Load Balancer (GWLB):
- Operates at Layer 3.
- Primarily used for distributing traffic to third-party virtual appliances (e.g., firewalls, intrusion detection systems).

Classic Load Balancer (CLB):
- Operates at both Layer 4 and Layer 7.
- Legacy solution; primarily used for simple use cases.

## Use cases

Website Hosting:
- Use ALB to distribute user requests to multiple web servers.

API Gateways:
- Use ALB for routing API requests based on endpoints.

Gaming Servers:
- Use NLB for low-latency traffic distribution.

Third-Party Integrations:
- Use GWLB for security appliances or third-party traffic inspection tools.

## Advantages

Scalability:
- Automatically scales to accommodate increased traffic or reduce capacity during low traffic periods.

High Availability:
- Distributes traffic across multiple AZs, ensuring fault tolerance and minimizing downtime.

Health Monitoring:
- Continuously checks the health of targets and stops sending traffic to unhealthy targets.

Cost-Effectiveness:
- Pay-as-you-go pricing model without upfront investments.

SSL Termination:
- Offloads SSL/TLS processing to the load balancer, reducing the computational burden on backend servers.

Integration with AWS Ecosystem:
- Fully integrates with AWS services like Auto Scaling, CloudWatch, and EC2.

Content-Based Routing (ALB):
- Routes requests to specific targets based on the URL, host header, or query parameters.

## Disadvantages

Cost:
- ELB can become expensive for small-scale applications with low traffic volumes.

Latency:
- Introduces a small amount of latency due to routing and health-check processing.

Complexity:
- Requires configuration and understanding of AWS networking and security (e.g., VPC, security groups, subnets).

Dependency:
- Relying on a managed service means you are dependent on AWS for uptime and service quality.

Limited Customization:
- While powerful, ELB configurations may not meet the needs of highly specific custom load-balancing requirements.

## How load balancing is done

Request Distribution:
- ELB uses various algorithms to distribute traffic:
- Round Robin: Distributes requests evenly to all registered targets (default for CLB and ALB).
- Least Connections: Sends requests to the target with the least active connections (common in custom setups).
- Sticky Sessions: Ensures requests from the same client are sent to the same target (enabled via session cookies).

Routing Logic:
- Content-Based Routing: ALB can route traffic based on URL paths, host headers, or HTTP methods (e.g., /api requests to one service and /static to another).
- IP Hashing: Ensures consistent routing of requests from the same IP to the same backend server (custom configurations with NLB).

Multi-AZ Failover:
- If a target in one AZ becomes unhealthy, ELB routes traffic to healthy targets in other AZs.

## Load balancing for different components

Application Servers:
- ALB is ideal for routing HTTP/HTTPS traffic to application servers. It supports advanced features like URL-based routing and WebSocket connections.

Web Servers:
- ALB or CLB can distribute traffic among web servers, ensuring high availability and scalability.

Database Replicas:
- NLB can distribute traffic to read replicas of databases for high-performance read operations.

Microservices:
- ALB supports containerized workloads and integrates with services like ECS and Kubernetes, distributing traffic among microservices.

Virtual Appliances:
- GWLB is specifically designed to distribute traffic to network virtual appliances (e.g., firewalls, NAT gateways).
