class Solution:
    def isPossibleDivide(self, nums: List[int], k: int) -> bool:
        if len(nums) % k != 0: return False
        frequency, minHeap = {}, []
        for i in range(len(nums)): frequency[nums[i]] = frequency.get(nums[i], 0) + 1
        for key, v in frequency.items(): heappush(minHeap, (key, v))
        # 1 2 2 3 3 4 6 7 8
        # 1 2 3, 2 3 4, 6 7 8
        while minHeap:
            prev, dups = -math.inf, []
            if len(minHeap) < k: return False
            for i in range(k):
                curr, freq = heappop(minHeap)
                if curr <= prev or (prev != -math.inf and curr - prev != 1): return False
                if freq > 1: dups.append((curr, freq))
                prev = curr
            
            while dups:
                curr, freq = dups.pop()
                heappush(minHeap, (curr, freq - 1))

        return True