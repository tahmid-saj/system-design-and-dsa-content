class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        # self.res = [[]]
        # self.recursive(nums, 0)
        # return self.res

        # self.res = []

        # def backtrack(index=0, comb=[]):
        #     if len(comb) == k:
        #         self.res.append(list(comb))
        #         return

        #     for i in range(index, len(nums)):
        #         comb.append(nums[i])
        #         backtrack(i + 1, comb)
        #         comb.pop()

        # for k in range(len(nums) + 1):
        #     backtrack()
        
        # return self.res

        return self.iterative(nums)
    
    def recursive(self, nums, index):
        if index == len(nums): return

        for i in range(len(self.res)):
            subset = list(self.res[i])
            subset.append(nums[index])
            self.res.append(subset)
        
        self.recursive(nums, index + 1)
    
    def iterative(self, nums):
        res = [[]]
        for i in range(len(nums)):
            for j in range(len(res)):
                subset = list(res[j])
                subset.append(nums[i])
                res.append(subset)
        
        return res
    
    def bitmask(self, nums):
        res = []
        for i in range(2**len(nums), 2**(len(nums) + 1)):
            bitmask = bit(i)[3:]
            res.append([nums[j] for j in range(len(nums)) if bitmask[j] == '1'])
        
        return res