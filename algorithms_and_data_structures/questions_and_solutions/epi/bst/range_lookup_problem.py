from collections import namedtuple
class Solution:
    def rangeLookupProblem(self, root, range):
        interval = namedtuple("interval", ("start", "end"))
        range = interval(range[0], range[1])
        self.res = []
        
        def dfs(node):
            if node.val >= range.start and node.val <= range.end: 
                if node.left: dfs(node.left)
                self.res.append(node.val)
                if node.right: dfs(node.right)
            if node.val < range.start and node.left: dfs(node.right)
            elif node.val > range.end and node.right: dfs(node.left)
        dfs(root)

        return self.res