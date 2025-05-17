class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        s = sum(nums)
        if s % 2 != 0: return False
        
        # return self.recursive(nums, s // 2, 0)

        # dp = [[False for _ in range(s + 1)] for _ in range(len(nums))]
        # return self.topDown(nums, s // 2, 0, dp)
        
        # return self.bottomUp(nums, s // 2)

        return self.bottomUpLinearSpace(nums, s // 2)

    def recursive(self, nums, s, index):
        if s == 0: return True
        if index >= len(nums) or s < 0: return False

        res1 = False
        if s - nums[index] >= 0: res1 = self.recursive(nums, s - nums[index], index + 1)
        res2 = self.recursive(nums, s, index + 1)
        return res1 or res2
    
    def topDown(self, nums, s, index, dp):
        if s == 0: return True
        if index >= len(nums) or s < 0: return False
        
        if s - nums[index] >= 0:
            if dp[index][s] == False: 
                dp[index][s] = self.recursive(nums, s - nums[index], index + 1)
                if dp[index][s] == True: return True
        dp[index][s] = self.recursive(nums, s, index + 1)
        
        return dp[index][s]
    
    def bottomUp(self, nums, s, dp):
        dp = [[False for _ in range(s + 1)] for _ in range(len(nums))]
        if len(nums) == 1: return False

        for i in range(len(nums)): dp[i][0] = True
        for j in range(1, s + 1):
            if nums[0] == j: dp[0][j] = True
        
        for i in range(1, len(nums)):
            for j in range(1, s + 1):
                if dp[i - 1][j] == True: dp[i][j] = dp[i - 1][j]
                elif j - nums[i] >= 0: dp[i][j] = dp[i - 1][j - nums[i]]
        
        return dp[len(nums) - 1][s]
    
    def bottomUpLinearSpace(self, nums, s):
        dp = [False for _ in range(s + 1)]
        dp[0] = True
        for j in range(1, s + 1):
            if nums[0] == j: dp[j] = True
        
        for i in range(1, len(nums)):
            for j in range(s, 0, -1):
                if dp[j] == True: continue
                elif j - nums[i] >= 0: dp[j] = dp[j - nums[i]]
        
        return dp[-1]