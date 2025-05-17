class Solution(object):
    def reverseVowels(self, s):
        """
        :type s: str
        :rtype: str
        """
        if len(s) == 1: return s

        sList = list(s)
        l, r = 0, len(s) - 1
        while l < r:
            if not sList[l] in "aeiouAEIOU": l += 1
            if not sList[r] in "aeiouAEIOU": r -= 1
            if sList[l] in "aeiouAEIOU" and sList[r] in "aeiouAEIOU": 
                sList[l], sList[r] = sList[r], sList[l]
                l += 1
                r -= 1
        return "".join(sList)