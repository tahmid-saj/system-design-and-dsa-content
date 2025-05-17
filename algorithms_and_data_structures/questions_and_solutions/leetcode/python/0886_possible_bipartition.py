class DSU:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.size = [0 for i in range(n)]
    
    def find(self, i):
        if self.parent[i] != i: self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        iSet, jSet = self.find(i), self.find(j)
        if iSet == jSet: return

        if self.size[iSet] < self.size[jSet]: self.parent[iSet] = jSet
        elif self.size[iSet] > self.size[iSet]: self.parent[jSet] = iSet
        else:
            self.size[jSet] += 1
            self.parent[iSet] = jSet

class Solution:
    def possibleBipartition(self, n: int, dislikes: List[List[int]]) -> bool:
        adjList = [[] for _ in range(n + 1)]
        for u, v in dislikes: 
            adjList[u].append(v)
            adjList[v].append(u)

        dsu = DSU(n + 1)

        for i in range(1, n + 1):
            if len(adjList[i]) > 0:
                parent = dsu.find(i)
                firstNeighbour = adjList[i][0]
                for neighbour in adjList[i]:
                    if parent == dsu.find(neighbour): return False
                    dsu.union(firstNeighbour, neighbour)
        
        return True