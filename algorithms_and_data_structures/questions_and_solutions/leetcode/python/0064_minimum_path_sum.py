class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        # DP 2D
        # DP 1D
        # DP constant space

        # dp = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
        # return self.dp2D(grid, dp)

        # dp = [0 for _ in range(len(grid[0]))]
        # return self.dp1D(grid, dp)

        return self.dp2DConstantSpace(grid)

    def dp2D(self, grid, dp):
        for i in range(len(grid)):
            if i > 0: dp[i][0] = dp[i - 1][0] + grid[i][0]
            else: dp[i][0] = grid[i][0]
        for j in range(1, len(grid[0])):
            dp[0][j] = dp[0][j - 1] + grid[0][j]
        
        for i in range(1, len(grid)):
            for j in range(1, len(grid[0])):
                dp[i][j] = grid[i][j]
                dp[i][j] += min(dp[i - 1][j], dp[i][j - 1])
        
        return dp[len(grid) - 1][len(grid[0]) - 1]
    
    def dp1D(self, grid, dp):
        for j in range(len(grid[0])):
            if j > 0: dp[j] = dp[j - 1] + grid[0][j]
            else: dp[j] = grid[0][j]
        
        for i in range(1, len(grid)):
            for j in range(len(grid[0])):
                if j > 0: dp[j] = min(dp[j - 1], dp[j])
                dp[j] += grid[i][j]
        
        return dp[-1]

    def dp2DConstantSpace(self, grid):
        for i in range(len(grid)):
            if i > 0: grid[i][0] += grid[i - 1][0]
        
        for j in range(1, len(grid[0])):
            grid[0][j] += grid[0][j - 1]
        
        for i in range(1, len(grid)):
            for j in range(1, len(grid[0])):
                grid[i][j] = grid[i][j] + min(grid[i - 1][j], grid[i][j - 1])
        
        return grid[-1][-1]