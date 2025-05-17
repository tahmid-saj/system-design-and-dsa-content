# Web crawler

A web crawler is a program that automatically traverses the web by downloading web pages and following links from one page to another. It is used to index the web for search engines, collect data for research, or monitor websites for changes.

## Requirements

### Questions

- What will the web crawler be used for?
  - Web crawlers can be used for many different use cases. For example, it can build documents for search engine indexing, most likely via some inverted index mapping and a ranking algorithm like PageRank. Also, the built documents could be used to train LLMs. Regardless of the use case, the output should still contain documents (raw text) from crawling web pages.

- What types of content will be crawled and retrieved?
  - HTML only
  - This is important because the answer can change the design. If we are writing a general-purpose crawler to download different media types, we might want to break down the crawling operation into different data formats: one for HTML, another for images, or another for videos, where there is different logic for crawling each data format

- Do we need to store the HTML pages crawled from the web pages?
  - Yes, for up to 5 years

- Should the crawler handle media content, as well as dynamic content like JS rendered pages?
  - No for simplicity, leave these out

- Is the crawling done on a recurring basis or a one-time crawl that can be manually trigerred via an admin / client?
  - Let's assume it's a one-time crawl, but if time permits, talk about the implementation for a scheduled crawling operation

- How many web pages will the web crawler collect?
  - 1B web pages crawled within a few days

### Functional

- The system crawls HTML content, and surveys the internet from a queue of seed URLs
- Storage for content extracted from URLs will be in a blob store
- The crawler could potentially be scheduled to repeat the web crawling process

- There are roughly 5.2B web pages and 1.1B websites in the internet. 1B web pages should be crawled per month, which is around 20% of the internet.
- A single web page is around 2 MB, thus 1B * 2 MB = 2 PB of data should be crawled and stored

### Non-functional

- Parallel processing / throughput:
	- Web pages should be crawled via multiprocessing / multithreading, and also support crawling with high throughput
- Politeness:
	- The crawler should adhere to robots.txt and not make too many requests to a URL within a short time
- Smart crawling:
	- The system should be smart to only obtain important data or also self-throttle (exit the process) if the the crawling time takes too long or the URL is malicious
- Extensibility (Optional):
	- The system should allow crawling for multiple	different formats of data via different communication protocols

**Note that it's not feasible to crawl every web page in the internet. There are numerous smaller sites which may not be accessed by the crawler.**

## Data model / entities

- URL metadata:
  - The URL metadata entity / table will contain all the URLs to be crawled and it's associated metadata
  - Because we want fast lookups based on the checksum value during deduplication, we can set a global secondary index (GSI) on the checksum field in DynamoDB, which let's us set a partition key that's different from the primary key - also we can set a sort key. This is useful if we want to query the data in a different way than by using the primary key (urlID) by using the checksum field.
  - The retryFetchCount will be increased upon each re-try, and will prevent unlimited re-tries on fetching from URLs' web servers by moving the re-tried URL to a DLQ when the retryFetchCount reaches a retry limit.
  
    - urlID
    - url
    - s3URLs: { HTMLLink, textDataLink }
    - lastCrawledTime
    - retryFetchCount
    - checksum: { urlChecksum, documentChecksum }

