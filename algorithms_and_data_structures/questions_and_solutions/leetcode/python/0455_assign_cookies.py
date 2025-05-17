class Solution:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        g.sort()
        s.sort()
        
        i = 0
        for j in range(0, len(s)):
            if s[j] >= g[i]:
                i += 1

            if i == len(g): return i

        return i