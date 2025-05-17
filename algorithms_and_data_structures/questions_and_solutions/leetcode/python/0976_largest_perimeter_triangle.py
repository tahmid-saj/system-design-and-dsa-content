class Solution:
    def largestPerimeter(self, nums: List[int]) -> int:
        # a + b > c to be formed
        # sort the array
        # traverse backwards to find nums[i] < nums[i - 1] + nums[i - 2]
        res = 0
        nums.sort()
        for i in range(len(nums) - 1, 1, -1):
            if nums[i] < nums[i - 1] + nums[i - 2]: 
                res = nums[i] + nums[i - 1] + nums[i - 2]
                break
        return res