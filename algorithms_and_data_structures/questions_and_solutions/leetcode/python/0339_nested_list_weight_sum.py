# """
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation
# """
#class NestedInteger:
#    def __init__(self, value=None):
#        """
#        If value is not specified, initializes an empty list.
#        Otherwise initializes a single integer equal to value.
#        """
#
#    def isInteger(self):
#        """
#        @return True if this NestedInteger holds a single integer, rather than a nested list.
#        :rtype bool
#        """
#
#    def add(self, elem):
#        """
#        Set this NestedInteger to hold a nested list and adds a nested integer elem to it.
#        :rtype void
#        """
#
#    def setInteger(self, value):
#        """
#        Set this NestedInteger to hold a single integer equal to value.
#        :rtype void
#        """
#
#    def getInteger(self):
#        """
#        @return the single integer that this NestedInteger holds, if it holds a single integer
#        Return None if this NestedInteger holds a nested list
#        :rtype int
#        """
#
#    def getList(self):
#        """
#        @return the nested list that this NestedInteger holds, if it holds a nested list
#        Return None if this NestedInteger holds a single integer
#        :rtype List[NestedInteger]
#        """

class Solution:
    def depthSum(self, nestedList: List[NestedInteger]) -> int:
        # return self.dfs(nestedList)
        return self.bfs(nestedList)
    
    def dfs(self, nestedList):
        self.res = 0
        def helper(elements, depth):
            for e in elements:
                if e.isInteger(): self.res += (e.getInteger() * depth)
                else: helper(e.getList(), depth + 1)

        helper(nestedList, 1)
        return self.res
    
    def bfs(self, nestedList):
        queue, depth, res = deque(nestedList), 1, 0

        while queue:
            elementsLength = len(queue)
            for _ in range(elementsLength):
                e = queue.pop()
                if e.isInteger(): res += depth * e.getInteger()
                else: queue.extendleft(e.getList())
            depth += 1
        return res