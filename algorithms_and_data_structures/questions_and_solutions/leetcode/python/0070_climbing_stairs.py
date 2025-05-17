class Solution:
    def climbStairs(self, n: int) -> int:
        dp = [1, 2]
        if n == 1: return dp[0]
        if n == 2: return dp[1]

        for i in range(3, n + 1):
            tmp = dp[1]
            dp[1] = dp[0] + dp[1]
            dp[0] = tmp

        return dp[1] 