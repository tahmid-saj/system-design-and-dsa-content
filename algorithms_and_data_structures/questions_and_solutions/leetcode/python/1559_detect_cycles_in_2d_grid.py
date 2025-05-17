class Solution:
    def containsCycle(self, grid: List[List[str]]) -> bool:
        visited = [[False for j in range(len(grid[0]))] for i in range(len(grid))]

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if not visited[i][j]:
                    if self.dfs(grid, i, j, visited, grid[i][j], i, j, -1, -1): return True
        
        return False
    
    def dfs(self, grid, i, j, visited, letter, originI, originJ, prevI, prevJ):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]): return False
        if grid[i][j] != letter: return False
        if visited[i][j]: return True

        visited[i][j] = True

        if (i + 1 != prevI) and self.dfs(grid, i + 1, j, visited, letter, originI, originJ, i, j): return True
        elif (i - 1 != prevI) and self.dfs(grid, i - 1, j, visited, letter, originI, originJ, i, j): return True
        elif (j + 1 != prevJ) and self.dfs(grid, i, j + 1, visited, letter, originI, originJ, i, j): return True
        elif (j - 1 != prevJ) and self.dfs(grid, i, j - 1, visited, letter, originI, originJ, i, j): return True

        return False