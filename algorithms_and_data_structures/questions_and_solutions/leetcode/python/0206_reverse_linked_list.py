# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def reverseList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if head == None: return None
        if head.next == None: return head

        prev, curr = None, head
        while curr != None:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp
        return prev