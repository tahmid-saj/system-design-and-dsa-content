from heapq import *
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        return self.heap(nums, k)
        # return self.quickselect(nums, k)

    def heap(self, nums, k):
        minHeap = []
        for i in range(k): heappush(minHeap, nums[i])
        for i in range(k, len(nums)):
            if minHeap[0] <= nums[i]:
                heappop(minHeap)
                heappush(minHeap, nums[i])

        return minHeap[0]
    
    def quickselect(self, nums, k):
        pivot = random.choice(nums)
        left, middle, right = [], [], []

        for num in nums:
            if num > pivot: left.append(num)
            elif num < pivot: right.append(num)
            else: middle.append(num)
        
        if k <= len(left): return self.quickselect(left, k)
        if k > len(left) + len(middle): return self.quickselect(right, k - len(left) - len(middle))
        return pivot