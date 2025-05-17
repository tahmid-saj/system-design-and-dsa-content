class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        return self.greedy(s)
        # return self.stack(s)

    def greedy(self, s):
        openPs, closePs = 0, 0

        for i in range(len(s)):
            if s[i] == "(": openPs += 1
            elif s[i] == ")":
                if openPs > 0: openPs -= 1
                else: closePs += 1
        
        return openPs + closePs
    
    def stack(self, s):
        stk = []
        closePs = 0

        for i in range(len(s)):
            if s[i] == "(": stk.append(s[i])
            else:
                if stk and stk[-1] == "(": stk.pop()
                else: closePs += 1
        
        return len(stk) + closePs