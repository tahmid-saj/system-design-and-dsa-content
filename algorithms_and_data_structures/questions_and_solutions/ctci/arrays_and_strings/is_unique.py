class Solution:
    def isUnique(self, s):
        # return self.withSet(s)
        return self.sorting(s)

    def withSet(self, s):
        if len(s) > 128: return False
        seen = set()
        for c in s:
            if c in seen: return False
            seen.add(c)
        return True

    def sorting(self, s):
        if len(s) > 128: return False
        s.sort()
        for i in range(len(s)):
            if i > 0 and s[i - 1] == s[i]: return False
        
        return True