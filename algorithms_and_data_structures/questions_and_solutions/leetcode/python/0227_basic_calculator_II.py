class Solution:
    def calculate(self, s: str) -> int:
        return self.stack(s)
        # return self.withoutStack(s)
    
    def stack(self, s):
        if not s: return 0
        stk, num, op = [], 0, "+"

        for i in range(len(s)):
            if s[i].isnumeric(): num = (num * 10) + int(s[i])
            if (not s[i].isnumeric() and s[i] != " ") or i == len(s) - 1:
                # op refers to the previous operation, not the current one
                if op == "+": stk.append(num)
                elif op == "-": stk.append(-num)
                elif op == "/": stk.append(int(stk.pop() / num))
                elif op == "*": stk.append(stk.pop() * num)
                num = 0
                op = s[i]
        
        res = 0
        while stk: res += stk.pop()
        return res
    
    def withoutStack(self, s):
        if not s or len(s) == 0: return 0
        num, lastNum, res, operation = 0, 0, 0, "+"

        for i in range(len(s)):
            curr = s[i]
            if curr.isnumeric(): num = (num * 10) + int(curr)
            if (not curr.isnumeric() and curr != " ") or i == len(s) - 1:
                # operation is the previous operator, not the current
                if operation == "-":
                    res += lastNum
                    lastNum = -num
                elif operation == "+":
                    res += lastNum
                    lastNum = num
                elif operation == "*": lastNum = lastNum * num
                elif operation == "/": lastNum = int(lastNum / num)
                operation = curr
                num = 0
        
        res += lastNum
        return res