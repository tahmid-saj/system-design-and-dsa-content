from functools import lru_cache
class Solution:
    def knapsackProblem(self, items, capacity):
        return self.topDown(self, items, capacity, 0, 0)
    
    @lru_cache(None)
    def topDown(self, items, capacity, i, c):
        if i == len(items): return 0
        if c >= capacity: return 0
        comb1, comb2 = 0, 0
        if c + items[i][0] <= capacity and i + 1 <= len(items): comb1 = items[i][1] + self.topDown(items, capacity, i + 1, c + items[i][0])
        if i + 1 <= len(items): comb2 = self.topDown(items, capacity, i + 1, c)
        return max(comb1, comb2)