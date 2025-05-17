# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        if root == None: return []
        self.res = []

        def helper(node, comb, s):
            comb.append(node.val)

            if node.left == None and node.right == None and s + node.val == targetSum: self.res.append(list(comb))
            if node.left: helper(node.left, comb, s + node.val)
            if node.right: helper(node.right, comb, s + node.val)

            comb.pop()
        
        helper(root, [], 0)
        return self.res