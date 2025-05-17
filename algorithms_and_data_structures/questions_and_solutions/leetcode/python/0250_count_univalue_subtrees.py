# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def countUnivalSubtrees(self, root: Optional[TreeNode]) -> int:
        return self.dfs(root)
    
    def dfs(self, root):
        self.res = 0
        def helper(node):
            if not node: return True
            leftUnivalue = helper(node.left)
            rightUnivalue = helper(node.right)

            if leftUnivalue and rightUnivalue:
                if node.left and node.val != node.left.val: return False
                if node.right and node.val != node.right.val: return False
                self.res += 1
                return True
            return False
        
        helper(root)
        return self.res