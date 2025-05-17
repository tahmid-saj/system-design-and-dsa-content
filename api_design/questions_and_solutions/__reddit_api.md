# Reddit API

## Requirements

### Questions

- What features are we focusing on?
  - Writing posts
  - Commenting on posts
  - Upvoting / downvoting posts
  - Let’s not focus on additional features like sharing and reporting posts

- Should posts or comments support attachments, like images and videos?
  - Let’s keep it simple and exclude attachments

- I’m thinking of defining the schemas for the main entities for a subreddit, and then defining their CRUD operations - like create / get / edit / delete / list items. Is this in-line with what I should be designing?
  - Yes, consider them as entities and list their CRUD based API endpoints
	
- Are posts, comments and votes the only entities I should consider?
  - Yes, these are the 3 core ones

- Should the API design include API signatures, API request / response parameters, and the types of the parameters?
  - Yes, include all of those

- Is there any other functionality that we should design?
  - Yes, you should allow people to award posts. Awards are a special currency that can be bought		for real money and gifted to comments and posts. Users can buy awards using real money, and		can give awards to posts and comments (user can give one award per post / comment)

### Functional

- Writing posts
- Commenting on posts
- Upvoting / downvoting posts

<br/>

- Supporting awards and giving awards to posts / comments

### Non-functional

- We want to efficiently store posts, comments and votes. It's likely that these entities will have a hierarchy, and we want to efficiently store and fetch them.

## Data model / entities

- Before coming up with the entities, it’s important to decide whether to have votes as a separate entity or store votes inside the post / comment entities. 

- If we store votes within the post / comment entity, we’ll introduce denormalization where additional dimensions such as upvote / downvote are stored in the post / comment table as well. With denormalization, reading becomes much easier since the vote / downvote data is already within the post / comment entities. However, writing or join operations may be more complex, since the vote / downvote data will also need to be added and considered when we create a new post / comment every time or perform a join. Thus, denormalization may have better reads, but worse writes.

- With normalization, where we store the votes as a separate entity, reads will be more complex because we will need to perform more complex join operations between the posts / comments entities and the votes entity (becuase these 3 are all individual entities). However, writes will be easier since we don't need to add additional fields for votes within the posts / comments entities. Overall, the data within subreddits may already be complex, since comments and posts will have their own hierarchy, therefore it will be more simpler to manage votes in a separate entity and use normalization to reduce redundancy as much as possible.

- The Reddit UI also shows if the user themself has upvoted or downvoted a post / comment, and thus we'll need a separate votes entity to store the data on which userID voted on which postID / commentID

<br/>

- Posts:
  - Note that the Posts table will still maintain a votesCount, but the actual votes themselves (which includes the userID that made the vote) will be maintained as a separate vote entity
  - Note how we're not storing the comments themselves as a list within this entity. This is because some posts could have hundreds or thousands of comments (Reddit allows an unlimited number of comments for a post), and storing it in the posts entity is inefficient.
    - postID
    - userID
    - subredditID
    - title, post
    - votesCount, commentsCount, awardsCount
    - createdAt, deletedAt

- Comments:
  - Comments will be similar to posts, but will have a parentID which points to the parent post or parent		comment. This parentID will allow the client to reconstruct the comment trees and hierarchy on the UI. If we use a GSI within DynamoDB, we can also likely return the paginated results of the comments by their createdAt times.

  - Note that we’ll store the parentID of the comment, instead of the reverse, where we store the child		comments for a post or comment. This way, we’ll build the tree of comments and posts from the child		comments to the parent comments or posts. We won't store the child commentIDs within the post or comment entities, because some comments could still have hundreds or thousands of nested comments (Reddit allows an unlimited number of comments for a post), and storing the child commentIDs within a list in the posts / comments entities is inefficientl - we'll instead store the parentID.
    - When a user views a post, we'll fetch the postID from the posts entity, then we'll fetch all the commentIDs which have their parentID as this postID. If a user clicks on a commentID for the postID, then we'll fetch all the comments again which have their parentID as the clicked commentID. This way, we'll only show the first nested level (or first few nested levels) or the comments for a post.

  - Also, we’ll use parentID because when we create a comment, it will always have a parentID, whereas when		we first create a comment or post, it will not have any subEntityIDs from any child comments by default.		We’ll need to append the child comments’ commentID to the subEntityIDs for the parent comment or post,	which will be more complex to maintain, since we’ll maintain a list of commentIDs instead of only having a	single parentID for a comment - a comment will always only have one parent comment or post.
	- commentID
	- userID
	- parentID
	- comment
	- votesCount, commentsCount, awardsCount
	- isDeleted
	- createdAt, deletedAt

