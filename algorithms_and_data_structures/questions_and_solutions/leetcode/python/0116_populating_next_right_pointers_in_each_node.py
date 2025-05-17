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
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        # return self.bfs(root)
        return self.constantSpace(root)

    def bfs(self, root):
        if root == None: return None
        queue = deque([root])

        while queue:
            length = len(queue)
            prev = None
            for i in range(length):
                node = queue.popleft()
                node.next = prev
                prev = node

                if node.right: queue.append(node.right)
                if node.left: queue.append(node.left)
        
        return root

    def constantSpace(self, root):
        if root == None: return None
        leftMost = root

        while leftMost.left:
            node = leftMost

            while node:
                node.left.next = node.right
                if node.next: node.right.next = node.next.left

                node = node.next
        
            leftMost = leftMost.left
    
        return root