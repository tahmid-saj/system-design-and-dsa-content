# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def generateTrees(self, n: int) -> List[Optional[TreeNode]]:
        # dp = {}
        # return self.topDown(1, n, dp)
        # return self.bottomUp(n)
        return self.bottomUpOptimized(n)
    
    def topDown(self, start, end, dp):
        res = []
        if start > end:
            res.append(None)
            return res
        if (start, end) in dp: return dp[(start, end)]

        for i in range(start, end + 1):
            leftSubtrees = self.topDown(start, i - 1, dp)
            rightSubtrees = self.topDown(i + 1, end, dp)

            for leftSubtree in leftSubtrees:
                for rightSubtree in rightSubtrees:
                    root = TreeNode(i, leftSubtree, rightSubtree)
                    res.append(root)
        
        dp[(start, end)] = res
        return dp[(start, end)]
    
    def bottomUp(self, n):
        dp = [[[] for _ in range(n + 1)] for _ in range(n + 1)]
        for i in range(1, n + 1): dp[i][i] = [TreeNode(i, None, None)]

        for numberOfNodes in range(2, n + 1):
            for start in range(1, n - numberOfNodes + 2):
                end = start + numberOfNodes - 1
                for i in range(start, end + 1):
                    leftSubtrees = dp[start][i - 1] if i != start else [None]
                    rightSubtrees = dp[i + 1][end] if i != end else [None]

                    for leftSubtree in leftSubtrees:
                        for rightSubtree in rightSubtrees:
                            root = TreeNode(i, leftSubtree, rightSubtree)
                            dp[start][end].append(root)
        
        return dp[1][n]
    
    def bottomUpOptimized(self, n: int) -> List[Optional[TreeNode]]:
        dp = [[] for _ in range(n + 1)]
        dp[0].append(None)

        for numberOfNodes in range(1, n + 1):
            for i in range(1, numberOfNodes + 1):
                j = numberOfNodes - i
                for left in dp[i - 1]:
                    for right in dp[j]:
                        root = TreeNode(i, left, self.clone(right, i))
                        dp[numberOfNodes].append(root)

        return dp[n]

    def clone(self, node: Optional[TreeNode], offset: int) -> Optional[TreeNode]:
        if not node:
            return None
        cloned_node = TreeNode(node.val + offset)
        cloned_node.left = self.clone(node.left, offset)
        cloned_node.right = self.clone(node.right, offset)
        return cloned_node