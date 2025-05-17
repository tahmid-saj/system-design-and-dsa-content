from collections import deque
class Vertex:
    def __init__(self):
        self.d = -1
        self.edges = []

class Solution:
    def makingWiredConnections(self, graph):
        for vertex in graph:
            if not self.bfs(graph, vertex): return False
        return True

    def bfs(self, graph, vertex):
        vertex.d = 0
        queue = deque([vertex])
        while queue:
            node = queue.popleft()
            for neighbour in node.edges:
                if neighbour.d == node.d: return False
                if neighbour.d == -1: neighbour.d = node.d + 1
        return True