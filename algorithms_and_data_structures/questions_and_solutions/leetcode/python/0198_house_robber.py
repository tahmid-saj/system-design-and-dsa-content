class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 2: return max(nums)
        # return self.recursive(nums, len(nums) - 1)
    
        # dp = {}
        # return self.topDown(nums, len(nums) - 1, dp)

        # dp = [0 for _ in range(len(nums))]
        # return self.bottomUp(nums, dp)

        return self.bottomUpConstantSpace(nums)

    def recursive(self, nums, index):
        path1 = nums[index]
        if index - 2 >= 0: path1 += self.recursive(nums, index - 2)
        path2 = 0
        if index - 1 >= 0: path2 = self.recursive(nums, index - 1)

        if index == 0: return nums[index]

        return max(path1, path2)
    
    def topDown(self, nums, index, dp):
        if index in dp: return dp[index]

        path1 = nums[index]
        if index - 2 >= 0: path1 += self.topDown(nums, index - 2, dp)
        path2 = 0
        if index - 1 >= 0: path2 = self.topDown(nums, index - 1, dp)

        if index == 0: return nums[index]

        dp[index] = max(path1, path2)

        return dp[index]
    
    def bottomUp(self, nums, dp):
        dp[-1] = nums[-1]
        dp[-2] = max(nums[-1], nums[-2])

        for i in range(len(nums) - 3, -1, -1):
            dp[i] = max(nums[i] + dp[i + 2], dp[i + 1])

        print(dp)
        return dp[0]
    
    def bottomUpConstantSpace(self, nums):
        prev = nums[-1]
        curr = max(nums[-1], nums[-2])

        for i in range(len(nums) - 3, -1, -1):
            tmp = max(nums[i] + prev, curr)
            prev = curr
            curr = tmp
        
        return curr
        