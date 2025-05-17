from heapq import *
class Solution:
    def kLargestMaxHeap(self, heap, k):
        res, maxHeap = [], [(-heap[0], 0)]

        for _ in range(k):
            val, i = heappop(maxHeap)
            val = -val
            res.append(val)

            leftIndex = i * 2 + 1
            if leftIndex < len(heap): heappush(maxHeap, (-heap[leftIndex], leftIndex))
            rightIndex = i * 2 + 2
            if rightIndex < len(heap): heappush(maxHeap, (-heap[rightIndex], rightIndex))
        
        return res