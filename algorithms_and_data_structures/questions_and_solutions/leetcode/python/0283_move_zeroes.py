class Solution(object):
    def moveZeroes(self, nums):
        """
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        if len(nums) == 0: return nums
        # 0 1 0 3 12
        # 1 0 0 3 12 -> 1 3 0 0 12 -> 1 3 12 0 0
        i = 0
        for j in range(1, len(nums)):
            if nums[i] == 0 and nums[j] != 0:
                nums[i], nums[j] = nums[j], nums[i]
            if nums[i] != 0: i += 1

        return nums