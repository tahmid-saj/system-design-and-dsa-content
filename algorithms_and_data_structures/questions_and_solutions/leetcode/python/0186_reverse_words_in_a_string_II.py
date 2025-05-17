class Solution:
    def reverseWords(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        if " " not in s: return s
        i, j = 0, len(s) - 1
        while i < j:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -= 1
        
        i = 0
        while i < len(s):
            if i == 0 or s[i] == " ":
                if s[i] == " ": i += 1
                i = self.reverseWord(s, i)
    
    def reverseWord(self, s, start):
        end = start
        while end + 1 < len(s) and s[end + 1] != " ": end += 1
        i = end + 1

        while start < end:
            s[start], s[end] = s[end], s[start]
            start += 1
            end -= 1
        
        return i