class Solution:
    def findErrorNums(self, nums: List[int]) -> List[int]:
        nums.sort()
        res = [0, 0]
        if nums[0] != 1 and nums[1] == nums[0]: return [nums[1], 1]
        if nums[0] != 1: res[1] = 1
        elif nums[-1] != len(nums): res[1] = len(nums)

        # 2 3 3 4 5 6
        # 1 3 4 5 5 6 7 8

        for i in range(1, len(nums)):
            if nums[i] - nums[i - 1] > 1:
                res[1] = nums[i - 1] + 1
            if nums[i] == nums[i - 1]:
                res[0] = nums[i]

            if res[0] != 0 and res[1] != 0: break
                
        
        return res