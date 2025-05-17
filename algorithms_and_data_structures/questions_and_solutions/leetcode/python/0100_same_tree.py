# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def isSameTree(self, p, q):
        """
        :type p: TreeNode
        :type q: TreeNode
        :rtype: bool
        """
        
        def helper(p, q):
            if p == None and q != None: return False
            if p != None and q == None: return False
            if p != None and q != None:
                if not helper(p.left, q.left): return False
                
                if p.val != q.val: return False

                if not helper(p.right, q.right): return False

            return True

        if not helper(p, q): return False
        return True