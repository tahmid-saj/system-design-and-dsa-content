class Solution:
  def kadaneProductVariant(self, nums):
    # finding the maximum product subarray
    localMax, localMin, res = nums[0], nums[0], nums[0]

    for i in range(1, len(nums)):
      tmpMax = max(localMax * nums[i], localMin * nums[i], nums[i])
      localMin = min(localMin * nums[i], localMax * nums[i], nums[i])
      localMax = tmpMax

      res = max(res, localMax)
    
    return res