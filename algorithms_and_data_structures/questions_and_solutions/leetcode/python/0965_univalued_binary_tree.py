# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isUnivalTree(self, root: Optional[TreeNode]) -> bool:
        return self.dfs(root)
    
    def dfs(self, root):
        val = root.val
        def helper(node):
            if node.val != val: return False
            if node.left and not helper(node.left): return False
            if node.right and not helper(node.right): return False
            return True
        
        return helper(root)