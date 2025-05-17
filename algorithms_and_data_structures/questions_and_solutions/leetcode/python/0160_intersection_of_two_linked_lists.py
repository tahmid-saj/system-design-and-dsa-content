# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        return self.alternatingPointers(headA, headB)
        # return self.twoPointersLength(headA, headB)
        # return self.seenSet(headA, headB)

    def alternatingPointers(self, headA, headB):
        first, second = headA, headB

        while first != second:
            first = headB if not first else first.next
            second = headA if not second else second.next
        
        return first
    
    def twoPointersLength(self, headA, headB):
        length1, length2 = self.length(headA), self.length(headB)
        if length1 > length2: headA, headB = headB, headA

        for _ in range(abs(length1 - length2)): headB = headB.next

        while headA and headB and headA != headB: headA, headB = headA.next, headB.next

        return headA
    
    def length(self, node):
        res = 0
        while node:
            res += 1
            node = node.next
        return res
    
    def seenSet(self, headA, headB):
        seen = set()
        while headA:
            seen.add(headA)
            headA = headA.next
        
        while headB:
            if headB in seen: return headB
            headB = headB.next
        
        return None