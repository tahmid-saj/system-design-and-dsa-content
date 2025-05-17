# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if (root and not root.left and not root.right) and root.val == key: return None

        def helper(node, key):
            if not node: return None

            if key < node.val: node.left = helper(node.left, key)
            elif key > node.val: node.right = helper(node.right, key)
            else:
                if not node.left and not node.right: node = None
                elif node.right:
                    node.val = self.successor(node)
                    node.right = helper(node.right, node.val)
                elif node.left:
                    node.val = self.predecessor(node)
                    node.left = helper(node.left, node.val)
            
            return node
                    
        helper(root, key)
        return root

    def successor(self, root):
        root = root.right
        while root.left: root = root.left
        return root.val
    
    def predecessor(self, root):
        root = root.left
        while root.right: root = root.right
        return root.val