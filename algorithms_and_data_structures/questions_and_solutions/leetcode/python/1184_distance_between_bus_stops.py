class Solution:
    def distanceBetweenBusStops(self, distance: List[int], start: int, destination: int) -> int:
        # clockwise
        res1, curr = 0, start
        while curr != destination:
            res1 += distance[curr]
            curr = (curr + 1) % len(distance)

        # counterclockwise
        res2, curr = 0, destination
        while curr != start:
            res2 += distance[curr]
            curr = (curr + 1) % len(distance)
        return min(res1, res2)