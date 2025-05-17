# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def longestConsecutive(self, root: Optional[TreeNode]) -> int:
        return self.dfs(root)
    
    def dfs(self, root):
        self.res = 0
        def helper(node):
            if not node: return 0
            left = helper(node.left)
            right = helper(node.right)

            left = left + 1 if (node.left and node.left.val == node.val + 1) else 1
            right = right + 1 if (node.right and node.right.val == node.val + 1) else 1
            self.res = max(self.res, left, right)
            return max(left, right)

        helper(root)
        return self.res