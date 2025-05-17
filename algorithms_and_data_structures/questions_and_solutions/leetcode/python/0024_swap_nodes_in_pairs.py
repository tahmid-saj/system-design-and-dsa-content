# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # keep track of prevEnd
        # prev.next = curr.next
        # curr.next = prev
        # prevEnd.next = curr
        # prevEnd = prev
        # prev = prev.next
        # if prev == None or prev.next == None: break
        # curr = prev.next

        # return self.iterative(head)
        if head == None: return None
        if head.next == None: return head
        return self.recursive(head)
    
    def iterative(self, head):
        if head == None: return None
        if head.next == None: return head

        prevEnd, res = ListNode(), None
        prevEnd.next = head
        
        prev, curr = head, head.next
        while curr:
            prev.next = curr.next
            curr.next = prev

            if res == None: res = curr

            prevEnd.next = curr
            prevEnd = prev
            prev = prev.next
            if prev == None or prev.next == None: break
            curr = prev.next

        return res
    
    def recursive(self, head):
        if head == None: return None
        if head.next == None: return head

        prev, curr = head, head.next
        prev.next = curr.next
        curr.next = prev

        prev.next = self.recursive(prev.next)

        return curr