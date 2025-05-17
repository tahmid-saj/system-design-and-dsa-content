from heapq import *
class Solution:
    def minRefuelStops(self, target: int, startFuel: int, stations: List[List[int]]) -> int:
        pq = []
        stations.append((target, math.inf))

        res = prev = 0
        tank = startFuel
        for location, capacity in stations:
            tank -= location - prev
            while pq and tank < 0:
                tank += -heappop(pq)
                res += 1
            if tank < 0: return -1
            heappush(pq, -capacity)
            prev = location
        
        return res