# API introduction

## What is an Application Programming Interface?

An application programming interface (API) is an intermediary through which two software components communicate to share data and to get useful work done. As the name implies, exchanging information is possible because of the presence of a software interface between these components. The software components can reside on the same or different machines connected through a network.

Using an API, an application can request services from another application without understanding the architecture of other applications. The only thing the requesting application should know is how to place the request, in other words, it should understand the interface for placing the request.

## What is an API gateway?

Modern software applications prefer microservices over monolithic architecture. This is because their rich features require multiple services to process tasks with added flexibility. The microservice architecture is easy to manage and develop and provides modularity to the application compared to the monolithic.

### Monolithic architecture

A monolithic architecture is one in which all the components of an application, such as, frontend, backend, databases, and any other component, are embedded in a single codebase. The application is developed, updated, and deployed as a monolith.

<img width="556" alt="image" src="https://github.com/user-attachments/assets/13d9cff2-9814-4021-b7d2-7e57b7154736">

### Microservice architecture

A microservice is an architecture in which an application is divided into smaller services. These services handle smaller functionalities and data of the application by communicating with each other using defined protocols. They can be physically separated but connected through protocols.

<img width="554" alt="image" src="https://github.com/user-attachments/assets/807f8553-e1aa-4495-ba47-5fe8faeff1b8">

In a scenario where a client application must interact with multiple microservices at a time, a typical approach would be to make a separate API call for each microservice. This impacts resource consumption, performance, and task time. The API gateway comes in to help by acting as a single entry point for all the API requests. It sits between the microservices and clients, acting as a gateway.

<img width="508" alt="image" src="https://github.com/user-attachments/assets/3c028616-4632-4367-b15c-d0773ae0b65d">

The API gateway takes the client’s calls and routes them to the appropriate microservice by processing the parameters in composite API calls. It retrieves the responses from all microservices and sends a unified response to the client’s requests. Most applications depend on APIs; therefore, cyber attacks target them because they can expose valuable users and system data. It is of utmost importance to protect APIs from unauthorized access. An API gateway plays the following essential roles:

- It provides security, authentication, and rate limiting to protect APIs from overuse.
- It provides an analysis mechanism to monitor the behavior of the users with the help of monitoring tools.
- It’s helpful in microservice architecture to disseminate a single API call to multiple services and compile an answer in return.
- It may provide stabilization to the system by balancing the network traffic.

Which type of applications are more suited for microservice architecture?

Applications with the following attributes should use microservice architecture:

- Clients need to interact with different independent subservices.
- Continuous development and deployment is needed.
- The application is large and aims to scale in the near future.
- Different teams are working independently.

## API endpoints

It’s imperative to locate the services of microservice architecture in order to acquire their functionality. Therefore, it’s required to define a mechanism for APIs to access the exact location where the service is being provided. We refer to those digital locations as the endpoints of APIs. In a communication channel, the endpoint is one end of a system we can reach with the help of a URL. A user of the service sends a request to the specified endpoint (the URL) to perform operations using the resources available from that endpoint. Usually, the API provider defines a set of endpoints to make the resources available to the users through an HTTP request. The endpoints are also helpful as their names indicate the type of operations they perform.

<img width="437" alt="image" src="https://github.com/user-attachments/assets/9c1dd63a-7c9d-4dc7-8146-ca6539089d62">

Internally when communicating via networking, the API endpoint is a combination of the IP address and the port.

## Characteristics of a good API

There are many desirable characteristics of an API. We’ve provided a nonexhaustive list of some of them to keep in mind when we study an API or design a new one. However, the evolution of technology often impacts how APIs are specified, and new characteristics can be added in the future.

<img width="560" alt="image" src="https://github.com/user-attachments/assets/15c5073d-2403-499f-ad73-61241fcf2611">

## Business considerations with APIs (Optional)

### Role of APIs in business

When an API is in the planning process, the business use cases must be considered a priority. Organizations that skip this will find themselves in trouble later because there are no business goals to meet. These goals can be driven by multiple factors, such as revenue, new market routes, and new products, but all of these must be outlined at the beginning so that all the decisions and choices lead toward the defined goals.

- Companies focusing on successful API initiatives focus on one or more of the following factors:

- Monetizing existing assets: An API is a great multiplier for the return on investment (ROI) on the company’s assets. Let’s say that we own a house and want to rent out a room to someone to help with the bills, such as electricity and mortgage costs. Companies with existing assets can do something similar. They can expose these tech assets to the world and get an ROI through APIs. An example would be IBM selling access to Watson for data analytics.

- Connecting business domains: This usually refers to interactions across multiple lines of business. These often work independently, but can also benefit from sharing data to smooth out some processes. An example of this is Google Suite, which contains different products that cater to different domains, such as Gmail and Google Drive. APIs allow the data to be shared in a controlled and safe manner. In some cases, domains may be physical locations. Big organizations have multiple locations, including cloud and on-site data centers. These companies occasionally use APIs to secure and control the data flow between these locations.

