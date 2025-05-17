class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        i = 0
        # loop through nums using j (1, len(nums)):
        # -> if nums[i] != val: i++
        # -> elif nums[i] == val and nums[j] != val: swap them, i++
        if len(nums) == 0: return 0
        if len(nums) == 1 and nums[0] == val: return 0
        if (len(nums) == 1): return 1

        for j in range(1, len(nums)):
            if nums[i] != val: i += 1
            elif nums[i] == val and nums[j] != val:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1

        if nums[i] != val: return i + 1
    
        return i