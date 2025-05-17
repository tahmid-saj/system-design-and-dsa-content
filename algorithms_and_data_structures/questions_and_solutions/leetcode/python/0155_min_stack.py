class MinStack:

    def __init__(self):
        self.stk = []
        
    def push(self, val: int) -> None:
        currMin = val
        if self.stk: currMin = min(self.stk[-1][1], val)
        self.stk.append((val, currMin))

    def pop(self) -> None:
        self.stk.pop()

    def top(self) -> int:
        return self.stk[-1][0]

    def getMin(self) -> int:
        return self.stk[-1][1]

# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()