from collections import deque
class MovingAverage:

    def __init__(self, size: int):
        self.size = size
        self.currSum = 0
        self.queue = deque()

    def next(self, val: int) -> float:
        self.currSum += val
        self.queue.append(val)
        if len(self.queue) <= self.size: return self.currSum / len(self.queue)
        
        startWindowVal = self.queue.popleft()
        self.currSum -= startWindowVal
        return self.currSum / self.size



# Your MovingAverage object will be instantiated and called as such:
# obj = MovingAverage(size)
# param_1 = obj.next(val)