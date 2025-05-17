# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        # return self.recursive(root)
        # return self.iterative(root)
        return self.morrisTraversal(root)
    
    def recursive(self, root):
        self.res = 0

        def helper(node, curr):
            curr *= 10
            curr += node.val

            if node.left == None and node.right == None: self.res += curr
            if node.left: helper(node.left, curr)
            if node.right: helper(node.right, curr)

        helper(root, 0)
        return self.res
    
    def iterative(self, root):
        res = 0
        stk = [(root, root.val)]

        while stk:
            node, val = stk.pop()

            if node.left == None and node.right == None: res += val
            if node.right: stk.append((node.right, (val * 10) + node.right.val))
            if node.left: stk.append((node.left, (val * 10) + node.left.val))
        
        return res
    
    def morrisTraversal(self, root):
        prev, curr = None, root
        res, s = 0, 0

        while curr:
            if curr.left == None:
                s *= 10
                s += curr.val
                if curr.right == None: res += s

                curr = curr.right
            else:
                steps = 1
                prev = curr.left
                while prev.right and prev.right != curr:
                    steps += 1 
                    prev = prev.right

                if prev.right == None:
                    s *= 10
                    s += curr.val

                    prev.right = curr
                    curr = curr.left
                else:
                    if prev.left == None: res += s
                    for _ in range(steps): s //= 10

                    prev.right = None
                    curr = curr.right

        return res