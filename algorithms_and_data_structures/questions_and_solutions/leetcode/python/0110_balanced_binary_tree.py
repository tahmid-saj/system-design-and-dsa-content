# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def isBalanced(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        # return self.topDown(root)
        return self.bottomUp(root)[0]
    
    def topDown(self, root):
        def getDepth(node):
            if node == None: return 0
            if node.left == None and node.right == None: return 1

            l = getDepth(node.left)
            r = getDepth(node.right)

            return max(l, r) + 1
        
        if root == None: return True 
        if not self.isBalanced(root.left): return False

        l = getDepth(root.left)
        r = getDepth(root.right)
        if abs(l - r) > 1: return False
        if abs(l - r) > 1: return False
        
        if not self.isBalanced(root.right): return False

        return True
    
    def bottomUp(self, node):
        if not node: return True, 0

        leftBalanced, leftHeight = self.bottomUp(node.left)
        if not leftBalanced: return False, 0
        rightBalanced, rightHeight = self.bottomUp(node.right)
        if not rightBalanced: return False, 0

        return abs(leftHeight - rightHeight) <= 1, max(leftHeight, rightHeight) + 1