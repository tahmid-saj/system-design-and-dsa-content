# Distributed search

## Requirements

### Functional

- Crawler (we won’t design the crawler):
  - The crawler fetches content from the web and creates 		documents of them

- Indexer (we will design the indexer):
  - The indexer builds the index mapping of the documents

- Searcher (we will design the searcher):
  - The searcher responds to search queries by running the		search query on the index mappings created by the indexer

### Non-functional

- Low latency:
  - Search results should be returned with low latency
- Search method should be efficient and likely build a searchable index

## Indexing 101

- Indexing is the organization of data such that it is easier and faster to perform queries on the data

There are several approaches to build an index mapping:

### Simple iterative indexing for each document

- The simplest way to build an index mapping is to assign a unique ID to each document and store the ID and document in a database

- Running a search query on the indexes for the documents wouldn’t be fast, and also it doesn’t help with quickly retrieving documents	with specific terms. The simple iterative indexing is not practical for querying millions of documents.

### Inverted index

- An inverted index mapping is a hash map containing the mapping of term : ([docIDs], [freq in docs], [[position in docIDs]]). It stores the	terms and maps them to a document-term matrix. A document-term matrix is a matrix that contains the frequency of the terms in a list of	documents. Any stop words are also ignored when creating the inverted index mapping. An example of inverted index is shown in 'Inverted index'.

- The inverted index contains the following:
  - list of document (docIDs) in which the term appeared
  - frequency of the term in each document (docIDs)
  - positions of the term in the document (docIDs)

- Inverted index is very popular, and is used by many search services like Apache Lucene and Elasticsearch. It is able to store terms for a	large number of documents, and it also doesn’t store duplicate versions of the same term since the term is the key.

- The downside of inverted index is that there is increased storage for maintaining the inverted index mappings, however inverted index	definitely reduces the search time

- Another downside is that when adding, updating or deleting a document, we’ll have to update all the terms in the document against the	inverted index mapping, which will take time to process if not done in a parallel fashion

- When searching for a phrase, such as “search engine”, we’ll first look for the docIDs in the inverted index mapping which contains the	terms “search” and “engine”. Afterwards, we’ll retrieve those docIDs and the frequency of which the terms appear in the docIDs. When	returning the search results, we may rank it based on the frequency, and we might also return the locations in which the terms appear in	the docIDs. This example is under the ‘Inverted Index’ image

- Since there may be too many documents which contains a term, we could also perform pagination and return only the first n documents	after sorting based on the frequency of the term in the docIDs

<br/>
<br/>

Inverted index:

<img width="500" alt="image" src="https://github.com/user-attachments/assets/8ba52279-4286-4880-87a7-025263f7efee" />

### Below are some factors we should consider when designing an index mapping

- Storage for the index mapping:
  - The index mapping will often be in a cache or a KV store for quick access, thus only the necessary info will need to be stored

- Search optimization:
  - If the index mapping is not optimized for fast searches, it may affect the search speed

- Maintenance of the index mapping:
  - The index mapping may need to be updated over time as new documents are added, removed, updated

### If building the index mapping in a centralized server, there could be some limitations as follows

- There will be an indexer that processed the documents and generated an inverted index mapping, which may be stored in a JSON or	binary files. There will also be a searcher that queries the inverted index mappings and retrieves the relevant documents in the storage.

- This centralized server will have a SPOF, and may likely have a server overload as the number of documents grow or concurrent		queries are made to the searcher.
	
- When using search services, usually a distributed indexes/searcher are used which are provided via Apache Lucene and Elasticsearch,	which can contain the documents and index mappings across nodes

## API design

### Searching using a search query

- Note that we’ll use cursor based pagination, as the number of documents returned may be quite large, so it is more suitable to have a	cursor to traverse through the results, rather than using offset based pagination where the entries have to be parsed from the starting entry to the offset

Request:
```bash
GET /search?query&nextCursor&limit
```

Response:
```bash
{
	documents: [ { docID, frequency, positionsInDocID: [ positions in docID ] } ],
	nextCursor, limit
}
```

## HLD

- In our search system there will be two phases, where one phase is the online phase of the client initiating the search requests, and the offline
phase is the crawler and indexer working together to create the documents and index mappings asynchronously

### Crawler

- The crawler will collect content from the web and provide the created documents to the blob store. The content could be maintained in a	binary or JSON file format, with info such as the document title, document content, updated timestamp, etc.

### Indexer

- The indexer will fetch the documents from the blob store and generate the inverted index mappings in a parallel fashion using			MapReduce. MapReduce will run on distributed machines which can generate the index mappings for terms in parallel.

- The indexer may first fetch a document, split it up into different fixed sized chunks, and then send those individual chunks to the		MapReduce servers which will generate the index mappings.

### Blob store

- The blob store will store both the documents and the index mappings. Both the documents and index mappings may be stored in binary	or JSON file formats. Storing the data in binary will reduce the overall storage, and make the chunking easier, however fetching the		content in binary will be difficult since the binary data will need to be converted to a readable format first. However, storing the data in		JSON may take up more storage, but will be easier to read as it doesn’t involve a conversion. 

