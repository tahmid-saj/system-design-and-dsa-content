class Solution:
    def isBoomerang(self, points: List[List[int]]) -> bool:
        # find if there is non-zero area of the triangle
        # A = (1/2) |x1(y2 − y3) + x2(y3 − y1) + x3(y1 − y2)|
        x1, y1 = points[0]
        x2, y2 = points[1]
        x3, y3 = points[2]
        return 0.5 * abs((x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2))) != 0