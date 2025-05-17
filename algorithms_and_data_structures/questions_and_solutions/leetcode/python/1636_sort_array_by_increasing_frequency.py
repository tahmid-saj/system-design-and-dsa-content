from heapq import *
class Solution:
    def frequencySort(self, nums: List[int]) -> List[int]:
        freq, minHeap = {}, []
        for i in range(len(nums)): freq[nums[i]] = freq.get(nums[i], 0) + 1
        for k, v in freq.items(): heappush(minHeap, (v, k))
        
        res, prevFreq, curr = [], 0, []
        while minHeap:
            f, num = heappop(minHeap)
            if f == prevFreq: 
                curr.extend([num for _ in range(f)])
            else:
                if len(curr) > 0: res.extend(sorted(curr, reverse=True))
                curr = [num for _ in range(f)]
            prevFreq = f
        
        if len(curr) > 0: res.extend(sorted(curr, reverse=True))
        
        return res