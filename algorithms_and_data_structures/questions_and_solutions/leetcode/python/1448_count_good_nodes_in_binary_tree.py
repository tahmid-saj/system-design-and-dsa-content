# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        # return self.recursive(root)
        # return self.iterativeDFS(root)
        return self.iterativeBFS(root)
    
    def recursive(self, root):
        self.res = 0
        def helper(node, currMax):
            if node.val >= currMax: 
                self.res += 1
                currMax = node.val
            if node.left: helper(node.left, currMax)
            if node.right: helper(node.right, currMax)

        helper(root, -math.inf)
        return self.res
    
    def iterativeDFS(self, root):
        res, stk = 0, [(root, -math.inf)]

        while stk:
            node, currMax = stk.pop()
            if node.val >= currMax:
                res += 1
                currMax = node.val

            if node.right: stk.append((node.right, currMax))
            if node.left: stk.append((node.left, currMax))
        
        return res
    
    def iterativeBFS(self, root):
        res, queue = 0, deque([(root, -math.inf)])

        while queue:
            node, currMax = queue.popleft()
            if node.val >= currMax:
                res += 1
                currMax = node.val
            
            if node.left: queue.append((node.left, currMax))
            if node.right: queue.append((node.right, currMax))
        
        return res