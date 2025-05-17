# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        # return self.iterative(root)

        return self.morrisTraversal(root)
    
    def iterative(self, root):
        stk, res = [root], []

        while stk and root:
            node = stk.pop()
            if node:
                res.append(node.val)
                if node.right: stk.append(node.right)
                if node.left: stk.append(node.left)
        
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
                while prev.right and prev.right != curr: prev = prev.right

                if prev.right == None:
                    res.append(curr.val)
                    prev.right = curr
                    curr = curr.left
                else:
                    prev.right = None
                    curr = curr.right
        
        return res