- Domains (It will be used since we're adhering to robots.txt):
  - The Domains table will contain metadata and the crawlDelay field for domains obtained from the robots.txt. A domain is different from a URL in that there could be multiple URLs belonging to the same domain.
    
    - domainID
    - domainName
    - crawlDelay
    - depth

- Document:
  - This entity will be directly stored in a blob store, most likely in a HTML / JSON format such that it can be used for search engine indexing, training LLMs, etc
    
    - documentID
    - crawledURL
    - rawHTML
    - embeddedURLs, extractedText
    - robots.txt

## API / interface design

**For backend specific SDIs (and non-user-facing SDIs which involves web apps / mobile apps, etc) such as a web crawler, it's important to define the system's inputa and outputs within the API design. This may not be a traditional CRUD focused API (it's really just an interface), however some form of an API model will still be followed within the overall system**

- Inputs:
  - Seed URLs
- Outputs:
  - HTML and text data extracted from web pages
 
### Requesting a URL's HTML from a web server

- Assuming the server renders the HTML via SSR, we can retrieve the web page's HTML using Peppeteer in JS, which is a "headless browser" that provides high level APIs to perform operations which are implemented in browsers, such as receiving and rendering returned server-side HTML content.

- Below is an example of how we can fetch the HTML from a URL using Puppeteer:

```js
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto('https://example.com', { waitUntil: 'networkidle2' });

  const htmlContent = await page.content();
  console.log(htmlContent);  // Full rendered HTML

  await browser.close();
})();
```

## Workflow / data flow

**Because the workflow / data flow is important for backend specific SDIs (and non-user-facing SDIs which involves web apps / mobile apps, etc) such as a web crawler, it's crucial to also go over the workflow / data flow**

**The workflow should explain the steps on how the API's inputs (seed URLs) are processed into outputs (text data extracted from web pages)**

1. Take seed URLs from URL frontier, and request for URL's IP address from the DNS provider. The client will also provide the seed URLs to the URL frontier. If the seed URLs are not directly provided - we can simply retrieve URLs for very popular sites, social media platforms or web directories.
2. Fetch HTML from the hosting web server using the URL's IP address
3. Extract embedded URLs and text data from the HTML
4. Store the text data in a blob store, and queue the embedded URLs to the URL frontier to crawl
5. Some form of deduplication, politeness handling, crawler trap avoidance, etc will be handled during the crawling operation (discussed more in HLD / DD)
6. Repeat steps 1 - 5 until all URLs have been crawled

## HLD

### URL frontier queue

- The URL frontier will contain the queued URLs we need to crawl. It will initially contain a list of seed URLs sent by the client, and we'll queue new URLs as we crawl the web pages.
- Note that the URL frontier should not store the actual HTML or text data, since queues are not optimized to contain large datasets. Instead, the fetched HTML and extracted text data should be stored in a blob store, and relevant metadata about the s3URLs should be stored in a separate metadata DB. The URL frontier should just contain the urlID, the URL itself, and possibly the s3URLs.

#### SQS vs Kafka for the URL frontier

- We can use the below technologies to implement the URL frontier queue (and also the Extraction queues in the crawler service):
  - Kafka:
    - Kafka retains messages in a log, and does not remove them even after they are read. The crawling operation (in the crawler service) will track it's progress via offsets within the log, which are not updated in Kafka until the URL is successfully fetched and processed. If the crawling operation fails, another worker in the crawler service can pick up right where the failed worker left off, ensuring no data is lost.
    - Kafka also does not support built-in re-tries unlike SQS, thus SQS may be more appropriate for this design
  - SQS:
    - With SQS, messages will remain in the queue until they are explicitly deleted. A visibility timeout hides a message from other consumers (workers) once the message is fetched. If the worker fails before confirming successful processing, the mesage will automatically become visible again after the visibility timeout expires, allowing another worker to attempt the fetch. On the other hand, once the HTML is stored in the blob store by a worker, the worker will delete the message from the queue, ensuring it is not processed again.
    - Given SQS's built-in support for re-tries, ensuring no two workers read the same dequeued message via visibility timeouts, exponential backoff using visibility timeouts, etc, we'll use SQS as the queues for the system.

**The worker above refers to the URL fetcher workers, but the same logic applies to the Extraction workers, where the URL will remain in the Extraction queue until the text data has been extracted and is stored in the blob store**

#### URL frontier as a priority queue

- If we want to implement a priority queue (based on web page traffic, website SEO rank, update frequency, etc) instead of a standard SQS queue, we can use a SQS FIFO queue, where messages will be placed in a specific group in the FIFO queue depending on the message's assigned ID. However, this may be a bit complex, and will have a high overhead to maintain.
- We could also use Redis sorted sets to implement a priority queue for the URL frontier as it may be much easier, since Redis directly provides a sorted set data structure which is very similar to a priority queue. Using a sorted set, nodes will be assigned a score (priority), and a location within the sorted set based on the score.

### Metadata database

- To maintain the metadata for URLs and domains that we're crawling or will crawl, we'll use a metadata database. This database will store the URL and domain metadata, such as the s3URLs to the raw HTML and text data, as well as the lastCrawledTime field.
- Both a NoSQL DB such as DynamoDB or a SQL DB should work fine here, however since the DB may be frequently updated, and won't contain that many relationships, thus we'll use DynamoDB as it's more suitable here.

### Blob store

- Because the web page's text data and HTML could still be very unstructured, we will store it in a blob store. A blob store like S3 works best here because it is highly durable and is optimal when storing large amounts of unstructured data cheaply.
- Also content from a single web page may be very different in both structure and size than content from other web pages, thus a NoSQL / SQL DB which still maintains some structure would not be the best choice here.

### Crawler service

**Note that we'll split the crawling operations in the Crawler service over many different pipelines stages to ensure fault tolerance when a single stage is down. If the whole crawling operation is handled by one single stage, then when this stage fails, all the progress of the crawling will be lost. Thus, we'll have multiple stages for the crawling. For example, fetching web pages from external web servers is the most likely task to fail, since the external web servers are a wildcard, and they could be down for whatever reason, or too slow to respond, etc.**

**For data processing operations like web crawling, it's best to break the entire operation into pipelined stages. Separating them into stages helps to isolate failure to a single stage, and to also save the output from a failed stage in a storage. This way, the failed stage can be retried without losing progress on the whole operation. We can also scale each stage independently.**

- The crawler service will perform the overall crawling operation in two stages:
  - URL fetcher stage:
    - It will request the DNS for the URL's IP addresses
    - It will fetch the HTML from the wep pages
  - URL and text extraction stage:
    - Extract the text data from the HTML to store in the blob store, and extract new URLs to add to the URL frontier

#### Crawler service pipelined stages

The Crawler service will have the following stages:

1. URL fetcher:
- This stage will fetch the HTML of the web page from the external web servers. It will first receive a URL from the URL frontier, then request the DNS for the URL's IP address so that it can fetch the HTML for the web page. The raw HTML from the fetched web page will also be stored in the blob store, so that if any failed operation needs to resume using this raw HTML, it could do so without restarting the whole crawling operation.

##### Re-trying fetching a URL's IP and HTML

- We can use the below approaches to re-try this stage upon failure to fetch the IP address or the HTML from the web servers ('Re-trying URL fetching upon failures'):
  - In-memory timer
  - Kafka with manual exponential backoff
  - SQS with exponential backoff:
    - If there is a failure when fetching the IP address from the DNS OR fetching the HTML from the web servers, this stage can retry the operation by enqueing the failed URL to the URL frontier, which will be a SQS standard queue. SQS allows us to configure a visibility timeout (default is 30 seconds), and increase the visibility timeout over time to fetch the IP address / HTML. This means that we can increase the interval between each re-tries by increasing the visibility timeout on each re-try failure.
    - To prevent unlimited re-tries, upon each re-try (re-dequeing the same URL from the URL frontier and trying the fetch again), we'll also increase the retryFetchCount field, and after the retryFetchCount reaches a specific limit, it will instead be enqueued to a SQS dead letter queue in the URL frontier. The URLs in the DLQ will be marked as unprocessible, and the site well be assumed to be offline.
2. Text and URL extraction:
- This stage extracts the text data and embedded URLs from the HTML provided by the URL fetcher stage. It will enqueue the embedded URLs to the URL frontier, and store the extracted text data in the blob store.
- Text extraction and URL extraction may seem like two separate stages, however both of these operations are simple and can be done in parallel in one stage instead of sequentially in two separate stages.
- URL filtering could also be implemented in this stage, such that we only extract relevant URLs based on domain, terms in extracted text data, etc

**Having pipelined stages also helps with extensibility. For example, if we wanted to also process images or media within web pages, a separate media extraction stage could be run in parallel with the text and URL extraction stage.**

#### Crawler service architecture

- To further ensure the crawler doesn't have a SPOF, we'll allocate the pipelines stages across different components of the crawler service: URL fetcher workers, extraction queue (SQS), and extraction workers.
- The below URL fetcher and Extraction workers can also perform their respective stages in parallel using multi-processing on individual URLs, since when workers will read a message from a SQS queue, other workers won't be able to read the same message during the visibility timeout. However, if URLs for the same domainID are fetched, it could have some potential concurrency issues when updating the Domains table. However, this can be resolved using rate limiting and a distributed lock provided by Redis (this will be discussed more in the DD).

##### URL fetcher workers

- The URL fetcher workers will perform the URL fetcher stage, where the IP address will first be fetched via the DNS, and then the HTML will be fetched from the web servers, and then saved to the blob store. Because web crawling is an IO bound task, where a lot of network requests will be made, both the URL fetcher workers and Extraction workers could use network optimized EC2 instances, which provides higher bandwidths (20k - 40k Mbps).
- Because we're using SQS as the URL frontier queue, the URL will stay in the queue until the HTML has been fetched and stored in the blob store by the URL fetcher stage. This way, if the URL fetcher stage fails within a URL fetcher worker, another URL fetcher worker can pickup the same URL from the URL frontier and re-try the URL fetcher stage.
- Once the HTML has been fetched, the URL fetcher worker will perform the below within a transaction using the AWS SDK:
  - Store the raw HTML in the blob store, and update the URL metadata table for the urlID entry (update the s3URLs)
  - The worker will delete the URL in the URL frontier, and enqueue the URL into the Extraction queue

##### Extraction queue (SQS)

- The Extraction queue will contain the queued URLs to extract. Only the necessary URL metadata such as urlID, url, etc should be in a message's payload.

##### Extraction workers

- The Extraction workers will perform the Text and URL extraction stage, where both the embedded URLs and text are extracted from the HTML
- An extraction worker will dequeue a URL from the Extraction queue, then fetch the HTML and the URL metadata from the blob store and URL metadata table respectively. Afterwards, it will perform the below in a transaction using the AWS SDK:
  - Save the extracted text to the blob store, and enqueue the embedded URLs to the URL frontier
  - Update the urlID entry in the URL metadata database (update the s3URLs and lastCrawledTime fields)
  - Delete the URL in the Extraction queue

Deduplication in Extraction workers:

- The URL and document deduplication can be performed by the extraction workers as they're extracting the embedded URLs and text data. These workers will calculate a hashed checksum value of the URL and text data. If the checksum value was already seen in the URL metadata table, then the crawling operation will be stopped, and the URL will be deleted from the queue to prevent duplicates. Otherwise, the crawling will continue, and the workers will update the checksum and other fields for the urlID in the URL metadata table.
- The deduplication will be discussed more in the DD.

Checksum:

- A checksum is a value that represents the number of bits in a message, and is used to detect duplicates or similarities within messages or text. A checksum value can be generated by running a cryptographic hash function, and every piece of data can be used to generate a checksum. The checksum can either be a 64-bit or 128-bit value.

### DNS provider

- The DNS provider will resolve domain names to IP addresses so that the crawler can fetch the web pages. The DNS provider may also cache frequently accessed domain names internally.
- The DNS will not directly be maintained within the system - it is external to the system, but will still play a part in the crawling operations.
- By default, a router uses DNS servers set up by the ISP. All devices on a network will use the router's DNS server. However, this could be configured differently and scaled for web crawling as discussed in the DD.

### Web servers

- The web servers hosts the web pages that we're crawling. The crawlers will fetch the HTML from these servers and extract the text data.

<img width="1050" alt="image" src="https://github.com/user-attachments/assets/c5e27170-838f-4e50-a000-d14644658575" />

## DD

### Politeness

- Politeness refers to respecting the web servers' bandwidth (not overloading the web servers with requests), and adhereing to any specific rules set by the robots.txt file. robots.txt is a file that websites use to communicate with web crawlers. It tells crawlers which pages they are allowed to crawl, and which pages they are not. It also tells crawlers how frequently they can crawl the site. An example of a robots.txt file is shown below:

```http
User-agent: *
Disallow: /private/
Disallow: /creatorhub/\*
Disallow: /rss/people/\*/reviews
Crawl-delay: 10
```

- User-agent:
  - The User-agent line specifies which crawlers the rules apply to. In this case, * means all crawlers.
- Disallow:
  - The Disallow line specifies which pages the crawler is not allowed to crawl. In this case, the crawler is not allowed to crawl the private, creatorhub, and rss/people/*/reviews pages.
- Crawl-delay:
  - The Crawl-delay line specifies how many seconds the crawler should wait between requests. In this case, 10 seconds.

**Note: the protocol for crawlers communicating with web sites via the robots.txt is called the Robots Exclusion Protocol.**
 
#### Adhering to robots.txt

- To adhere to robots.txt, we'll need to do the following:

##### Parse robots.txt

- We'll first save the robots.txt file in the blob store when we start the URL and text extraction stage.
- Before crawling a page, we'll need to parse the robots.txt file to see if we're allowed to crawl the website or a specific page via the User-agent and Disallow fields respectively. If we're not allowed to crawl the page, we should skip it and remove it from the Extraction queue, and move on to the next queued URL.

##### Adhere to the Crawl-delay

- We'll also need to adhere to the Crawl-delay, and possibly introduce a new Domains table which contains the metadata and crawlDelay field for a specific domain. A domain is different from a URL in that there could be multiple URLs belonging to the same domain. This way, we'll wait until the current time is past lastCrawledTime + crawlDelay (crawlDelay from the Domain table), before we'll request the website again. The crawlDelay field can also be used to set the visibility timeout of the URL appropriately, when we place the URL back into the URL frontier / Extraction queue.
- If an Extraction worker does pull a URL from the Extraction queue before the crawlDelay time has passed, the worker can still just put the URL back into the Extraction queue and set the visibility timeout appropriately using the crawlDelay (or time left until the crawlDelay passes), so that the worker can dequeue the same URL after the crawlDelay.

- The steps for the URL and text extraction stage is now as follows:
  - Fetch the robots.txt file for the domain of the dequeued URL either by requesting for the URL's robots.txt file (by requesting www.example.com/robots.txt for example) OR fetching the robots.txt file from the blob store.
  - Parse the robots.txt and store it in the blob store, and also add / update the domainID entry for the URL's domain in the Domains table - we'll update the crawlDelay field. This way, whenever URLs are dequeued, the robots.txt can be fetched from the blob store, and the crawlDelay field can also be checked from the Domains table.
  - If the crawlDelay time has passed, extract the embedded URLs and text from the web page, and update the lastCrawledTime field for the URL in the URL metadata table.
  - If the crawlDelay time has not passed, put the URL back into the Extraction queue, and also set a visibility timeout according to the crawlDelay

##### Rate limiting using Redis persistent data store + distributed lock

- We'll also limit the number of requests we make to a domain. For example, we can limit 1 request per second to the same domain. Rate limiting to 1 request per second to the same domain can be tricky if we have multiple Extraction workers.
- We'll need to implement a global rate limiting mechanism at the Domain level using a centralized data store like Redis, which can be used to track the request counts per domain per second. An extraction worker will first check this Redis data store to ensure the rate limit has not exceeded for the domain. If the rate limit has exceeded, the URL could be put back into the Extraction queue with a visibility timeout according to the time remaining until the rate limit is reset
- The rate limiting algorithm can be the fixed window counter algorithm, which will split the timeline into fixed sized windows, where the window size will be equal to 1 second since we can make 1 request per second. The algorithm will keep track of the number of requests made for the current window (for a specific domain) using Redis's distributed data store. Redis can also store the request limit and window size for the specific domain. If the number of requests exceed the limit (ie, 1 request per second) for a specific domain, then the request will be throttled. An entry in the Redis data store may be as follows:

```bash
domainID: { requestsMade: 1, requestsLimit: 1, requestWindowSize: 1 second }
```

- Redis is preferred since it is single-threaded and can be used with a Redis distributed lock to increment the requestsMade value when requests are made. However, if multiple URL fetcher workers are trying to make requests to the same domain at the same time, only one or a few will succeed depending on the requestsLimit. While this might seem good since only the appropriate number of requests are being made using the requestsLimit, there could be several URL fetcher workers wasting network requests by requesting the same domain at the same time, but end up being rate limited because other URL fetcher workers already requested the domain.
- We can prevent the above behavior by adding "jitter", or a random delay value to the visibility timeout (that's still greater than the crawlDelay) to the queued URL. This way, the URL fetcher workers do not all request the same domain at the same time, and end up wasting network requests. The workers will request the same domain at randomized different times.
- The above behavior could also be resolved by using a "smart scheduler", which enqueues URLs into the URL frontier such that multiple URL fetcher workers won't request URLs belonging to the same domain. However, the implementation of this "smart scheduler" may be complex and abstract.

### Deduplication in crawling operation

- Different URLs and domains could still contain the same content, for example www.example1.com and www.example2.com could still contain the exact same text data. For cases like this, we'll need deduplication using a hash of the content, instead of comparing just the URLs. Thus, some deduplication will need to be introduced to the crawling operation as explained below and in 'Deduplication in crawling operation':
  - Hash and store in metadata DB with index:
    - A checksum could be generated for both the URL and text data via a cryptographic hashing function like SHA-256 or MD5. A checksum will be of the same length regardless of the URL or text data. This checksum value will help us perform deduplication of the crawled content.
  - Bloom filter:
    - A bloom filter can be directly implemented in Redis, where there is a bloom filter data structure. It also trades accuracy of an item being in a set for space efficiency. If we don't have a space constraint, then a bloom filter may be an overkill to perform deduplication.

**A bloom filter is a cool data structure and will work efficiently if used in Redis, however it may be an overkill to perform deduplication. However, it's still worth talking about it in an SDI**

### Crawler traps

- The validation and prevention for the crawler traps discussed below should be mainly implemented in the URL fetcher workers and Extraction workers. These workers will also impose a time limit via the visibility timeout in SQS to prevent long crawling operations.
- Crawler traps could also be stored in a separate table to prevent future traps from the same URL

- There could be multiple crawler traps which prevent the usual crawling of a web page:
  - When the URLs contain multiple embedded URLs
  - URLs could contain very large pages
  - URLs could contain very dynamically changing content
  - URLs could contain redirection cycles

- Below are some of the ways to avoid crawler traps:
  - Set a "depth limit" on how deep a crawling operation can go for a single domain. Each time we extract the content from an embedded URL for a domain, the depth value will increase by 1. If the domain's depth value is passed the depth limit, then the crawling operation will be stopped
  - Check the HTML, ie if it has numerous embedded URLs, then limit the number of extracted embedded URLs to a threshold
  - Check the web server's Content-Length header in it's response OR the length of the HTML, and if it is past a threshold
  - Identify cycles by checking the checksum value in the URL metadata table for duplicate URLs
  - Avoid URLs with multiple directories (these are called spider traps) such as								google.com/foo/bar/foo/bar/foo/bar/foo/bar

### Handling URL scheduling

- At some point, the system will have crawled all the embedded URLs and seed URLs provided to the URL frontier, While our requirements are for a one-time crawl, we may want to consider how we would handle URL scheduling. For example, this could be that we plan to re-train the model every month or that our crawler is for a search engine that needs to be updated regularly.
- I'd suggest adding a new component "URL Scheduler" that is responsible for scheduling URLs to be crawled. So rather than putting URLs on the URL frontier directly from the Extraction workers, the Extraction workers would put URLs in a "URLs to schedule" table, which will contain the scheduling details, and the URL Scheduler would be responsible for scheduling URLs to be crawled by using some logic based on the lastCrawledTime field, recrawl frequency, etc. The URL scheduler would then pull URLs from this "URLs to schedule" table, and enqueue them into the URL frontier on a recurring basis.

### Scaling to 1B web pages

#### Estimation on number of network optimized EC2 instances required for URL fetcher workers + Extraction workers

- Web crawling is an IO bound task, where multiple network requests to the DNS, web servers, DB, queues, etc will need to be made. An average network optimized EC2 instance can handle about 40 Gbps, which means that 40 Gbps / (8 bits / byte) / (2 MB / page) = 2.5K pages per second can be requested per second. However, 2.5K pages / second is not likely - we can't use all of the bandwidth maximally. There will be other factors such as DNS resolution, web servers response latency, rate limiting, politeness adherence, retries, etc which will greately reduce the 2.5K pages / second to 20% of it's amount, which will be 500 pages / second.
- Thus, if we have 1B pages we need to crawl, it will take:
  - 1B pages / (500 pages / second) = 23 days to crawl 1B pages on a single EC2 instance
  - To prevent a SPOF and for scalability purposes, we can have 3-5 EC2 instances where it will instead take roughly 5 days

**Note that the number of EC2 instances will likely also be equal to the number of queues (where a worker pulls a URL from it's queue), and if the crawling speed were to increase, the EC2 instances and queues could be auto-scaled to keep up with the crawling speed**

#### Scaling DNS lookups

- We'll likely use a 3rd party DNS provider, instead of the default DNS provider supported by the ISP. This will give us more flexibility in the DNS lookups
- Most 3rd party DNS services like CloudFlare or OpenDNS allows us to increase the provider's rate limits when requesting for DNS lookups, however it may be costly. Other optimizations are also available, such as:
  - DNS caching
    - We can cache DNS lookups in our crawling operation to reduce the number of DNS requests we need to make. This way, all URLs for the same domain will reuse the same cached DNS lookup
  - Multiple DNS providers:
    - Instead of sticking to one DNS provider which imposes a rate limit, we can use multiple DNS providers and round-robin between them. This can help distribute the load across multiple providers and reduce the risk of hitting a single provider's rate limit.
   
### Recrawling

- To ensure we don't waste time on recrawling pages, we can introduce a recrawlTime field in the URL metadata DB, and update it to an appropriate value depending on how frequent the web page updates.
- We could initially set a default recrawlTime value, and update it over time. For example, a reddit page may update frequently, so the recrawlTime could be 5 days, while another website could update less frequently, so the recrawlTime could be 1 month.
- We could also have a recrawl frequency field for the urlID, depending on how frequently we expect the web page to update. The recrawling can be done using this recrawl frequency

### Additional deep dives

Below are some deep dives which could be discussed if time permits in a SDI:

#### Handling dynamic content (CSR)

- Many websites are built with JavaScript frameworks like React or Angular. This means that the content of the page is not in the HTML that is returned by the server, but is instead loaded dynamically by the JavaScript. To handle this, we'll need to use a headless browser like Puppeteer to render the page and extract the content.

#### Crawling speed adjusted using TTFB

- Different web sites will have different TTFB values (time to first byte values) depending on the web servers hosting the web site. The TTFB measures the time it takes for the client to receive the first byte from a web server. The crawling speed could be adjusted depending on the TTFB of the web site.

#### Supporting different formats of crawled data in HTML (other than just text)

- We can include additional modules to the URL fetcher workers to support different communication protocols to request the web servers, and retrieve different types of file formats from the web servers. 

- We can include other communication protocols like FTP or MIME (multi-purpose internet mail extension) to handle transfer of different file formats, other than just using HTTP. For example, FTP can be used to transfer files from a server to a client via TCP. The MIME protocol also allows servers to transfer different kinds of data such as audio, video, images, etc over email. If a web page contains a video or image, the MIME protocol can be used to fetch the content for them from the web servers

- Additionally, other functionalities can be added such as fetching PNG / JPG images from the fetched HTML

#### Forward proxy servers to get passed NATs or firewalls

- Forward proxy servers could also be used when requesting the web servers. Forward proxy servers will act as intermediaries, and hide the client's IP address (client refers to URL fetcher workers requesting the web servers) for ensuring the requests are not blocked due to any NATs or firewalls.
- Forward proxies could also be used to rotate client IP addresses, and randomize the User-Agent header when requesting web servers.

#### BFS vs DFS

- To get the embedded URLs nested deep in a HTML, the Extraction workers could use DFS to parse through and find nested embedded URLs.
- However, to find the embedded URLs within the "first level" in a HTML, we could use BFS.

#### Monitoring system health

We'll want to monitor the health of the system to ensure that everything is running smoothly. We can use a monitoring service like Datadog or New Relic to monitor the performance of the crawlers and parser workers and to alert us if anything goes wrong.

#### Path-ascending crawling

Path-ascending crawling can help discover a lot of isolated resources or resources for which no inbound link would have been found in regular crawling of a particular Web site. In this scheme, a crawler would ascend to every path in each URL that it intends to crawl. For example, when given a seed URL of http://foo.com/a/b/page.html, it will attempt to crawl /a/b/, /a/, and /.

## Wrap up

- Backup on S3
- Server and database replication
- Logging / caching of crawler traps

