# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def lcaDeepestLeaves(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        return self.recursive(root)
    
    def recursive(self, root):
        self.maxNodes = []
        self.max = 0
        def helper(node, curr):
            if not node: return
            helper(node.left, curr + 1)
            helper(node.right, curr + 1)
            if curr > self.max:
                self.max = curr
                self.maxNodes = [node]
            elif curr == self.max: self.maxNodes.append(node)
        
        helper(root, 0)
        return self.lcaOfNodes(root)
    
    def lcaOfNodes(self, root):
        self.res = None
        def helper(node):
            if not node: return 0
            left = helper(node.left)
            right = helper(node.right)
            found = 1 if node in self.maxNodes else 0
            if left + right + found == len(self.maxNodes):
                if not self.res: self.res = node
            
            return left + right + found
        
        helper(root)
        return self.res