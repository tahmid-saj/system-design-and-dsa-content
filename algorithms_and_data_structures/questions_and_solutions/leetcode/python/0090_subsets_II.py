class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        # return self.iterative(nums)

        nums.sort()
        self.res = []
        # self.recursive(nums, 0, 1)
        # return self.res

        for length in range(0, len(nums) + 1):
            self.backtrack(nums, length, 0, [])
        
        return self.res
    
    def iterative(self, nums):
        nums.sort()
        res = [[]]
        end = 0
        for i in range(len(nums)):
            start = 0
            if i > 0 and nums[i] == nums[i - 1]: start = end + 1
            end = len(res) - 1
            for j in range(start, end + 1):
                subset = list(res[j])
                subset.append(nums[i])
                res.append(list(subset))

        return res
    
    def recursive(self, nums, index, end):
        if index == len(nums): return

        start = 0
        if index > 0 and nums[index] == nums[index - 1]: start = end + 1
        end = len(self.res) - 1
        for i in range(start, end + 1):
            subset = list(self.res[i])
            subset.append(nums[index])
            self.res.append(subset)
        
        self.recursive(nums, index + 1, end)

    def backtrack(self, nums, length, index, comb):
        if len(comb) == length:
            self.res.append(list(comb))
            return
        
        for i in range(index, len(nums)):
            if i > index and nums[i] == nums[i - 1]: continue
            comb.append(nums[i])
            self.backtrack(nums, length, i + 1, comb)
            comb.pop()