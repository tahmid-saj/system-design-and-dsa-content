# AWS Lambda

## What is Lambda

Run code without provisioning or managing servers, creating workload-aware cluster scaling logic, maintaining event integrations, or managing runtimes. 

Run code for virtually any type of application or backend service. Just upload your code as a ZIP file or container image, and Lambda automatically allocates compute execution power and runs your code based on the incoming request or event, for any scale of traffic.

Write Lambda functions in your favorite language (Node.js, Python, Go, Java, and more) and use both serverless and container tools, such as AWS SAM or Docker CLI, to build, test, and deploy your functions.

You can use AWS Lambda to run code without provisioning or managing servers.

Lambda runs your code on a high-availability compute infrastructure and performs all of the administration of the compute resources, including server and operating system maintenance, capacity provisioning and automatic scaling, and logging. With Lambda, all you need to do is supply your code in one of the language runtimes that Lambda supports.

You organize your code into Lambda functions. The Lambda service runs your function only when needed and scales automatically. You only pay for the compute time that you consume—there is no charge when your code is not running.

AWS Lambda automatically runs code in response to multiple events, such as HTTP requests via Amazon API Gateway, modifications to objects in Amazon Simple Storage Service (Amazon S3) buckets, table updates in Amazon DynamoDB, and state transitions in AWS Step Functions.

Lambda runs your code on high availability compute infrastructure and performs all the administration of your compute resources. This includes server and operating system maintenance, capacity provisioning and automatic scaling, code and security patch deployment, and code monitoring and logging. All you need to do is supply the code.

## How does it work

AWS Lambda is a serverless computing service provided by Amazon Web Services (AWS). Users of AWS Lambda create functions, self-contained applications written in one of the supported languages and runtimes, and upload them to AWS Lambda, which executes those functions in an efficient and flexible manner.

The Lambda functions can perform any kind of computing task, from serving web pages and processing streams of data to calling APIs and integrating with other AWS services.

The concept of “serverless” computing refers to not needing to maintain your own servers to run these functions. AWS Lambda is a fully managed service that takes care of all the infrastructure for you. And so “serverless” doesn’t mean that there are no servers involved: it just means that the servers, the operating systems, the network layer and the rest of the infrastructure have already been taken care of, so that you can focus on writing application code.

Each Lambda function runs in its own container. When a function is created, Lambda packages it into a new container and then executes that container on a multi-tenant cluster of machines managed by AWS. Before the functions start running, each function’s container is allocated its necessary RAM and CPU capacity.

The entire infrastructure layer of AWS Lambda is managed by AWS. Customers don’t get much visibility into how the system operates, but they also don’t need to worry about updating the underlying machines, avoiding network contention, and so on—AWS takes care of this itself.

And since the service is fully managed, using AWS Lambda can save you time on operational tasks. When there is no infrastructure to maintain, you can spend more time working on the application code—even though this also means you give up the flexibility of operating your own infrastructure.

The following key features help you develop Lambda applications that are scalable, secure, and easily extensible:

### Environment variables

Use environment variables to adjust your function's behavior without updating code.

### Versions

Manage the deployment of your functions with versions, so that, for example, a new function can be used for beta testing without affecting users of the stable production version.

### Container images

Create a container image for a Lambda function by using an AWS provided base image or an alternative base image so that you can reuse your existing container tooling or deploy larger workloads that rely on sizable dependencies, such as machine learning.

### Layers

Package libraries and other dependencies to reduce the size of deployment archives and makes it faster to deploy your code.

### Lambda extensions

Augment your Lambda functions with tools for monitoring, observability, security, and governance.

### Function URLs

Add a dedicated HTTP(S) endpoint to your Lambda function.

### Private networking

Create a private network for resources such as databases, cache instances, or internal services.

### File system access

Configure a function to mount an Amazon Elastic File System (Amazon EFS) to a local directory, so that your function code can access and modify shared resources safely and at high concurrency.

### What's in a lambda function?

AWS Lambda functions into independent containers when you use the Serverless Application Model (SAM) for your code.

