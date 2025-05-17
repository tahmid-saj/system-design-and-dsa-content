class Solution:
    def largeGroupPositions(self, s: str) -> List[List[int]]:
        start, end, res = 0, 0, []
        while end < len(s):
            if s[end] != s[start]:
                if end - start > 2: res.append([start, end - 1])
                start = end
            end += 1
        if end - start > 2: res.append([start, end - 1])
        return res