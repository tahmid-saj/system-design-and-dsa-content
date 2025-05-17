class Solution:
    def tripleStep(self, n):
        dp = [1, 2, 4]
        
        for i in range(4, n + 1):
            print(dp[2])
            tmp3, tmp2 = dp[2], dp[1]
            dp[2] += dp[0] + dp[1]
            dp[0] = tmp2
            dp[1] = tmp3
        
        return dp[2]

sol = Solution()
print(sol.tripleStep(5))