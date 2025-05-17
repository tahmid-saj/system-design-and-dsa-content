# """
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation
# """
#class NestedInteger:
#    def isInteger(self) -> bool:
#        """
#        @return True if this NestedInteger holds a single integer, rather than a nested list.
#        """
#
#    def getInteger(self) -> int:
#        """
#        @return the single integer that this NestedInteger holds, if it holds a single integer
#        Return None if this NestedInteger holds a nested list
#        """
#
#    def getList(self) -> [NestedInteger]:
#        """
#        @return the nested list that this NestedInteger holds, if it holds a nested list
#        Return None if this NestedInteger holds a single integer
#        """
class NestedIterator:
    def __init__(self, nestedList: [NestedInteger]):
        # self.list = []
        # self.pos = -1
        # self.recursivelyFlatten(nestedList)

        # self.stk = list(reversed(nestedList))

        # self.stk = [[nestedList, 0]]

        self.gen = self.genRecursivelyFlatten(nestedList)
        self.peeked = None

    def next(self) -> int:
        # self.pos += 1
        # return self.list[self.pos]

        # self.makeTopOfStackInteger()
        # return self.stk.pop().getInteger()

        # self.makeTopOfStackInteger()
        # e = self.stk[-1][0]
        # index = self.stk[-1][1]
        # self.stk[-1][1] += 1
        # return e[index].getInteger()

        if not self.hasNext(): return None
        nextInt, self.peeked = self.peeked, None
        return nextInt

    def hasNext(self) -> bool:
        # return self.pos + 1 < len(self.list)

        # self.makeTopOfStackInteger()
        # return len(self.stk) > 0

        # self.makeTopOfStackInteger()
        # return len(self.stk) > 0
        
        if self.peeked is not None: return True
        try:
            self.peeked = next(self.gen)
            return True
        except: return False
        
    def makeTopOfStackInteger(self):
        # while self.stk and not self.stk[-1].isInteger(): self.stk.extend(reversed(self.stk.pop().getList()))

        # while self.stk:
        #     e = self.stk[-1][0]
        #     index = self.stk[-1][1]
        #     if len(e) == index:
        #         self.stk.pop()
        #         continue
        #     if e[index].isInteger(): break
        #     else:
        #         nextList = e[index].getList()
        #         self.stk[-1][1] += 1
        #         self.stk.append([nextList, 0])
        pass

    def recursivelyFlatten(self, nestedList):
        # for e in nestedList:
        #     if e.isInteger(): self.list.append(e.getInteger())
        #     else: self.recursivelyFlatten(e.getList())
        pass
    
    def genRecursivelyFlatten(self, nestedList):
        for e in nestedList:
            if e.isInteger(): yield e.getInteger()
            else:
                for i in self.genRecursivelyFlatten(e.getList()):
                    yield i