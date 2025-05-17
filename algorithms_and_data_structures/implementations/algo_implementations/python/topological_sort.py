from collections import defaultdict, deque

class TopologicalSortDFS:
  def __init__(self, vertices):
    self.adjList = defaultdict(list)
    self.vertices = vertices
  
  def addEdge(self, u, v):
    self.adjList[u].append(v)
  
  def topologicalSortUtil(self, stk, node, visited):
    visited[node] = True
    
    for neighbor in self.adjList[node]:
      if not visited[neighbor]: self.topologicalSortUtil(stk, neighbor, visited)
    
    stk.append(node)
  
  def topologicalSort(self):
    stk = []
    visited = [False for _ in range(self.vertices)]
    
    for i in range(self.vertices):
      if not visited[i]: self.topologicalSortUtil(stk, i, visited)
    
    return stk[::-1]

class TopologicalSortBFS:
  def __init__(self, vertices):
    self.vertices = vertices
    self.adjList = defaultdict(list)
  
  def addEdge(self, u, v):
    self.adjList[u].append(v)
  
  def topologicalSort(self):
    inDegree = [0 for _ in range(self.vertices)]
    
    for i in range(self.vertices):
      for neighbor in self.adjList[i]: inDegree[neighbor] += 1
    
    queue = deque()
    for i in range(self.vertices):
      if inDegree[i] == 0: queue.append(i)
    
    count = 0
    res = []
    while queue:
      node = queue.popleft()
      res.append(node)
      
      for neighbor in self.adjList[node]:
        inDegree[neighbor] -= 1
        if inDegree[neighbor] == 0: queue.append(neighbor)
      
      count += 1
    
    if count != self.vertices: return None
    
    return res