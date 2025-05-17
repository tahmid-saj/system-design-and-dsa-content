def dutchNationalFlag(nums):
  zero, two, i = 0, len(nums) - 1, 0
  while i <= two:
    if nums[i] == 0:
      nums[i], nums[zero] = nums[zero], nums[i]
      i += 1
      zero += 1
    elif nums[i] == 1:
      i += 1
    elif nums[i] == 2:
      nums[i], nums[two] = nums[two], nums[i]
      two -= 1