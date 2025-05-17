# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        queue = []
        queue.append((root, 0))
        res, levelSum, nodes = [], 0, 0

        while len(queue) > 0:
            node, l = queue.pop(0)
            levelSum += node.val
            nodes += 1

            # if the len(queue) == 0 or the nxt l in the queue.pop(0) != l: then add the average of the nodes and update the level and nodes
            nextL = queue[0][1] if len(queue) != 0 else 1e8
            if len(queue) == 0 or nextL != l:
                res.append(levelSum / nodes)
                levelSum = 0
                nodes = 0

            if node.left != None: queue.append((node.left, l + 1))
            if node.right != None: queue.append((node.right, l + 1))

        return res