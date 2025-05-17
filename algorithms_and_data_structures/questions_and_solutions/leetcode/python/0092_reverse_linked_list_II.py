# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        # return self.iterative(head, left, right)

        self.l, r = head, head
        self.stop = False
        self.recursive(r, left, right)
        return head
    
    def recursive(self, r, m, n):
        if n == 1: return
        else: r = r.next

        if m > 1: self.l = self.l.next

        self.recursive(r, m - 1, n - 1)

        if self.l == r or r.next == self.l: self.stop = True

        if self.stop == False:
            self.l.val, r.val = r.val, self.l.val
            self.l = self.l.next

    def iterative(self, head, left, right):
        if head.next == None: return head

        sentinel, k = ListNode(), left
        sentinel.next = head

        l, lPrev, r = sentinel, sentinel, sentinel
        while right > 0:
            if k < left: lPrev = lPrev.next
            if right <= k:
                l = l.next
                k -= 1
            r = r.next
            right -= 1

        rNext = r.next
        prev, curr = None, l
        while curr != rNext:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp

        lPrev.next = prev
        l.next = rNext

        return sentinel.next