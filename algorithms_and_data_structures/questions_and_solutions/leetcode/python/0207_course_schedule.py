from collections import defaultdict, deque
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        return self.bfs(numCourses, prerequisites)

    def bfs(self, numCourses, prerequisites):
        if len(prerequisites) == 0: return True
        adjList = {i: [] for i in range(numCourses)}
        inDegrees = defaultdict(int)

        for u, v in prerequisites:
            adjList[v].append(u)
        
        for i in range(numCourses):
            for neighbor in adjList[i]: inDegrees[neighbor] += 1

        queue = deque()
        for node in adjList:
            if node not in inDegrees or inDegrees[node] == 0: queue.append(node)
        
        count = 0
        while queue:
            node = queue.popleft()
            count += 1

            for neighbor in adjList[node]:
                inDegrees[neighbor] -= 1
                if inDegrees[neighbor] == 0: queue.append(neighbor)
        
        return count == numCourses