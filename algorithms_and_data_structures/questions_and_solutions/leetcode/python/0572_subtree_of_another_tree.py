# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        if root.left == None and root.right == None and subRoot.left == None and subRoot.right == None and root.val == subRoot.val: return True

        def helper(node, subNode):
            # check if these are the same tree
            if (node == None and subNode != None) or (node != None and subNode == None): return False
            if node != None and subNode != None:
                if helper(node.left, subNode.left) == False: return False
                if node.val != subNode.val: return False
                if helper(node.right, subNode.right) == False: return False
                return True

        stk = [root]

        while len(stk) > 0:
            node = stk.pop()
            if node.val == subRoot.val:
                if helper(node, subRoot) == True: return True
            if node.left != None: stk.append(node.left)
            if node.right != None: stk.append(node.right)
            
        return False