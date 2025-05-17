class Node:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next

class Bucket:
    def __init__(self):
        self.head = Node(-1, None)
    
    def update(self, key):
        existingNode = self.contains(key)
        if not existingNode:
            node = Node(key, None)
            firstNode = self.head.next
            self.head.next = node
            node.next = firstNode
        else:
            existingNode.val = key
    
    def remove(self, key):
        prev, curr = self.head, self.head.next
        while curr:
            if curr.val == key:
                prev.next = curr.next
                del curr
                return
            prev = curr
            curr = curr.next
    
    def contains(self, key):
        curr = self.head.next
        while curr:
            if curr.val == key: return curr
            curr = curr.next
        return None

class MyHashSet:
    def __init__(self):
        self.keySpace = 2069
        self.hashSet = [Bucket() for _ in range(self.keySpace)]
    
    def hashFunction(self, key):
        return key % self.keySpace

    def add(self, key: int) -> None:
        hashKey = self.hashFunction(key)
        self.hashSet[hashKey].update(key)

    def remove(self, key: int) -> None:
        hashKey = self.hashFunction(key)
        return self.hashSet[hashKey].remove(key)

    def contains(self, key: int) -> bool:
        hashKey = self.hashFunction(key)
        if self.hashSet[hashKey].contains(key): return True
        return False


# Your MyHashSet object will be instantiated and called as such:
# obj = MyHashSet()
# obj.add(key)
# obj.remove(key)
# param_3 = obj.contains(key)