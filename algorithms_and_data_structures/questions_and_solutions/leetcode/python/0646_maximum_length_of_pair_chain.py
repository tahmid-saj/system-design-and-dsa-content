class Solution:
    def findLongestChain(self, pairs: List[List[int]]) -> int:
        pairs.sort(key=lambda x: x[1])
        res, prev = 1, pairs[0][1]
        
        for i in range(1, len(pairs)):
            if pairs[i][0] > prev:
                res += 1
                prev = pairs[i][1]
        
        return res