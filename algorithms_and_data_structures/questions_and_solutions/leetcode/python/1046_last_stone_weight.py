from heapq import *
class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        maxHeap = []
        for i in range(len(stones)): heappush(maxHeap, -stones[i])

        while len(maxHeap) > 1:
            x = -heappop(maxHeap)
            y = -heappop(maxHeap)
            if x != y: heappush(maxHeap, -abs(y - x))
        
        if maxHeap: return -heappop(maxHeap)
        return 0