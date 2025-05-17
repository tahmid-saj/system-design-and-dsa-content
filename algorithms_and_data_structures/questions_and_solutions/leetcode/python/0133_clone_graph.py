"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node == None: return None
        if len(node.neighbors) == 0: return Node(node.val, [])
        clones = {}
        # self.iterativeDFS(node, clones)
        # self.iterativeBFS(node, clones)
        self.recursiveDFS(node, clones)
        return clones[node]
    
    def iterativeDFS(self, node, clones):
        stk = [node]
        clones[node] = Node(node.val, [])
        
        while stk:
            node = stk.pop()
            for neighbor in node.neighbors:
                if neighbor not in clones:
                    clones[neighbor] = Node(neighbor.val, [])
                    stk.append(neighbor)
                clones[node].neighbors.append(clones[neighbor])
    
    def recursiveDFS(self, node, clones):
        if not node: return None
        if node in clones: return clones[node]
        clones[node] = Node(node.val, [])

        for neighbor in node.neighbors:
            clone = self.recursiveDFS(neighbor, clones)
            clones[node].neighbors.append(clone)
        
        return clones[node]
    
    def iterativeBFS(self, node, clones):
        queue = deque([node])
        clones[node] = Node(node.val, [])

        while queue:
            node = queue.popleft()
            for neighbor in node.neighbors:
                if neighbor not in clones:
                    clones[neighbor] = Node(neighbor.val, [])
                    queue.append(neighbor)
                clones[node].neighbors.append(clones[neighbor])