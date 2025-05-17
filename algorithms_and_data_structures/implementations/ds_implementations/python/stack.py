class Stack:
  def __init__(self):
    self.stk = []
  
  def isEmpty(self):
    return self.stk == []

  def push(self, val):
    self.stk.append(val)
  
  def pop(self):
    if self.isEmpty(): return None
    return self.stk.pop()

  def peek(self):
    if self.isEmpty(): return None
    return self.stk[-1]