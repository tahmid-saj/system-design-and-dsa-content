class Solution:
    def sortArrayByParity(self, nums: List[int]) -> List[int]:
        # return self.dutchNationalFlag(nums)
        return self.quickSort(nums)

    def dutchNationalFlag(self, nums):
        l, r, i = 0, len(nums) - 1, 0
        while l < r:
            if nums[i] % 2 == 0:
                nums[i], nums[l] = nums[l], nums[i]
                i += 1
                l += 1
            else:
                nums[i], nums[r] = nums[r], nums[i]
                r -= 1
        return nums
    
    def quickSort(self, nums):
        i, j = 0, len(nums) - 1
        while i < j:
            if nums[i] % 2 > nums[j] % 2: nums[i], nums[j] = nums[j], nums[i]
            if nums[i] % 2 == 0: i += 1
            if nums[j] % 2 == 1: j -= 1
        return nums