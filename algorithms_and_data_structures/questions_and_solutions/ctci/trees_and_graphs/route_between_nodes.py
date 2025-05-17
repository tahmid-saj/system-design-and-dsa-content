class Solution:
    def routeBetweenNodes(self, s, e):
        visited = set()
        return self.dfs(s, e, s, visited)
    
    def dfs(self, s, e, node, visited):
        if not node: return False
        if node == e: return True

        visited.add(node)
        for neighbour in node.neighbours:
            if neighbour not in visited: 
                if self.dfs(s, e, neighbour, visited): return True
        return False