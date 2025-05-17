class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        # return self.cyclicSort1(nums)
        # return self.cyclicSort2(nums)
        # return self.cyclicSortRecursive(nums, 0)
        return self.binarySearch(nums)
        # return self.floydsTortoiseAndHare(nums)
        # return self.sorting(nums)
        # return self.hashset(nums)
        # return self.negativeMarking(nums)
    
    def cyclicSort1(self, nums):
        i = 0
        while i < len(nums):
            j = nums[i] - 1
            if nums[i] != nums[j]: nums[i], nums[j] = nums[j], nums[i]
            else: i += 1
        
        for i in range(len(nums)):
            if nums[i] != i + 1: return nums[i]
        
        return -1
    
    def cyclicSort2(self, nums):
        while nums[0] != nums[nums[0]]:
            nums[nums[0]], nums[0] = nums[0], nums[nums[0]]
        return nums[0]
    
    def cyclicSortRecursive(self, nums, curr):
        if curr == nums[curr]: return curr
        nxt = nums[curr]
        nums[curr] = curr
        return self.cyclicSortRecursive(nums, nxt)
    
    def binarySearch(self, nums):
        l, r, res = 1, len(nums) - 1, 0
        while l <= r:
            middle = (r + l) // 2
            counts = 0
            counts = sum(1 for num in nums if num <= middle)
            # counts = sum(num <= middle for num in nums)

            if middle < counts:
                res = middle
                r = middle - 1
            else: l = middle + 1
        
        return res
    
    def floydsTortoiseAndHare(self, nums):
        slow, fast = nums[0], nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast: break
        
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        
        return slow
    
    def sorting(self, nums):
        nums.sort()
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]: return nums[i]
        
        return -1
    
    def hashset(self, nums):
        seen = set()
        for i in range(len(nums)):
            if nums[i] in seen: return nums[i]
            seen.add(nums[i])
        
        return -1
    
    def negativeMarking(self, nums):
        res = 0
        for i in range(len(nums)):
            j = abs(nums[i])
            if nums[j] < 0:
                res = abs(nums[i])
                break
            nums[j] = -nums[j]
        
        for i in range(len(nums)): nums[i] = abs(nums[i])
        return res