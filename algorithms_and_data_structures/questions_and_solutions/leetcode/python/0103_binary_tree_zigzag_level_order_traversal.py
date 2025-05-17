# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # return self.iterativeBFS(root)
        # return self.recursiveDFS(root)
        return self.iterativeDFS(root)

    def iterativeBFS(self, root):
        if root == None: return []
        leftToRight = True
        res, queue = [], deque()
        queue.append(root)

        while queue:
            curr = []
            length = len(queue)
            for i in range(length):
                node = queue.popleft()
                if leftToRight: curr.append(node.val)
                else: curr.insert(0, node.val)
                
                if node.left: queue.append(node.left)
                if node.right: queue.append(node.right)
            leftToRight = not leftToRight
            res.append(curr)
        
        return res
    
    def recursiveDFS(self, root):
        if not root: return []
        self.res = []

        def helper(node, level):
            if len(self.res) == level: self.res.append([])

            if level % 2 == 0: self.res[level].append(node.val)
            else: self.res[level].insert(0, node.val)

            if node.left: helper(node.left, level + 1)
            if node.right: helper(node.right, level + 1)

        helper(root, 0)
        return self.res
    
    def iterativeDFS(self, root):
        if root == None: return []
        res, stk = [], [(root, 0)]

        while stk:
            node = stk.pop()
            if len(res) == node[1]: res.append([])

            if node[1] % 2 != 0: res[node[1]].append(node[0].val)
            else: res[node[1]].insert(0, node[0].val)
            
            if node[0].left: stk.append((node[0].left, node[1] + 1))
            if node[0].right: stk.append((node[0].right, node[1] + 1))
        
        return res