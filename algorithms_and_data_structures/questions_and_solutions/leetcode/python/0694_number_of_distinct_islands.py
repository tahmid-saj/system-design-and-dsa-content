class Solution:
    def numDistinctIslands(self, grid: List[List[int]]) -> int:
        distinctIslands = set()
        visited = [[False for j in range(len(grid[0]))] for i in range(len(grid))]

        for i in range(0, len(grid)):
            for j in range(0, len(grid[0])):
                if grid[i][j] == 1 and not visited[i][j]:
                    distinctIslands.add(self.dfs(grid, i, j, visited, "O"))
                    print(distinctIslands)
        
        return len(distinctIslands)
    
    def dfs(self, grid, i, j, visited, direction):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]): return ""
        if grid[i][j] == 0 or visited[i][j]: return ""

        visited[i][j] = True
        
        path = direction
        path += self.dfs(grid, i - 1, j, visited, "U")
        path += self.dfs(grid, i + 1, j, visited, "D")
        path += self.dfs(grid, i, j - 1, visited, "L")
        path += self.dfs(grid, i, j + 1, visited, "R")
        path += "B" # back

        return path