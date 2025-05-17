# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def deleteNode(self, node):
        """
        :type node: ListNode
        :rtype: void Do not return anything, modify node in-place instead.
        """
        # return self.looping(node)
        return self.constantTime(node)

    def looping(self, node):
        while True:
            node.val = node.next.val
            if node.next.next: node = node.next
            else:
                node.next = None
                break
    
    def constantTime(self, node):
        nxt = node.next.next
        tmp = node.next
        node.val = tmp.val
        node.next = nxt
        tmp.next = None
        del tmp