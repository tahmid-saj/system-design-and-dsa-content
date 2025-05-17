class Solution:
    def frequencySort(self, s: str) -> str:
        maxHeap = []
        frequency = {}
        for i in range(0, len(s)): frequency[s[i]] = frequency.get(s[i], 0) + 1

        for k, v in frequency.items(): heappush(maxHeap, (-v, k))

        res = []
        while len(maxHeap) > 0:
            c = heappop(maxHeap)
            res.append(c[1] * -c[0])
        
        return "".join(res)