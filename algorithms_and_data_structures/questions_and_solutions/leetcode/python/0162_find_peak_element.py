class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        # return self.iterative(nums)
        return self.recursive(nums, 0, len(nums) - 1)

    def iterative(self, nums):
        if len(nums) == 1: return 0
        l, r = 0, len(nums) - 1

        while l < r:
            middle = l + (r - l) // 2

            if middle > 0 and middle < len(nums) - 1 and nums[middle - 1] < nums[middle] > nums[middle + 1]: return middle
            elif middle == 0 and middle < len(nums) - 1 and nums[middle] > nums[middle + 1]: return middle
            elif middle == len(nums) - 1 and middle  > 0 and nums[middle] > nums[middle - 1]: return middle

            if nums[middle] < nums[middle + 1]: l = middle + 1
            else: r = middle

        return l

    def recursive(self, nums, l, r):
        if r <= l: return l

        middle = l + (r - l) // 2
        
        if middle > 0 and middle < len(nums) - 1 and nums[middle] > nums[middle - 1] and nums[middle] > nums[middle + 1]: return middle
        elif middle == 0 and middle < len(nums) - 1 and nums[middle] > nums[middle + 1]: return middle
        elif middle == len(nums) - 1 and middle  > 0 and nums[middle] > nums[middle - 1]: return middle

        if nums[middle] < nums[middle + 1]: return self.recursive(nums, middle + 1, r)
        else: return self.recursive(nums, l, middle)