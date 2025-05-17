# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        return self.onePassV2(head, n)
    
    def onePassV1(self, head, n):
        # if not head.next and n == 1: return None
        # n1, n2 = None, head
        # while n2.next:
        #   if n == 0 and not n1: n1 = head
        #   n2 = n2.next
        #   if n > 0: n -= 1
        #   elif n == 0: n1 = n1.next
        # if n1 == None: return head.next
        # n3 = n1.next, tmp = n3.next, n1.next = tmp, del n3
        if not head.next and n == 1: return None
        
        prev, curr, n1 = None, None, head
        while n1:
            n1 = n1.next
            if n > 0: n -= 1
            elif n == 0:
                curr = curr.next
                if prev: prev = prev.next
            if n == 0 and not curr: curr = head
            if curr == head.next: prev = head

        if curr == head: return head.next

        tmp = curr.next
        prev.next = tmp
        del curr
        return head
    
    def onePassV2(self, head, n):
        dummy = ListNode()
        dummy.next = head
        first, second = dummy, dummy

        while n >= 0:
            n -= 1
            first = first.next
        
        while first:
            first = first.next
            second = second.next
        
        second.next = second.next.next
        
        return dummy.next