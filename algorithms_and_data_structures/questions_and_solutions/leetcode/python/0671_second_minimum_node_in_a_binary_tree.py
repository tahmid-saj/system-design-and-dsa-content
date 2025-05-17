# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findSecondMinimumValue(self, root: Optional[TreeNode]) -> int:
        self.firstMin = None
        self.secondMin = None

        def helper(node):
            # firstMin = None: self.firstMin = node.val
            # secondMin = None and node.val > self.firstMin: self.secondMin = node.val
            # secondMin = None and node.val < self.firstMin: self.secondMin = self.firstMin, self.firstMin = node.val
            # firstMin = 5, secondMin = 7, val = 6 -> secondMin = 6, firstMin = 5
            # firstMin = 5, secondMin = 7, val = 8 -> unchanged
            # firstMin = 5, secondMin = 7, val = 4 -> secondMin = 5, firstMin = 4
            if node.left != None: helper(node.left)

            if self.firstMin == None: self.firstMin = node.val
            elif self.secondMin == None and node.val > self.firstMin: self.secondMin = node.val
            elif self.secondMin == None and node.val < self.firstMin: 
                self.secondMin = self.firstMin
                self.firstMin = node.val
            elif node.val > self.firstMin and node.val < self.secondMin:
                self.secondMin = node.val
            elif node.val < self.firstMin and node.val < self.secondMin:
                self.secondMin = self.firstMin
                self.firstMin = node.val

            if node.right != None: helper(node.right)

        helper(root)
        if self.secondMin == None: return -1
        return self.secondMin