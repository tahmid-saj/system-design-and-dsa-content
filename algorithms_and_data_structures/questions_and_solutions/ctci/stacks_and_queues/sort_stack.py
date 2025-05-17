class Solution:
    # maintaining sorted order of stack
    def __init__(self):
        self.stk = []
    
    def push(self, val):
        if len(self.stk) == 0: 
            self.stk.append(val)
            return
        
        tmp = []
        while self.stk[-1] < val: tmp.append(self.stk.pop())
        self.stk.append(val)
        while tmp: self.stk.append(tmp.pop())

    def pop(self):
        if len(self.stk) == 0: return None
        return self.stk.pop()

    def peek(self):
        if len(self.stk) == 0: return None
        return self.stk[-1]
    
    # sorting a stack using another temporary stack
    def sort(self, stk):
        tmpStk = []
        while len(stk) > 0:
            stkTop = stk.pop()
            while len(tmpStk) > 0 and tmpStk[-1] > stkTop: stk.append(tmpStk.pop())
            tmpStk.append(stkTop)
        
        while tmpStk: stk.append(tmpStk.pop())