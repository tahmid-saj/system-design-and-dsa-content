class Solution:
    def validPalindrome(self, s: str) -> bool:
        i, j = 0, len(s) - 1
        while i < j:
            if s[i] != s[j]: return self.isPalindrome(s, i + 1, j) or self.isPalindrome(s, i, j - 1)
            i += 1
            j -= 1
        return True
    
    def isPalindrome(self, s, i, j):
        while i < j:
            if s[i] != s[j]: return False
            i += 1
            j -= 1
        return True