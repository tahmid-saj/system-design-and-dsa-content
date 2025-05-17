class Solution(object):
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        l, r, middle = 0, len(nums) - 1, 0

        while (l <= r):
            middle = l + (r - l) / 2

            if target < nums[middle]:
                r = middle - 1
            elif target > nums[middle]:
                l = middle + 1
            else:
                return middle
        
        return l