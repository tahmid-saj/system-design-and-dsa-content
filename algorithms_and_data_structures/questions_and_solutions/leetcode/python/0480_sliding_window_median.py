class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        result = [0.0 for x in range(len(nums) - k + 1)]
        self.maxHeap = []
        self.minHeap = []

        for i in range(0, k):
            self.insert(nums, i)

        windowStart, i = 0, 0
        for windowEnd in range(k - 1, len(nums)):
            result[i] = self.median()
            if windowEnd + 1 == len(nums): break

            if nums[windowStart] <= -self.maxHeap[0]: self.remove(-nums[windowStart], self.maxHeap)
            else: self.remove(nums[windowStart], self.minHeap)

            self.insert(nums, windowEnd + 1)
            windowStart += 1
            i += 1

        return result
    
    def insert(self, nums, i):
        if not self.maxHeap or nums[i] <= -self.maxHeap[0]: heappush(self.maxHeap, -nums[i])
        else: heappush(self.minHeap, nums[i])

        self.rebalance()
    
    def rebalance(self):
        if len(self.maxHeap) > len(self.minHeap) + 1: heappush(self.minHeap, -heappop(self.maxHeap))
        elif len(self.minHeap) > len(self.maxHeap): heappush(self.maxHeap, -heappop(self.minHeap))
    
    def remove(self, ele, heap):
        ind = heap.index(ele)
        del heap[ind]
        heapq.heapify(heap)

        self.rebalance()
    
    def median(self):
        if len(self.maxHeap) == len(self.minHeap): return (-self.maxHeap[0] + self.minHeap[0]) / 2.0
        else: return -self.maxHeap[0] / 1.0