class Solution:
    def alternatingArray(self, nums):
        for i in range(len(nums)):
            nums[i:i + 2] = sorted(nums[i:i + 2], reverse=(i % 2 == 0))
        
        return nums

# time: O(n)
# space: O(1)