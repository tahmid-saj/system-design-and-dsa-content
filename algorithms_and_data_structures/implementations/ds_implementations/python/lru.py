
class Node:
    def __init__(self, key=None, val=None, next=None, prev=None):
        self.key = key
        self.val = val
        self.next = next
        self.prev = prev

class LRUCache:
    def __init__(self, capacity: int):
        self.lru = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.lru: return -1
        
        node = self.lru[key]
        self.remove(node)
        self.add(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.lru:
            node = self.lru[key]
            node.val = value
            self.remove(node)
            self.add(node)
        else:
            if len(self.lru) == self.capacity: 
                delNode = self.remove(self.tail.prev)
                self.lru.pop(delNode.key)
                del delNode
            node = Node(key, value)
            self.add(node)
            self.lru[key] = node


    def add(self, node):
        nextNode = self.head.next
        nextNode.prev = node
        node.next = nextNode
        node.prev = self.head
        self.head.next = node
    
    def remove(self, node):
        prevNode = node.prev
        nextNode = node.next
        prevNode.next = nextNode
        nextNode.prev = prevNode
        node.next = None
        node.prev = None
        return node

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)