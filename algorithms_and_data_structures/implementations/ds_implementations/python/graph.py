from collections import defaultdict

class GraphUndirected:
  def __init__(self):
    self.adjacencyList = defaultdict(list)
  
  def addVertex(self, vertex):
    if vertex not in self.adjacencyList: self.adjacencyList[vertex] = []
  
  def removeVertex(self, vertex):
    if vertex not in self.adjacencyList: return
    self.adjacencyList.pop(vertex)
    for neighbors in self.adjacencyList.values():
      if vertex in neighbors: neighbors.remove(vertex)
  
  def addEdge(self, vertex1, vertex2):
    self.adjacencyList[vertex1].append(vertex2)
    self.adjacencyList[vertex2].append(vertex1)
  
  def removeEdge(self, vertex1, vertex2):
    self.adjacencyList[vertex1].remove(vertex2)
    self.adjacencyList[vertex2].remove(vertex1)
  
  def getVertices(self):
    return list(self.adjacencyList.keys())

  def getEdges(self):
    edges = []
    for vertex, neighbors in self.adjacencyList.items():
      for neighbor in neighbors:
        edges.append((vertex, neighbor))
    
    return edges

  def getNeighbors(self, vertex):
    return self.adjacencyList[vertex]
  
  def isAdjacent(self, vertex1, vertex2):
    return vertex2 in self.adjacencyList[vertex1]

  def getVertexCount(self):
    return len(self.adjacencyList)
  
  def getEdgeCount(self):
    count = sum(len(neighbors) for neighbors in self.adjacencyList.values())
    return count // 2