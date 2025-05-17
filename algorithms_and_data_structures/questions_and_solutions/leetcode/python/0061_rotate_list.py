# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head == None: return None
        if k == 0: return head
        # find the length of the list, find offset = k % length
        # move first by offset
        # then move second until first.next == None
        # second.next = None, first.next = head
        length, n = 0, head
        while n:
            length += 1
            n = n.next
        offset = k % length
        if offset == 0: return head

        first, second = head, head
        while first.next:
            if offset > 0:
                offset -= 1
            else:
                second = second.next
            first = first.next
        
        res = second.next
        second.next = None
        first.next = head

        return res