class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # return self.recursive(m, n)

        # dp = [[0 for _ in range(n)] for _ in range(m)]
        # return self.bottomUpDP(m, n, dp)

        return self.binomialCoefficients(m, n)

    def recursive(self, m, n):
        if m == 1 or n == 1: return 1

        return self.recursive(m - 1, n) + self.recursive(m, n - 1)
    
    def bottomUpDP(self, m, n, dp):
        if m == 1 or n == 1: return 1
        
        for i in range(n): dp[0][i] = 1
        for i in range(m): dp[i][0] = 1

        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        
        return dp[m - 1][n - 1]
    
    def binomialCoefficients(self, m, n):
        return factorial(m + n - 2) // (factorial(m - 1) * factorial(n - 1))