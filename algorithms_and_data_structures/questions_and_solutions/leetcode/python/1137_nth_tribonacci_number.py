class Solution:
    def tribonacci(self, n: int) -> int:
        first, second, third = 0, 1, 1
        if n == 0: return first
        if n == 1: return second
        if n == 2: return third
        
        for i in range(3, n + 1):
            tmp = first + second + third
            first = second
            second = third
            third = tmp
        return third