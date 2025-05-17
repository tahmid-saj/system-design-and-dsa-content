class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        res, stk = 0, []
        for token in tokens:
            if token in "+-/*":
                num1 = stk.pop()
                num2 = stk.pop()
                if token == "+": stk.append(num1 + num2)
                elif token == "-": stk.append(num2 - num1)
                elif token == "/": stk.append(int(num2 / num1))
                elif token == "*": stk.append(num1 * num2)
            else: stk.append(int(token))
        
        return stk[-1]