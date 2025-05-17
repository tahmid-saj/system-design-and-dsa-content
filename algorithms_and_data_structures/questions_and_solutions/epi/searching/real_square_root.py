import math
class Solution:
    def realSquareRoot(self, n):
        l, r = (1.0, n) if n > 1.0 else (n, 1.0)

        while not math.isclose(l, r):
            middle = l + (r - l) // 2
            res = middle * middle
            if res == n: return middle
            elif res < n: l = middle
            elif res > n: r = middle
        
        return l

