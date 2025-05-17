class Stack:
  def __init__(self, size):
    self.stk = [None] * size
    # Initialize the top pointer to -1, indicating an empty stack
    self.top = -1
  
  def push(self, val):
    if self.top == len(self.stk) - 1: return None
    self.top += 1
    self.stk[self.top] = val
  
  def pop(self):
    if self.isEmpty(): return None
    val = self.stk[self.top]
    self.stk[self.top] = None
    self.top -= 1
    return val

  def peek(self):
    if self.isEmpty(): return None
    return self.stk[self.top]
  
  def isEmpty(self):
    return self.top == -1