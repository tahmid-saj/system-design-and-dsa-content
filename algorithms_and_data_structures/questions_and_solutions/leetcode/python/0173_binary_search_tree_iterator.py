# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
# 1. Morris traversal to flatten BST and store an array of the inorder traversal
# 2. Iterative inorder traversal (controlled recursion) using stack
class BSTIterator:

    def __init__(self, root: Optional[TreeNode]):
        # prev, curr = None, root
        # self.inorder = []
        # self.ptr = -1
        # while curr:
        #     if curr.left == None:
        #         self.inorder.append(curr.val)
        #         curr = curr.right
        #     else:
        #         prev = curr.left
        #         while prev.right: prev = prev.right

        #         prev.right = curr
        #         tmp = curr
        #         curr = curr.left
        #         tmp.left = None

        self.stk = []
        self._traverseLeftMost(root)

    def next(self) -> int:
        # self.ptr += 1
        # return self.inorder[self.ptr]

        node = self.stk.pop()
        if node.right: self._traverseLeftMost(node.right)
        return node.val

    def hasNext(self) -> bool:
        # return self.ptr + 1 <= len(self.inorder) - 1

        return len(self.stk) > 0

    def _traverseLeftMost(self, node):
        while node:
            self.stk.append(node)
            node = node.left

# Your BSTIterator object will be instantiated and called as such:
# obj = BSTIterator(root)
# param_1 = obj.next()
# param_2 = obj.hasNext()