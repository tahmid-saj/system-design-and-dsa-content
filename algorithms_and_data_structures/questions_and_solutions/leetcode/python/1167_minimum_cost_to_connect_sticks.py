class Solution:
    def connectSticks(self, sticks: List[int]) -> int:
        minHeap = []
        for i in range(len(sticks)): heappush(minHeap, sticks[i])

        cost, currCost = 0, 0
        while len(minHeap) > 1:
            currCost = heappop(minHeap) + heappop(minHeap)
            cost += currCost
            heappush(minHeap, currCost)

        return cost 