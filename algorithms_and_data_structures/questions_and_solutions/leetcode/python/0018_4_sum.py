class Solution:
  def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
    # return self.twoPointers(nums, target)
    return self.twoPointersSet(nums, target)
  
  def twoPointers(self, nums, target):
    res = []
    nums.sort()

    for i in range(0, len(nums) - 3):
      if i > 0 and nums[i] == nums[i - 1]: continue
      for j in range(i + 1, len(nums) - 2):
        if j > i + 1 and nums[j] == nums[j - 1]: continue
        l, r = j + 1, len(nums) - 1
        while l < r:
          s = nums[i] + nums[j] + nums[l] + nums[r]
          if s == target:
            res.append([nums[i], nums[j], nums[l], nums[r]])
            l += 1
            r -= 1
            while l < r and nums[l] == nums[l - 1]: l += 1
            while r > l and nums[r] == nums[r + 1]: r -= 1
          elif s < target: l += 1
          elif s > target: r -= 1
    
    return res
  
  def twoPointersSet(self, nums, target):
    res = []
    nums.sort()

    for i in range(0, len(nums) - 2):
      if i > 0 and nums[i] == nums[i - 1]: continue
      
      for j in range(i + 1, len(nums) - 1):
        if j > i + 1 and nums[j] == nums[j - 1]: continue
        
        k = j + 1
        seen = set()
        while k < len(nums):
          complement = target - nums[i] - nums[j] - nums[k]
          if complement in seen:
            if complement > nums[k]: res.append([nums[i], nums[j], nums[k], complement])
            else: res.append([nums[i], nums[j], complement, nums[k]])
            
            while k + 1 < len(nums) and nums[k] == nums[k + 1]: k += 1
          seen.add(nums[k])
          k += 1
    
    return res