# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        # return self.recursive1(root1, root2)
        return self.recursive2(root1, root2)
    
    def recursive1(self, root1, root2):
        def helper(node):
            if node:
                if not node.left and not node.right: yield node.val
                yield from helper(node.left)
                yield from helper(node.right)
        
        return list(helper(root1)) == list(helper(root2))
    
    def recursive2(self, root1, root2):
        def helper(node, nodes):
            if node.left: helper(node.left, nodes)
            if node.right: helper(node.right, nodes)
            if not node.left and not node.right: nodes.append(node.val)
            return nodes
        
        return helper(root1, []) == helper(root2, [])