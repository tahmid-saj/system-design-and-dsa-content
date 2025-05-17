class Solution:
    def __init__(self):
        self.queue = []
        self.max = []

    def enqueue(self, x):
        self.queue.append(x)
        while self.max and self.max[-1] < x: self.max.pop()
        self.max.append(x)
    
    def dequeue(self):
        res = self.queue.pop(0)
        if res == self.max[0]: self.max.pop(0)
        return res
    
    def max(self):
        return self.max[0]