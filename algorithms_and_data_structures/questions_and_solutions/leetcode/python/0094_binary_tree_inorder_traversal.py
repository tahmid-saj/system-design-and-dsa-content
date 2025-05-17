# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        # return self.iterative(root)

        return self.morrisTraversal(root)
    
    def iterative(self, root):
        stk, res = [], []
        
        while stk or root:
            while root:
                stk.append(root)
                root = root.left
            root = stk.pop()

            res.append(root.val)
            root = root.right
        
        return res
    
    def morrisTraversal(self, root):
        res = []
        prev, curr = None, root

        while curr:
            if curr.left == None:
                res.append(curr.val)
                curr = curr.right
            else:
                prev = curr.left
                while prev.right: prev = prev.right

                prev.right = curr

                tmp = curr
                curr = curr.left
                tmp.left = None
        
        return res