- Votes:
  - The votes entity is maintained separately here, where a user can create a new vote (up / down vote) for	a post or comment.

  - Note that the entityID is either the postID or the commentID the vote refers to. It makes sense to have a separate	entity for votes since the vote could refer to either a post or comment, which might make these 2 types of votes different.
  - Depending on the interview, if the UI needs to have the vote icon light up if the user voted on the post / comment or not, then we could remove this votes entity.
	- voteID
	- userID
	- entityID
	- voteType: UP / DOWN

- Users:
  - Since we’ll also need to integrate the buying / giving awards functionality, we can maintain another		entity, the user, which contains the awardsQuantity representing the number of awards a user has

	- userID
	- userName
	- userEmail
	- awardsQuantity


## API design

- Note that we’ll use userID if the user is authenticated to send requests to the endpoints. The userID could be placed in a session token or JWT in the Authentication header as such:
	- Authentication: Bearer <JWT>

- The below caching header could also be applied to fetch frequently accessed messages quicker. “no-cache” means that a browser may cache a response, but it must first send a validation request to an origin server before caching it. “Public” means that the entry can be cached by any intermediary such as a proxy server between the client and server - which is beneficial for static content like images and stylesheets. “Private” means that an entry can only be cached by the browser and no other intermediary. This is important for private content:
	- Cache-Control: no-cache max-age Private/Public

- Note that there will be an API gateway which performs authentication using the userID and performs ACL checks (access control list checks) to ensure the client has the necessary permissions to the endpoints. If the user is authenticated and authorized, the client will use this userID to send requests to the API endpoints

### Posts

#### Get post

Request:
```bash
GET /subreddits/:subredditID/posts/:postID
```

Response:
```bash
{
  subredditID,
  postID,
  userID,
  title, post,
  votesCount, commentsCount, awardsCount,
  createdAt, deletedAt
}
```

#### List posts

- Since a subreddit may have hundreds or thousands of posts, we can provide paginated results via		cursor based pagination, and use lazy loading to load only the posts within the client’s viewport. The nextCursor could also be set to the viewport's oldest createdAt time for the post. This way, the next paginated result will fetch the postIDs which are older than the viewport's oldest createdAt time.

- On Reddit, when we get view a post or comment, either the upvote or downvote button will be lit up,			which indicates the user has upvoted or downvoted on the post or comment. This endpoint can 			further gather this data from the votes table and attach a userVote field to the response as seen below which shows if the user voted on the post / comment or not.

- The endpoint will check the votes table, and check if the userID voted on the entityID (the postID / commentID that's on the viewport).

Request:
```bash
GET /subreddits/:subredditID/posts?query&nextCursor={ viewport's oldest createdAt time for post }&limit
```

Response:
```bash
{
  posts: [ { postID, userID, title, votesCount, commentsCount, awardsCount, createdAt, deletedAt, userVote: UP / DOWN } ],
  nextCursor, limit
}
```

#### Create post

Request:
```bash
POST /subreddits/:subredditID/posts
{
  title, post
}
```

#### Edit post

Request:
```bash
PUT /subreddits/:subredditID/posts
{
  title, post
}
```

#### Delete post

- When we delete a post, we also want to delete the comments for the post. However, when deleting a		comment, we don’t want to also delete the child comments.

Request:
```bash
DELETE /subreddits/:subredditID/posts/:postID
```

### Comments

#### Get comment

Request:
```bash
GET /subreddits/:subredditID/posts/:postID/comments/:commentID
```

Response:
```bash
{
  commentID,
  parentID,
  userID,
  comment,
  votesCount, awardsCount,
  createdAt, deletedAt,
}
```

#### List comments

- Like we did with posts, we'll use the userVote to show on the UI (light up the vote icon on the UI) if the user voted on the comment or not. We will check the votes table, and check if the userID voted on the entityID (the postID / commentID that's on the viewport)

- The nextCursor value could also be set to the viewport's oldest createdAt time for the comment. This way, the next paginated result will have comments which are older than the viewport's oldest createdAt time

Request:
```bash
GET /subreddits/:subredditID/posts/:postID/comments?query&nextCursor={ viewport's oldest createdAt for comment }&limit
```

Response:
```bash
{
  comments: [ { commentID, userID, parentID, comment, votesCount, awardsCount, createdAt, deletedAt, userVote: UP / DOWN } ],
  nextCursor, limit
}
```

#### Create comment

