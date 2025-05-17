class Solution:
    def trailingZeroes(self, n: int) -> int:
        # return self.findingFactorial(n)
        # return self.countingFactorsOf5(n)
        return self.logn(n)
    
    def findingFactorial(self, n):
        factorial, i = 1, n
        while i > 0:
            factorial *= i
            i -= 1
        
        res = 0
        while factorial > 0:
            if factorial % 10 != 0: break
            elif factorial % 10 == 0: res += 1
            factorial //= 10
        
        return res
    
    def countingFactorsOf5(self, n):
        res = 0
        for i in range(5, n + 1, 5):
            curr = i
            while curr % 5 == 0:
                res += 1
                curr //= 5
        
        return res
    
    def logn(self, n):
        res = 0
        while n > 0:
            n //= 5
            res += n
        
        return res