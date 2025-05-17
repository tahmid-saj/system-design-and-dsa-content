# Sorted sets

## What are they?

A sorted set is a data structure that combines the properties of sets (unique elements) and sorted sequences (ordered by a score). It is commonly used in Redis, where it is known as a ZSet.

Each element in a sorted set is associated with a score (a floating-point number), which determines its order in the set. The elements are stored in a way that allows fast retrieval, insertion, and ranking.

## How do they work?

- Each element has a unique key and a score.
- Sorting is based on scores (not insertion order).
- Efficient lookup by score range or rank is possible.
- Duplicate elements are not allowed, but an element's score can be updated.

## Operations and their time complexity

<img width="576" alt="image" src="https://github.com/user-attachments/assets/fd693965-943b-4ac4-ba61-2493dc119fbd" />

## Underlying storage in Redis

Redis Sorted Sets (ZSet) use a combination of two data structures:

- Hash Table (Dictionary):
  - Stores the mapping of members to scores.
  - Provides O(1) time complexity for looking up a member’s score.

- Skip List:
  - Maintains the sorted order of elements based on their scores.
  - Allows fast range queries (ZRANGEBYSCORE, ZRANK, etc.).
  - Provides O(log n) time complexity for insertions, deletions, and rank lookups.

The combination ensures both fast lookups (hash table) and efficient ordering (skip list).

## Use cases of sorted sets

- Leaderboards (e.g., ranking players in a game by score)
- Task scheduling (e.g., queueing jobs by priority)
- Expiration-based caching (e.g., storing items with decay)
- Rate limiting (e.g., tracking API requests over time)
- Time-series data storage (e.g., tracking user activity logs)

## Summary

- Sorted Sets maintain elements in a sorted order based on a score.
- Operations are efficient due to a combination of hash table + skip list.
- Useful for ranking, range queries, and priority-based retrieval.

## Important references / documentation

Redis sorted sets:
- https://redis.io/docs/latest/develop/data-types/sorted-sets/
- https://redis.io/glossary/redis-sorted-sets/


