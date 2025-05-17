class Solution:
    def longestPalindrome(self, s: str) -> int:
        from collections import Counter

        letters = Counter(s)

        res, odd = 0, False
        for i, v in letters.items():
            if v % 2 == 0: res += v
            else:
                res += v - 1
                odd = True
        
        if odd == True: res += 1
        return res