The Lambda function is usually a container because it comprises configuration information that relates to that function. That information includes the function name, description, resource requirements, and entry point.

<img width="578" alt="image" src="https://github.com/user-attachments/assets/50730695-d888-4f2c-a567-8c93c7421b7d">

## Use cases

Lambda is an ideal compute service for application scenarios that need to scale up rapidly, and scale down to zero when not in demand. For example, you can use Lambda for:

When using Lambda, you are responsible only for your code. Lambda manages the compute fleet that offers a balance of memory, CPU, network, and other resources to run your code. Because Lambda manages these resources, you cannot log in to compute instances or customize the operating system on provided runtimes. Lambda performs operational and administrative activities on your behalf, including managing capacity, monitoring, and logging your Lambda functions.

## Event driven applications

Build event-driven functions for easy communication between decoupled services. Reduce costs by running applications during times of peak demand without crashing or over-provisioning resources.

With its event-driven model and flexibility, AWS Lambda is a great fit for automating various business tasks that don’t require an entire server at all times. This might include running scheduled jobs that perform cleanup in your infrastructure, processing data from forms submitted on your website, or moving data around between different datastores on demand.

## Web applications

By combining AWS Lambda with other AWS services, developers can build powerful web applications that automatically scale up and down and run in a highly available configuration across multiple data centers – with zero administrative effort required for scalability, back-ups, or multi-data center redundancy.

## Machine learning

You can use AWS Lambda to preprocess data before feeding it to your machine learning model. With Lambda access to EFS, you can also serve your model for prediction at scale without having to provision or manage any infrastructure.

## Data processing

Execute code in response to triggers such as changes in data, shifts in system state, or actions by users. Lambda can be triggered by AWS services such as S3, DynamoDB, Kinesis, or SNS, and can connect to existing EFS file systems or into workflows with AWS Step Functions. This allows you to build a variety of real-time serverless data processing systems.

## Advantages

Pay per use. In AWS Lambda, you pay only for the compute your functions use, plus any network traffic generated. For workloads that scale significantly according to time of day, this type of billing is generally more cost-effective.
‍
Fully managed infrastructure. Now that your functions run on the managed AWS infrastructure, you don’t need to think about the underlying servers—AWS takes care of this for you. This can result in significant savings on operational tasks such as upgrading the operating system or managing the network layer.
‍
Automatic scaling. AWS Lambda creates the instances of your function as they are requested. There is no pre-scaled pool, no scale levels to worry about, no settings to tune—and at the same time your functions are available whenever the load increases or decreases. You only pay for each function’s run time.
‍
Tight integration with other AWS products. AWS Lambda integrates with services like DynamoDB, S3 and API Gateway, allowing you to build functionally complete applications within your Lambda functions.

### Serverless

Run code without provisioning or managing infrastructure. Simply write and upload code as a .zip file or container image.

### Auto-scaling

Automatically respond to code execution requests at any scale, from a dozen events per day to hundreds of thousands per second.

### Pay-as-you-go pricing

Save costs by paying only for the compute time you use—by the millisecond—instead of provisioning infrastructure upfront for peak capacity.

With AWS Lambda, one doesn’t pay anything when the code isn’t running. The user has to only be charged for every 100ms of code execution and the number of times his code is actually triggered.

### Performance optimization

Optimize code execution time and performance with the right function memory size. Respond to high demand in double-digit milliseconds with Provisioned Concurrency.

## Disadvantages

While AWS Lambda has many advantages, there are a few things you should know before using it in production.

### Cold start time

While aws lambda is going to be activated after a long gap it will take some time to initialize the service which is required to deploy the application at that time end users will face latency issues.

When a function is started in response to an event, there may be a small amount of latency between the event and when the function runs. If your function hasn’t been used in the last 15 minutes, the latency can be as high as 5-10 seconds, making it hard to rely on Lambda for latency-critical applications.

### Function limits

