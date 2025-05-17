# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # return self.iterative(root)
        return self.recursive(root)

    def iterative(self, root):
        if root == None: return []
        res, queue = [], [root]

        while queue:
            curr = []
            length = len(queue)
            for i in range(length):
                node = queue.pop(0)
                curr.append(node.val)

                if node.left: queue.append(node.left)
                if node.right: queue.append(node.right)
            res.append(curr)

        return res

    def recursive(self, root):
        if not root: return []
        self.res = []

        def helper(node, level):
            if len(self.res) < level + 1: self.res.append([])
            self.res[level].append(node.val)

            if node.left: helper(node.left, level + 1)
            if node.right: helper(node.right, level + 1)
        
        helper(root, 0)
        return self.res