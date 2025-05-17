class Solution:
    def wiggleSort(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # return self.sorting(nums)
        return self.greedy(nums)
    
    def sorting(self, nums):
        for i in range(len(nums)):
            nums[i:i + 2] = sorted(nums[i:i + 2], reverse=(i % 2 != 0))
    
    def greedy(self, nums):
        for i in range(len(nums) - 1):
            if (i % 2 == 0 and nums[i] > nums[i + 1]) or (i % 2 != 0 and nums[i] < nums[i + 1]): nums[i], nums[i + 1] = nums[i + 1], nums[i]
        