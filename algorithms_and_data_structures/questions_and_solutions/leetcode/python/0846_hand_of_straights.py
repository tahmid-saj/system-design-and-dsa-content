from heapq import *
class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        if len(hand) % groupSize != 0: return False
        frequency, minHeap = {}, []
        for i in range(len(hand)): frequency[hand[i]] = frequency.get(hand[i], 0) + 1
        for key, v in frequency.items(): heappush(minHeap, (key, v))
        # 1 2 2 3 3 4 6 7 8
        # 1 2 3, 2 3 4, 6 7 8
        while minHeap:
            prev, dups = -math.inf, []
            if len(minHeap) < groupSize: return False
            for i in range(groupSize):
                curr, freq = heappop(minHeap)
                if curr <= prev or (prev != -math.inf and curr - prev != 1): return False
                if freq > 1: dups.append((curr, freq))
                prev = curr
            
            while dups:
                curr, freq = dups.pop()
                heappush(minHeap, (curr, freq - 1))

        return True