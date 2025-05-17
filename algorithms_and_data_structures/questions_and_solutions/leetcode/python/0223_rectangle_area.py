class Solution:
    def computeArea(self, ax1: int, ay1: int, ax2: int, ay2: int, bx1: int, by1: int, bx2: int, by2: int) -> int:
        areaA, areaB = (ax2 - ax1) * (ay2 - ay1), (bx2 - bx1) * (by2 - by1)
        if ax2 <= bx1 or bx2 <= ax1 or ay2 <= by1 or ay1 >= by2: return areaA + areaB

        xLength, yLength = 0, 0
        if ax2 > bx1 or bx2 > ax1: xLength = min(ax2, bx2) - max(ax1, bx1)
        if by2 > ay1 or ay2 > by1: yLength = min(ay2, by2) - max(ay1, by1)

        return areaA + areaB - (xLength * yLength)