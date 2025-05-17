# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findMode(self, root: Optional[TreeNode]) -> List[int]:
        if root.left == None and root.right == None: return [root.val]

        mode = []
        self.count = 0
        self.currCount = 0
        self.currMode = None

        def helper(node):
            if node == None: return
            helper(node.left)

            if node.val != self.currMode:
                self.currCount = 0
                self.currMode = node.val
            elif node.val == self.currMode:
                self.currCount += 1
            
            if self.currCount > self.count:
                mode.clear()
                mode.append(self.currMode)
                self.count = self.currCount
            elif self.currCount == self.count:
                mode.append(self.currMode)

            helper(node.right)
        
        helper(root)
        return mode