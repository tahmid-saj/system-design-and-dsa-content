import heapq
import math

def dijkstra(graph, start):
  # graph is an adjacency list containing (neighbor, weight) tuples
  # start is the start node
  
  # we'll find the distance from the start node to every node in the graph
  distances = {node: math.inf for node in graph}
  distances[start] = 0
  pq = [(0, start)] # minheap as a priority queue containing (distance, node). we use a minheap to find the closest neighbor and process it first
  
  while pq:
    currDistance, node = heapq.heappop(pq)
    
    # skip this node if we already found a shorter distance
    if currDistance > distances[node]: continue
    
    for neighbor, weight in graph[node]:
      distance = currDistance + weight
      
      if distance < distances[neighbor]:
        distances[neighbor] = distance
        heapq.heappush(pq, (distance, neighbor))
  
  return distances

# time complexity: O((V + E)logV) since we process all vertices + edges using the heap, we have VlogV + ElogV = (V + E)logV
# space complexity: O(V + E) since we store the vertices in the distances dictionary and also store the vertices in the pq. 
# If we consider the edges inside the adj list, then we have O(V + E)

def dijkstraShortestPath(graph, start, target):  
  # graph is an adjacency list containing (neighbor, weight) tuples
  # start is the start node, target is the target node
  
  distances = {node: math.inf for node in graph}
  distances[start] = 0
  pq = [(0, start)]
  parents = {node: None for node in graph} # to construct the path
  
  while pq:
    currDistance, node = heapq.heappop(pq)
    
    if node == target: break
    if currDistance > distances[node]: continue
    
    for neighbor, weight in graph[node]:
      distance = currDistance + weight
      
      if distance < distances[neighbor]:
        distances[neighbor] = distance
        heapq.heappush(pq, (distance, neighbor))
        
        parents[neighbor] = node
  
  if distances[target] == math.inf: return math.inf, [] # there is no possible path between start and target
  
  path = []
  curr = target
  while curr:
    path.append(curr)
    curr = parents[curr]
  
  return distances[target], path[::-1]

# time complexity: O((V + E)logV)
# space complexity: O(V + E)

# TESTS --------------------------------------------------------------------------

# DIJKSTRA

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 6)],
    'C': [('A', 4), ('B', 2), ('D', 3)],
    'D': [('B', 6), ('C', 3)],
}

print(dijkstra(graph, "A"))
print(dijkstraShortestPath(graph, "A", "D"))