class Solution(object):
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        # loop through haystack using i, and needle using j:
        # -> if haystack[i] == needle[j]: j++, start = i
        # -> if haystack[i] != needle[j]: j = 0, i = start
        # -> if j == len(needle): return start
        # return -1
        i, j, start = 0, 0, 0
        while i < len(haystack):
            if haystack[i] == needle[j]:
                if j == 0: start = i
                j += 1
                print(j)
            elif haystack[i] != needle[j]:
                if j > 0: i = start
                j = 0

            if j == len(needle): return start
            i += 1
        
        return -1