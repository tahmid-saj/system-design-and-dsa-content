# Indexes

## Indexes introduction

Indexes are well known when it comes to databases. Sooner or later there comes a time when database performance is no longer satisfactory. One of the very first things you should turn to when that happens is database indexing.

The goal of creating an index on a particular table in a database is to make it faster to search through the table and find the row or rows that we want. Indexes can be created using one or more columns of a database table, providing the basis for both rapid random lookups and efficient access of ordered records.

### Example: A library catalog

A library catalog is a register that contains the list of books found in a library. The catalog is organized like a database table generally with four columns: book title, writer, subject, and date of publication. There are usually two such catalogs: one sorted by the book title and one sorted by the writer name. That way, you can either think of a writer you want to read and then look through their books or look up a specific book title you know you want to read in case you don’t know the writer’s name. These catalogs are like indexes for the database of books. They provide a sorted list of data that is easily searchable by relevant information.

Simply saying, an index is a data structure that can be perceived as a table of contents that points us to the location where actual data lives. So when we create an index on a column of a table, we store that column and a pointer to the whole row in the index. Let's assume a table containing a list of books, the following diagram shows how an index on the 'Title' column looks like:

![image](https://github.com/user-attachments/assets/ea3b5027-3b9f-4ae7-a668-701608a60042)

Just like a traditional relational data store, we can also apply this concept to larger datasets. The trick with indexes is that we must carefully consider how users will access the data. In the case of data sets that are many terabytes in size, but have very small payloads (e.g., 1 KB), indexes are a necessity for optimizing data access. Finding a small payload in such a large dataset can be a real challenge, since we can’t possibly iterate over that much data in any reasonable time. Furthermore, it is very likely that such a large data set is spread over several physical devices—this means we need some way to find the correct physical location of the desired data. Indexes are the best way to do this.

### Why use indexes

#### Faster Data Retrieval

Indexes significantly speed up query execution by providing a more efficient means of locating data, which can lead to a reduction in the number of disk I/O operations and CPU usage.

#### Sorting and Ordering

Indexes can be used to quickly sort and order the data in a table based on specific criteria, which can be useful for reporting or displaying data in a specific order.

#### Reduced Table Scans

By using an index, the database can avoid full table scans, which require reading every row in a table. Instead, the database can directly access the indexed columns, reducing the amount of data that needs to be read and processed.

#### Efficient Data Access

Indexes provide a more efficient means of accessing data by organizing it in a way that allows the database to quickly locate the rows that meet the query criteria.

#### Index Selectivity

Indexes with high selectivity can improve query performance by reducing the number of rows that need to be accessed. High selectivity means that the index can effectively filter out a large number of rows, thereby reducing the amount of work required to process a query.

### Indexes can decrease write performance

It's important to note that while indexes can significantly improve query performance, they also come with some overhead. Indexes require additional storage space and can slow down write operations, such as INSERT, UPDATE, and DELETE, since the indexes must be updated along with the table data. Therefore, it's essential to strike a balance between the number of indexes and their impact on query performance and storage requirements.

An index can dramatically speed up data retrieval but may itself be large due to the additional keys, which slow down data insertion & update.

When adding rows or making updates to existing rows for a table with an active index, we not only have to write the data but also have to update the index. This will decrease the write performance. This performance degradation applies to all insert, update, and delete operations for the table. For this reason, adding unnecessary indexes on tables should be avoided and indexes that are no longer used should be removed. 

To reiterate, adding indexes is about improving the performance of search queries. If the goal of the database is to provide a data store that is often written to and rarely read from, in that case, decreasing the performance of the more common operation, which is writing, is probably not worth the increase in performance we get from reading.

## Types of indexes

Database indexes are designed to improve the speed and efficiency of data retrieval operations. They function by maintaining a separate structure that points to the rows in a table, allowing the database to look up data more quickly without scanning the entire table.

There are various types of database indexes, each with its unique characteristics and use cases. Understanding these different index types is crucial for optimizing the performance of database systems and ensuring efficient data retrieval.

In this section, we will explore several common types of database indexes, including clustered, non-clustered, unique, partial, filtered, full-text, and spatial indexes, along with examples to illustrate their applications.

### Clustered indexes

Clustered indexes determine the physical order of data storage in a table. The table's data is sorted and stored based on the columns specified in the clustered index. Since the order of the data is the same as the index, there can only be one clustered index per table. Clustered indexes are highly efficient for range queries, as the data is stored in a contiguous manner.

Example: In a table with a clustered index on the 'DateOfBirth' column, the rows would be stored in the order of the 'DateOfBirth' values.

### Non-clustered indexes

Non-clustered indexes do not affect the physical order of data storage in a table. Instead, they maintain a separate data structure that points to the rows in the table. Multiple non-clustered indexes can be created for a table, and they can be used to optimize specific queries or access patterns.

Example: In a table with a non-clustered index on the 'LastName' column, the index would store pointers to the rows sorted by the 'LastName' values, while the actual table data remains unordered.

### Unique indexes

A unique index ensures that the indexed columns do not contain duplicate values. This constraint helps maintain data integrity and can be used to enforce uniqueness across one or more columns in a table.

Example: In a table with a unique index on the 'Email' column, no two rows can have the same email address.

### Partial indexes

A partial index includes only a subset of rows in a table based on a specified filter condition. This type of index is useful when a large table has a relatively small number of rows that are frequently queried, reducing the size and maintenance overhead of the index.

Example: In a table with a partial index on the 'Status' column where the condition is "Status = 'Active'", only rows with an 'Active' status would be included in the index.

### Filtered indexes

Similar to partial indexes, filtered indexes include only a subset of rows based on a specified filter condition. However, filtered indexes are specific to Microsoft SQL Server and provide additional optimization options for queries with specific predicates.

Example: In a table with a filtered index on the 'ProductID' column where the condition is "Price > 100", only rows with a price greater than 100 would be included in the index.

### Full-text indexes

Full-text indexes are designed to support complex text-based searches, such as natural language queries or pattern matching. This type of index enables searching for words or phrases within large text fields or documents, offering more advanced search capabilities compared to traditional indexes.

Example: In a table with a full-text index on the 'Description' column, users can search for rows containing specific words or phrases in the 'Description' field.

### Spatial indexes

Spatial indexes are used to optimize queries involving spatial data types, such as geometry or geography data. They enable efficient processing of spatial queries, such as finding objects within a specific area or calculating distances between objects.

Example: In a table containing location information, a spatial index on the 'GeoCoordinates' column would enable fast retrieval of nearby locations based on latitude and longitude coordinates.

