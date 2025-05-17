class Solution:
    def isOneEditDistance(self, s: str, t: str) -> bool:
        # loop through s and t using i and j respectively
        #   if len(s) < len(t) and s[i] != t[j]: j -= 1, editDistance = True
        #   elif len(s) > len(t) and s[i] != t[j]: i -= 1, editDistance = True
        #   elif len(s) == len(t) and s[i] != t[j], i -= 1, j -= 1, editDistance = True
        #   else: i -= 1, j -= 1
        if s == t: return False
        if abs(len(s) - len(t)) > 1: return False
        if (len(s) == 1 and t == "") or (len(t) == 1 and s == ""): return True

        editDistance, i, j = False, len(s) - 1, len(t) - 1
        while i > -1 and j > -1:
            if editDistance == True and s[i] != t[j]: return False
            if s[i] != t[j]:
                if len(s) < len(t) and s[i] != t[j]: 
                    j -= 1
                elif len(s) > len(t) and s[i] != t[j]: 
                    i -= 1
                elif len(s) == len(t) and s[i] != t[j]:
                    i -= 1
                    j -= 1
                editDistance = True
            else: 
                i -= 1
                j -= 1
        if editDistance == False and abs(i - j) == 1: return True
        
        return i == -1 and j == -1