# Security

This section could use some updates. Consider contributing!

Security is a broad topic. Unless you have considerable experience, a security background, or are applying for a position that requires knowledge of security, you probably won't need to know more than the basics:

- Encrypt in transit and at rest.
- Sanitize all user inputs or any input parameters exposed to user to prevent XSS and SQL injection.
- Use parameterized queries to prevent SQL injection.
- Use the principle of least privilege.

## Parameterized queries

Parameterized queries are a database-level coding technique that uses parameters to improve security and efficiency. They are also known as prepared statements.

Here are some benefits of parameterized queries:

- Security
  - Parameterized queries are a strong defense against SQL injection attacks. SQL injection is a dangerous web vulnerability that allows attackers to change a web application's SQL statement to steal or modify data. Parameterized queries prevent this by separating the SQL logic from the data being passed. 

- Efficiency
  - Parameterized queries can be used repeatedly without re-compiling. 

- Code reuse
  - Parameterized queries encourage abstracting patterns and writing code with the "don't repeat yourself" (DRY) pattern. 

- Unit testing
  - Parameterized queries make unit testing easier. 

Parameterized queries work by predefining an SQL query template with placeholders for user-supplied values. When the query is executed, the placeholders are replaced with actual data. The database engine treats the placeholders as data, not executable code.

PostgreSQL, MySQL and other SQL databases allow the use of parameterized queries via a '?' and other syntax for the placeholder containing the user input data.
