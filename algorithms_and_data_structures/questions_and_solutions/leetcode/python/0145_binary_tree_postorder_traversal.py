# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        # return self.iterativeTwoStacks(root)
        return self.iterativeOneStack(root)
        # return self.morrisTraversal(root)

        
    def iterativeTwoStacks(self, root):
        if root == None: return []
        res, stk1, stk2 = [], [root], []

        while stk1:
            curr = stk1.pop()
            stk2.append(curr)

            if curr.left: stk1.append(curr.left)
            if curr.right: stk1.append(curr.right)
        
        while stk2: res.append(stk2.pop().val)

        return res
    
    def iterativeOneStack(self, root):
        if root == None: return []
        
        new, leftDone, rightDone = 0, 1, 2
        res, stk = [], [(root, new)]
        while stk:
            node, status = stk[-1]
            if status == rightDone:
                stk.pop()
                res.append(node.val)
            else:
                stk[-1] = (stk[-1][0], stk[-1][1] + 1)
                nextNode = [node.left, node.right][status]
                if nextNode != None: stk.append((nextNode, new))
        
        return res

    def morrisTraversal(self, root):
        res = []
        prev, curr = None, root

        while curr:
            if curr.right == None:
                res.append(curr.val)
                curr = curr.left
            else:
                prev = curr.right
                while prev.left and prev.left != curr: prev = prev.left

                if prev.left == None:
                    res.append(curr.val)
                    prev.left = curr
                    curr = curr.right
                else:
                    prev.left = None
                    curr = curr.left
        
        return res[::-1]