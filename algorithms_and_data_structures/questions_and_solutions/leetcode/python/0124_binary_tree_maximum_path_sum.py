# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.globalMaximumSum = -math.inf

        def helper(node):
            if node == None: return 0

            lMaxSum = helper(node.left)
            rMaxSum = helper(node.right)
            lMaxSum = max(lMaxSum, 0)
            rMaxSum = max(rMaxSum, 0)

            maxSum = max(lMaxSum, rMaxSum) + node.val
            self.globalMaximumSum = max(self.globalMaximumSum, lMaxSum + rMaxSum + node.val)

            return maxSum

        helper(root)
        return self.globalMaximumSum