Request:
```bash
POST /subreddits/:subredditID/posts/:postID/comments
{
  parentID,
  comment
}
```

#### Edit comment

Request:
```bash
PUT /subreddits/:subredditID/posts/:postID/comments/:commentID
{
  comment
}
```

#### Delete comment

- Note when we delete a comment, the child comments should not be directly get deleted. Only the 		comment itself will be marked as “deleted” and unviewable. The comment text will be set to null or			empty. This is because we still want to view child comments for parent comments that were deleted.

Request:
```bash
DELETE /subreddits/:subredditID/posts/:postID/comments/:commentID
```

### Votes

#### Up-vote / down-vote

- Note that we’ll use a POST request since we’ll also create a new vote entry in the votes table. Also,		we’ll also increase or decrease the votesCount of the post or comment asynchronously. We’ll do this		in the background because the up-vote / down-vote doesn’t need to be immediately registered in the			database. However, the client side may still see that their vote was counted.

Request:
```bash
POST /subreddits/:subredditID/posts/:postID/votes?op={UP or DOWN} (For posts)
POST /subreddits/:subredditID/posts/:postID/comments/:commentID/votes?op={UP or DOWN} (For comments)
```

### Awards

#### Buy awards

- This endpoint will increase the awardsQuantity for the userID in the Users table. The endpoint will likely first send the user a paymentURL, then the user can go to this paymentURL and input their paymentDetails to buy the awards.

##### Fetching paymentURL

Request:
```bash
PATCH /awards?op={ BUY }
```

Response:
```bash
{
  paymentURL
}
```

##### Buy awards

Request:
```bash
POST /<paymentURL>
{
  paymentDetails (the payment details will be encrypted or retrieved by a separate payment service entirely)
}
```

Response:
```bash
{
  updatedAwardsQuantity
}
```

#### Give award

- This endpoint will decrease the awardsQuantity for the userID in the Users table. The endpoint will		give an award to the entityID, which can either be a post or comment. Afterwards, the				awardsCount for the entityID will increase by 1.

Request:
```bash
PATCH /subreddits/:subredditID/posts/:postID?op={ GIVE_AWARD } (For posts)
PATCH /subreddits/:subredditID/posts/:postID/comments/:commentID?op={ GIVE_AWARD } (For comments)
```

## HLD

### API servers

- The API servers will handle all the CRUD based operations on the posts, comments, votes and awards entities. It will frequently communicate with the database.

### Database / cache

- The database will store the posts, comments, votes and awards entities. Either a SQL or NoSQL database will work here with tweaks such as indexing and partitioning made within the database. The data is read heavy, where we'll need optimal indexing and partitioning for fast queries, thus we'll use DynamoDB here, where we can set GSIs on the tasks and task instances data.
- The partition key can be the subredditID, and the sort key can be the createdAt times for both posts and comments. We could also set a GSI on the votes entity, where the partition key is also the subredditID, and the sort key is the createdAt time for the vote. This way, when we're fetching posts, comments or votes, we'll only query a single shard, and also return the relevant entries in sorted order using the createdAt field.

- The awards entity will likely be attached to a user profile entity, and be managed by a separate User profile service which might support in buying awards and giving awards.

#### Cache

- Because the data is read heavy, where it's more likely for users to read posts / comments, rather than create them, we can cache the frequently accessed entries. It might also be easier to cache the entries based on the createdAt time, so that we can return the results to the client in a sorted order. Therefore, we can cache the frequently accessed posts, comments and votes entries in a Redis sorted set.

### Search service

- The Search service will connect to the database and handle any search queries (in the API endpoint for listing posts and comments). The Search service will likely use inverted index mappings on text based fields of the posts and comments data, and perform efficient searching using the mappings. Thus, it could use a tool such as Lucene or Elasticsearch which can maintain inverted index mappings for a data store.

### Architecture style

- The API mainly performs CRUD operations on different entities, thus REST will be suitable here. It's not necessary to use GraphQL, because there's not too many entities we're working with. Also, the communication does not have a high throughput or a need to have subchannels, thus gRPC won't be necessary.

### Communication protocols

- We can use HTTP/1.1 to communicate between the client and the API servers and Search service since the communication follows a request-response pattern. Using HTTP/2.0 might be too complex, since the data we're dealing with doesn't require multiple channels or multiplexing.

### Data formats

- The communication between the client and API servers / Search service will use JSON, since it is suitable with REST, and is easy to debug with

<img width="550" alt="image" src="https://github.com/user-attachments/assets/bfb07a5b-170a-49f6-9081-53388d550d99" />





