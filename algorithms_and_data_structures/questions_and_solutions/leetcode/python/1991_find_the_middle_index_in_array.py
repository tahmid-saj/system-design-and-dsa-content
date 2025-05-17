class Solution:
    def findMiddleIndex(self, nums: List[int]) -> int:
        prefixLeft, prefixRight = 0, sum(nums[1:])
        for i in range(len(nums)):
            if prefixLeft == prefixRight: return i
            prefixLeft += nums[i]
            if i + 1 < len(nums): prefixRight -= nums[i + 1]
        
        return -1