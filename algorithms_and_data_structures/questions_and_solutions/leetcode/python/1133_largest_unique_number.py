class Solution:
    def largestUniqueNumber(self, nums: List[int]) -> int:
        freq = {}
        for i in range(len(nums)): freq[nums[i]] = freq.get(nums[i], 0) + 1

        res = -math.inf
        for i, v in freq.items():
            if v == 1: res = max(res, i)

        if res == -math.inf: return -1
        return res