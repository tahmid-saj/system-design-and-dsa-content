class Solution:
    def __init__(self, capacity):
        self.stk = []
        self.capacity = capacity

    def push(self, val):
        if len(self.stk) == 0 or len(self.stk[-1]) == self.capacity:
            self.stk.append([val])
            return
        self.stk[-1].append(val)

    def pop(self):
        if len(self.stk) == 0: return None
        res = self.stk[-1].pop()
        if len(self.stk[-1]) == 0: self.stk.pop()
        return res

    def popAt(self, index):
        if len(self.stk) == 0: return None
        return self.leftShift(index, True)
    
    # rollover the bottom values from the next stacks onto the current stack's top at index where the top was popped
    def leftShift(self, index, removeTop):
        stack = self.stk[index]
        removedItem = None
        if removeTop: removedItem = stack.pop()
        else: removedItem = self.removeBottom(index)

        if len(self.stk[index]) == 0: del self.stk[index]
        else:
            val = self.leftShift(index + 1, False)
            self.stk[index].append(val)
        
        return removedItem
    
    def removeBottom(self, index):
        return self.stk[index].pop(0)