class DSU:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.size = [1 for i in range(n)]
        self.maxLength = 1
    
    def find(self, i):
        if self.parent[i] != i: self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        iSet, jSet = self.find(i), self.find(j)
        if iSet == jSet: return

        if self.size[iSet] < self.size[jSet]:
            self.size[jSet] += self.size[iSet]
            self.parent[iSet] = jSet
            self.maxLength = max(self.maxLength, self.size[jSet])
        elif self.size[iSet] > self.size[jSet]:
            self.size[iSet] += self.size[jSet]
            self.parent[jSet] = iSet
            self.maxLength = max(self.maxLength, self.size[iSet])
        else:
            self.size[jSet] += self.size[iSet]
            self.parent[iSet] = jSet
            self.maxLength = max(self.maxLength, self.size[jSet])

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # return self.cubicTime(nums)
        # return self.sorting(nums)
        # return self.linearTime(nums)
        return self.unionFind(nums)
    
    def unionFind(self, nums):
        if len(nums) == 0: return 0
        pos = {nums[i]: i for i in range(len(nums))}
        dsu = DSU(len(nums))

        for i in range(len(nums)):
            if (nums[i] - 1) in pos and dsu.find(pos[nums[i]]) != dsu.find(pos[nums[i] - 1]): dsu.union(pos[nums[i]], pos[nums[i] - 1])
            if (nums[i] + 1) in pos and dsu.find(pos[nums[i]]) != dsu.find(pos[nums[i] + 1]): dsu.union(pos[nums[i]], pos[nums[i] + 1])

        return dsu.maxLength
    
    def cubicTime(self, nums):
        if len(nums) == 0: return 0
        res = 1

        for i in range(len(nums)):
            consecutive, offset = True, 1
            while consecutive:
                if nums[i] + offset in nums: 
                    offset += 1
                    res = max(res, offset)
                else: consecutive = False
        
        return res

    def sorting(self, nums):
        if len(nums) == 0: return 0
        nums.sort()

        res, curr = 1, 1

        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]: continue
            if nums[i] == nums[i - 1] + 1: curr += 1
            else: curr = 1

            res = max(res, curr)
        
        return res
    
    def linearTime(self, nums):
        if len(nums) == 0: return 0
        numSet = set(nums)
        res = 1

        for i in range(len(nums)):
            if nums[i] - 1 not in numSet:
                curr, currNum = 1, nums[i] + 1

                while currNum in numSet:
                    curr += 1
                    currNum += 1
            
                res = max(res, curr)
        
        return res