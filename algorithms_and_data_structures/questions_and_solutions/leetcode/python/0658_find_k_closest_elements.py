class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        index = self.binarySearch(arr, x)

        minHeap = []
        start, end = index - k, index + k
        start = max(start, 0)
        end = min(end, len(arr) - 1)
        for i in range(start, end + 1):
            heapq.heappush(minHeap, (abs(x - arr[i]), arr[i]))
        
        res = []
        for i in range(k): res.append(heapq.heappop(minHeap)[1])

        res.sort()
        return res
    
    def binarySearch(self, arr, x):
        l, r = 0, len(arr) - 1
        while l <= r:
            middle = l + (r - l) // 2
            if arr[middle] == x: return middle
            if arr[middle] < x: l = middle + 1
            else: r = middle - 1
        
        if l == 0: return l
        return l - 1