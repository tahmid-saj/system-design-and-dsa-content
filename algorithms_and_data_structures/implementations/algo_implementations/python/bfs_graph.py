from collections import defaultdict, deque

class GraphUndirected:
  def __init__(self, vertices):
    self.vertices = vertices
    self.adjList = defaultdict(list)
  
  def addEdge(self, u, v):
    self.adjList[u].append(v)
    self.adjList[v].append(u)
  
  def bfs(self, start):
    visited = [False for _ in range(self.vertices)]
    queue = deque([start])
    visited[start] = True
    
    while queue:
      node = queue.popleft()
      
      for neighbor in self.adjList[node]:
        if not visited[neighbor]:
          queue.append(neighbor)
          visited[neighbor] = True

# Time complexity: O(V + E) from visiting all vertices + edges
# Space complexity: O(V) from the queue in iterative approach