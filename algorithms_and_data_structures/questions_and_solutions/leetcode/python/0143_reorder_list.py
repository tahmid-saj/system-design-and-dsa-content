# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        # find the midpoint of the list, reverse from the midpoint to the end
        # traverse from both sides of the list towards the midpoint, and change their next pointer values
        if not head: return
        if not head.next: return
        first, second, prevNode = head, head, ListNode(None, head)
        while second and second.next:
            prevNode = prevNode.next
            first = first.next
            second = second.next.next
        prevNode.next = None

        prev, curr = None, first
        while curr:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp
        
        l, r = head, prev
        while l and r:
            lNext, rNext = l.next, r.next
            l.next = r
            if lNext: r.next = lNext
            l = lNext
            r = rNext