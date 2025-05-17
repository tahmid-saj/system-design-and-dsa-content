# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        self.nodes = set()

        def helper(node):
            if node != None:
                if node.left != None and helper(node.left) == True: return True

                if (k - node.val) in self.nodes: return True
                else: self.nodes.add(node.val)

                if node.right != None and helper(node.right) == True: return True

        if helper(root) == True: return True
        return False
        