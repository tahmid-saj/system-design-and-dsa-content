# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def isSymmetric(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        def helper(l, r):
            if l == None and r != None: return False
            if l != None and r == None: return False
            if l != None and r != None:
                if not helper(l.left, r.right): return False
                if l.val != r.val: return False
                if not helper(l.right, r.left): return False
            return True

        if not helper(root.left, root.right): return False
        return True
        