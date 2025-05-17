class Solution:
    def canPermutePalindrome(self, s: str) -> bool:
        freq = {}
        for i in range(len(s)): freq[s[i]] = freq.get(s[i], 0) + 1
        odd = 0
        for k, v in freq.items():
            if v % 2 != 0: odd += 1
            if odd > 1: return False
        
        return odd <= 1