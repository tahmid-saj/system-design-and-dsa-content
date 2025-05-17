# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def increasingBST(self, root: TreeNode) -> TreeNode:
        return self.inorder(root)
    
    def inorder(self, root):
        res = self.curr = TreeNode()
        def helper(node):
            if node.left: helper(node.left)
            node.left = None
            self.curr.right = node
            self.curr = node
            if node.right: helper(node.right)

        helper(root)
        return res.right