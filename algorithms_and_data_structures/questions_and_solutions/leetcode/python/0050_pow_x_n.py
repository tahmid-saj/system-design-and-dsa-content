class Solution:
    def myPow(self, x: float, n: int) -> float:
        # if n == 0: return 1
        # if n < 0: return self.helper(1 / x, -n)
        # return self.recursive(x, n)

        # return self.iterative(x, n)

        # return self.recursiveBinaryExponentiation(x, n)

        return self.iterativeBinaryExponentiation(x, n)

    def recursiveBruteForce(self, x, n):
        if n == 1: return x
        return x * self.helper(x, n - 1)
    
    def iterativeBruteForce(self, x, n):
        if n == 0: return 1
        if n < 0:
            x = 1 / x
            n = -n

        res = 1
        while n > 0:
            res *= x
            n -= 1
        
        return res

    def recursiveBinaryExponentiation(self, x, n):
        if n == 0: return 1

        if n < 0: return 1 / self.recursiveBinaryExponentiation(x, -n)

        if n % 2 != 0: return x * self.recursiveBinaryExponentiation(x * x, (n - 1) // 2)

        if n % 2 == 0: return self.recursiveBinaryExponentiation(x * x, n // 2)
    
    def iterativeBinaryExponentiation(self, x, n):
        if n == 0: return 1
        if n < 0:
            n = -n
            x = 1.0 / x

        res = 1
        while n > 0:
            if n % 2 != 0:
                res *= x
                n -= 1
            x *= x
            n //= 2

        return res