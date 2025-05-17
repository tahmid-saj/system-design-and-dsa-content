class Solution:
  def sort(self, nums):
    i = 0
    while i < len(nums):
      j = nums[i] - 1
      if nums[i] != nums[j]: nums[i], nums[j] = nums[j], nums[i]
      else: i += 1
    
    return nums