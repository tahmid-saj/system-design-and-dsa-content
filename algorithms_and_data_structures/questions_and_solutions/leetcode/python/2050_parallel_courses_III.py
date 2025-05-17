from collections import deque
class Solution:
    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        if n <= 0: return 0

        inEdges = [0 for _ in range(n)]
        adjList = defaultdict(list)

        for u, v in relations:
            inEdges[v - 1] += 1
            adjList[u - 1].append(v - 1)
        
        sources, maxTime = deque(), [0 for _ in range(n)]
        for v in range(n):
            if inEdges[v] == 0: 
                sources.append(v)
                maxTime[v] = time[v]

        while sources:
            v = sources.popleft()
            for child in adjList[v]:
                maxTime[child] = max(maxTime[child], maxTime[v] + time[child])
                inEdges[child] -= 1
                if inEdges[child] == 0: sources.append(child)
        
        return max(maxTime)