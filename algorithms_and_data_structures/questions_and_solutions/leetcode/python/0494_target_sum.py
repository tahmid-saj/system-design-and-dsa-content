class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        s = sum(nums) + target
        if s % 2 != 0: return 0
        # return self.recursive(nums, target, 0, 0)
        
        self.total = sum(nums)
        # dp = [[-math.inf for j in range(self.total * 2 + 1)] for i in range(len(nums))]
        # return self.topDown(nums, target, 0, 0, dp)
    
        # return self.bottomUp(nums, target)
        
        return self.bottomUpLinearSpace(nums, target)

    def recursive(self, nums, s, curr, index):
        if index == len(nums) and curr == s: return 1
        if index == len(nums): return 0

        res1 = self.recursive(nums, s, curr + nums[index], index + 1)
        res2 = self.recursive(nums, s, curr - nums[index], index + 1)
        return res1 + res2
    
    def topDown(self, nums, s, curr, index, dp):
        if index == len(nums) and curr == s: return 1
        if index == len(nums): return 0

        if dp[index][curr + self.total] != -math.inf: return dp[index][curr + self.total]
        res1 = self.topDown(nums, s, curr + nums[index], index + 1, dp)
        res2 = self.topDown(nums, s, curr - nums[index], index + 1, dp)
        dp[index][curr + self.total] = res1 + res2

        return dp[index][curr + self.total]
    
    def bottomUp(self, nums, target):
        if self.total < target: return 0

        dp = [[0 for j in range(2 * self.total + 1)] for i in range(len(nums))]
        dp[0][nums[0] + self.total] = 1
        dp[0][-nums[0] + self.total] += 1

        for i in range(1, len(nums)):
            for j in range(-self.total, self.total + 1):
                if dp[i - 1][j + self.total] > 0:
                    dp[i][j + self.total + nums[i]] += dp[i - 1][j + self.total]
                    dp[i][j + self.total - nums[i]] += dp[i - 1][j + self.total]

        return dp[len(nums) - 1][target + self.total]
    
    def bottomUpLinearSpace(self, nums, target):
        if self.total < target: return 0

        dpPrev = [0 for j in range(2 * self.total + 1)]
        dpPrev[nums[0] + self.total] = 1
        dpPrev[-nums[0] + self.total] += 1

        for i in range(1, len(nums)):
            dpCurr = [0 for j in range(2 * self.total + 1)]
            for j in range(-self.total, self.total + 1):
                if dpPrev[j + self.total] > 0:
                    dpCurr[j + self.total + nums[i]] += dpPrev[j + self.total]
                    dpCurr[j + self.total - nums[i]] += dpPrev[j + self.total]
            dpPrev = dpCurr
        
        return dpPrev[target + self.total]