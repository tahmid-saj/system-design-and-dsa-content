class Solution:
    def firstUniqChar(self, s: str) -> int:
        freq = {}
        for i in range(len(s)):
            if s[i] in freq: freq[s[i]] = (freq[s[i]][0], freq[s[i]][1] + 1)
            else: freq[s[i]] = (i, 1)

        res = math.inf
        for k, v in freq.items():
            if v[1] == 1: res = min(res, v[0])
        
        if res == math.inf: return -1
        return res