
# EC2

## What is EC2

Amazon Elastic Compute Cloud (Amazon EC2) is a web service that provides secure, resizable compute capacity in the cloud.

Access reliable, scalable infrastructure on demand. Scale capacity within minutes with SLA commitment of 99.99% availability.

Optimize performance and cost with flexible options like AWS Graviton-based instances, Amazon EC2 Spot instances, and AWS Savings Plans.

Amazon Elastic Compute Cloud (Amazon EC2) provides on-demand, scalable computing capacity in the Amazon Web Services (AWS) Cloud. Using Amazon EC2 reduces hardware costs so you can develop and deploy applications faster. You can use Amazon EC2 to launch as many or as few virtual servers as you need, configure security and networking, and manage storage. You can add capacity (scale up) to handle compute-heavy tasks, such as monthly or yearly processes, or spikes in website traffic. When usage decreases, you can reduce capacity (scale down) again.

An EC2 instance is a virtual server in the AWS Cloud. When you launch an EC2 instance, the instance type that you specify determines the hardware available to your instance. Each instance type offers a different balance of compute, memory, network, and storage resources.

<img width="323" alt="image" src="https://github.com/user-attachments/assets/aab18ea4-c584-4507-8d9c-071bad4659c1">

## How does it work

Amazon Web Service EC2 is a web service which is provided by the AWS cloud which is secure, resizable, and scalable. These virtual machines are pre-configured with the operating systems and some of the required software. Instead of managing the infrastructure AWS will do that so you can just launch and terminate the EC2 instance whenever you want. You can scale up and down the EC2 instance depending on the incoming traffic. The other advantage of AWS EC2 is that you need to pay only for how much you use it is like the pay-as-you-go model.

You configure the EC2-Instance in a very secure manner by using the VPC, Subnets, and Security groups. You can scale the configuration of the EC2 instance you have configured based on the demand of the application by attaching the autoscaling group to the EC2 instance. You can scale up and scale down the instance based on the incoming traffic of the application.

The following figure shows the EC2-Instance which is deployed in VPC (Virtual Private Cloud).

<img width="246" alt="image" src="https://github.com/user-attachments/assets/bebc7163-cc5e-4960-9c13-4aac8c7d6a8f">

Amazon EC2 provides the following high-level features:

Instances:
- Virtual servers. An instance is a copy of the AMI in the AWS cloud. When launched, its configuration is a copy of the AMI that was specified at the time of launch. Once an instance is created in Amazon EC2, it runs until the user stops, hibernates or terminates it. Stopped instances can be restarted; terminated instances get deleted and cannot be restarted.

Amazon Machine Images (AMIs):
- Preconfigured templates for your instances that package the components you need for your server (including the operating system and additional software).

Instance types:
- Various configurations of CPU, memory, storage, networking capacity, and graphics hardware for your instances. An instance type determines the hardware of the host computer used for that instance.

Amazon EBS volumes:
- Persistent storage volumes for your data using Amazon Elastic Block Store (Amazon EBS).

Instance store volumes:
- Storage volumes for temporary data that is deleted when you stop, hibernate, or terminate your instance.

Key pairs:
- Secure login information for your instances. AWS stores the public key and you store the private key in a secure place.

Security groups:
- A virtual firewall that allows you to specify the protocols, ports, and source IP ranges that can reach your instances, and the destination IP ranges to which your instances can connect.

### Instance pricing options

EC2 provides the following instance pricing options:

#### On-Demand Instances

On-demand instances are charged by the hour or second. No long-term commitments are required. This pricing plan is suitable for users who need to use Amazon EC2 without having to make upfront payments as well as for applications that have unpredictable workloads or are being developed on EC2 for the first time.

#### Savings Plans

This pricing model is suitable for users looking to save money or need compute offerings for committed and steady-state usage. It can help users to reduce their EC2 bills compared to the on-demand plan. However, it requires a one- or three-year usage commitment.

#### Reserved Instances

Like savings plans, a reserved instance also provides a discount over on-demand instances. It also requires a one- or three-year usage commitment for standard or convertible reserved instances. Payments can be made up front or at a discounted hourly rate.

#### Spot Instances

Request unused EC2 instances, which can reduce your Amazon EC2 costs significantly.

Amazon EC2 spot instances are available at a discount compared to on-demand instances. "Spot" literally refers to the spot price that's in effect for the period when the instances are running. This plan is suitable for fault-tolerant or stateless workloads, applications with flexible start and end times, and applications running on heterogenous hardware.

#### Dedicated Hosts

Reduce costs by using a physical EC2 server that is fully dedicated for your use, either On-Demand or as part of a Savings Plan. You can use your existing server-bound software licenses and get help meeting compliance requirements.

#### On-Demand Capacity Reservations

Reserve compute capacity for your EC2 instances in a specific Availability Zone for any duration of time.

### Instance types

Different Amazon EC2 instance types are designed for certain activities. Consider the unique requirements of your workloads and applications when choosing an instance type. This might include needs for computing, memory, or storage.

#### General purpose instances

