class Solution:
    def checkBalanced(self, root):
        return self.dfs(root)
    
    def height(self, node, height):
        if not node: return 0
        if not node.left and not node.right: return 1
        l = self.height(node.left, height)
        r = self.height(node.right, height)
        return max(l, r) + 1
    
    def dfs(self, root):
        def helper(node):
            if not node: return True
            if node.left: 
                if not helper(node.left): return False
            l = self.height(node.left)
            r = self.height(node.right)
            if abs(l - r) > 1: return False
            if node.right:
                if not helper(node.right): return False
            return True

        return helper(root)