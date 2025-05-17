from collections import OrderedDict
# class ListNode:
#     def __init__(self, key, val):
#         self.key = key
#         self.val = val
#         self.next = None
#         self.prev = None

class LRUCache:
    def __init__(self, capacity: int):
        # self.head = ListNode(-1, -1)
        # self.tail = ListNode(-1, -1)
        # self.head.next = self.tail
        # self.tail.prev = self.head
        # self.lru = {}
        # self.capacity = capacity
        self.lru = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        # if key not in self.lru: return -1
        # node = self.lru[key]
        # res = node.val

        # self.remove(node)
        # self.add(node)
        # return res
        if key not in self.lru: return -1
        self.lru.move_to_end(key)
        return self.lru[key]

    def put(self, key: int, value: int) -> None:
        # if key not in self.lru: 
        #     if len(self.lru) == self.capacity: 
        #         n = self.remove(self.tail.prev)
        #         self.lru.pop(n.key)
        #         del n

        #     node = ListNode(key, value)
        #     self.add(node)
        #     self.lru[key] = node
        # else:
        #     node = self.lru[key]
        #     node.val = value
        #     self.remove(node)
        #     self.add(node)
        if key in self.lru: self.lru.move_to_end(key)
        elif len(self.lru) == self.capacity: self.lru.popitem(False)
        
        self.lru[key] = value

    # def remove(self, node):
    #     prev = node.prev
    #     nxt = node.next
    #     prev.next = nxt
    #     nxt.prev = prev

    #     node.next = None
    #     node.prev = None
    #     return node
    
    # def add(self, node):
    #     prevHead = self.head.next
    #     prevHead.prev = node
    #     node.next = prevHead

    #     node.prev = self.head
    #     self.head.next = node

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)