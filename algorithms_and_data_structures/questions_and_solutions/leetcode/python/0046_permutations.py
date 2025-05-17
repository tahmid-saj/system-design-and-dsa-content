class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        # return self.iterative(nums)
        self.res = []
        # self.recursive(nums, [], 0)
        # return self.res

        self.backtrack(nums, [])
        return self.res

    def iterative(self, nums):
        res = []
        queue = [[]]

        for i in range(0, len(nums)):
            queueLength = len(queue)
            for j in range(0, queueLength):
                p = queue.pop(0)
                for k in range(0, len(p) + 1):
                    newPermutation = list(p)
                    newPermutation.insert(k, nums[i])
                    if len(newPermutation) == len(nums): res.append(newPermutation)
                    else: queue.append(newPermutation)

        return res
    
    def recursive(self, nums, comb, index):
        if len(comb) == len(nums):
            self.res.append(list(comb))
            return

        if index == len(nums): return

        for j in range(0, len(comb) + 1):
            p = list(comb)
            p.insert(j, nums[index])
            self.recursive(nums, p, index + 1)

    def backtrack(self, nums, comb):
        if len(nums) == len(comb):
            self.res.append(list(comb))
            return

        for num in nums:
            if num not in comb:
                comb.append(num)
                self.backtrack(nums, comb)
                comb.pop()