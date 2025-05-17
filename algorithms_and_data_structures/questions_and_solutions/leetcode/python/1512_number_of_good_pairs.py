class Solution:
    def numIdenticalPairs(self, nums: List[int]) -> int:
        pairCount = 0
        occurance = {}
        for i, x in enumerate(nums): occurance[x] = occurance.get(x, 0) + 1

        for k, v in occurance.items(): pairCount += (v * (v - 1)) // 2
        
        return pairCount