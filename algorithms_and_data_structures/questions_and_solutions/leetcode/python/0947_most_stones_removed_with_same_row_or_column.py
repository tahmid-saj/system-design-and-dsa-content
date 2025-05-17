class DSU:
    def __init__(self, n):
        self.parent = {}
        self.size = {}
    
    def find(self, i):
        if self.parent[i] != i: self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        self.parent.setdefault(i, i)
        self.parent.setdefault(j, j)

        self.size.setdefault(i, 0)
        self.size.setdefault(j, 0)

        if self.size[i] < self.size[j]: self.parent[self.find(i)] = self.find(j)
        elif self.size[i] > self.size[j]: self.parent[self.find(j)] = self.find(i)
        else:
            self.parent[self.find(i)] = self.find(j)
            self.size[j] += 1

class Solution:
    def removeStones(self, stones: List[List[int]]) -> int:
        dsu = DSU(len(stones))
        offset = 100000

        for x, y in stones: dsu.union(x, y + 100000)
        
        sets = set()
        for i in dsu.parent: sets.add(dsu.find(i))
        
        return len(stones) - len(sets)