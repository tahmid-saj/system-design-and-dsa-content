# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isEvenOddTree(self, root: Optional[TreeNode]) -> bool:
        queue = deque([(root, 0)])
        while queue:
            nodeLength = len(queue)
            prev = None
            for _ in range(nodeLength):
                node, level = queue.popleft()
                if (level % 2 == 0 and node.val % 2 == 0) or (level % 2 != 0 and node.val % 2 != 0): return False
                if prev and ((level % 2 == 0 and prev.val >= node.val) or (level % 2 != 0 and prev.val <= node.val)): return False
                prev = node
                if node.left: queue.append((node.left, level + 1))
                if node.right: queue.append((node.right, level + 1))
        return True