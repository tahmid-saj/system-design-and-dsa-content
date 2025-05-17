class Solution:
    def lengthOfLongestSubstringTwoDistinct(self, s: str) -> int:
        freq, start, res = {}, 0, 0

        for end in range(0, len(s)):
            freq[s[end]] = freq.get(s[end], 0) + 1

            while len(freq) > 2:
                freq[s[start]] -= 1
                if freq[s[start]] == 0: freq.pop(s[start])
                start += 1

            res = max(res, end - start + 1)
        
        return res