class Solution:
    def towersOfHanoi(self, rings, pegs):
        self.pegRings = [[i for i in range(rings, 0, -1)]] + [[] for _ in range(1, pegs)]
        self.res = []
        def helper(rings, fromPeg, toPeg, usePeg):
            if rings > 0:
                helper(rings - 1, fromPeg, usePeg, toPeg)
                self.pegRings[toPeg].append(self.pegRings[fromPeg].pop())
                self.res.append((fromPeg, toPeg))
                helper(rings - 1, usePeg, toPeg, fromPeg)
        
        helper(rings, 0, 1, 2)
        return self.res

sol = Solution()
print(sol.towersOfHanoi(6, 3))