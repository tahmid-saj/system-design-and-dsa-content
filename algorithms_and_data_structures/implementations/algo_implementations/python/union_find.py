class UnionFind:
  def __init__(self, n):
    self.parent = [i for i in range(n)]
    
  def find(self, i):
    if self.parent[i] == i: return i
    return self.find(self.parent[i])

  def union(self, i, j):
    iRep = self.find(i)
    jRep = self.find(j)
    
    if iRep == jRep: return
    
    self.parent[iRep] = jRep
    
class UnionFindOptimized:
  def __init__(self, n):
    self.rank = [1 for _ in range(n)]
    self.parent = [i for i in range(n)]
  
  def find(self, i):
    if self.parent[i] != i: self.parent[i] = self.find(self.parent[i])
    return self.parent[i]
  
  def union(self, i, j):
    iRep = self.find(i)
    jRep = self.find(j)
    
    if iRep == jRep: return
    
    if self.rank[iRep] < self.rank[jRep]: self.parent[iRep] = jRep
    elif self.rank[iRep] > self.rank[jRep]: self.parent[jRep] = iRep
    else:
      self.parent[iRep] = jRep
      self.rank[jRep] += 1