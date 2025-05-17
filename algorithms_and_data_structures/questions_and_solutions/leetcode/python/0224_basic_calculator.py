class Solution:
    def calculate(self, s: str) -> int:
        stk, currNum, sign, res = [], 0, 1, 0

        for i in range(len(s)):
            if s[i].isnumeric():
                currNum *= 10
                currNum += int(s[i])
            elif s[i] in "+-":
                res += currNum * sign
                sign = 1
                if s[i] == "-": sign = -1
                currNum = 0
            elif s[i] == "(":
                stk.append(res)
                stk.append(sign)
                res = 0

                sign = 1
                currNum = 0
            elif s[i] == ")":
                res += currNum * sign
                res *= stk.pop()
                res += stk.pop()

                sign = 1
                currNum = 0
        
        return res + (currNum * sign)