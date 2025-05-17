# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        return self.dfs(root, low, high)
    
    def dfs(self, root, low, high):
        self.res = 0
        def helper(node):
            if node.left: helper(node.left)
            if node.val > high: return
            if low <= node.val <= high: self.res += node.val
            if node.right: helper(node.right)

        helper(root)
        return self.res