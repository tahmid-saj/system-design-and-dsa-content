class Solution(object):
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        s = s.lower()
        # loop through s using i (0, len(s), 1) and j (len(s) - 1, -1, -1):
        # if s[i] is not an alphanumeric: i++
        # if s[j] is not an alphanumeric: j--
        # if both s[i] and s[j] are alphanumeric and s[i] != s[j]: return False
        # return True
        i, j = 0, len(s) - 1
        while i < j:
            if not s[i].isalnum(): i += 1
            if not s[j].isalnum(): j -= 1
            if s[i].isalnum() and s[j].isalnum() and s[i] != s[j]: return False
            elif s[i].isalnum() and s[j].isalnum() and s[i] == s[j]:
                i += 1
                j -= 1
        
        return True