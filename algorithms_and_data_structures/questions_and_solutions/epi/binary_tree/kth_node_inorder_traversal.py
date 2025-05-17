class Solution:
    def kthNodeInorderTraversal(self, root, k):
        while root:
            leftSize = root.left.size if root.left else 0
            if leftSize + 1 < k:
                k -= leftSize + 1
                root = root.right
            elif leftSize + 1 == k: return root
            else: root = root.left
        
        return None