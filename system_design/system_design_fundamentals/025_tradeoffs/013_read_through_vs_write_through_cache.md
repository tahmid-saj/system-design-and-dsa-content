# Read through vs write through cache

Read-through and write-through caching are two caching strategies used to manage how data is synchronized between a cache and a primary storage system. They play crucial roles in system performance optimization, especially in applications where data access speed is critical.

## Read through cache

In a read-through cache, data is loaded into the cache on demand, typically when a read request occurs for data that is not already in the cache.

![image](https://github.com/user-attachments/assets/ee44fc20-f18a-44a6-a6f2-1f536c3072dc)

### Process

- When a read request is made, the cache first checks if the data is available (cache hit).
- If the data is not in the cache (cache miss), the cache system reads the data from the primary storage, stores it in the cache, and then returns the data to the client.
- Subsequent read requests for the same data will be served directly from the cache until the data expires or is evicted.

### Pros

- Transparency
  - The application only needs to interact with the cache, simplifying data access logic.
- Reduced Latency on Hits
  - Frequently accessed data is served quickly from the cache.
- Reduces Load on Primary Storage
  - Frequent read operations are offloaded from the primary storage.

### Cons

- Cache Miss Penalty
  - The first request for data not in the cache incurs latency due to fetching from the data store.
 
### Example: E-commerce online product catalog

- Scenario
  - Imagine an e-commerce website with an extensive online product catalog.
- Read-Through Process
  - Cache Miss: When a customer searches for a product that is not currently in the cache, the system experiences a cache miss.
  - Fetching and Caching: The system then fetches the product details from the primary database (like a SQL database) and stores this information in the cache.
  - Subsequent Requests: The next time any customer searches for the same product, the system delivers the product information directly from the cache, significantly faster than querying the primary database.
- Benefits in this Scenario
  - Reduced Database Load: Frequent queries for popular products are served from the cache, reducing the load on the primary database.
  - Improved Read Performance: After initial caching, product information retrieval is much faster.

## Write through cache

In a write-through cache, data is written simultaneously to the cache and the primary storage system. This approach ensures that the cache always contains the most recent data.

![image](https://github.com/user-attachments/assets/1f95dbcc-2933-437e-8b09-abfafa085b16)

### Process

- When a write request is made, the data is first written to the cache.
- Simultaneously, the same data is written to the primary storage.
- Read requests can then be served from the cache, which contains the up-to-date data.

### Pros

- Data Consistency
  - Provides strong consistency between the cache and the primary storage.
- No Data Loss on Crash
  - Since data is written to the primary storage, there’s no risk of data loss if the cache fails.
- Simplified Writes
  - The application only interacts with the cache for write operations.

### Cons

- Latency on Write Operations
  - Each write operation incurs latency as it requires simultaneous writing to both the cache and the primary storage.
- Higher Load on Primary Storage
  - Every write request impacts the primary storage.

### Example: Banking system transaction

- Scenario
  - Consider a banking system processing financial transactions.
- Write-Through Process
  - Transaction Execution: When a user makes a transaction, such as a deposit, the transaction details are written to the cache.
  - Simultaneous Database Write: Simultaneously, the transaction is also recorded in the primary database.
  - Consistent Data: This ensures that the cached data is always up-to-date with the database. If the user immediately checks their balance, the updated balance is already in the cache for fast retrieval.
- Benefits in this Scenario
  - Data Integrity: Crucial in banking, as it ensures that the cache and the primary database are always synchronized, reducing the risk of discrepancies.
  - Reliability: In the event of a cache system failure, the data is safe in the primary database.

## Read through vs write through cache

- In the Read-Through Cache (Product Catalog), the emphasis is on efficiently loading and serving read-heavy data after the initial request, which is ideal for data that is read frequently but updated less often.
- In the Write-Through Cache (Banking System), the focus is on maintaining high data integrity and consistency between the cache and the database, which is essential for transactional data where every write is critical.
- Data Synchronization Point
  - Read-through caching synchronizes data at the point of reading, while write-through caching synchronizes data at the point of writing.
- Performance Impact
  - Read-through caching improves read performance after the initial load, whereas write-through caching ensures write reliability but may have slower write performance.
- Use Case Alignment
  - Read-through is ideal for read-heavy workloads with infrequent data updates, whereas write-through is suitable for environments where data integrity and consistency are crucial, especially for write operations.

### When to use read through vs write through

#### Read-Through

- Ideal when read operations are frequent, and data changes infrequently.
- Useful when you can tolerate eventual consistency for reads.

#### Write-Through

- Suitable when data consistency is critical, and you cannot afford stale data.
- Necessary when the system requires immediate propagation of updates.

<img width="706" alt="image" src="https://github.com/user-attachments/assets/1541ddb0-2702-4293-aced-0df7ca31a7fd" />

Read-through caching is optimal for scenarios where read performance is crucial and the data can be loaded into the cache on the first read request. Write-through caching is suited for applications where data integrity and consistency on write operations are paramount. Both strategies enhance performance but in different aspects of data handling – read-through for read efficiency, and write-through for reliable writes.

