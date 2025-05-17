class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums.sort()
        # 1 1 2 2 4
        # 1 2 2
        # 1 1 2 3 3
        if len(nums) == 1: return nums[0]

        i, j, res = 0, 1, 0

        while j <= len(nums):
            if j == len(nums): return nums[-1]

            if nums[i] != nums[j]: return nums[i]

            i += 2
            j += 2

        return res