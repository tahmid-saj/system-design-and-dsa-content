class Solution:
    def reorganizeString(self, s: str) -> str:
        frequency = {}
        maxHeap = []

        res = ""
        for i in range(0, len(s)): frequency[s[i]] = frequency.get(s[i], 0) + 1
        for k, v in frequency.items(): heapq.heappush(maxHeap, (-v, k))

        while len(maxHeap) > 1:
            freq1, c1 = heapq.heappop(maxHeap)
            freq1 = -freq1
            freq2, c2 = heapq.heappop(maxHeap)
            freq2 = -freq2

            res += c1 + c2
            if freq1 - 1 > 0: heapq.heappush(maxHeap, (-1 * (freq1 - 1), c1))
            if freq2 - 1 > 0: heapq.heappush(maxHeap, (-1 * (freq2 - 1), c2))

        if len(maxHeap) == 1:
            freq, c = heapq.heappop(maxHeap)
            if -freq > 1: return ""
            res += c

        return res