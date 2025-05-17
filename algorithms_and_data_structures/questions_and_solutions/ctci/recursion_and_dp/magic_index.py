class Solution:
    def magicIndex(self, nums):
        # return self.distinct(nums)
        return self.notDistinct(nums, 0, len(nums) - 1)

    def distinct(self, nums):
        l, r = 0, len(nums) - 1

        while l <= r:
            middle = l + (r - l) // 2
            if nums[middle] == middle: return middle
            if nums[middle] < middle: l = middle + 1
            else: r = middle - 1
        
        return -1
    
    def notDistinct(self, nums, l, r):
        if r < l: return -1
        middle = l + (r - l) // 2
        if nums[middle] == middle: return middle
        
        leftIndex = min(nums[middle], middle - 1)
        left = self.notDistinct(nums, l, leftIndex)
        if left >= 0: return left

        rightIndex = max(middle + 1, nums[middle])
        right = self.notDistinct(nums, rightIndex, r)
        return right
