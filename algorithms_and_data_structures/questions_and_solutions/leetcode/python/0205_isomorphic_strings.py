class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        if len(s) != len(t): return False
        match = {}

        for i in range(len(s)):
            if s[i] not in match:
                if t[i] in match.values(): return False
                match[s[i]] = t[i]
            else:
                if match[s[i]] != t[i]: return False
        
        return True