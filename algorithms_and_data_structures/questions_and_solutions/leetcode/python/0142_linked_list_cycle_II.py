# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # return self.fastSlowPointers(head)
        return self.floydsTortioseAndHare(head)
    
    def fastSlowPointers(self, head):
        if not head: return None
        if not head.next: return None

        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break

        if not slow or not fast or slow != fast: return None
        length = self.length(slow)

        first, second = head, head
        for i in range(length): first = first.next

        while first != second:
            first = first.next
            second = second.next
        
        return first

    def length(self, node):
        length, n = 1, node.next
        while n != node:
            length += 1
            n = n.next
        return length
    
    def floydsTortioseAndHare(self, head):
        tortiose, hare = head, head

        while hare and hare.next:
            tortiose = tortiose.next
            hare = hare.next.next
            if tortiose == hare: break
        
        if hare == None or hare.next == None: return None

        tortiose = head
        while tortiose != hare:
            tortiose = tortiose.next
            hare = hare.next
        
        return tortiose