class Solution:
  def maxArea(self, height: List[int]) -> int:
    # loop through height using two pointers i, j from (0, len(s)), (len(s) - 1, 0) respectively
    #   area = (j - i) * min(height[i], height[j])
    #   res = max(res, area)
    #   if height[j] > height[i]: i += 1
    #   else: j -= 1
    i, j = 0, len(height) - 1
    res = 0
    
    while i < j:
      area = (j - i) * min(height[i], height[j])
      res = max(res, area)

      if height[j] > height[i]: i += 1
      else: j -= 1
    
    return res