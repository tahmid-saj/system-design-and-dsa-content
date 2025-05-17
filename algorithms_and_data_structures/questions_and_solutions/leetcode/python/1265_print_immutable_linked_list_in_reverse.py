# """
# This is the ImmutableListNode's API interface.
# You should not implement it, or speculate about its implementation.
# """
# class ImmutableListNode:
#     def printValue(self) -> None: # print the value of this node.
#     def getNext(self) -> 'ImmutableListNode': # return the next node.

class Solution:
    def printLinkedListInReverse(self, head: 'ImmutableListNode') -> None:
        # return self.recursive(head)
        return self.stack(head)

    def recursive(self, head):
        if head:
            self.printLinkedListInReverse(head.getNext())
            print(head.printValue())
    
    def stack(self, head):
        stk = []
        while head:
            stk.append(head)
            head = head.getNext()

        while stk:
            head = stk.pop()
            head.printValue()