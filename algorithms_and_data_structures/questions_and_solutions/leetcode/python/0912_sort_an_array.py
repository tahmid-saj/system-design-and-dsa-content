from heapq import *
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        return self.heap(nums)

    def heap(self, nums):
        minHeap = []
        for i in range(len(nums)): heappush(minHeap, nums[i])

        res = []
        while minHeap: res.append(heappop(minHeap))

        return res