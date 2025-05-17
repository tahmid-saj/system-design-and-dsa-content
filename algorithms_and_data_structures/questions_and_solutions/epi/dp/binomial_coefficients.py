from functools import lru_cache
class Solution:
    @lru_cache(None)
    def binomialCoefficients2(self, k, n):
        if k == 0 or k == n: return 1

        withK = self.binomialCoefficients2(k, n - 1)
        withoutK = self.binomialCoefficients2(k - 1, n - 1)
        return withK + withoutK