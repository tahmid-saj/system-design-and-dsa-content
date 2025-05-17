# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        # return self.sentinel(head, x)

        return self.beforeAfterLists(head, x)

    def sentinel(self, head, x):
        if head == None: return None
        if head.next == None: return head
        sentinel = ListNode()
        sentinel.next = head
        # use three pointers: prev (previous node to ge), ge (first node greater than or equal to x), firstX (first node that is equal to x)
        prev, ge, firstX = sentinel, sentinel, sentinel
        while firstX and firstX.val != x:
            if ge == sentinel and prev == sentinel and firstX.next and firstX.next.val >= x:
                prev = firstX 
                ge = firstX.next
            firstX = firstX.next
        
        # check for any nodes with val lower than x, if so then insert them between prev and ge
        if ge == sentinel and prev == sentinel: return head
        second, first = ge, ge.next
        while first:
            if first.val < x:
                tmp = first.next

                prev.next = first
                first.next = ge
                prev = prev.next

                second.next = tmp
                first = tmp
                continue

            first = first.next
            second = second.next
        
        return sentinel.next
    
    def beforeAfterLists(self, head, x):
        before = beforeHead = ListNode()
        after = afterHead = ListNode()

        while head:
            if head.val >= x:
                after.next = head
                after = after.next
            else:
                before.next = head
                before = before.next
            head = head.next
        
        before.next = afterHead.next
        after.next = None
        
        return beforeHead.next