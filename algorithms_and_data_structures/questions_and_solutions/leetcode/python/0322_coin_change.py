class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # base case: if s == 0: return 0
        # 1. s - coins[index] and move to the same index: change1 = 1, change1 += self.recursive()
        # 2. s - coins[index] and move to the next index: change2 = 1, change2 += self.recursive()
        # 3. dont subtract coins[index] and move to the next index: change3 = 0, change3 += self.recursive()

        # res = self.recursive(coins, amount, 0)
        # if res == math.inf: return -1
        # return res

        # self.coins = coins
        # return self.recursive2(amount)

        # dp = [[math.inf for s in range(amount + 1)] for i in range(len(coins))]
        # res = self.topDown(coins, amount, 0, dp)
        # if res == math.inf: return -1
        # return res

        # dp = [[math.inf for s in range(amount + 1)] for i in range(len(coins))]
        # res = self.bottomUp(coins, amount, dp)
        # if res == math.inf: return -1
        # return res

        # dp = [math.inf for s in range(amount + 1)]
        # res = self.bottomUpLinearSpace(coins, amount, dp)
        # if res == math.inf: return -1
        # return res

        dp = [math.inf for s in range(amount + 1)]
        res = self.bottomUpLinearSpace2(coins, amount, dp)
        if res == math.inf: return -1
        return res

    def recursive(self, coins, s, index):
        if s == 0: return 0
        if index >= len(coins): return 0

        change1, change2, change3 = math.inf, math.inf, math.inf
        if s - coins[index] >= 0: change1 = 1 + self.recursive(coins, s - coins[index], index)
        if s - coins[index] >= 0 and index + 1 <= len(coins) - 1: change2 = 1 + self.recursive(coins, s - coins[index], index + 1)
        if index + 1 <= len(coins) - 1: change3 = self.recursive(coins, s, index + 1)
        
        return min(change1, change2, change3)
    
    @lru_cache(None)
    def recursive2(self,  s):
        if s < 0: return -1
        if s == 0: return 0

        minCost = math.inf
        for coin in self.coins:
            res = self.recursive2(s - coin)
            if res != -1: minCost = min(minCost, res + 1)
        
        if minCost == math.inf: return -1
        return minCost 
    
    def topDown(self, coins, s, index, dp):
        if s == 0: return 0
        if index >= len(coins): return 0

        change1, change2, change3 = math.inf, math.inf, math.inf
        if s - coins[index] >= 0:
            if dp[index][s] == math.inf: change1 = 1 + self.topDown(coins, s - coins[index], index, dp)
            dp[index][s] = min(dp[index][s], change1)

        if s - coins[index] >= 0 and index + 1 <= len(coins) - 1:
            if dp[index][s] == math.inf: change2 = 1 + self.topDown(coins, s - coins[index], index + 1, dp)
            dp[index][s] = min(dp[index][s], change2)

        if index + 1 <= len(coins) - 1: change3 = self.topDown(coins, s, index + 1, dp)
        dp[index][s] = min(dp[index][s], change3)

        return dp[index][s]
    
    def bottomUp(self, coins, amount, dp):
        if amount == 0: return 0

        for i in range(0, len(coins)): dp[i][0] = 0
        for j in range(1, amount + 1):
            if j % coins[0] == 0:
                dp[0][j] = j // coins[0]
        
        for i in range(1, len(coins)):
            for s in range(1, amount + 1):
                change1, change2, change3 = math.inf, math.inf, math.inf
                if s - coins[i] >= 0: 
                    change1 = 1 + dp[i][s - coins[i]]
                    change2 = 1 + dp[i - 1][s - coins[i]]
                change3 = dp[i - 1][s]

                dp[i][s] = min(change1, change2, change3)
        
        return dp[len(coins) - 1][amount]
    
    def bottomUpLinearSpace(self, coins, amount, dp):
        if amount == 0: return 0

        dp[0] = 0
        for j in range(1, amount + 1):
            if j % coins[0] == 0:
                dp[j] = j // coins[0]
        
        for i in range(1, len(coins)):
            for s in range(1, amount + 1):
                change1, change2 = math.inf, math.inf
                if s - coins[i] >= 0: change1 = 1 + dp[s - coins[i]]
                change2 = dp[s]

                dp[s] = min(change1, change2)
        
        return dp[amount]
    
    def bottomUpLinearSpace2(self, coins, amount, dp):
        if amount == 0: return 0

        dp[0] = 0
        
        for i in range(1, amount + 1):
            if i % coins[0] == 0:
                dp[i] = i // coins[0]
        
        for coin in coins:
            for s in range(coin, amount + 1):
                dp[s] = min(dp[s], dp[s - coin] + 1)
        
        return dp[amount]