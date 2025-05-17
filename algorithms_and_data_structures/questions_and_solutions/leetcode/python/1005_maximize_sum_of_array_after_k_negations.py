class Solution:
    def largestSumAfterKNegations(self, nums: List[int], k: int) -> int:
        s, minHeap = 0, []
        for num in nums: 
            s += num
            heappush(minHeap, num)

        while k > 0:
            num = heappop(minHeap)
            s -= num
            heappush(minHeap, num * -1)
            s += num * -1
            k -= 1
        return s