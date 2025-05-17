class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def reconstructPreorder(self, preorder):
        def helper(pre):
            node = next(pre)
            if not node: return None
            
            left = helper(pre)
            right = helper(pre)
            return TreeNode(node.val, left, right)
        
        return helper(iter(preorder))