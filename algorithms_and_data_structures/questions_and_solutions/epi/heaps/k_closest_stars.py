import math
from heapq import *
class Solution:
    def kClosestStars(self, stars, k):
        maxHeap = []
        for i in range(k): 
            distance = math.sqrt((stars[i][0])**2 + (stars[i][1])**2 + (stars[i][2])**2)
            heappush(maxHeap, (-distance, stars[i]))
        
        for i in range(k, len(stars)):
            distance = math.sqrt((stars[i][0])**2 + (stars[i][1])**2 + (stars[i][2])**2)
            if distance < -maxHeap[0][0]:
                heappop(maxHeap)
                heappush(maxHeap, (-distance, stars[i]))
        
        res = []
        while maxHeap:
            _, star = heappop(maxHeap)
            res.append(star)
        return res