# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        return self.recursive(root)
    
    def recursive(self, root):
        if not root.left and not root.right: return 0
        self.res = 0
        def helper(node, direction, curr):
            self.res = max(self.res, curr)

            if direction == "":
                if node.left: helper(node.left, "left", curr + 1)
                if node.right: helper(node.right, "right", curr + 1)
            else:
                if node.left and direction == "right": helper(node.left, "left", curr + 1)
                elif node.left: helper(node.left, "left", 1)
                if node.right and direction == "left": helper(node.right, "right", curr + 1)
                elif node.right: helper(node.right, "right", 1)

        helper(root, "", 0)
        return self.res