# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
  def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    if l1 == None: return l2
    if l2 == None: return l1

    carry = 0
    res = ListNode()
    n = res
    while l1 or l2:
      val1, val2 = 0, 0

      if not l1: val1 = 0
      else: val1 = l1.val
      if not l2: val2 = 0
      else: val2 = l2.val

      if carry == 0:
        if val1 + val2 < 10: n.val = (val1 + val2) % 10
        else:
          n.val = (val1 + val2) % 10
          carry = 1
      elif carry == 1:
        if val1 + val2 + carry < 10:
          n.val = (val1 + val2 + carry) % 10
          carry = 0
        else: n.val = (val1 + val2 + carry) % 10

      if l1: l1 = l1.next
      if l2: l2 = l2.next
      if l1 or l2: 
        n.next = ListNode()
        n = n.next
    
    if carry == 1: n.next = ListNode(carry)

    return res