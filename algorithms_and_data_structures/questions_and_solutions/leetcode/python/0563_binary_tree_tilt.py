# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findTilt(self, root: Optional[TreeNode]) -> int:
        self.res = 0

        def helper(node):
            # recursively get the left and right branch sums of every node, find the tilt and add it to self.res
            if node == None: return 0

            lSum = helper(node.left)
            rSum = helper(node.right)
            tilt = abs(lSum - rSum)
            self.res += tilt

            return lSum + rSum + node.val

        helper(root)
        return self.res