class Solution:
    def sortArrayByParityII(self, nums: List[int]) -> List[int]:
        # return self.twoPass(nums)
        return self.onePass(nums)

    def twoPass(self, nums):
        res = [None for _ in range(len(nums))]
        i, l = 0, 0
        while i < len(nums) and l < len(nums):
            if nums[i] % 2 == 0: 
                res[l] = nums[i]
                l += 2
            i += 1
        
        i, r = 0, len(nums) - 1
        while i < len(nums) and r > 0:
            if nums[i] % 2 != 0: 
                res[r] = nums[i]
                r -= 2
            i += 1
        
        return res
    
    def onePass(self, nums):
        j = 1
        for i in range(0, len(nums), 2):
            if nums[i] % 2 != 0:
                while nums[j] % 2 != 0: j += 2
                nums[i], nums[j] = nums[j], nums[i]
        return nums