class Solution:
    def maxCount(self, m: int, n: int, ops: List[List[int]]) -> int:
        if len(ops) == 0: return m * n

        res, minA, minB = 0, 1e8, 1e8
        for i in range(0, len(ops)):
            minA = min(minA, ops[i][0])
            minB = min(minB, ops[i][1])
        
        return minA * minB