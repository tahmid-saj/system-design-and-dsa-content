# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sumRootToLeaf(self, root: Optional[TreeNode]) -> int:
        return self.dfs(root)
    
    def dfs(self, root):
        self.res = 0
        def helper(node, curr):
            curr = (curr << 1) | node.val
            if node.left: helper(node.left, curr)
            if node.right: helper(node.right, curr)
            if not node.left and not node.right: self.res += curr
        helper(root, 0)
        return self.res