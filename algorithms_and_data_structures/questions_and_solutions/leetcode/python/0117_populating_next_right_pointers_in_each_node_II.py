"""
# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next
"""

class Solution:
    def connect(self, root: 'Node') -> 'Node':
        # return self.bfs(root)
        return self.constantSpace(root)
    
    def bfs(self, root):
        if not root: return None
        prev, queue = None, deque([root])

        while queue:
            queueLength = len(queue)
            prev = None
            for _ in range(queueLength):
                node = queue.popleft()
                node.next = prev
                prev = node
                if node.right: queue.append(node.right)
                if node.left: queue.append(node.left)

        return root
    
    def constantSpace(self, root):
        if root == None: return None

        def helper(prev, node, leftMost):
            if prev: prev.next = node
            else: leftMost = node
            prev = node

            return prev, leftMost

        leftMost = root

        while leftMost:
            prev, curr = None, leftMost
            leftMost = None

            while curr:
                if curr.left: prev, leftMost = helper(prev, curr.left, leftMost)
                if curr.right: prev, leftMost = helper(prev, curr.right, leftMost)
                curr = curr.next
        
        return root