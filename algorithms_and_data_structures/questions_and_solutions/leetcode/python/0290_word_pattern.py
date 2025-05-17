class Solution(object):
    def wordPattern(self, pattern, s):
        """
        :type pattern: str
        :type s: str
        :rtype: bool
        """
        # a -> dog, a -> fish NO
        # a -> dog, b -> dog NO
        # i to traverse through pattern, word to contain substring of s between start and j
        # letterMap
        # traverse through s using j:
        # if s[j] == " " or j == len(s) - 1:
        #   if s[j] == " ": word = s[start:j]
        #   elif j == len(s) - 1: word = s[start:]
        #   if pattern[i] in letterMap.keys() and pattern[i] != word: return False
        #   letterMap[pattern[i]] = word
        #   i += 1, start = j + 1
        # return True
        letterMap, i, start = {}, 0, 0
        for j in range(0, len(s)):
            if i > len(pattern) - 1: return False

            if s[j] == " " or j == len(s) - 1:
                if s[j] == " ": word = s[start:j]
                elif j == len(s) - 1: word = s[start:]
                if pattern[i] in letterMap.keys() and letterMap[pattern[i]] != word: return False
                if word in letterMap.values() and not pattern[i] in letterMap.keys(): return False 
                letterMap[pattern[i]] = word
                i += 1
                start = j + 1

        if i != len(pattern): return False

        return True