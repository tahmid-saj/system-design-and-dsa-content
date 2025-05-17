# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head == None: return None
        if head.next == None: return head

        evenHead, oddHead, i = ListNode(), ListNode(), 0
        even, odd, node = evenHead, oddHead, head
        while node:
            if i % 2 == 0: 
                even.next = node
                even = even.next
            else:
                odd.next = node
                odd = odd.next
            node = node.next
            i += 1
        
        even.next = oddHead.next
        odd.next = None
        return evenHead.next