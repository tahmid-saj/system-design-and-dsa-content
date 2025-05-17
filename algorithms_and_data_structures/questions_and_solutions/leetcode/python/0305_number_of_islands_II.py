class DSU:
    def __init__(self, positions, rows, cols):
        self.parent = []
        self.size = []
        self.count = len(positions)
        for i in range(rows):
            for j in range(cols):
                self.parent.append(i * cols + j)
                self.size.append(0)
    
    def find(self, i):
        if self.parent[i] != i: self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        iSet, jSet = self.find(i), self.find(j)
        if iSet == jSet: return

        self.count -= 1
        if self.size[iSet] < self.size[jSet]: self.parent[iSet] = jSet
        elif self.size[iSet] > self.size[jSet]: self.parent[jSet] = iSet
        else:
            self.size[jSet] += 1
            self.parent[iSet] = jSet

class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        grid, res = set(), []
        dsu = DSU(positions, m, n)
        land = 1
        
        for i, j in positions:
            if (i, j) not in grid: 
                grid.add((i, j))
                if i - 1 >= 0 and (i - 1, j) in grid: dsu.union(i * n + j, (i - 1) * n + j)
                if i + 1 < m and (i + 1, j) in grid: dsu.union(i * n + j, (i + 1) * n + j)
                if j - 1 >= 0 and (i, j - 1) in grid: dsu.union(i * n + j, i * n + (j - 1))
                if j + 1 < n and (i, j + 1) in grid: dsu.union(i * n + j, i * n + (j + 1))
                res.append(land - (len(positions) - dsu.count))
                land += 1
            else: res.append(res[-1])
        
        return res
