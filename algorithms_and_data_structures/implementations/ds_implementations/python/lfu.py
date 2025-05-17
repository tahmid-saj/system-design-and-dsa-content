
from collections import OrderedDict, defaultdict
class Node:
    def __init__(self, key=None, val=None):
        self.key = key
        self.val = val
        self.freq = 1
        self.next = self.prev = None

class DLL:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0
    
    def __len__(self):
        return self.size
    
    def add(self, node):
        nextNode = self.head.next
        node.prev = self.head
        node.next = nextNode
        self.head.next = node
        nextNode.prev = node

        self.size += 1
    
    def remove(self, node):
        if self.size == 0: return
        prevNode = node.prev
        nextNode = node.next
        prevNode.next = nextNode
        nextNode.prev = prevNode
        node.next = node.prev = None

        self.size -= 1
        return node

class LFUCache:
    def __init__(self, capacity: int):
        # Manual DLL
        self.freq = defaultdict(DLL)
        self.lfu = {}
        self.capacity = capacity
        self.minFreq = 0

        # OrderedDict
        # self.cache = {}
        # self.frequencies = defaultdict(OrderedDict)
        # self.minf = 0
        # self.capacity = capacity

    # OrderedDict    
    # def insert(self, key, frequency, value):
    #     # Manual DLL
    #     self.cache[key] = (frequency, value)
    #     self.frequencies[frequency][key] = value

    def get(self, key: int) -> int:
        # Manual DLL
        if key not in self.lfu: return -1

        node = self.lfu[key]
        self.freq[node.freq].remove(node)

        if len(self.freq[node.freq]) == 0: 
            self.freq.pop(node.freq)
            # The DLL needs to be deleted if it's size is 0. If the freq of the DLL is equal to the minFreq, 
            # then we need to increase minFreq by 1 since freq == minFreq (and we're performing a get operation, so we increase the freq by 1)
            if node.freq == self.minFreq: self.minFreq += 1

        node.freq += 1
        self.freq[node.freq].add(node)
        return node.val

        # OrderedDict
        # if key not in self.cache: return -1
        # frequency, value = self.cache[key]
        # del self.frequencies[frequency][key]

        # if not self.frequencies[frequency]:
        #     del self.frequencies[frequency]
        #     if frequency == self.minf: self.minf += 1

        # self.insert(key, frequency + 1, value)

        # return value

    def put(self, key: int, value: int) -> None:
        # Manual DLL
        if self.capacity == 0: return
        if key in self.lfu:
            self.lfu[key].val = value
            self.get(key)
            return
        
        if len(self.lfu) == self.capacity:
            dll = self.freq[self.minFreq]
            toDelete = self.freq[self.minFreq].remove(dll.tail.prev)
            self.lfu.pop(toDelete.key)
            del toDelete
        
        node = Node(key, value)
        self.lfu[key] = node
        self.freq[1].add(node)
        self.minFreq = 1

        # OrderedDict
        # if self.capacity <= 0: return
        # if key in self.cache:
        #     frequency = self.cache[key][0]
        #     self.cache[key] = (frequency, value)
        #     self.get(key)
        #     return

        # if self.capacity == len(self.cache):
        #     key_to_delete, frequency = self.frequencies[self.minf].popitem(last=False)
        #     del self.cache[key_to_delete]

        # self.minf = 1
        # self.insert(key, 1, value)


# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)