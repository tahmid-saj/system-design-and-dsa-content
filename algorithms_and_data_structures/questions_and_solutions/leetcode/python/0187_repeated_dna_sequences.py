class Solution:
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        if len(s) < 10: return []
        start, seen, res = 0, set(), set()

        for end in range(9, len(s)):
            curr = s[start: end + 1]
            if curr in seen: res.add(curr)

            seen.add(curr)
            start += 1
        
        return list(res)