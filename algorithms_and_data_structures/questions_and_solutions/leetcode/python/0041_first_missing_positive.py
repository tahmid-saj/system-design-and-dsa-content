class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        i = 0
        while i < len(nums):
            j = nums[i] - 1
            if j < len(nums) and j >= 0 and nums[j] != nums[i]: nums[j], nums[i] = nums[i], nums[j]
            else: i += 1

        for i in range(0, len(nums)):
            if nums[i] != i + 1: return i + 1

        return len(nums) + 1