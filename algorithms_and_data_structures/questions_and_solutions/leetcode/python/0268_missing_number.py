class Solution(object):
    def missingNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums.sort()
        # 0 1 2 3 4 5 6 7 9
        # 1 2 3
        # 0 1 2
        # 0 1 3
        if nums[0] != 0: return 0
        if nums[-1] != len(nums): return len(nums)

        res = 0
        for i in range(1, len(nums)):
            if nums[i] - nums[i - 1] > 1:
                res = nums[i] - 1

        return res