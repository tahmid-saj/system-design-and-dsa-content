class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.minHeap = []
        self.k = k
        for i in range(0, len(nums)): self.add(nums[i])

    def add(self, val: int) -> int:
        heappush(self.minHeap, val)

        if len(self.minHeap) > self.k: heappop(self.minHeap)

        return self.minHeap[0]


# Your KthLargest object will be instantiated and called as such:
# obj = KthLargest(k, nums)
# param_1 = obj.add(val)