Amazon EC2 general-purpose instances can handle a variety of workloads. They provide a balance of compute, memory and networking resources, making them ideal for applications such as code repositories, web applications, microservices, small and medium databases and web servers.

- It provides the balanced resources for a wide range of workloads.
- It is suitable for web servers, development environments, and small databases.
- Examples: T3, M5 instances

#### Compute optimized instances

Compute-optimized instances are used to run compute-intensive applications that require large amounts of processing power and memory on the AWS cloud. Some of these instances deliver the best price performance in Amazon EC2, while others offer high packet processing performance per virtual CPU (vCPU).

- It provides high-performance processors for compute-intensive applications.
- It will be Ideal for high-performance web servers, scientific modeling, and batch processing.
- Examples: C5, C6g instances

#### GPU instances

GPU instances provide a way to run graphics-intensive applications faster than with the standard EC2 instances. Systems that rely on GPUs include gaming and design work. For example, Linux distributions often take advantage of GPUs for rendering graphical user interfaces, improving compression speeds and speeding up database queries.

#### Memory optimized instances

Memory optimized instances are larger in size with more memory and vCPUs than other types of instances. Some instances feature DDR5, or Double Data Rate 5, memory that offers more bandwidth than DDR4 memory. Others include discrete in-memory analytics accelerators that enable efficient offload, accelerate data operations, and optimize performance for many types of memory-intensive workloads.

- High memory-to-CPU ratios for large data sets.
- Perfect for in-memory databases, real-time big data analytics, and high-performance computing (HPC).
- Examples: R5, X1e instances

#### Storage optimized instances

Storage-optimized instances are ideal for applications that require high IOPS, specifically, high sequential read/write access to large data sets on local storage. Some of these instances provide excellent price performance for storage-intensive workloads in Amazon EC2, some offer very low cost per terabyte of solid state drive storage, and others deliver high local storage performance in Amazon EC2.

All storage optimized instances deliver tens of thousands of low-latency, random IOPS. For this reason, they are suitable for applications like real-time analytics, transactional databases, relational databases, NoSQL databases, search engines, data streaming and large distributed file systems.

- It provides optimized resource of instance for high, sequential read and write access to large data sets.
- Best for data warehousing, Hadoop, and distributed file systems.
- Examples: I3, D2 instances

#### Accelerated computed instances

Accelerated computing instances on Amazon EC2 perform many types of functions more efficiently than software running on CPUs. These GPU-based instances use hardware accelerators or co-processors to perform functions like floating point number calculations, graphics processing and data pattern matching.

Deep learning, generative AI, and HPC workloads are well-suited for accelerated computing instances. These instances also provide excellent performance for applications such as seismic analysis, weather forecasting, computational finance, financial modeling, speech recognition, autonomous vehicles, and computational fluid dynamics (CFD).

- It facilitates with providing hardware accelerators or co-processors for graphics processing and parallel computations.
- It is ideal for machine learning, gaming, and 3D rendering.
- Examples: P3, G4 instances

#### HPC optimized

As the name suggests, HPC instances are optimized for running HPC applications at scale while offering the best price performance. Applications that require high-performance processors can best benefit from these instances, including deep learning workloads, complex simulations, CFD, weather forecasting, multiphysics simulations, finite element analysis for crash simulations, and structural simulations.

#### Micro

A micro instance is meant for applications with low throughput. The micro instance type can serve as a small database server, as a platform for software testing or as a web server that does not require high transaction rates.

## EC2 architecture

Amazon EC2 is a cloud computing platform that can be auto-scaled to to meet demand.

Different hardware and software configurations can be selected. Different geographical locations can be selected be closer to users, as well as providing redundancy in case of failures.

Persistent storage can be provided by Amazon EBS (Elastic Block Storage). Amazon S3 (Simple Storage Service) data can also be accessed with Amazon EC2 instances, and is free if they are in the same region.

### Operating systems

Amazon EC2 includes a wide range of operating systems to choose from while selecting your AMI. Not only are these selected options, but users are also even given the privilege to upload their own operating systems and opt for that while selecting AMI during launching an EC2 instance. Currently, AWS has the following most preferred set of operating systems available on the EC2 console.

- Amazon Linux
- Windows
- Ubuntu
- Red Hat Linux
- SUSE Linux

## Use cases

### Deploying spplications

In the AWS EC2 instance, you can deploy your application like .jar,.war, or .ear application without maintaining the underlying infrastructure.

### Scaling applications

Once you deployed your web application in the EC2 instance know you can scale your application based upon the demand you are having by scaling the AWS EC2-Instance.

### Deploying ML models

You can train and deploy your ML models in the EC2-instance because it offers up to 400 Gbps), and storage services purpose-built to optimize the price performance for ML projects.

### Hybrid cloud environment

You can deploy your web application in EC2-Instance and you can connect to the database which is deployed in the on-premises servers.

## Advantages

### Availability

It offers multiple geographic regions and availability zones for strong fault tolerance and disaster recovery.

### Scalability

It helps to easily scale the instances up or down based on the demand with ensuring the optimal performance and cost-efficiency.

### Flexibility

