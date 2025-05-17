# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        inorder_nodes = {}
        for i, v in enumerate(inorder): inorder_nodes[v] = i
        postorder_index = len(postorder) - 1

        def helper(l, r):
            nonlocal postorder_index
            if l > r: return None

            rootVal = postorder[postorder_index]
            mid = inorder_nodes[rootVal]
            postorder_index -= 1

            right = helper(mid + 1, r)
            left = helper(l, mid - 1)

            node = TreeNode(rootVal)
            node.right = right
            node.left = left

            return node
        
        return helper(0, len(inorder) - 1)