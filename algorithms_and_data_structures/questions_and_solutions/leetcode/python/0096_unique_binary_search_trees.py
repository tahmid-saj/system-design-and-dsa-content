class Solution:
    def numTrees(self, n: int) -> int:
        # return self.bottomUp(n)
        return self.math(n)
    
    def bottomUp(self, n):
        dp = [0 for _ in range(n + 1)]
        dp[0], dp[1] = 1, 1

        for numberOfNodes in range(2, n + 1):
            for i in range(1, numberOfNodes + 1):
                dp[numberOfNodes] += dp[i - 1] * dp[numberOfNodes - i]
        
        return dp[n]
    
    def math(self, n):
        C = 1
        for i in range(0, n):
            C = C * 2*(2*i+1)/(i+2)
        return int(C)