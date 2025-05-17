class Solution:
    def inorderParentPtrs(self, node):
        res, prev = [], None
        while node:
            if node.parent == prev:
                if node.left: next = node.left
                else:
                    res.append(node.val)
                    next = node.right or node.parent
            elif node.left == prev:
                res.append(node.val)
                next = node.right or node.parent
            else: next = node.parent
            prev, node = node, next
        
        return res