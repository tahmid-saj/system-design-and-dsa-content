# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def verticalOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # return self.bfs(root)
        return self.dfs(root)
    
    def bfs(self, root):
        if not root: return []
        vertical, res, minCol, maxCol = defaultdict(list), [], 0, 0
        queue = deque([(root, 0)])
        
        while queue:
            nodesLength = len(queue)
            for _ in range(nodesLength):
                node, col = queue.popleft()
                minCol = min(minCol, col)
                maxCol = max(maxCol, col)
                vertical[col].append(node.val)
                if node.left: queue.append((node.left, col - 1))
                if node.right: queue.append((node.right, col + 1))
        
        for col in range(minCol, maxCol + 1): res.append(vertical[col])
        return res
    
    def dfs(self, root):
        if not root: return []
        self.vertical = defaultdict(list)
        self.minCol = 0
        self.maxCol = 0
        self.minRow = 0
        self.maxRow = 0
        def helper(node, col, row):
            if not node: return
            self.minCol = min(self.minCol, col)
            self.maxCol = max(self.maxCol, col)
            self.minRow = min(self.minRow, row)
            self.maxRow = max(self.maxRow, row)

            self.vertical[(col, row)].append(node.val)
            if node.left: helper(node.left, col - 1, row + 1)
            if node.right: helper(node.right, col + 1, row + 1)

        helper(root, 0, 0)
        
        res = []
        for col in range(self.minCol, self.maxCol + 1):
            for row in range(self.minRow, self.maxRow + 1):
                if (col, row) in self.vertical:
                    print(col, len(res))
                    if col + abs(self.minCol) == len(res): res.append([])
                    res[col + abs(self.minCol)].extend(self.vertical[(col, row)])
        return res