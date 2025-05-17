class Solution:
    def exteriorBinaryTree(self, root):
        self.res = [root]

        def rootToLeftmost(node):
            if not node: return
            self.res.append(node.val)
            if node.left: rootToLeftmost(node.left)
            else: rootToLeftmost(node.right)

        def leaves(node):
            if not node: return
            if not node.left and not node.right and self.res[-1] != node.val: self.res.append(node.val)
            leaves(node.left)
            leaves(node.right)

        def rootToRightmost(node):
            if not node: return
            self.res.append(node.val)
            if node.right: rootToRightmost(node.right)
            else: rootToRightmost(node.left)

        rootToLeftmost(root.left)
        leaves(root.left)
        leaves(root.right)
        rootToRightmost(root.right)
        return self.res[:-1]