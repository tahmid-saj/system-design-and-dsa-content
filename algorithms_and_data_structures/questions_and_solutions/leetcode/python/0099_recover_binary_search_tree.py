class Solution:
    def recoverTree(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        # sorted array from inorder traversal
        # self.res = []
        # def isBST(node):
        #     if node.left and isBST(node.left): return True

        #     self.res.append(node)
        #     if len(self.res) > 2:
        #         if self.res[-1].val < self.res[-2].val and self.res[-2].val < self.res[-3].val: 
        #             self.res[-1].val, self.res[-3].val = self.res[-3].val, self.res[-1].val
        #             return True
        #         elif self.res[-2].val < self.res[-3].val: 
        #             self.res[-3].val, self.res[-2].val = self.res[-2].val, self.res[-3].val
        #             return True
        #         elif self.res[-1].val < self.res[-2].val: 
        #             self.res[-1].val, self.res[-2].val = self.res[-2].val, self.res[-1].val
        #             return True
            
        #     if node.right and isBST(node.right): return True

        #     return False

        # if not isBST(root) and len(self.res) == 2 and self.res[-1].val < self.res[-2].val: self.res[-1].val, self.res[-2].val = self.res[-2].val, self.res[-1].val

        # recursive inorder traversal
        # self.first = None
        # self.second = None
        # self.prev = None
        # def helper(node):
        #     if not node: return
        #     if node.left: helper(node.left)

        #     if self.prev and self.prev.val > node.val:
        #         if not self.first: self.first = self.prev
        #         self.second = node
            
        #     self.prev = node

        #     if node.right: helper(node.right)
        
        # helper(root)
        # self.first.val, self.second.val = self.second.val, self.first.val

        # iterative inorder traversal
        prev = None
        first = None
        second = None
        stk = []

        while stk or root:
            while root:
                stk.append(root)
                root = root.left
            root = stk.pop()

            if prev and prev.val > root.val:
                if not first: first = prev
                second = root
            prev = root
            root = root.right
        
        first.val, second.val = second.val, first.val

        # inorder morris traversal
        # first = second = prev = None
        # pred, curr = None, root

        # while curr:
        #     if curr.left == None:
        #         if prev and curr.val < prev.val:
        #             second = curr
        #             if first == None: first = prev
        #         prev = curr
                
        #         curr = curr.right
        #     else:
        #         pred = curr.left
        #         while pred.right and pred.right != curr: pred = pred.right

        #         if pred.right == None:
        #             pred.right = curr
        #             curr = curr.left
        #         else:
        #             if prev and curr.val < prev.val:
        #                 second = curr
        #                 if first == None: first = prev
        #             prev = curr

        #             pred.right = None
        #             curr = curr.right
        
        # first.val, second.val = second.val, first.val