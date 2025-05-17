class DSUOptimized:
    def __init__(self, n):
        self.rank = {i:1 for i in range(1, n + 1)}
        self.parent = {i:i for i in range(1, n + 1)}
    
    def find(self, i):
        if self.parent[i] != i: self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        iRep = self.find(i)
        jRep = self.find(j)

        if iRep == jRep: return

        if self.rank[iRep] < self.rank[jRep]: self.parent[iRep] = jRep
        elif self.rank[iRep] > self.rank[jRep]: self.parent[jRep] = iRep
        else:
            self.parent[jRep] = iRep
            self.rank[iRep] += 1

class DSU:
    def __init__(self, n):
        self.parent = {i:i for i in range(1, n + 1)}
    
    def find(self, i):
        if self.parent[i] != i: return self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        iSet, jSet = self.find(i), self.find(j)

        if iSet == jSet: return
        self.parent[iSet] = jSet

class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        dsu = DSUOptimized(len(edges) + 1)
        # dsu = DSU(len(edges) + 1)
        res = None

        for u, v in edges:
            if dsu.find(u) != dsu.find(v): dsu.union(u, v)
            else: res = [u, v]
        
        return res