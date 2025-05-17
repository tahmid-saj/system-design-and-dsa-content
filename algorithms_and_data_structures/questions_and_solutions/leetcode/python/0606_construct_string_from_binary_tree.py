# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def tree2str(self, root: Optional[TreeNode]) -> str:
        self.res = str(root.val)

        def helper(node):
            if node != root and node != None: self.res += "(" + str(node.val)
            elif node == None: 
                self.res += "()"
                return

            if node != None and node.left != None: helper(node.left)
            elif node != None and node.left == None and node.right != None: helper(node.left)
            if node != None and node.right != None: helper(node.right)

            self.res += ")"

        helper(root)
        return self.res[:-1]