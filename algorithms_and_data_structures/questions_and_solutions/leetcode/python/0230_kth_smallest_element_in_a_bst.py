# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        # return self.recursive(root, k)
        # return self.iterative(root, k)
        return self.morris(root, k)
    
    def recursive(self, root, k):
        self.i = k
        self.res = None

        def helper(node):
            if node.left and helper(node.left): return True
            self.i -= 1
            if self.i == 0: 
                self.res = node.val
                return True
            if node.right and helper(node.right): return True
            return False

        helper(root)
        return self.res
    
    def iterative(self, root, k):
        i, res, stk = 0, None, []

        while stk or root:
            while root:
                stk.append(root)
                root = root.left
            root = stk.pop()

            i += 1
            if i == k:
                res = root.val
                break
            root = root.right
        
        return res
    
    def morris(self, root, k):
        i, res = 0, None
        prev, curr = None, root

        while curr:
            if curr.left == None:
                i += 1
                if i == k:
                    res = curr.val
                    break
                curr = curr.right
            else:
                prev = curr.left
                while prev.right: prev = prev.right

                prev.right = curr
                
                tmp = curr
                curr = curr.left
                tmp.left = None
        
        return res