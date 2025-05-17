import collections
class Solution:
    def searchMinMax(self, nums):
        minmax =  collections.namedtuple("minmax", ("min", 'max'))
        def minMax(self, a, b):
            return minmax(a, b) if a < b else minmax(b, a)
        
        if len(nums) <= 1: return minmax(nums[0], nums[0])
        res = minMax(nums[0], nums[1])
        for i in range(2, len(nums) - 1, 2):
            curr = minMax(nums[i], nums[i + 1])
            res = minmax(min(res.min, curr.min), max(res.max, curr.max))
        
        if len(nums) % 2: res = minmax(min(res.min, nums[-1]), max(res.max, nums[-1]))

        return res