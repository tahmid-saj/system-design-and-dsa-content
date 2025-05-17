class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        stk, res = [], ""
        for i in range(len(s)):
            if len(stk) >= 1: res += s[i]
            if s[i] == "(": stk.append("(")
            else: stk.pop()
            if len(stk) == 0: res = res[:-1]
        return res