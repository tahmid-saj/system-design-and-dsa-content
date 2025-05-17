# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        stk, curr = [], head

        while curr != None:
            while len(stk) != 0 and stk[-1].val < curr.val:
                stk.pop()
            if stk: stk[-1].next = curr
            stk.append(curr)
            curr = curr.next

        return stk[0] if stk else None