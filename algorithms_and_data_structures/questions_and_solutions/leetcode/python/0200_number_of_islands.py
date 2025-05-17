class DSU:
    def __init__(self, grid, rows, cols):
        self.parent = []
        self.size = []
        self.count = 0
        for i in range(rows):
            for j in range(cols):
                self.size.append(1)
                if grid[i][j] == '1':
                    self.count += 1
                    self.parent.append(i * cols + j)
                else:
                    self.parent.append(-1)
    
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
    def numIslands(self, grid: List[List[str]]) -> int:
        # return self.dfsBfs(grid)
        return self.unionFind(grid)
    
    def unionFind(self, grid):
        dsu = DSU(grid, len(grid), len(grid[0]))
        # loop through grid using i:
        # loop through grid[i] using j:
        #   if grid[i][j] == 1:
        #       grid[i][j] = 0
        #       union i - 1, i + 1, j - 1, j + 1 from (i, j) if they are == 1
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '1':
                    grid[i][j] = '0'

                    if i - 1 >= 0 and grid[i - 1][j] == '1': dsu.union(i * len(grid[0]) + j, (i - 1) * len(grid[0]) + j)
                    if i + 1 < len(grid) and grid[i + 1][j] == '1': dsu.union(i * len(grid[0]) + j, (i + 1) * len(grid[0]) + j)
                    if j - 1 >= 0 and grid[i][j - 1] == '1': dsu.union(i * len(grid[0]) + j, i * len(grid[0]) + (j - 1))
                    if j + 1 < len(grid[0]) and grid[i][j + 1] == '1': dsu.union(i * len(grid[0]) + j, i * len(grid[0]) + (j + 1))
        
        return dsu.count

    def dfsBfs(self, grid):
        res = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "1":
                    res += 1
                    self.bfs(grid, i, j)
        
        return res
    
    def dfs(self, grid, i, j):
        if grid[i][j] == "0": return
        grid[i][j] = "0"

        if i > 0: self.dfs(grid, i - 1, j)
        if i < len(grid) - 1: self.dfs(grid, i + 1, j)
        if j > 0: self.dfs(grid, i, j - 1)
        if j < len(grid[0]) - 1: self.dfs(grid, i, j + 1)
    
    def bfs(self, grid, i, j):
        queue = deque([(i, j)])
        while queue:
            i, j = queue.popleft()
            if grid[i][j] == "0": continue
            grid[i][j] = "0"

            if i > 0: queue.append((i - 1, j))
            if i < len(grid) - 1: queue.append((i + 1, j))
            if j > 0: queue.append((i, j - 1))
            if j < len(grid[0]) - 1: queue.append((i, j + 1))