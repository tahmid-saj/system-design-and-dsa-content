# The knows API is already defined for you.
# return a bool, whether a knows b
# def knows(a: int, b: int) -> bool:

class Solution:
    def findCelebrity(self, n: int) -> int:
        # return self.bruteForce(n)
        return self.cachedLogicalDeducing(n)
    
    @lru_cache(maxsize=None)
    def cachedLogicalDeducing(self, n):
        return self.logicalDeducing(n)
    
    def bruteForce(self, n):
        for i in range(n):
            if self.isCelebrity(n, i): return i
        return -1
    
    def isCelebrity(self, n, i):
        for j in range(n):
            if i == j: continue
            if knows(i, j) or not knows(j, i): return False
        return True
    
    def logicalDeducing(self, n):
        candidate = 0
        for i in range(1, n):
            if knows(candidate, i): candidate = i
        if self.isCelebrity(n, candidate): return candidate
        return -1