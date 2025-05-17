class Solution:
    def checkValidString(self, s: str) -> bool:
        return self.greedy(s)
    
    def greedy(self, s):
        # find the balance range (possible number of open "(" brackets)
        lo, hi, = 0, 0
        for i in range(len(s)):
            if s[i] == "(": lo += 1
            else: lo -= 1

            if s[i] != ")": hi += 1
            else: hi -= 1
            
            if hi < 0: break
            lo = max(lo, 0)
        
        return lo == 0