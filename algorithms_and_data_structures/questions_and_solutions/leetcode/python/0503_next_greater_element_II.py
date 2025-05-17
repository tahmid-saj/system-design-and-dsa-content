class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        res, nextGreater, stk = [-1] * len(nums), {}, []

        for i in range((len(nums) * 2) - 1, -1, -1):
            while stk and stk[-1] <= nums[i % len(nums)]:
                stk.pop()
            
            if stk: res[i % len(nums)] = stk[-1]
            stk.append(nums[i % len(nums)])
        
        return res