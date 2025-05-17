# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def deleteDuplicates(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if head == None: return None
        if head.next == None: return head

        res, curr, prev = head, head.next, head
        # while curr != None:
        # -> if curr.val != prev.val: prev.next = curr, prev = prev.next
        # curr = curr.next
        # return res
        while curr != None:
            if curr.val != prev.val:
                prev.next = curr
                prev = prev.next

            if prev.val == curr.val and curr.next == None:
                prev.next = None
            
            curr = curr.next

        return res