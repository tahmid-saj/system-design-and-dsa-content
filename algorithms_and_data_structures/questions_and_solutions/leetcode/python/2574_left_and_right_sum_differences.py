class Solution:
    def leftRightDifference(self, nums: List[int]) -> List[int]:
        lSum, s = 0, sum(nums)
        res = [0 for _ in range(len(nums))]

        for i, v in enumerate(nums):
            rSum = s - lSum - nums[i]
            
            res[i] = abs(lSum - rSum)
            lSum += nums[i]
        
        return res