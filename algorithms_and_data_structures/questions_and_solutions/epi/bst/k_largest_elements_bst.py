class Solution:
    def kLargestElementsBST(self, root, k):
        self.res = []
        # reverse inorder traversal
        def helper(node):
            if len(self.res) < k:
                if node.right: helper(node.right)
                if len(self.res) < k: self.res.append(node.val)
                if node.left: helper(node.left)
        
        helper(root)
        return self.res