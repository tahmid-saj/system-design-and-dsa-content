class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        maxLength, windowStart, maxCharKey, maxCharValue = 0, 0, "", 0
        characters = {}
        # move windowEnd from (0, len(s)):
        # add s[windowEnd] to characters
        # if len(characters) <= 2:
        #   looping through characters, there exists at least one key with a value <= k: maxLength = max(maxLength, window - windowStart + 1)
        # while len(characters) > 2:
        #   decrement character key's value or remove
        #   windowStart -= 1
        for windowEnd in range(0, len(s)):
            characters[s[windowEnd]] = characters.get(s[windowEnd], 0) + 1
            if characters[s[windowEnd]] >= maxCharValue:
                maxCharValue = characters[s[windowEnd]]
                maxCharKey = s[windowEnd]

            # if the sum of all the characters' key's values excluding the character's key with max value > k: then do the following
            while (windowEnd - windowStart + 1 - maxCharValue) > k:
                if characters[s[windowStart]] == 1:
                    characters.pop(s[windowStart])
                else:
                    characters[s[windowStart]] -= 1
                windowStart += 1
            
            maxLength = max(maxLength, windowEnd - windowStart + 1)

        return maxLength