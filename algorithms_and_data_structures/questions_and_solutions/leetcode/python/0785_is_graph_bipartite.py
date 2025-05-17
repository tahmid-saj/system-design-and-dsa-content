class DSUOptimized:
    def __init__(self, n):
        self.rank = {i:1 for i in range(n)}
        self.parent = {i:i for i in range(n)}
    
    def find(self, i):
        if self.parent[i] != i: self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        iSet, jSet = self.find(i), self.find(j)
        if iSet == jSet: return

        if self.rank[iSet] < self.rank[jSet]: self.parent[iSet] = jSet
        elif self.rank[iSet] > self.rank[jSet]: self.parent[jSet] = iSet
        else:
            self.parent[iSet] = jSet
            self.rank[jSet] += 1

class DSU:
    def __init__(self, n):
        self.parent = {i:i for i in range(n)}
    
    def find(self, i):
        if self.parent[i] != i: return self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        iSet, jSet = self.find(i), self.find(j)
        if iSet == jSet: return
        self.parent[iSet] = jSet

class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        dsu = DSUOptimized(len(graph))
        # dsu = DSU(len(graph))

        for i in range(len(graph)):
            if len(graph[i]) > 0:
                parent = dsu.find(i)
                firstNeighbor = dsu.find(graph[i][0])
                for j in range(1, len(graph[i])):
                    if dsu.find(graph[i][j]) == parent: return False
                    dsu.union(firstNeighbor, dsu.find(graph[i][j]))
        
        return True