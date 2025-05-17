class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # loop through nums using i (0, len(nums)) and j (1, len(nums)):
        # -> if nums[i + 1] != nums[j]: swap them, i++
        # -> if nums[i + 1] == nums[j]: continue
        # j++ regardless
        i = 0
        for j in range(1, len(nums)):
            if nums[i] != nums[j]:
                nums[i + 1], nums[j] = nums[j], nums[i + 1]
                i += 1
        return i + 1