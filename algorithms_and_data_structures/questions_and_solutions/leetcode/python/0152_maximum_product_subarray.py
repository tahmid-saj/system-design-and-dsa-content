class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        # quadratic time, linear time
        # return self.quadraticTime(nums)
        return self.linearTime(nums)
    
    def quadraticTime(self, nums):
        res = -math.inf

        for i in range(len(nums)):
            curr = 1
            for j in range(i, len(nums)):
                curr *= nums[j]
                res = max(res, curr)
        
        return res
    
    def linearTime(self, nums):
        localMin, localMax, res = nums[0], nums[0], nums[0]

        for i in range(1, len(nums)):
            tmpLocalMin = min(localMin * nums[i], localMax * nums[i], nums[i])
            tmpLocalMax = max(localMax * nums[i], localMin * nums[i], nums[i])
            res = max(res, tmpLocalMax)
            localMin = tmpLocalMin
            localMax = tmpLocalMax
        
        return res