class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        maxArea = 0

        for i in range(0, len(grid)):
            for j in range(0, len(grid[0])):
                if grid[i][j] == 1: maxArea = max(maxArea, self.dfs(grid, i, j))
        
        return maxArea

    def dfs(self, grid, i, j):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]): return 0
        if grid[i][j] == 0: return 0

        area = 1
        grid[i][j] = 0

        area += self.dfs(grid, i - 1, j)
        area += self.dfs(grid, i + 1, j)
        area += self.dfs(grid, i, j - 1)
        area += self.dfs(grid, i, j + 1)

        return area