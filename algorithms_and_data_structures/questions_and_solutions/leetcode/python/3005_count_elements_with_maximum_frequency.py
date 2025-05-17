class Solution:
    def maxFrequencyElements(self, nums: List[int]) -> int:
        freq = {}
        for i in range(len(nums)): freq[nums[i]] = freq.get(nums[i], 0) + 1
        maxFreq = max(freq.values())
        res = 0
        for v in freq.values():
            if v == maxFreq: res += v
        return res