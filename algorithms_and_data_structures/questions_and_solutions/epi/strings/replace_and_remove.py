class Solution:
    def replaceAndRemove(self, size, s):
        if len(s) == 0: return s
        # a b a c _
        # a a c _ _
        # a a _ _ c
        # a a d d c
        # d d d d c
        # remove b first
        i, a = 0, 0
        for j in range(size):
            if s[j] == "a": a += 1
            if s[j] != "b":
                s[i] = s[j]
                i += 1
        
        curr = i - 1
        i += a - 1
        res = i + 1
        while curr >= 0:
            if s[curr] == "a":
                s[i - 1:i + 1] = "dd"
                i -= 2
            elif s[curr] != "a":
                s[i] = s[curr]
                i -= 1
            curr -= 1

        return res
        
