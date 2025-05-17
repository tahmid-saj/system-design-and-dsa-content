class Solution:
    def find132pattern(self, nums: List[int]) -> bool:
        return self.monotonicStack(nums)
    
    def monotonicStack(self, nums):
        stk = []
        twoNum = -math.inf
        for i in range(len(nums) - 1, -1, -1):
            if nums[i] < twoNum: return True
            while stk and nums[i] > stk[-1]: twoNum = stk.pop()
            stk.append(nums[i])
        
        return False