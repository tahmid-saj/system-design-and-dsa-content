class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def minimalTree(self, nums, l, r):
        if l > r: return None
        middle = l + (r - l) // 2
        val = nums[middle]
        n = TreeNode(val)
        n.left = self.minimalTree(nums, l, middle - 1)
        n.right = self.minimalTree(nums, middle + 1, r)
        return n