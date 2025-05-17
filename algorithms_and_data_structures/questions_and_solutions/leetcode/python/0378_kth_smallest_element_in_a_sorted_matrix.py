class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        number = 0
        minHeap = []
        for i in range(0, len(matrix)): heapq.heappush(minHeap, (matrix[i][0], i, 0))

        while minHeap and k > 0:
            num, row, index = heapq.heappop(minHeap)
            k -= 1
            if k == 0:
                number = num
                break
            if index + 1 < len(matrix[row]): heapq.heappush(minHeap, (matrix[row][index + 1], row, index + 1))

        return number