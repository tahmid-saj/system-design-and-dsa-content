class Solution:
  def canPartition(self, num):
    s = sum(num)
    dp = [[-1 for j in range(s + 1)] for i in range(len(num))]
    dpOptimized = [[False for j in range((s // 2) + 1)] for i in range(len(num))]

    # return self.knapsackRecursive(num, 0, 0, 0)
    # return self.knapsackRecursiveTopDown(num, 0, 0, 0, dp)
    return self.bottomUp(num, dpOptimized, s // 2, s)
  
  def knapsackRecursive(self, nums, index, sum1, sum2):
    if index >= len(nums): return abs(sum1 - sum2)

    diff1 = self.knapsackRecursive(nums, index + 1, sum1 + nums[index], sum2)
    diff2 = self.knapsackRecursive(nums, index + 1, sum1, sum2 + nums[index])
    
    return min(diff1, diff2)
  
  def knapsackRecursiveTopDown(self, nums, index, sum1, sum2, dp):
    if index >= len(nums): return abs(sum1 - sum2)

    if dp[index][sum1] == -1:
      dp[index][sum1] = self.knapsackRecursiveTopDown(nums, index + 1, sum1 + nums[index], sum2, dp)
    if dp[index][sum2] == -1:
      dp[index][sum2] = self.knapsackRecursiveTopDown(nums, index + 1, sum1, sum2 + nums[index], dp)

    return min(dp[index][sum1], dp[index][sum2])
  
  def bottomUp(self, nums, dp, sm, sum):
    if len(nums) == 0: return 0

    for i in range(len(nums)): dp[i][0] = True
    for s in range(1, sm + 1):
      if s == nums[0]: dp[0][s] = True
    
    for i in range(1, len(nums)):
      for s in range(1, sm + 1):
        if dp[i - 1][s] == True: dp[i][s] = dp[i - 1][s]
        elif s >= nums[i]: dp[i][s] = dp[i - 1][s - nums[i]]

    # find the sum of the subset closest to sm
    res = 0
    for s in range(sm, -1, -1):
      if dp[len(nums) - 1][s] == True:
        res = (sum - s) - s
        break
    
    return res