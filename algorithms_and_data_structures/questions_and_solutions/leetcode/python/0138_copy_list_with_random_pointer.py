"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        clones = {}
        # return self.recursive(head, clones)
        # return self.iterative(head, clones)
        return self.iterativeConstantSpace(head)
    
    def recursive(self, node, clones):
        # if node is not in clones: create a new Node object and assign clones[node] = object
        # if the randompointer is not in clones: create it, else assign clones[node].random = random
        if not node: return None
        clones[node] = Node(node.val, None, None)

        nextClone, randomClone = None, None
        if node.next and node.next not in clones: nextClone = self.recursive(node.next, clones)
        elif node.next in clones: nextClone = clones[node.next]

        if node.random and node.random not in clones: randomClone = self.recursive(node.random, clones)
        elif node.random in clones: randomClone = clones[node.random]

        clones[node].next = nextClone
        clones[node].random = randomClone

        return clones[node]
    
    def iterative(self, head, clones):
        if head == None: return None

        node = head
        while node:
            if node not in clones:
                if node == None: clones[node] = None
                else: 
                    clones[node] = Node(node.val, None, None)
            
            if node.random not in clones:
                if node.random == None: clones[node.random] = None
                else: clones[node.random] = Node(node.random.val, None, None)
            clones[node].random = clones[node.random]
            
            if node.next not in clones:
                if node.next == None: clones[node.next] = None
                else: clones[node.next] = Node(node.next.val, None, None)
            clones[node].next = clones[node.next]
            
            node = node.next
        
        return clones[head]
    
    def iterativeConstantSpace(self, head):
        if not head:
            return head

        # Creating a new weaved list of original and copied nodes.
        ptr = head
        while ptr:

            # Cloned node
            new_node = Node(ptr.val, None, None)

            # Inserting the cloned node just next to the original node.
            # If A->B->C is the original linked list,
            # Linked list after weaving cloned nodes would be A->A'->B->B'->C->C'
            new_node.next = ptr.next
            ptr.next = new_node
            ptr = new_node.next

        ptr = head

        # Now link the random pointers of the new nodes created.
        # Iterate the newly created list and use the original nodes random pointers,
        # to assign references to random pointers for cloned nodes.
        while ptr:
            ptr.next.random = ptr.random.next if ptr.random else None
            ptr = ptr.next.next

        # Unweave the linked list to get back the original linked list and the cloned list.
        # i.e. A->A'->B->B'->C->C' would be broken to A->B->C and A'->B'->C'
        ptr_old_list = head # A->B->C
        ptr_new_list = head.next # A'->B'->C'
        head_new = head.next
        while ptr_old_list:
            ptr_old_list.next = ptr_old_list.next.next
            ptr_new_list.next = ptr_new_list.next.next if ptr_new_list.next else None
            ptr_old_list = ptr_old_list.next
            ptr_new_list = ptr_new_list.next
        return head_new