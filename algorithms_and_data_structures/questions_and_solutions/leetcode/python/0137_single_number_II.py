class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        # sorting -> nlogn
        # hashmap
        # math
        # return self.sorting(nums)
        # return self.hashmap(nums)
        return self.math(nums)
    
    def sorting(self, nums):
        nums.sort()

        for i in range(0, len(nums) - 1, 3):
            if nums[i] == nums[i + 1]:
                continue
            else:
                return nums[i]
        
        return nums[len(nums) - 1]
    
    def hashmap(self, nums):
        if len(nums) == 1: return nums[0]
        numsMap, res = {}, 0
        for i in range(len(nums)): numsMap[nums[i]] = numsMap.get(nums[i], 0) + 1
        for i, v in numsMap.items():
            if v == 1: res = i

        return res
    
    def math(self, nums):
        return (3 * sum(set(nums)) - sum(nums)) // 2