class Solution:
    def permutation(self, perm, nums):
        for i in range(len(nums)):
            while perm[i] != i:
                nums[perm[i]], nums[i] = nums[i], nums[perm[i]]
                perm[perm[i]], perm[i] = perm[i], perm[perm[i]]
        
        return nums