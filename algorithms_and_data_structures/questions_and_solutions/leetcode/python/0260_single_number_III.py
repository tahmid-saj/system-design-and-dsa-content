class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:
        freq = {}
        for i in range(len(nums)): freq[nums[i]] = freq.get(nums[i], 0) + 1

        res = []
        for k, v in freq.items():
            if v == 1: res.append(k)
        
        return res