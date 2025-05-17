class Solution:
    def isValid(self, s: str) -> bool:
        stk = []
        for p in s:
            if p in "([{": stk.append(p)
            elif p == ")" and stk and stk[-1] == "(": stk.pop()
            elif p == "]" and stk and stk[-1] == "[": stk.pop()
            elif p == "}" and stk and stk[-1] == "{": stk.pop()
            else: return False
        return len(stk) == 0