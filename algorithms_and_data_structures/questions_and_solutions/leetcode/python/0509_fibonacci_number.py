class Solution:
    def fib(self, n: int) -> int:
        self.fibMap = {}

        def helper(n):
            if n == 0: return 0
            if n == 1: return 1
            if n in self.fibMap.keys(): return self.fibMap[n]

            self.fibMap[n] = helper(n - 1) + helper(n - 2)
            return self.fibMap[n]

        return helper(n)