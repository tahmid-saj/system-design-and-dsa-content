from collections import deque
class Solution:
    def listOfDepths(self, root):
        return self.bfs(root)

    def bfs(self, root):
        queue, res = deque([root]), []
        while queue:
            nodesLength = len(queue)
            curr = []
            for _ in range(nodesLength):
                node = queue.popleft()
                curr.append(node)
                if node.left: queue.append(node.left)
                if node.right: queue.append(node.right)
        return res