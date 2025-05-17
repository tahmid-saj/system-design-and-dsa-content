def floydTortoiseHare(nums):
  slow, fast = nums[0], nums[0]

  while True:
    slow = nums[slow]
    fast = nums[nums[fast]]
    if slow == fast: break
  
  first, second = nums[0], slow
  while first != second:
    first = nums[first]
    second = nums[second]

  return first