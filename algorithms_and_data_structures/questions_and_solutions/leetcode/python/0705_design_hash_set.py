class Node:
    def __init__(self, key, next=None):
        self.key = key
        self.next = next

class LL:
    def __init__(self):
        self.head = Node(-1, None)
    
    def addToHead(self, key):
        if self.contains(key): return

        nextNode = self.head.next
        node = Node(key, nextNode)
        self.head.next = node
    
    def removeFromHead(self, key):
        prev, curr = self.head, self.head.next
        while curr:
            if curr.key == key:
                prev.next = curr.next
                del curr
                return
            prev = prev.next
            curr = curr.next
    
    def contains(self, key):
        curr = self.head.next
        while curr:
            if curr.key == key: return True
            curr = curr.next
        return False

class MyHashSet:
    def __init__(self):
        self.keySpace = 2069
        self.set = [LL() for _ in range(self.keySpace)]
    
    def hashFunction(self, key):
        return key % self.keySpace

    def add(self, key: int) -> None:
        index = self.hashFunction(key)
        self.set[index].addToHead(key)

    def remove(self, key: int) -> None:
        index = self.hashFunction(key)
        self.set[index].removeFromHead(key)

    def contains(self, key: int) -> bool:
        index = self.hashFunction(key)
        return self.set[index].contains(key)


# Your MyHashSet object will be instantiated and called as such:
# obj = MyHashSet()
# obj.add(key)
# obj.remove(key)
# param_3 = obj.contains(key)