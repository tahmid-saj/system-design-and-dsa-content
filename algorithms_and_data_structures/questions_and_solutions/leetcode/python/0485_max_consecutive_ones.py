class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        res, currRes = 0, 0
        # loop through nums using i:
        # if nums[i] == 1: currRes += 1
        # else: currRes = 0
        # res = max(res, currRes)
        # return res
        for i in range(0, len(nums)):
            if nums[i] == 1: 
                currRes += 1
                res = max(res, currRes)
            else: currRes = 0

        return res