class Solution:
  def smallestRange(self, nums: List[List[int]]) -> List[int]:
    currMax = -math.inf
    minHeap = []
    for i in range(len(nums)):
      heapq.heappush(minHeap, (nums[i][0], i, 0))
      currMax = max(currMax, nums[i][0])
    
    start, end = 0, math.inf
    while len(minHeap) == len(nums):
      num, l, index = heapq.heappop(minHeap)
      if end - start > currMax - num:
        start = num
        end = currMax
      
      if index + 1 < len(nums[l]):
        heapq.heappush(minHeap, (nums[l][index + 1], l, index + 1))
        currMax = max(currMax, nums[l][index + 1])
    
    return [start, end]