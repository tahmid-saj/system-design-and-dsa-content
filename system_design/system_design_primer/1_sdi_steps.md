# How to approach a system design interview

## Step 1: Outline use cases, constraints, and assumptions

Gather requirements and scope the problem. Ask questions to clarify use cases and constraints. Discuss assumptions.

Who is going to use it?
How are they going to use it?
How many users are there?
What does the system do?
What are the inputs and outputs of the system?
How much data do we expect to handle?
How many requests per second do we expect?
What is the expected read to write ratio?

## Step 2: Create a high level design

Outline a high level design with all important components.

- Sketch the main components and connections
- Justify your ideas

## Step 3: Design core components

Dive into details for each core component. For example, if you were asked to design a url shortening service, discuss:

- Generating and storing a hash of the full url
  - MD5 and Base62
  - Hash collisions
  - SQL or NoSQL
  - Database schema
- Translating a hashed url to the full url
  - Database lookup
- API and object-oriented design

## Step 4: Scale the design

Identify and address bottlenecks, given the constraints. For example, do you need the following to address scalability issues?

- Load balancer
- Horizontal scaling
- Caching
- Database sharding

Discuss potential solutions and trade-offs. Everything is a trade-off.

These are time based steps of a system design interview: https://leetcode.com/discuss/career/229177/My-System-Design-Template

