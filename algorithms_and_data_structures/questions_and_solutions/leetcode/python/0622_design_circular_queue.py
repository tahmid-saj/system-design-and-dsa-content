class Node:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class MyCircularQueue:
    def __init__(self, k: int):
        self.queue = [0] * k
        self.head = 0
        self.count = 0
        self.k = k

        # self.size = 0
        # self.k = k
        # self.head = Node()
        # self.tail = Node()

    def enQueue(self, value: int) -> bool:
        if self.isFull(): return False
        self.queue[(self.head + self.count) % self.k] = value
        self.count += 1
        return True

        # insert at the tail
        # if self.isFull(): return False
        # node = Node(value)
        # if self.size == 0:
        #     self.head.next = node
        #     self.tail.next = node
        # else:
        #     self.tail.next.next = node
        #     self.tail.next = node
        # self.size += 1
        # return True

    def deQueue(self) -> bool:
        if self.isEmpty(): return False
        self.head = (self.head + 1) % self.k
        self.count -= 1
        return True

        # # remove at the head
        # if self.isEmpty(): return False
        # node = self.head.next
        # newHead = self.head.next.next
        # del node
        # self.head.next = newHead
        # self.size -= 1
        # return True

    def Front(self) -> int:
        if self.isEmpty(): return -1
        return self.queue[self.head % self.k]

        # if self.isEmpty(): return -1
        # return self.head.next.val

    def Rear(self) -> int:
        if self.isEmpty(): return -1
        return self.queue[(self.head + self.count - 1) % self.k]

        # if self.isEmpty(): return -1
        # return self.tail.next.val

    def isEmpty(self) -> bool:
        return self.count == 0

        # return self.size == 0

    def isFull(self) -> bool:
        return self.count == self.k

        # return self.size == self.k

# Your MyCircularQueue object will be instantiated and called as such:
# obj = MyCircularQueue(k)
# param_1 = obj.enQueue(value)
# param_2 = obj.deQueue()
# param_3 = obj.Front()
# param_4 = obj.Rear()
# param_5 = obj.isEmpty()
# param_6 = obj.isFull()