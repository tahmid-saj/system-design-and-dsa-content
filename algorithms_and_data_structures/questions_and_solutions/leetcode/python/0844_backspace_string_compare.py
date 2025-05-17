class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        i, j = len(s) - 1, len(t) - 1

        while i >= 0 or j >= 0:
            i = self.findIndex(s, i)
            j = self.findIndex(t, j)

            if i < 0 and j < 0: return True
            elif i < 0 or j < 0: return False
            elif s[i] != t[j]: return False

            i -= 1
            j -= 1
        
        return True

    def findIndex(self, s, i):
        backspaces = 0

        while i >= 0:
            if s[i] == "#": backspaces += 1
            elif backspaces > 0: backspaces -= 1
            else: break

            i -= 1

        return i