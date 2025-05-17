class Solution:
    def isArmstrong(self, n: int) -> bool:
        k = 0
        res, curr = 0, n
        while curr > 0:
            k += 1
            curr //= 10

        curr = n
        while curr > 0:
            res += (curr % 10) ** k
            curr //= 10
        
        return res == n