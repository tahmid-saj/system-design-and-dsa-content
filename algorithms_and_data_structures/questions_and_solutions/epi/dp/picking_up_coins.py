from functools import lru_cache
class Solution:
    def pickingUpCoins(self, coins):
        return self.topDown(coins, 0, len(coins) - 1)
    
    @lru_cache(None)
    def topDown(self, coins, i, j):
        if i > j: return 0
        comb1 = coins[i] + min(self.topDown(coins, i + 1, j - 1), self.topDown(coins, i + 2, j))
        comb2 = coins[j] + min(self.topDown(coins, i + 1, j - 1), self.topDown(coins, i, j - 2))
        return max(comb1, comb2)