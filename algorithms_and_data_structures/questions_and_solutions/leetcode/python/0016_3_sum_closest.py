class Solution:
  def threeSumClosest(self, nums: List[int], target: int) -> int:
    res = [0, math.inf]
    nums.sort()

    for i in range(0, len(nums) - 2):
      if i > 0 and nums[i] == nums[i - 1]: continue

      l, r = i + 1, len(nums) - 1
      while l < r:
        s = nums[i] + nums[l] + nums[r]
        diff = abs(target - s)
        if diff < res[1]:
          res = [s, diff]

        if diff == 0: return s
        elif s < target:
          l += 1
          while l < r and nums[l] == nums[l - 1]: l += 1
        elif s > target: 
          r -= 1
          while r > l and nums[r] == nums[r + 1]: r -= 1
    
    return res[0]