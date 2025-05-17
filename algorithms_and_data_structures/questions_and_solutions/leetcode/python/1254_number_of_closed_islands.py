class Solution:
    def closedIsland(self, grid: List[List[int]]) -> int:
        closedIslands = 0
        visited = [[False for j in range(len(grid[0]))] for i in range(len(grid))]

        for i in range(0, len(grid)):
            for j in range(0, len(grid[0])):
                if grid[i][j] == 0 and not visited[i][j]:
                    if self.dfs(grid, i, j, visited): closedIslands += 1
        
        return closedIslands
    
    def dfs(self, grid, i, j, visited):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]): return False
        if grid[i][j] == 1 or visited[i][j]: return True

        visited[i][j] = True

        closed = True
        closed &= self.dfs(grid, i - 1, j, visited)
        closed &= self.dfs(grid, i + 1, j, visited)
        closed &= self.dfs(grid, i, j - 1, visited)
        closed &= self.dfs(grid, i, j + 1, visited)

        return closed