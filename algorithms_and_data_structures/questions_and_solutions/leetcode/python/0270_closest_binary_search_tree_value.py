# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def closestValue(self, root: Optional[TreeNode], target: float) -> int:
        # return self.recursive(root, target)
        return self.recursiveBS(root, target)
    
    def recursive(self, root, target):
        self.dist = math.inf
        self.res = None
        def helper(node):
            if not node: return
            helper(node.left)
            if self.dist > abs(node.val - target):
                self.dist = abs(node.val - target)
                self.res = node.val
            elif self.dist == abs(node.val - target): self.res = min(self.res, node.val)
            helper(node.right)
        
        helper(root)
        return self.res
    
    def recursiveBS(self, root, target):
        self.dist = math.inf
        self.res = None
        def helper(node):
            if not node: return
            if node.val > target:
                if self.dist > abs(node.val - target):
                    self.dist = abs(node.val - target)
                    self.res = node.val
                elif self.dist == abs(node.val - target): self.res = min(self.res, node.val)
                helper(node.left)

            if node.val <= target:
                if self.dist > abs(node.val - target):
                    self.dist = abs(node.val - target)
                    self.res = node.val
                elif self.dist == abs(node.val - target): self.res = min(self.res, node.val)
                helper(node.right)

        helper(root)
        return self.res