The Lambda functions have a few limits applied to them:
‍
Execution time/run time. A Lambda function will time out after running for 15 minutes. There is no way to change this limit. If running your function typically takes more than 15 minutes, AWS Lambda might not be a good solution for your task.
‍
Memory available to the function. The options for the amount of RAM available to the Lambda functions range from 128MB to 3,008MB with a 64MB step.
‍
Code package size. The zipped Lambda code package should not exceed 50MB in size, and the unzipped version shouldn’t be larger than 250MB.
‍
Concurrency. By default, the concurrent execution for all AWS Lambda functions within a single AWS account are limited to 1,000. (You can request a limit increase for this number by contacting AWS support.)

Any Lambda executions triggered above your concurrency limit will be throttled and will be forced to wait until other functions finish running.
‍
Payload size. When using Amazon API Gateway to trigger Lambda functions in response to HTTP requests (i.e. when building a web application), the maximum payload size that API Gateway can handle is 10MB.

### Limited number of supported runtimes

While AWS Lambda allows adding custom runtimes, creating them can be a lot of work. So if the version of the programming language you are using isn’t supported on Lambda, you might be better off using AWS EC2 or a different cloud provider.

### Vendor lock-in

If you want to execute the lambda function then you need the support of any cloud provider as here we are using AWS because it is widely used in the market.

### Stateless

Lambdas are stateless executions of code. However, Lambda will let you access stateful data when you call other internet-available services such as Amazon DynamoDB and Amazon S3.

## Lambda vs EC2

Lambda is a fully managed serverless computing service where you only need to upload and run your code to start.

EC2 contrasts that by using cloud-based virtual machines (VMs) architecture. So EC2 will let you control or customize instances, provision capacity, operating system, and network tools, and tweak the underlying infrastructure to improve security.

But that is if you have experience handling those responsibilities.

With EC2, you can migrate existing applications to the cloud more rapidly because you do not have to change their architecture too much. Instead, you can change the EC2 infrastructure to support the app.

But suppose you do not have the experience, budget, and time to swim in a pool of technical responsibilities. In that case, Lambda provides a managed, readily available, highly scalable, and secure serverless computing platform.

You won’t have access to its infrastructure because AWS handles everything on your behalf.

Lambda also only runs in response to a trigger known as an event. Unlike other Platform-as-a-Service (PaaS) offerings, it does not run 24/7. That makes it more cost-effective because AWS charges you for only the resources you use.

However, Lambdas have a cold start time, whereas EC2 can be constantly running to handle requests.

## Using lambda

As of now, AWS Lambda doesn’t support all programming languages, but it does support a number of the most popular languages and runtimes.

For each of the supported languages, AWS provides an SDK that makes it easier for you to write your Lambda functions and integrate them with other AWS services.

While you don’t need to, be sure to write the code in a stateless style. That means writing code that assumes no affinity to the underlying AWS Lambda infrastructure.

You can create, call, and manage Lambda functions using these five interfaces:

AWS Management Console
AWS CloudFormation
AWS Serverless Application Models (SAM)
AWS SDKs
AWS Command Line Interface

### Programming languages

Lambda supports the following languages natively:

- Node.js (14, 12) with Amazon Linux 2 OS.
- Python (3.6, 3.7) with Amazon Linux and (3.8) with Amazon Linux 2 OS.
- Go Runtimes (1.x) with Amazon Linux 2 OS.
- C# runtimes (.NET Core 3.1) with Amazon Linux 2.
- Ruby 2.7 with Amazon Linux 2 OS.
- Java 8 with Amazon Linux OS.
- Java 8 (Java8.la2) and Java 11 with Amazon Linux 2 OS.

Custom Runtime (provided al2 and provided) with Amazon Linux 2 and Amazon Linux, respectively. So you can give any Docker Container Image as a custom runtime.
Also, AWS provides a Runtime API you can use to write your code in additional languages.
‍
## Best practices

### Optimizing function performance

By minimizing the cold starts by keeping the functions warm and reduce the execution time by optimizing your code and dependencies.

### Efficient resource management

Through allocating the appropriate amount of memory to your function based on performance needs and cost considerations.

### Retry mechanisms

By using try-catch blocks, AWS SDK retries and dead letter queues (DLQs), we handle the errors gracefully.
