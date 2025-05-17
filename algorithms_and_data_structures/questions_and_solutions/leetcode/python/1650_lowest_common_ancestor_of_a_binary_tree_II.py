"""
# Definition for a Node.
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
"""
class Solution:
    def lowestCommonAncestor(self, p: 'Node', q: 'Node') -> 'Node':
        depthP, depthQ = self.depth(p), self.depth(q)
        if depthP < depthQ: p, q = q, p

        for _ in range(abs(depthP - depthQ)): p = p.parent

        while p != q:
            p = p.parent
            q = q.parent
        
        return q
        
    def depth(self, node):
        res = 0
        while node.parent:
            res += 1
            node = node.parent
        return res