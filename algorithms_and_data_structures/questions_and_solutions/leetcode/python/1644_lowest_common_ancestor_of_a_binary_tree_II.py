# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # return self.recursive1(root, p, q)
        # return self.recursive2(root, p, q)
        return self.recursive3(root, p, q)
        # return self.iterative1(root, p, q)
        # return self.iterativePostorder(root, p, q)
    
    def recursive1(self, root, p, q):
        self.res = None
        def helper(node, p, q):
            if not node: return False
            left = helper(node.left, p, q)
            right = helper(node.right, p, q)
            middle = node == p or node == q

            if left + right + middle >= 2:
                self.res = node
                return True
            
            return left or right or middle
        
        helper(root, p, q)
        return self.res
    
    def recursive2(self, root, p, q):
        def dfs(node, target):
            if not node: return False
            if node == target: return True

            if dfs(node.left, target): return True
            if dfs(node.right, target): return True
            return False
        
        def helper(node, p, q):
            if not node or node == p or node == q: return node
            left = helper(node.left, p, q)
            right = helper(node.right, p, q)
            if left and right: return node
            if left: return left
            if right: return right
        
        lca = helper(root, p, q)
        if lca == p: return p if dfs(p, q) else None
        if lca == q: return q if dfs(q, p) else None
        return lca
    
    def recursive3(self, root, p, q):
        self.oneNodeFound = False
        self.res = None

        def helper(node, p, q):
            if not node: return False
            left = helper(node.left, p, q)
            right = helper(node.right, p, q)
            middle = node == p or node == q

            if middle or left or right: self.oneNodeFound = True
            if middle + left + right >= 2: self.res = node

            return left or right or middle
        
        helper(root, p, q)
        if self.oneNodeFound: return self.res
        return None
    
    def iterative1(self, root, p, q):
        parent, stk = {root: None}, [root]

        while stk and (p not in parent or q not in parent):
            node = stk.pop()
            if node.right:
                stk.append(node.right)
                parent[node.right] = node
            if node.left:
                stk.append(node.left)
                parent[node.left] = node
        
        if p not in parent or q not in parent: return None
        
        ancestors = set()
        while p:
            ancestors.add(p)
            p = parent[p]
        
        while q not in ancestors: q = parent[q]

        return q
    
    def iterativePostorder(self, root, p, q):
        new, leftDone, rightDone, lcaIndex, oneNodeFound = 0, 1, 2, -1, False
        stk = [(root, new)]

        while stk:
            node, status = stk[-1]
            if status == rightDone:
                if oneNodeFound and lcaIndex == len(stk) - 1: lcaIndex -= 1
                stk.pop()
            else:
                if status == new:
                    if node == p or node == q:
                        if oneNodeFound:
                            return stk[lcaIndex][0]
                        oneNodeFound = True
                        lcaIndex = len(stk) - 1
                stk[-1] = (stk[-1][0], stk[-1][1] + 1)
                nextNode = [node.left, node.right][status]
                if nextNode: stk.append((nextNode, new))
        
        return None