def boyerMooreVoting(self, nums):
  count, candidate = 0, None

  for num in nums:
    if candidate == num: count += 1
    elif count == 0:
      candidate = num
      count += 1
    else: count -= 1
  return candidate