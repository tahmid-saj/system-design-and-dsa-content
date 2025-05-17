class Solution:
    def binarySearch(self, nums):
        l, r = 0, len(nums) - 1

        while l <= r:
            middle = l + (r - l) // 2
            if middle == nums[middle]: return middle
            elif middle < nums[middle]: r = middle - 1
            else: l = middle + 1
        
        return -1