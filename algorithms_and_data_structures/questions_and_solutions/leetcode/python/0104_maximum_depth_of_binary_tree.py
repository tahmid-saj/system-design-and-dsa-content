# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def maxDepth(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        if root == None: return 0
        if root.left == None and root.right == None: return 1
        
        l = self.maxDepth(root.left)
        r = self.maxDepth(root.right)
        return max(l, r) + 1 