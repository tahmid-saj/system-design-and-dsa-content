class Solution:
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        if len(nums) == 1: return 1
        # -3 0 1 2 3 -5 6 7 8 9 10 11
        # maxLength, currLength = 1, 1
        # loop through nums using i (1, len(nums)):
        # if nums[i] > nums[i - 1]: currLength += 1
        # else: currLength = 1
        # maxLength = max(currLength, maxLength)
        maxLength, currLength = 1, 1
        for i in range(1, len(nums)):
            if nums[i] > nums[i - 1]: currLength += 1
            else: currLength = 1
            maxLength = max(currLength, maxLength)

        return maxLength