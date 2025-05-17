from heapq import *
class Solution:
    def smallestDistancePair(self, nums: List[int], k: int) -> int:
        pairs = []
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)): pairs.append(abs(nums[i] - nums[j]))
        
        maxHeap = []
        for pair in pairs:
            heappush(maxHeap, -pair)
            if len(maxHeap) > k: heappop(maxHeap)
        
        return -maxHeap[0]