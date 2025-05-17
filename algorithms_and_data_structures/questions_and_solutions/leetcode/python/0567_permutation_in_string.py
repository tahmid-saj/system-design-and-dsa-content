class Solution:
    def checkInclusion(self, pattern: str, str1: str) -> bool:
        windowStart, matched = 0, 0
        characters = {}
        for i in range(0, len(pattern)): characters[pattern[i].lower()] = characters.get(pattern[i].lower(), 0) + 1 

        for windowEnd in range(0, len(str1)):
            if str1[windowEnd] in characters:
                characters[str1[windowEnd]] -= 1
                if characters[str1[windowEnd]] == 0: matched += 1

            if matched == len(characters): return True

            if windowEnd >= len(pattern) - 1:
                if str1[windowStart] in characters:
                    if characters[str1[windowStart]] == 0: matched -= 1
                    characters[str1[windowStart]] += 1
                windowStart += 1
            
        return False