- Self-service: The ability to extend our outreach worldwide can be made possible via a self-service portal API. Potential clients can learn about these features and services at any time, and they can integrate any of the features they need. These individual customers can then be contacted later to be able to retain them. An easy-to-integrate API is necessary for developers looking for an API, because it’s likely they’ll test the service for integrations immediately. Developers might move on to other options if they cannot integrate features quickly.

- Innovation: APIs can fuel a product's innovation by providing a simple point of access to talented developers. These developers can then build something unique and give value to the business and to end users. After making the Google Maps navigation service, Google offered their API for integration to the world. Now ride-sharing apps, for example, Uber and Lyft, rely on that API for their core business. This provides value to Google while also allowing for innovative services like Uber to exist.

- Automation: Because of APIs, big enterprise IT teams can automate data transfers between various applications. This helps to reduce the need for manual processes and custom scripts. As a result, it allows for higher business efficiency, reliability, and faster roll-outs of new solutions. This automation can help the business save funds and resources in the long run.

### API business models

Before we discuss the API business and monetization models, it’s important to discuss the API value chain and the roles within it:

- API providers make business assets available to consumers as an API, with certain terms and conditions.

- API consumers are developers using the API under the agreed-upon terms and conditions. They use the API to provide a service to the end users.

- End users/customers do not see the API but benefit from it by using the applications in which it is provided.

Several companies have built their business around the APIs that they provide to consumers and customers. Quite a few widely used APIs are open-sourced, but most of them are premium paid products/services that provide excellent value for their cost. Let’s take a look at some monetization options that we can pursue for our APIs:

- Free: As the name implies, there are no direct purchases made. The API must follow a business purpose even without any monetary benefit. An example of such an API would be the social login options offered by Google, Facebook, and so on. Several companies use these APIs to identify end users—this also has a benefit for the provider. Users might sign up for their platform for the convenience of using this option elsewhere. Some providers limit the calls to their API for free users to encourage developers to subscribe to their services for full access to the API.

- Developer Pays: This model charges developers for using the API. Let's look at the different ways this can be done:

  - Subscription: In this model, the provider charges directly through a subscription (monthly or yearly) for the API. Developers must be convinced of the API's value to use this model effectively. To that end, creating a sandbox where they can test out the capabilities of the API is a good option. Another way to convince developers is to use a model where the primary features will be free, with some higher-value features that will only be accessible through a subscription. This option is convenient for billing by the API provider, but the consumers might end up paying for features they never use.

  - Pay-as-you-go: This is also known as the usage-based model. The price the developer has to pay is based on how much of the API they use or how many calls they make to the API. This option is often cheaper for the consumers, but it can be challenging for the provider to bill them properly. An example of this model is the Amazon Web Services (AWS) API. AWS prompts consumers to add their credit cards, charges them monthly based on usage, and provides them with a detailed monthly report.

  - Transaction fees: This model is commonly used by payment gateways like Visa and Mastercard. They charge their consumers a fixed rate for each transaction they make. The rate is usually a percentage of the transaction being completed.

- Developer gets paid: This is an effective model when the service provider incentivizes developers to promote their product while it’s in use. This can be done in the following ways:

  - Adverts: The developers get paid to include advertisements from the API provider in their applications. In this scenario, they get paid regardless of whether an end user actually engages with the advertisements.

  - Affiliate: In this scenario, a developer gets paid whenever an end user clicks or engages with the provider's content. An example of this would be Google Adsense.

### Performance measures

So far, we’ve discussed the value APIs can provide businesses and what monetization options a business can pursue to profit from APIs. However, there’s another aspect of business that we have yet to explore—the performance of the API. The business stakeholders, users, and developers might have different views about the performance and quality of the API, which might lead to conflicts between the stakeholders. For that reason, all the stakeholders must be on the same page.

For this purpose, we rely on service level indicators (SLIs), service level objectives (SLOs), and service level agreements (SLAs). They are tools that provide developers, business managers, and other stakeholders with metrics to drive business decisions about their products.

#### SLIs

A service level indicator (SLI) is a carefully defined quantitative measure of an aspect of the level of service that has been provided. There are several SLIs that we can use for this. Some of them have been described in the table below:

<img width="541" alt="image" src="https://github.com/user-attachments/assets/3f529d97-490e-4884-a516-b6912ac5af86">

#### SLOs

A service level objective (SLO) is a target range of value for a service we measure through an SLI

An example of this structure for the request latency indicator is as follows:

<img width="443" alt="image" src="https://github.com/user-attachments/assets/c3cfc535-ae81-4b88-8906-6850e1c69647">


#### SLA

A service level agreement (SLA) is a contract that outlines the service’s terms and conditions. It also provides the service’s availability and performance, as well as other features that the customer can anticipate from the service. The SLA also defines the metrics and methods for measuring the service, such as uptime, response time, throughput, and errors. It also establishes the remedies or consequences if the service fails to meet the agreed-upon objectives. Defining SLAs should have the customer experience as the primary focus to ensure their satisfaction with the service or product.
