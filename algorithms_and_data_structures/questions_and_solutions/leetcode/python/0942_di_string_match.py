class Solution:
    def diStringMatch(self, s: str) -> List[int]:
        r, l, res = 0, len(s), []

        for c in s:
            if c == "I":
                res.append(r)
                r += 1
            else:
                res.append(l)
                l -= 1
        
        return res + [l]