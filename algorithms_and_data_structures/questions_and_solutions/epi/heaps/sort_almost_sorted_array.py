from heapq import *
class Solution:
    def sortAlmostSortedArray(self, arr, k):
        res, minHeap = [], []

        for i in range(k): heappush(minHeap, arr[i])
        for i in range(k, len(arr)):
            num = heappushpop(arr[i])
            res.append(num)
        while minHeap: res.append(heappop(minHeap))

        return res