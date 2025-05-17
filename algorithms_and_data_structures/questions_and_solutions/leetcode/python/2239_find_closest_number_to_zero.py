class Solution:
    def findClosestNumber(self, nums: List[int]) -> int:
        dist, res = math.inf, -math.inf

        for i in range(len(nums)):
            d = abs(nums[i])
            if d < dist: 
                res = nums[i]
                dist = d
            elif d == dist:
                res = max(res, nums[i])
        
        return res