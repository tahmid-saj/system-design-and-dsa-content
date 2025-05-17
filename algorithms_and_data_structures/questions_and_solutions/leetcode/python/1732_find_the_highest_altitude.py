class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        prefix, res = 0, 0
        for i in range(len(gain)): 
            g = prefix + gain[i]
            prefix += gain[i]
            res = max(res, g)
        return res