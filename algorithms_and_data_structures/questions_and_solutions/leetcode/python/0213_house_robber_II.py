class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 3: return max(nums)

        # self.nums = nums
        # return self.recursive(0, None)
        
        return max(
            self.dp(nums[1:]), self.dp(nums[:-1])
        )

    @lru_cache(None)
    def recursive(self, index, start):
        if index >= len(self.nums): return 0

        path1, path2 = 0, 0
        if not start or index < len(self.nums) - 1: path1 = self.nums[index] + self.recursive(index + 2, True if index == 0 else start)
        path2 = self.recursive(index + 1, False if index == 0 else start)

        return max(path1, path2)
    
    def dp(self, nums):
        # below paths are arranged as follows: path2, path1, num where path2 is on the 1st house, path1 is on the 2nd house, num is on the 3rd house

        path1, path2 = 0, 0
        for num in nums:
            tmp = path1
            path1 = max(path2 + num, path1)
            path2 = tmp
        
        return path1