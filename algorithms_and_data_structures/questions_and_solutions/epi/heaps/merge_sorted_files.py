from heapq import *
class Solution:
    def mergeSortedFiles(self, sortedArrays):
        minHeap = []
        for i in range(len(sortedArrays)): heappush(minHeap, (sortedArrays[i][0][0], i, 0, sortedArrays[i][0]))

        res = []
        while minHeap:
            time, i, j, file = heappop(minHeap)
            res.append(file)
            if j + 1 < len(sortedArrays[i]): heappush(minHeap, (sortedArrays[i][j + 1][0], i, j + 1, sortedArrays[i][j + 1]))
        
        return res