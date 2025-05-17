class CircularQueue:
    def __init__(self, k):
        self.SCALING_FACTOR = 2
        self.queue = [0 for _ in range(k)]
        self.k = k
        self.head = self.tail = self.count = 0

    def enqueue(self, val):
        if self.count == self.k:
            self.queue = self.queue[self.head:] + self.queue[:self.head]
            self.queue += [0] * (self.k * self.SCALING_FACTOR) - self.k
            self.k *= self.SCALING_FACTOR 
            self.head, self.tail = 0, self.count
        
        self.count += 1
        self.queue[self.tail % self.k] = val
        self.tail = (self.tail + 1) % self.k
    
    def dequeue(self):
        res = self.queue[self.head]
        self.head = (self.head + 1) % self.k
        self.count -= 1
        return res
    
    def size(self):
        return self.count