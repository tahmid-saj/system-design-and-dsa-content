class Solution:
    def sinusoidalString(self, s):
        res = []
        # peaks: loop through s from 1 to len(s) in increments of 4 and append to res
        # middle: loop through s from 0 to len(s) in increments of 2
        # troughs: loop through s from 3 to len(s) in increments of 4 and append to res
        i = 1
        while i < len(s):
            res.append(s[i])
            i += 4
        
        i = 0
        while i < len(s):
            res.append(s[i])
            i += 2
        
        i = 3
        while i < len(s):
            res.append(s[i])
            i += 4

        return "".join(res)