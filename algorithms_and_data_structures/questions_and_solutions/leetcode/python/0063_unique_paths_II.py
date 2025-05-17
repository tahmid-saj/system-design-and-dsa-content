class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        dp = [[0 for _ in range(len(obstacleGrid[0]))] for _ in range(len(obstacleGrid))]
        # return self.bottomUpDP(obstacleGrid, dp)
        
        # return self.bottomUpDPLinearSpace(obstacleGrid)
        return self.bottomUpDPConstantSpace(obstacleGrid)
    
    def bottomUpDP(self, grid, dp):
        for i in range(len(grid)): 
            if grid[i][0] != 1: dp[i][0] = 1
            else: break
        
        for j in range(len(grid[0])):
            if grid[0][j] != 1: dp[0][j] = 1
            else: break
        
        for i in range(1, len(grid)):
            for j in range(1, len(grid[0])):
                if grid[i][j] != 1: dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
                else: dp[i][j] = 0
        
        return dp[len(grid) - 1][len(grid[0]) - 1]
    
    def bottomUpDPLinearSpace(self, grid):
        prev = [0 for _ in range(len(grid[0]))]

        for j in range(len(grid[0])):
            if grid[0][j] != 1: prev[j] = 1
            else: break
        
        obstacle = False
        for i in range(1, len(grid)):
            curr = [0 for _ in range(len(grid[0]))]
            if grid[i][0] == 1 or prev[0] == 0: obstacle = True
            if not obstacle: curr[0] = 1
            for j in range(1, len(grid[0])):
                if grid[i][j] != 1: curr[j] = prev[j] + curr[j - 1]
                else: curr[j] = 0
            prev = curr

        return prev[len(grid[0]) - 1]

    def bottomUpDPConstantSpace(self, obstacleGrid):
        obstacle = False
        for i in range(len(obstacleGrid)):
            if obstacleGrid[i][0] == 1 or obstacle:
                obstacleGrid[i][0] = 0
                obstacle = True
            else: obstacleGrid[i][0] = 1
        
        obstacle = True if obstacleGrid[0][0] == 0 else False
        for i in range(1, len(obstacleGrid[0])):
            if obstacleGrid[0][i] == 1 or obstacle:
                obstacleGrid[0][i] = 0
                obstacle = True
            else: obstacleGrid[0][i] = 1
        
        for i in range(1, len(obstacleGrid)):
            for j in range(1, len(obstacleGrid[0])):
                if obstacleGrid[i][j] == 1:
                    obstacleGrid[i][j] = 0
                    continue
                obstacleGrid[i][j] = obstacleGrid[i - 1][j] + obstacleGrid[i][j - 1]
        
        return obstacleGrid[len(obstacleGrid) - 1][len(obstacleGrid[0]) - 1]