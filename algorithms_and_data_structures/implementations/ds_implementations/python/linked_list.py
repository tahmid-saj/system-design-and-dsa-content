# Single linked list solution
class Node:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next
    
class SinglyLinkedList:
    def __init__(self):
        self.head = Node(-1, None)
        self.tail = Node(-1, None)
        self.size = 0
    
    def get(self, index):
        if index < 0 or index >= self.size: return None

        curr, i = self.head.next, 0
        while curr:
            if i == index: return curr
            curr = curr.next
            i += 1
    
    def addAtHead(self, val):
        nextNode = self.head.next
        newNode = Node(val, nextNode)
        self.head.next = newNode
        if not self.tail.next: self.tail.next = newNode

        self.size += 1
    
    def addAtTail(self, val):
        prevNode = self.tail.next
        newNode = Node(val, None)
        self.tail.next = newNode
        if prevNode: prevNode.next = newNode
        elif not self.head.next: self.head.next = newNode
    
        self.size += 1
    
    def addAtIndex(self, index, val):
        if index > self.size: return
        if index == self.size: 
            self.addAtTail(val)
            return

        prev, curr, i = self.head, self.head.next, 0
        while curr:
            if i == index:
                newNode = Node(val, curr)
                prev.next = newNode
                self.size += 1
                return
            prev = prev.next
            curr = curr.next
            i += 1
        
    def deleteAtIndex(self, index):
        if index < 0 or index >= self.size: return

        prev, curr, i = self.head, self.head.next, 0
        while curr:
            if i == index:
                prev.next = curr.next

                # check if the tail node is to be deleted
                if self.tail.next == curr:
                    self.tail.next = prev

                del curr
                self.size -= 1
                return
            prev = prev.next
            curr = curr.next
            i += 1

class MyLinkedList:

    def __init__(self):
        self.singlyLinkedList = SinglyLinkedList()

    def get(self, index: int) -> int:
        node = self.singlyLinkedList.get(index)
        if node: return node.val
        return -1

    def addAtHead(self, val: int) -> None:
        self.singlyLinkedList.addAtHead(val)

    def addAtTail(self, val: int) -> None:
        self.singlyLinkedList.addAtTail(val)

    def addAtIndex(self, index: int, val: int) -> None:
        self.singlyLinkedList.addAtIndex(index, val)

    def deleteAtIndex(self, index: int) -> None:
        self.singlyLinkedList.deleteAtIndex(index)


# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)