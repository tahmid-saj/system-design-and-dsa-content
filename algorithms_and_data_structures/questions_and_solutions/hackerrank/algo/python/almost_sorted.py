def almostSorted(nums):
  def isSorted(arr, left, right):
    i = left + 1
    while i <= right:
      if arr[i - 1] > arr[i]: return False
      i += 1
    return True
  
  if isSorted(nums, 0, len(nums) - 1): print("yes")
  else:
    sortedNums = list(nums)
    sortedNums.sort()
    
    # find first left index's element which is not equal to sortedNums
    l = 0
    while l < len(nums) and nums[l] == sortedNums[l]: l += 1
    
    # find first right index's element which is not equal to sortedNums
    r = len(nums) - 1
    while r >= 0 and nums[r] == sortedNums[r]: r -= 1
    
    # check if exchanging l, r makes it sorted
    nums[l], nums[r] = nums[r], nums[l]
    if isSorted(nums, 0, len(nums) - 1): print("yes\nswap {i} {j}".format(i=l + 1, j=r + 1))
    else:
      nums[l], nums[r] = nums[r], nums[l]
      seg = list(nums[l:r + 1])
      seg.reverse()
      if isSorted(seg, 0, len(seg) - 1): print("yes\nreverse {i} {j}".format(i=l + 1, j=r + 1))
      else: print("no")