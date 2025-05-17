class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # return self.constantSpaceDPDFS(root)
        # return self.recursiveLimits(root)
        # return self.iterativeLimits(root)
        # return self.recursiveInorder(root)
        return self.iterativeInorder(root)

    def constantSpaceDPDFS(self, root):
        self.dp = []
        def helper(node):
            if not node: return
            if node.left and not helper(node.left): return False

            self.dp.append(node.val)
            if len(self.dp) > 2: self.dp.pop(0)
            if len(self.dp) == 2 and self.dp[0] >= self.dp[1]: return False

            if node.right and not helper(node.right): return False
            return True
        
        return helper(root)
        
    def recursiveLimits(self, root):
        def helper(node, lLimit, rLimit):
            if not node: return
            if node.left and not helper(node.left, lLimit, node.val - 1): return False

            if not (lLimit <= node.val <= rLimit): return False

            if node.right and not helper(node.right, node.val + 1, rLimit): return False
            return True
        
        return helper(root, -math.inf, math.inf)

    def iterativeLimits(self, root):
        stk = [(root, -math.inf, math.inf)]

        while stk:
            node, lLimit, rLimit = stk.pop()
            if not (lLimit <= node.val <= rLimit): return False

            if node.right: stk.append((node.right, node.val + 1, rLimit))
            if node.left: stk.append((node.left, lLimit, node.val - 1))
        
        return True

    def recursiveInorder(self, root):
        self.prev = -math.inf
        def helper(node):
            if not node: return
            if node.left and not helper(node.left): return False

            if not (self.prev < node.val): return False 
            self.prev = node.val

            if node.right and not helper(node.right): return False
            return True
        
        return helper(root)

    def iterativeInorder(self, root):
        prev, stk = -math.inf, []

        while stk or root:
            while root:
                stk.append(root)
                root = root.left
            root = stk.pop()

            if not (prev < root.val): return False
            prev = root.val
            root = root.right
        
        return True