class Node:
  def __init__(self, val, next=None):
    self.val = val
    self.next = next

class Stack:
  def __init__(self):
    self.top = None
  
  def push(self, val):
    node = self.Node(val)
    node.next = self.top
    self.top = node
    
  def pop(self):
    if self.top is None: return None
    val = self.top.val
    self.top = self.top.next
    return val
  
  def peek(self):
    if self.top is None: return None
    return self.top.val
  
  def isEmpty(self):
    return self.top is None