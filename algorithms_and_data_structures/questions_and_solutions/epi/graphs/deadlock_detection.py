class Vertex:
    WHITE, GRAY, BLACK = range(3)
    def __init__(self):
        self.colour = Vertex.WHITE
        self.edges = []

class Solution:
    def deadlockDetection(self, graph):
        for vertex in graph:
            if vertex.colour == Vertex.WHITE and self.dfs(graph, vertex): return True
        return False
    
    def dfs(self, graph, vertex):
        if vertex.colour == Vertex.GRAY: return True
        vertex.colour = Vertex.GRAY

        for neighbour in vertex.edges:
            if neighbour.colour != Vertex.BLACK and self.dfs(graph, neighbour): return True
        vertex.colour = Vertex.BLACK
        return False