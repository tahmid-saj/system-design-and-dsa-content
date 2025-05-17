"""
# Definition for a Node.
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children
"""

class Solution:
    def maxDepth(self, root: 'Node') -> int:
        # dfs
        if root == None: return 0

        queue = deque()
        queue.append((root, 1))
        maxDepth = 0
        
        while len(queue) > 0:
            currNode, currVal = queue.popleft()
            maxDepth = currVal
            if len(currNode.children) > 0:
                for child in currNode.children:
                    queue.append((child, currVal + 1))

        return maxDepth