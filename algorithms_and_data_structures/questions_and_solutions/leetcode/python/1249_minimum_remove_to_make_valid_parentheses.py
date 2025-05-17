class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        stk = []
        s = list(s)
        for i in range(len(s)):
            if stk and s[i] == ")" and stk[-1][0] == "(": stk.pop()
            elif s[i] == "(" or s[i] == ")": stk.append((s[i], i))
        
        while stk: s[stk.pop()[1]] = ""

        return "".join(s)