# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDiffInBST(self, root: Optional[TreeNode]) -> int:
        return self.dfs(root)
    
    def dfs(self, root):
        self.res = math.inf
        self.prev = None
        def helper(node):
            if node.left: helper(node.left)
            if self.prev != None: self.res = min(self.res, node.val - self.prev)
            self.prev = node.val
            if node.right: helper(node.right)
        
        helper(root)
        return self.res