- We could store the documents in a binary file format with fixed sized chunks, and store the index mappings in a JSON format to make	reading the data easier

### Searcher

- The searcher will parse the terms in the search query, then fetch the index mappings for the terms in the blob store, and then return the	relevant and ranked documents from the index mappings. As searching will require a lot latency, the searching can be done in parallel via	a similar MapReduce process in the indexing

<img width="600" alt="image" src="https://github.com/user-attachments/assets/888b3f95-e468-430d-b64d-66df552e4c2e" />

## DD

- In the detailed design, we’ll address additional parts of the system:

### Partitioning the documents

The partitioning of the documents will further help with availability and scalability. We can partition the documents by the		documents themselves or the terms:

#### Document partitioning

- In document partitioning, all the documents collected by the web crawler are partitioned into groups by their docID.	 		To assign a document to a partition, a hashing function can be used on the docID. A single node will contain different		document partitions

- By using document partitioning, there will be less inter-node communication than term partitioning, as there will be			more terms in a document partition, so less communication will take place outside the node

#### Term partitioning

- In term partitioning, all the terms will be partitioned by likely the first n characters of the term. A single node will			contain different term partitions

- Search queries will be sent to the nodes which contains the term in the query. Therefore, for a very large search			query, there will be more inter-node communication

#### Document partitioning vs term partitioning

- Using document partitioning, one node will contain different document partitions, and one partition will contain a set of		documents. We’ll use a cluster manager, which will perform the overall partitioning of the documents, and replication of the	nodes. The cluster manager can also maintain a separate storage of the mapping between the docID : nodeID, and			nodeID: partitionID which specifies which node contains which document, and which node contains which partition. The		searcher can then use the cluster manager to retrieve the correct partitions containing the documents, and fetch the			documents from those partitions.

- The size of each partition can be decided by the cluster manager depending on the size and number of the documents.		Additionally, as the nodes are replicated, the nodes in a replica set can send periodic heartbeats using heartbeat protocol		to ensure they’re active, and notify the cluster manager if one of the nodes are down

- As the nodes are optimized for parallel computation, the searcher can utilize a MapReduce model to fetch the documents	from the nodes in a parallel fashion, after it has acquired the docIDs from the inverted index mapping in the blob store.

- The relevant documents from the nodes can then be merged and returned

### Indexing

- The indexer will run the inverted indexing algorithm via MapReduce and process the documents in parallel. The inverted		index mappings will then be stored on the blob store.

### Searching

- When a search query comes in, the searcher will fetch the index mappings for the terms in the search query. The			searcher will then fetch the appropriate partitions from the cluster manager which will maintain the mappings for the			docID : nodeID, nodeID : partitionID. The searcher will fetch the documents from the relevant partitions in a parallel			fashion using MapReduce, then merge the documents. The merger may also rank and paginate the documents based on		the frequency of the terms in the documents,

- The merged result will then be returned to the client

### Replication of nodes

- The nodes could be replicated to provide a higher availability and scalability as more search requests are coming in to a		single node. We can follow a primary-secondary replication model, where the primary node handles writes to the			documents, and the secondary nodes handle the reads. Additionally, if the nodes are distributed across data centers,		asynchronous replication could be used across data centers to reduce the latency

### Caching

- Overall we could cache both the frequent searches and frequently accessed index mappings for the searcher to use. As		the document and inverted index data may be more complex, Redis could be more suitable than Memcached since Redis		provides different data structures such as lists, sorted sets, hash maps, etc which could be used

### MapReduce for inverted index

- The MapReduce model is implemented using a set of worker nodes called the Mappers and Reducers. The input to the		MapReduce model is a set of documents, and it’s output are the inverted index mappings.
	
- The MapReduce model contains a cluster manager that is separate from the one we created for performing replication /		partitioning. The cluster manager assigns a set of documents to the Mappers. Once the Mappers are done processing the		documents, the cluster manager then sends the output of the Mappers to the Reducers.

- The Mappers perform the overall inverted indexing algorithm to generate the index mappings for a set of documents.		The Mappers can process different documents in parallel.

- The Reducers takes the output from the Mappers, and combines the index mappings into a summarized output. The 		Reducers cannot start combining the outputs until the Mappers are completed. This process is shown in			'MapReduce inverted indexing process'.

<br/>

MapReduce inverted indexing process:

<img width="950" alt="image" src="https://github.com/user-attachments/assets/41402e72-27f1-4bc8-af5d-d87af63bac10" />

<img width="700" alt="image" src="https://github.com/user-attachments/assets/4156d733-474d-4fb2-bd45-3c1ab2d66d44" />

## Wrap up

- Geo-replication
- Inconsistency resolution
  - quorum based approach
- Filter layer in front of the cache to filter unwanted suggestions
- Bloom filter for checking if value exists in cache

- We could use unicode characters to handle multiple languages
- Use of CDN for geographical result oriented search results
