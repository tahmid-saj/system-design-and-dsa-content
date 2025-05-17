from collections import deque
class Solution:
    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        res, sortedOrder = 0, []
        if n <= 0: return sortedOrder

        inEdges = {i + 1: 0 for i in range(n)}
        adjList = {i + 1: [] for i in range(n)}

        for u, v in relations:
            inEdges[v] += 1
            adjList[u].append(v)
        
        sources = deque()
        for v in adjList:
            if inEdges[v] == 0: sources.append(v)
        
        while sources:
            res += 1
            sourcesLength = len(sources)
            for i in range(sourcesLength):
                v = sources.popleft()
                sortedOrder.append(v)
                for child in adjList[v]:
                    inEdges[child] -= 1
                    if inEdges[child] == 0: sources.append(child)
        
        if len(sortedOrder) != n: return -1
        return res