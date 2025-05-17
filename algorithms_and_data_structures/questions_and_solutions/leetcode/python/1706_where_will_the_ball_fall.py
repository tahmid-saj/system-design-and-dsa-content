class Solution:
    def findBall(self, grid: List[List[int]]) -> List[int]:
        res = [None for _ in range(len(grid[0]))]

        for j in range(len(res)): 
            self.col = None
            res[j] = self.dfs(grid, 0, j)
            if self.col != None: res[j] = self.col
        return res
    
    def dfs(self, grid, i, j):
        if i == len(grid): 
            self.col = j
            return j
        if j < 0 or j >= len(grid[0]): return -1
        if grid[i][j] == 1 and (j == len(grid[0]) - 1 or grid[i][j + 1] == -1): return -1
        if grid[i][j] == -1 and (j == 0 or grid[i][j - 1] == 1): return -1

        if grid[i][j] == 1 and self.dfs(grid, i + 1, j + 1) == -1: return -1
        if grid[i][j] == -1 and self.dfs(grid, i + 1, j - 1) == -1: return -1