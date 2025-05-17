# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def sumOfLeftLeaves(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        if root.left == None and root.right == None: return 0

        stk, res = [root], 0
        while len(stk) != 0:
            node = stk.pop()
            if node.left and node.left.left == None and node.left.right == None:
                res += node.left.val
            if node.left: stk.append(node.left)
            if node.right: stk.append(node.right)
        
        return res