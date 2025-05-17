# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        # return self.bfs(root)
        return self.dfs(root)
    
    def bfs(self, root):
        currMax, res, queue = -math.inf, 0, deque([(root, 1)])

        while queue:
            length = len(queue)
            currSum = 0
            for _ in range(length):
                node, level = queue.popleft()
                currSum += node.val
                if node.left: queue.append((node.left, level + 1))
                if node.right: queue.append((node.right, level + 1))
            if currSum > currMax:
                currMax = currSum
                res = level

        return res
    
    def dfs(self, root):

        def helper(node, level, levelSum):
            if len(levelSum) == level: levelSum.append(node.val)
            else: levelSum[level] += node.val

            if node.left: helper(node.left, level + 1, levelSum)
            if node.right: helper(node.right, level + 1, levelSum)

        levelSum = []
        helper(root, 0, levelSum)
        return levelSum.index(max(levelSum)) + 1