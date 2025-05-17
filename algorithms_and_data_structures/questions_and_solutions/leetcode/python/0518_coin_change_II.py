class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        if amount == 0: return 1

        # return self.recursive(amount, coins, 0, amount)

        # dp = [[-1 for j in range(amount + 1)] for i in range(len(coins))]
        # return self.topDown(amount, coins, 0, amount, dp)

        # return self.bottomUp(amount, coins)

        return self.bottomUpLinearSpace(amount, coins)

    def recursive(self, amount, coins, index, curr):
        if curr == 0: return 1
        if curr < 0 or index >= len(coins): return 0

        if coins[index] > amount:
            return self.recursive(amount, coins, index + 1, curr)
        else:
            return self.recursive(amount, coins, index, curr - coins[index]) + self.recursive(amount, coins, index + 1, curr)

    def topDown(self, amount, coins, index, curr, dp):
        if curr == 0: return 1
        if curr < 0 or index >= len(coins): return 0

        if dp[index][curr] != -1: return dp[index][curr]

        if coins[index] > curr: dp[index][curr] = self.topDown(amount, coins, index + 1, curr, dp)
        else: dp[index][curr] = self.topDown(amount, coins, index, curr - coins[index], dp) + self.topDown(amount, coins, index + 1, curr, dp)

        return dp[index][curr]
    
    def bottomUp(self, amount, coins):
        dp = [[0 for j in range(amount + 1)] for i in range(len(coins))]

        for i in range(len(coins)): dp[i][0] = 1
        for j in range(1, amount + 1):
            if j % coins[0] == 0: dp[0][j] = 1
        
        for i in range(1, len(coins)):
            for j in range(1, amount + 1):
                if coins[i] > j: dp[i][j] = dp[i - 1][j]
                else: dp[i][j] = dp[i - 1][j] + dp[i][j - coins[i]]
        
        return dp[len(coins) - 1][amount]
    
    def bottomUpLinearSpace(self, amount, coins):
        dp = [0 for j in range(amount + 1)]

        for j in range(amount + 1):
            if j % coins[0] == 0: dp[j] = 1
        
        for i in range(1, len(coins)):
            print(dp)   
            for j in range(1, amount + 1):
                if coins[i] > j: continue
                else: dp[j] = dp[j] + dp[j - coins[i]]
        
        
        return dp[amount]