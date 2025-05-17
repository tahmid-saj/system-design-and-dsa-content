# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        # return self.recursiveArray(head)
        # return self.recursiveArray2(head)
        # return self.recursive(head)
        return self.inorderSimulation(head)
    
    def recursiveArray(self, head):
        if head == None: return None
        nodes = []
        while head:
            nodes.append(head.val)
            head = head.next
        
        def helper(nodes):
            mid = len(nodes) // 2
            if len(nodes) == 0: return None
            middle = TreeNode(nodes[mid])

            middle.left = helper(nodes[:mid])
            middle.right = helper(nodes[mid + 1:])

            return middle

        return helper(nodes)
    
    def recursiveArray2(self, head):
        if head == None: return None
        nodes = []
        while head:
            nodes.append(head.val)
            head = head.next
        
        def helper(l, r):
            if l > r: return None
            mid = (l + r) // 2
            middle = TreeNode(nodes[mid])
            if l == r: return middle

            middle.left = helper(l, mid - 1)
            middle.right = helper(mid + 1, r)

            return middle

        return helper(0, len(nodes) - 1)
    
    def recursive(self, head):
        if head == None: return None

        def findMiddle(start):
            prev, slow, fast = None, start, start

            while fast and fast.next:
                prev = slow
                slow = slow.next
                fast = fast.next.next
            
            if prev: prev.next = None

            return slow

        mid = findMiddle(head)
        middle = TreeNode(mid.val)
        if head == mid: return middle

        middle.left = self.recursive(head)
        middle.right = self.recursive(mid.next)

        return middle
    
    def inorderSimulation(self, head):
        if head == None: return None
        length, n = 0, head
        while n:
            length += 1
            n = n.next
        
        def helper(l, r):
            nonlocal head
            if l > r: return None

            mid = (l + r) // 2

            left = helper(l, mid - 1)

            middle = TreeNode(head.val)
            middle.left = left
            head = head.next

            middle.right = helper(mid + 1, r)

            return middle
        
        return helper(0, length - 1)