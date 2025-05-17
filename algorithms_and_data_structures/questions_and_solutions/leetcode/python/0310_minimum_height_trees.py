from collections import defaultdict, deque
class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n == 1 and len(edges) == 0: return [0]

        adjList = defaultdict(list)
        inDegree = defaultdict(int)

        for u, v in edges:
            adjList[u].append(v)
            adjList[v].append(u)
            inDegree[v] += 1
            inDegree[u] += 1
        
        leaves = deque()
        for i in range(n):
            # if the neighbor has an inDegree of 1, then its a leaf
            if inDegree[i] == 1: leaves.append(i)
        
        # We can only have 2 centroids, so we remove leaves up until we get to the possible 2 centroids
        while n > 2:
            leavesLength = len(leaves)
            n -= leavesLength
            for _ in range(leavesLength):
                node = leaves.popleft()
                for neighbor in adjList[node]:
                    inDegree[neighbor] -= 1
                    # if the neighbor has an inDegree of 1, then its a leaf
                    if inDegree[neighbor] == 1: leaves.append(neighbor)

        return list(leaves)