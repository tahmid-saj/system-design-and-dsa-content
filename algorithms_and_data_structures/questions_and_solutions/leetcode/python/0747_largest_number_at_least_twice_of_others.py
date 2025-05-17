class Solution:
    def dominantIndex(self, nums: List[int]) -> int:
        maxVal = max(nums)
        maxIndex = nums.index(maxVal)
        for num in nums:
            if num != maxVal and 2 * num > maxVal: return -1
        return maxIndex