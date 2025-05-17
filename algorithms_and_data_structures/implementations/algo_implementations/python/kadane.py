def kadane(nums):
  localMax, res = 0, -1e8

  for i in range(0, len(nums)):
    localMax = max(nums[i], localMax + nums[i])
    res = max(res, localMax)
  
  return res