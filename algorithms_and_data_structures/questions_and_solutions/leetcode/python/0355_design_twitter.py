from collections import defaultdict, deque
from heapq import *
class Twitter:
    def __init__(self):
        self.followerMapping = defaultdict(set)
        # each userID is mapped to a queue that keeps track of the recency of the posts (userID: [(self.time, tweetId)]). The length of the queue won't exceed 10
        self.posts = {}
        self.time = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        if userId not in self.posts: self.posts[userId] = deque([(self.time, tweetId)])
        else:
            if len(self.posts[userId]) == 10: self.posts[userId].popleft()
            self.posts[userId].append((self.time, tweetId))
        self.time += 1

    def getNewsFeed(self, userId: int) -> List[int]:
        maxHeap = []

        if userId in self.posts:
            for i in range(len(self.posts[userId])): heappush(maxHeap, (-1 * self.posts[userId][i][0], self.posts[userId][i][1]))

        for followee in self.followerMapping[userId]:
            if followee in self.posts:
                for i in range(len(self.posts[followee])):
                    if len(maxHeap) == 10 and -maxHeap[0][0] > self.posts[followee][i][0]:
                        heappop(maxHeap)
                        heappush(maxHeap, (-1 * self.posts[followee][i][0], self.posts[followee][i][1]))
                    else: heappush(maxHeap, (-1 * self.posts[followee][i][0], self.posts[followee][i][1]))
        
        res = []
        while maxHeap:
            _, tweetId = heappop(maxHeap)
            res.append(tweetId)
        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        self.followerMapping[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId not in self.followerMapping[followerId]: return
        self.followerMapping[followerId].remove(followeeId)


# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)