class GraphUndirected:
  def __init__(self, vertices):
    self.vertices = vertices
    self.adjList = [[] for _ in range(vertices)]
  
  def addEdge(self, u, v):
    self.adjList[u].append(v)
    self.adjList[v].append(u)
  
  def dfsIterative(self, start):
    visited = [False for _ in range(self.vertices)]
    stack = [start]
    visited[start] = True
    
    while stack:
      node = stack.pop()
      
      for neighbor in self.adjList[node]:
        if not visited[neighbor]:
          stack.append(neighbor)
          visited[neighbor] = True
  
  def dfsRecursive(self, start):
    visited = [False for _ in range(self.vertices)]
    self.dfs(start, visited)
  
  def dfs(self, vertex, visited):
    visited[vertex] = True
    
    for neighbor in self.adjList[vertex]:
      if not visited[neighbor]:
        self.dfs(neighbor, visited)

# Time complexity: O(V + E) from visiting all vertices + edges
# Space complexity: O(V) from the stack in iterative approach + call stack in recursive approach