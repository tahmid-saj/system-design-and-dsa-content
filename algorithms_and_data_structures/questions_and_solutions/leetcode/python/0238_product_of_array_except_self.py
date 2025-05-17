class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # return self.twoPrefixProducts(nums)
        return self.constantSpace(nums)

    def twoPrefixProducts(self, nums):
        l, r, res = [1 for _ in range(len(nums))], [1 for _ in range(len(nums))], [0 for _ in range(len(nums))]

        for i in range(1, len(nums)): l[i] = nums[i - 1] * l[i - 1]
        for i in range(len(nums) - 2, -1, -1): r[i] = nums[i + 1] * r[i + 1]
        for i in range(len(nums)): res[i] = l[i] * r[i]
        
        return res
    
    def constantSpace(self, nums):
        res = [1 for _ in range(len(nums))]

        for i in range(len(nums) - 2, -1, -1): res[i] = nums[i + 1] * res[i + 1]

        l = 1
        for i in range(len(nums)): 
            if i > 0: l *= nums[i - 1]
            res[i] = res[i] * l
        
        return res