class Solution:
    def overlappingListsCycles(self, headA, headB):
        cycleA, cycleB = self.startOfCycle(headA), self.startOfCycle(headB)

        if not cycleA and not cycleB: return self.overlappingLists(headA, headB)
        elif (not cycleA and cycleB) or (not cycleB and cycleA): return None

        tmp = cycleA.next
        while tmp and tmp != cycleB: tmp = tmp.next

        return tmp if tmp == cycleB else None
    
    def overlappingLists(self, headA, headB):
        first, second = headA, headB

        while first and second and first != second:
            first = headB if not first else first.next
            second = headA if not second else second.next
        
        return first

    def startOfCycle(self, node):
        fast, slow = node, node
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast: break
        
        if slow: length = self.cycleLength(slow)
        else: return None

        first, second = slow, node
        for _ in range(length):
            first = first.next
            second = second.next
        
        return first

    def cycleLength(self, node):
        res, n = 1, node.next
        while n != node:
            res += 1
            n = n.next

        return res