class Solution:
    def gcd(self, x, y):
        if x == 0: return y
        elif y == 0: return x
        
        if x > y: return self.gcd(x % y, y)
        return self.gcd(x, y % x)