class Solution:
  def threeSum(self, nums: List[int]) -> List[List[int]]:
    # return self.twoPointers(nums)
    # return self.twoPointersSet(nums)
    return self.twoPointersHashMapNoSort(nums)
  
  def twoPointers(self, nums):
    nums.sort()
    res = []

    for i in range(0, len(nums) - 2):
      if i > 0 and i < len(nums) - 2 and nums[i] == nums[i - 1]: continue
      if nums[i] > 0: break

      l, r = i + 1, len(nums) - 1
      while l < r:
        s = nums[i] + nums[l] + nums[r]
        if s == 0:
          res.append([nums[i], nums[l], nums[r]])
          l += 1
          r -= 1
          while l < r and nums[l] == nums[l - 1]: l += 1
          while r > l and nums[r] == nums[r + 1]: r -= 1
        elif s < 0: l += 1
        elif s > 0: r -= 1

    return res
  
  def twoPointersSet(self, nums):
    res = []
    nums.sort()

    for i in range(0, len(nums)):
      if nums[i] > 0: break
      if i > 0 and nums[i] == nums[i - 1]: continue

      j = i + 1
      seen = set()
      while j < len(nums):
        complement = (-1 * nums[i]) - nums[j]
        if complement in seen:
          res.append([nums[i], nums[j], complement])
          while j + 1 < len(nums) and nums[j] == nums[j + 1]:
            j += 1
            print('j')
        seen.add(nums[j])
        j += 1
    
    return res
  
  def twoPointersHashMapNoSort(self, nums):
    res = set()
    seen, dups = {}, set()

    for i in range(0, len(nums)):
      if nums[i] not in dups:
        dups.add(nums[i])

        for j in range(i + 1, len(nums)):
          complement = -nums[i] - nums[j]
          if complement in seen and seen[complement] == i:
            res.add(tuple(sorted([nums[i], nums[j], complement])))
          seen[nums[j]] = i
    
    return list(res)