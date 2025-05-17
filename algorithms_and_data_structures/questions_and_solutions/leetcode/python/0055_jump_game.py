class Solution:
    def canJump(self, nums: List[int]) -> bool:
        # return self.greedy1(nums)
        return self.greedy2(nums)
        # return self.backtrack(nums, 0)

        # dp = [0 for _ in range(len(nums))]
        # dp[len(nums) - 1] = 1
        # return self.topDownDP(nums, 0, dp)

        # return self.bottomUpDP(nums, dp)
    
    def greedy1(self, nums):
        if len(nums) == 1: return True

        dist = 1
        for i in range(len(nums) - 2, -1, -1):
            if nums[i] >= dist: 
                if i == 0: return True
                dist = 0
            dist += 1
        
        return False
    
    def greedy2(self, nums):
        if len(nums) == 1: return True
        furthestReach, i = 0, 0
        while i <= furthestReach and furthestReach < len(nums) - 1:
            furthestReach = max(furthestReach, i + nums[i])
            i += 1
        return furthestReach >= len(nums) - 1
    
    def backtrack(self, nums, pos):
        if pos == len(nums) - 1: return True

        furthestJump = min(pos + nums[pos], len(nums) - 1)
        for i in range(furthestJump, pos, -1):
            if self.backtrack(nums, i): return True
        
        return False

    def topDownDP(self, nums, pos, dp):
        if dp[pos] != 0:
            return True if dp[pos] == 1 else False
        
        furthestJump = min(pos + nums[pos], len(nums) - 1)
        for i in range(furthestJump, pos, -1):
            if self.topDownDP(nums, i, dp):
                dp[pos] = 1
                return True
        
        dp[pos] = -1
        return False

    def bottomUpDP(self, nums, dp):
        for i in range(len(nums) - 2, -1, -1):
            furthestJump = min(i + nums[i], len(nums) - 1)
            for j in range(i + 1, furthestJump + 1):
                if dp[j] == 1:
                    dp[i] = 1
                    break
        
        return dp[0]