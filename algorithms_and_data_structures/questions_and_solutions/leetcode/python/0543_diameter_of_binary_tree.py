# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.res = -1e8

        def helper(node):
            if node == None: return 0

            l = helper(node.left)
            r = helper(node.right)
            self.res = max(self.res, l + r)

            return 1 + max(l, r)

        helper(root)
        return self.res