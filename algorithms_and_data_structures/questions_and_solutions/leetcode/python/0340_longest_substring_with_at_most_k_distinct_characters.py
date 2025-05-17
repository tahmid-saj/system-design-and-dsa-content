class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        if len(s) <= k: return len(s)
        maxLength, windowStart = 0, 0
        characters = {}

        for windowEnd in range(0, len(s)):
            characters[s[windowEnd]] = characters.get(s[windowEnd], 0) + 1
            if len(characters) == k: maxLength = max(maxLength, windowEnd - windowStart + 1)

            while len(characters) > k:
                if characters[s[windowStart]] == 1: characters.pop(s[windowStart])
                else: characters[s[windowStart]] -= 1
                windowStart += 1

        return maxLength