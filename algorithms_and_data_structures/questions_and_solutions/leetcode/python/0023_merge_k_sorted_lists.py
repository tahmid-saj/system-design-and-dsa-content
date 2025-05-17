# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from queue import PriorityQueue

class Solution():
    def mergeKLists(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        class Wrapper():
            def __init__(self, node):
                self.node = node
            def __lt__(self, other):
                return self.node.val < other.node.val
        
        pq = PriorityQueue()
        for l in lists:
            if l: pq.put(Wrapper(l))
        
        head, tail = None, None
        while not pq.empty():
            node = pq.get().node
            if head == None: head = tail = node
            else:
                tail.next = node
                tail = tail.next
            
            if node.next: pq.put(Wrapper(node.next))

        return head