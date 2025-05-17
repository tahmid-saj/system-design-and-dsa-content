class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # return self.kadanesAlgorithm(nums)

        return self.divideAndConquer(nums, 0, len(nums) - 1)
    
    def kadanesAlgorithm(self, nums):
        localMax, res = 0, -1e8

        for i in range(0, len(nums)):
            localMax = max(nums[i], localMax + nums[i])
            res = max(res, localMax)
        
        return res
    
    def divideAndConquer(self, nums, left, right):
        if left > right: return -math.inf
        middle = (left + right) // 2

        # left side
        lMax, curr = 0, 0
        for i in range(middle - 1, left - 1, -1):
            curr += nums[i]
            lMax = max(lMax, curr)
        
        rMax, curr = 0, 0
        for i in range(middle + 1, right + 1):
            curr += nums[i]
            rMax = max(rMax, curr)
        
        bothSum = lMax + nums[middle] + rMax

        lMax = self.divideAndConquer(nums, left, middle - 1)
        rMax = self.divideAndConquer(nums, middle + 1, right)

        bestSum = max(lMax, bothSum, rMax)

        return bestSum