It provides wide variety of instance types and configurations for matching different workload requirements and operating systems.

Multiple storage options - Users can select from multiple storage options including block level storage (Amazon EBS), instance storage and object storage (Amazon Simple Storage Service 3).

Operating system - EC2 supports many OSes, including Linux, Microsoft Windows Server, CentOS and Debian.

Persistent storage - Amazon's EBS service lets users attach enables block-level storage volumes to EC2 instances and be used as hard drives. With EBS, it is possible to increase or decrease the amount of storage available to an EC2 instance and attach EBS volumes to more than one instance at the same time.

Elastic IP addresses - Amazon's Elastic IP service lets users associate IP addresses with an instance. Elastic IP addresses can be moved from instance to instance without requiring a network administrator's help. This makes them ideal for use in failover clusters, for load balancing or for other purposes where there are multiple servers running the same service.

Automated scaling - Amazon EC2 Auto Scaling automatically adds or removes capacity from Amazon EC2 virtual servers in response to application demand. Auto Scaling provides more capacity to handle temporary increases in traffic during a product launch or to increase or decrease capacity based on whether use is above or below certain thresholds.

Bare-metal instances - These virtual server instances consist of the hardware resources, such as a processor, storage and network. They are not virtualized and do not run an OS, reducing their memory footprint, providing extra security and increasing their processing power.

Amazon EC2 Fleet - This service lets users deploy and manage instances as a single virtual server. The Fleet service makes it possible to launch, stop and terminate EC2 instances across EC2 instance types with one action. Amazon EC2 Fleet also provides programmatic access to fleet operations using an API. Fleet management can be integrated into existing management tools. With EC2 Fleet, policies can be scaled to automatically adjust the size of a fleet to match the workload.

Pause and resume instances - EC2 instances can be paused and resumed from the same state later. For example, if an application uses too many resources, it can be paused without incurring charges for instance usage.

### Cost

It comes with providing Pay-as-you-go model with options like On-Demand, Reserved, and Spot Instances for managing cost efficiently.

### Elastic load balancing

EC2 has several benefits. One of the main benefits of AWS EC2 is its elastic load balancing, which automatically distributes incoming application traffic across several instances while identifying unhealthy instances, and reroutes traffic to the healthy versions until restored.

## Disadvantages

While Amazon EC2 (Elastic Compute Cloud) offers powerful and flexible cloud computing services, it also comes with certain disadvantages that users should consider before adoption. Here are some of the key drawbacks:

### Cost complexities

- Costs can escalate quickly, especially with unpredictable workloads, misconfigured resources, or prolonged use of on-demand instances.
- Overprovisioning (allocating larger instances than needed) can lead to unnecessary expenses.
- EC2 has a complicated pricing model with options like on-demand, reserved instances, spot instances, and savings plans, making it difficult to estimate costs accurately.
- Charges for data transfers between EC2 instances and other AWS services or regions can add up, especially in data-intensive applications.

### Security challenges

- While AWS ensures infrastructure security, the customer is responsible for securing their applications, data, and configurations. Misconfigurations (e.g., open ports in security groups) can lead to vulnerabilities.
- EC2 instances, if improperly secured, can become targets for attacks like DDoS, data breaches, or unauthorized access.

### Instance limitations

- Each instance type comes with specific hardware and performance limits, which might not match the unique needs of certain workloads, requiring careful selection.

### Vendor lock-in

- Applications built for EC2 often rely on other AWS services, making migration to another provider challenging and time-consuming.
- The proprietary nature of AWS tools can lead to dependency on their ecosystem.

### Limited on-premises integration

Integrating EC2 instances with existing on-premises infrastructure can be complex and require additional solutions like AWS Direct Connect or VPN.

### Spot instance limitations

Spot instances, while cost-effective, can be terminated by AWS if the capacity is needed for on-demand customers, making them unsuitable for critical or long-running workloads.

## Accessing EC2

You can create and manage your Amazon EC2 instances using the following interfaces:

### Amazon EC2 console

A simple web interface to create and manage Amazon EC2 instances and resources. If you've signed up for an AWS account, you can access the Amazon EC2 console by signing into the AWS Management Console and selecting EC2 from the console home page.

### AWS Command Line Interface

Enables you to interact with AWS services using commands in your command-line shell. It is supported on Windows, Mac, and Linux.

### AWS CloudFormation

Amazon EC2 supports creating resources using AWS CloudFormation. You create a template, in JSON or YAML format, that describes your AWS resources, and AWS CloudFormation provisions and configures those resources for you. You can reuse your CloudFormation templates to provision the same resources multiple times, whether in the same Region and account or in multiple Regions and accounts.

### AWS SDKs

If you prefer to build applications using language-specific APIs instead of submitting a request over HTTP or HTTPS, AWS provides libraries, sample code, tutorials, and other resources for software developers. These libraries provide basic functions that automate tasks such as cryptographically signing your requests, retrying requests, and handling error responses, making it easier for you to get started.

### Query API

Amazon EC2 provides a Query API. These requests are HTTP or HTTPS requests that use the HTTP verbs GET or POST and a Query parameter named Action.
