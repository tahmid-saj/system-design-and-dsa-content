# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head.next: return None
        prev = ListNode(next=head)
        slow, fast = head, head
        while fast and fast.next:
            prev = prev.next
            slow = slow.next
            fast = fast.next.next
        
        prev.next = slow.next
        del slow
        return head