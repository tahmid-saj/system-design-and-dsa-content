class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        # hashmap to contain elements already visited
        # loop through nums:
        # -> if target - nums[i] is in hashmap: res = [hashmap[target - nums[i]], i], break
        # return res
        ele = {}
        res = []
        for i in range(len(nums)):
            if target - nums[i] in ele:
                res = [ele[target - nums[i]], i]
                break
            else:
                ele[nums[i]] = i
        
        return res