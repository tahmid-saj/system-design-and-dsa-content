# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        self.res = None

        def helper(node):
            if node != None:
                if node.val == val:
                    self.res = node
                    return True

                if node.left != None and helper(node.left) == True: return True
                if node.right != None and helper(node.right) == True: return True

        helper(root)
        return self.res