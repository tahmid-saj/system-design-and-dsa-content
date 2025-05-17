class OrderedSet:
  def __init__(self):
    self.set = set()
    self.nums = []
  
  def add(self, x):
    if x not in self.set:
      self.set.add(x)
      self.nums.append(x)
      self.nums.sort()
  
  def findByOrder(self, i):
    if i < 0 or i >= len(self.set): return None
    return self.nums[i]

  def orderOfKey(self, x):
    return sum(1 for val in self.nums if val < x)