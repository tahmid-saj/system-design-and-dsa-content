# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        self.res = 1e8
        self.preVal = None

        def helper(node):
            if node.left != None: helper(node.left)

            if self.preVal != None and abs(self.preVal - node.val) < self.res: self.res = min(self.res, abs(self.preVal - node.val))
            self.preVal = node.val 

            if node.right != None: helper(node.right)
        
        helper(root)
        return self.res