class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        minHeap = []
        frequency = {}

        for i in range(len(nums)): frequency[nums[i]] = frequency.get(nums[i], 0) + 1

        for key, val in frequency.items():
            if len(minHeap) < k:
                heappush(minHeap, (val, key))
                continue
            if minHeap[0][0] < val:
                heappop(minHeap)
                heappush(minHeap, (val, key))
        
        return [ele[1] for ele in minHeap]