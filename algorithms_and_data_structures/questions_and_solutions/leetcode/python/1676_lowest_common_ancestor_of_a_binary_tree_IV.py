# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', nodes: 'List[TreeNode]') -> 'TreeNode':
        self.res = None
        def helper(node, nodes):
            if not node: return 0
            left = helper(node.left, nodes)
            right = helper(node.right, nodes)
            found = 1 if node in nodes else 0
            
            if left + right + found == len(nodes):
                if not self.res: self.res = node
            
            return left + right + found

        helper(root, nodes)
        return self.res