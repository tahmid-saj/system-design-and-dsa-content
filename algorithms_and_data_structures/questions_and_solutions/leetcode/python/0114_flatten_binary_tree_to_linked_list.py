# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        # return self.recursive(root)
        return self.iterative(root)
        # return self.constantSpace(root)
    
    def recursive(self, node):
        if node == None: return None
        if node.left == None and node.right == None: return node

        leftTail = self.recursive(node.left)
        rightTail = self.recursive(node.right)

        if leftTail:
            leftTail.right = node.right
            node.right = node.left
            node.left = None
        
        return rightTail if rightTail else leftTail
    
    def iterative(self, root):
        if root == None: return
        leftLeft, done = 1, 2
        stk = [root]

        while stk:
            node = stk.pop()

            if node.left != None:
                prev, end = node.left, node.right
                while prev.right: prev = prev.right

                prev.right = end
                node.right = node.left
                node.left = None
            
            if node.right: stk.append(node.right)
            if node.left: stk.append(node.left)

    def constantSpace(self, root):
        prev, curr = None, root

        while curr:
            if curr.left == None:
                curr = curr.right
            else:
                prev, end = curr.left, curr.right
                while prev.right: prev = prev.right

                tmp = curr.left
                curr.right = tmp
                prev.right = end
                curr.left = None
                curr = curr.right