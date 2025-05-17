class Solution(object):
    def findTheDifference(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        if s == "": return t

        s = sorted(s)
        t = sorted(t)

        for i in range(0, len(s)):
            if s[i] != t[i]: return t[i]

        return t[-1]