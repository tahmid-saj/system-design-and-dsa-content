class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        if k == 1: return ""
        stk, res = [], ""

        for i in range(0, len(s)):
            if len(stk) > 0 and stk[-1][0] == s[i]:
                stk[-1][1] += 1
            else: stk.append([s[i], 1])
            if len(stk) > 0 and stk[-1][1] == k: stk.pop()

        for i in range(0, len(stk)):
            e = stk.pop()
            res += e[0] * e[1]
        
        return res[::-1]