# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isCousins(self, root: Optional[TreeNode], x: int, y: int) -> bool:
        return self.bfs(root, x, y)
    
    def bfs(self, root, x, y):
        queue = deque([(root, None)])

        while queue:
            nodeLength, xFound, yFound, xParent, yParent = len(queue), False, False, None, None
            for _ in range(nodeLength):
                node, parent = queue.popleft()
                if node.val == x: xFound, xParent = True, parent
                elif node.val == y: yFound, yParent = True, parent
                if xFound and yFound and xParent != yParent: return True

                if node.left: queue.append((node.left, node))
                if node.right: queue.append((node.right, node))
        return False