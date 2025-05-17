# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def bstFromPreorder(self, preorder: List[int]) -> Optional[TreeNode]:
        # return self.inorderPreorderSimulation(preorder)
        # return self.recursivePreorderSimulation(preorder)
        return self.iterativePreorderSimulation(preorder)
    
    def inorderPreorderSimulation(self, preorder):
        self.i = 0
        def helper(preorder, l=0, r=len(preorder)):
            if l == r: return None
            node = TreeNode(preorder[self.i])
            nodeIndex = self.inorderMap[preorder[self.i]]
            self.i += 1

            node.left = helper(preorder, l, nodeIndex)
            node.right = helper(preorder, nodeIndex + 1, r)
            return node

        self.inorder = sorted(preorder)
        self.inorderMap = {val: index for index, val in enumerate(self.inorder)}
        return helper(preorder)
    
    def recursivePreorderSimulation(self, preorder):
        self.i = 0
        def helper(preorder, lower=-math.inf, upper=math.inf):
            if self.i == len(preorder): return None
            val = preorder[self.i]
            if val < lower or val > upper: return None
            
            node = TreeNode(val)
            self.i += 1
            node.left = helper(preorder, lower, val)
            node.right = helper(preorder, val, upper)
            return node

        return helper(preorder)
    
    def iterativePreorderSimulation(self, preorder):
        root = TreeNode(preorder[0])
        stk = [root]

        for i in range(1, len(preorder)):
            node, child = stk[-1], TreeNode(preorder[i])
            while stk and stk[-1].val < child.val: node = stk.pop()

            if child.val < node.val: node.left = child
            elif child.val > node.val: node.right = child
            stk.append(child)
        
        return root