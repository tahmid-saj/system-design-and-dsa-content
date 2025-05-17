# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, root):
        self.maximum = 1e8
        if root == None:
            return 0

        def helper(node, depth):
            if not node.left and not node.right:
                self.maximum = min(self.maximum, depth + 1)
            if node.left:
                helper(node.left, depth + 1)
            if node.right:
                helper(node.right, depth + 1)

        helper(root, 0)
        return self.maximum