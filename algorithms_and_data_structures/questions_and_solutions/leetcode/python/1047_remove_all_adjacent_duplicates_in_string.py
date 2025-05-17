class Solution:
    def removeDuplicates(self, s: str) -> str:
        stk = []

        for i in range(len(s)):
            if stk and stk[-1] == s[i]: stk.pop()
            else: stk.append(s[i])
        
        return "".join(stk)