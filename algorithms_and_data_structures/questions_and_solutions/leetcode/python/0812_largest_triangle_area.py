class Solution:
    def largestTriangleArea(self, points: List[List[int]]) -> float:
        # Area = (1/2) * |x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)|
        res = 0
        for x1, y1 in points:
            for x2, y2 in points:
                for x3, y3 in points:
                    area = 0.5 * abs( (x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2)) )
                    res = max(res, area)
        return res