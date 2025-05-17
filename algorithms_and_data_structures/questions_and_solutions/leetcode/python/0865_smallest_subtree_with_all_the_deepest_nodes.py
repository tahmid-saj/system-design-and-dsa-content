# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def subtreeWithAllDeepest(self, root: TreeNode) -> TreeNode:
        # return self.recursive(root)
        # return self.paintNodes(root)
        return self.recursive2(root)
    
    def recursive(self, root):
        self.maxNodes = []
        self.max = 0
        def helper(node, curr):
            if not node: return
            left = helper(node.left, curr + 1)
            right = helper(node.right, curr + 1)
            if curr > self.max:
                self.max = curr
                self.maxNodes = []
                self.maxNodes.append(node)
            elif curr == self.max: self.maxNodes.append(node)
        
        helper(root, 0)
        
        return self.lcaOfNodes(root)
    
    def lcaOfNodes(self, root):
        self.res = None
        def helper(node):
            if not node: return 0
            left = helper(node.left)
            right = helper(node.right)
            found = 1 if node in self.maxNodes else 0
            if left + right + found == len(self.maxNodes): 
                if not self.res: self.res = node
            
            return left + right + found
        
        helper(root)
        return self.res
    
    def paintNodes(self, root):
        self.depth = {None: -1}
        def putDepths(node, parent=None):
            if not node: return
            self.depth[node] = self.depth[parent] + 1
            putDepths(node.left, node)
            putDepths(node.right, node)

        putDepths(root)
        maxDepth = max(iter(self.depth.values()))
        print(self.depth.values())

        def helper(node):
            if not node: return None
            if self.depth.get(node, 0) == maxDepth: return node
            left = helper(node.left)
            right = helper(node.right)

            return node if (left and right) else left or right
        
        return helper(root)
    
    def recursive2(self, root):
        self.result = collections.namedtuple("result", ("node", "dist"))
        def helper(node):
            if not node: return self.result(None, 0)
            left, right = helper(node.left), helper(node.right)
            if left.dist > right.dist: return self.result(left.node, left.dist + 1)
            if left.dist < right.dist: return self.result(right.node, right.dist + 1)
            return self.result(node, left.dist + 1)

        return helper(root).node