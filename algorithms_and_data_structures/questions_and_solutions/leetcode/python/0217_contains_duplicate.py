class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        nums.sort()
        # 1 1 2 3
        if len(nums) == 1: return False
        # loop through using i (0, len(nums) - 1) and j (1, len(nums) - 1):
        # if nums[i] == nums[j]: return True
        # return False
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]: return True
        
        return False