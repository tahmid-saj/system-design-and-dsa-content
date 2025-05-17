# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def removeElements(self, head, val):
        """
        :type head: ListNode
        :type val: int
        :rtype: ListNode
        """
        if head == None: return None
        if head.next == None and head.val == val: return None

        res, prev, curr = None, ListNode(), head

        # loop through liked list while curr != None:
        # -> if res == None and curr.val != val: res = curr, prev.next = curr
        # -> if curr.val == val: prev.next = curr.next, curr = curr.next
        # -> elif curr.val != val: prev = prev.next, curr = curr.next
        # return res
        while curr != None:
            if res == None and curr.val != val:
                res = curr
                prev.next = curr
            if curr.val == val:
                prev.next = curr.next
                curr = curr.next
            elif curr.val != val:
                prev = prev.next
                curr = curr.next

        return res