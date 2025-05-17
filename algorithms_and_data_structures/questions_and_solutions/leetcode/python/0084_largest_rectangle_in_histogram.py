class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stk, res = [], 0
        for i, h in enumerate(heights + [0]):
            while stk and heights[stk[-1]] >= h:
                height = heights[stk.pop()]
                width = i if len(stk) == 0 else i - stk[-1] - 1
                res = max(res, width * height)
            stk.append(i)
        return res