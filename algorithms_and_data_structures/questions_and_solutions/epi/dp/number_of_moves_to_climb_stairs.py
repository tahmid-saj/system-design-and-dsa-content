from functools import lru_cache
class Solution:
    def numberOfMovesToClimbStairs(self, n, k):
        return self.topDown(n, k, 0)
    
    @lru_cache(None)
    def topDown(self, n, k, stair):
        if stair == n: return 1
        if stair > n: return 0
        res = 0
        for i in range(1, min(k, n - stair) + 1):
            if stair + i <= n: res += self.topDown(n, k, stair + i)
        return res