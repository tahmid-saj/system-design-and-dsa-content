# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        inorder_nodes = {}
        for i, v in enumerate(inorder): inorder_nodes[v] = i
        preorderIndex = 0

        def helper(l, r):
            nonlocal preorderIndex
            if l > r: return None

            rootVal = preorder[preorderIndex]
            node = TreeNode(rootVal)
            preorderIndex += 1

            node.left = helper(l, inorder_nodes[rootVal] - 1)
            node.right = helper(inorder_nodes[rootVal] + 1, r)

            return node

        return helper(0, len(inorder) - 1)