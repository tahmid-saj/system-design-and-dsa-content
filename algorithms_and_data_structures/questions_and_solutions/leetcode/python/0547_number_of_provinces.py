class DSUOptimized:
    def __init__(self, n):
        self.rank = {i:1 for i in range(n)}
        self.parent = {i:i for i in range(n)}
        self.provinces = n
    
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
            self.parent[iRep] = jRep
            self.rank[jRep] += 1
        self.provinces -= 1

class DSU:
    def __init__(self, n):
        self.parent = {i:i for i in range(n)}
        self.provinces = n
    
    def find(self, i):
        if self.parent[i] != i: return self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        iSet, jSet = self.find(i), self.find(j)
        if iSet == jSet: return
        self.parent[iSet] = jSet
        self.provinces -= 1

class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        res = 0
        visited = set()

        for i in range(len(isConnected)):
            if i not in visited:
                res += 1
                # self.dfsRecursive(isConnected, visited, i)
                self.dfsIterative(isConnected, visited, i)
        
        return res

        # return self.unionFind(isConnected)

    def dfsIterative(self, isConnected, visited, i):
        visited.add(i)
        stk = [i]

        while stk:
            i = stk.pop()

            for j in range(len(isConnected[i])):
                if i != j and isConnected[i][j] == 1 and j not in visited: 
                    visited.add(j)
                    stk.append(j)
    
    def dfsRecursive(self, isConnected, visited, i):
        visited.add(i)

        for j in range(len(isConnected[i])):
            if i != j and isConnected[i][j] == 1 and j not in visited: self.dfsRecursive(isConnected, visited, j)

    def unionFind(self, isConnected):
        dsu = DSUOptimized(len(isConnected))
        # dsu = DSU(len(isConnected))
        res = 0

        for i in range(len(isConnected)):
            for j in range(len(isConnected[0])):
                if i != j and isConnected[i][j] == 1 and dsu.find(i) != dsu.find(j): dsu.union(i, j)
        
        return dsu.provinces