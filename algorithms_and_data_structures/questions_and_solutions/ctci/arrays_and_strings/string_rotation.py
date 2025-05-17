class Solution:
    def stringRotation(self, s1, s2):
        return len(s1) == len(s2) and self.isSubstring(s1, s2 + s2)
    
    def isSubstring(self, sub, s):
        pass