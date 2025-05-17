# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # return self.mySolution(head)
        
        return self.sentinel(head)
    
    def mySolution(self, head):
        if head == None: return None
        if head.next == None: return head

        prev = ListNode()
        prev.next = head
        res, first, second = None, head, head.next
        while second:
            if first.val == first.next.val and first.val != second.val:
                prev.next = second
                first = second
            elif first.val != first.next.val:
                first = first.next
                prev = prev.next
                if res == None: res = prev
            second = second.next
        
        # removing duplicates at the end
        if first.next and first.val == first.next.val: prev.next = None
        
        # if res is None, duplicates in the beginning
        if res == None: res = prev.next
        
        return res
    
    def sentinel(self, head):
        sentinel = ListNode()
        sentinel.next = head
        prev, node = sentinel, head

        while node:
            if node.next and node.val == node.next.val:
                while node.next and node.val == node.next.val:
                    node = node.next
                prev.next = node.next
            else:
                prev = prev.next
            
            node = node.next
        
        return sentinel.next