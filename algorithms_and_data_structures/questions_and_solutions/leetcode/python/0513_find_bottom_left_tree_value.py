# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findBottomLeftValue(self, root: Optional[TreeNode]) -> int:
        # return self.bfs(root)
        return self.dfs(root)
    
    def bfs(self, root):
        queue = deque([root])
        res = None
        while queue:
            nodeLength = len(queue)
            for i in range(nodeLength):
                node = queue.popleft()
                if i == 0: res = node.val
                if node.left: queue.append(node.left)
                if node.right: queue.append(node.right)
        
        return res
    
    def dfs(self, root):
        self.res = None
        self.maxDepth = 0
        def helper(node, depth):
            if not node: return
            helper(node.left, depth + 1)
            helper(node.right, depth + 1)
            if depth > self.maxDepth:
                self.maxDepth = depth
                self.res = node.val
        
        helper(root, 1)
        return self.res