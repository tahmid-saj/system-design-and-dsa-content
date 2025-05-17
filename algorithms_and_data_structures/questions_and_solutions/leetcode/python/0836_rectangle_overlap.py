class Solution:
    def isRectangleOverlap(self, rec1: List[int], rec2: List[int]) -> bool:
        d1, b1 = (rec1[0], rec1[1]), (rec1[2], rec1[3])
        a1, c1 = (rec1[0], rec1[1] + (rec1[3] - rec1[1])), (rec1[2], rec1[3] - (rec1[3] - rec1[1]))
        d2, b2 = (rec2[0], rec2[1]), (rec2[2], rec2[3])
        a2, c2 = (rec2[0], rec2[1] + (rec2[3] - rec2[1])), (rec2[2], rec2[3] - (rec2[3] - rec2[1]))

        if (c1[0] <= d2[0] or c2[0] <= d1[0]) or (c1[1] >= b2[1] or b1[1] <= c2[1]): return False
        return True