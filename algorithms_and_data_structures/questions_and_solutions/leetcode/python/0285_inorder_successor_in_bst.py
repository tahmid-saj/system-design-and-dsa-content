# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def inorderSuccessor(self, root: TreeNode, p: TreeNode) -> Optional[TreeNode]:
        return self.binaryTreeSuccessor(root, p)
        # return self.bstSuccessor(root, p)
    
    def binaryTreeSuccessor(self, root, p):
        if p.right:
            p = p.right
            while p.left: p = p.left
            return p
        
        self.res = None
        self.pred = None
        def helper(node, p):
            if not node: return
            helper(node.left, p)
            if self.pred == p and not self.res: self.res = node
            self.pred = node
            helper(node.right, p)
        
        helper(root, p)
        return self.res

    def bstSuccessor(self, root, p):
        res = None
        while root:
            if root.val <= p.val: root = root.right
            else:
                res = root
                root = root.left
        return res