class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if s == t or len(s) == 0: return True
        if len(s) > len(t): return False

        i = 0
        for j in range(0, len(t)):
            if s[i] == t[j]: i += 1
            if i == len(s): return True

        return i == len(s)