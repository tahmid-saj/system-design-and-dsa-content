# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def countNodes(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        if root == None: return 0
        if root.left == None and root.right == None: return 1

        res = [0]
        def helper(node):
            if node != None:
                helper(node.left)
                res[0] += 1
                helper(node.right)
        
        helper(root)
        return res[0]