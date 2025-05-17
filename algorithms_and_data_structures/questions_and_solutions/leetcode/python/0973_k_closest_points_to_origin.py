class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        maxHeap = []
        for i in range(k): heappush(maxHeap, (-1 * ((math.pow(points[i][0], 2) +  math.pow(points[i][1], 2))), points[i]))

        for i in range(k, len(points)):
            distance = (math.pow(points[i][0], 2) +  math.pow(points[i][1], 2))
            if -maxHeap[0][0] > distance:
                heappop(maxHeap)
                heappush(maxHeap, (-distance, points[i]))
        
        result = []
        while len(maxHeap) > 0:
            result.append(heappop(maxHeap)[1])
        
        return result