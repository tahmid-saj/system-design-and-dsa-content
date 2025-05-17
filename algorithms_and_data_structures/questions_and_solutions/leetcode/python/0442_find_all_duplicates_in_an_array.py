class Solution:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        duplicateNumbers = []
        i = 0
        while i < len(nums):
            j = nums[i] - 1
            if nums[j] != nums[i]: nums[i], nums[j] = nums[j], nums[i]
            else: i += 1
        
        for i in range(0, len(nums)):
            if nums[i] != i + 1: duplicateNumbers.append(nums[i])

        return duplicateNumbers