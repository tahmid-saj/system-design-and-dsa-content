class MyStack(object):

  
    def __init__(self):
        self.queue = deque()
        # append to the back
        # pop to pop from the front
        # appendleft to append to the front
        # popleft to pop from the back
        # 1 2 3 4

    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        self.queue.append(x)
        
        for i in range(len(self.queue) - 1):
            self.queue.append(self.queue.pop())

    def pop(self):
        """
        :rtype: int
        """
        return self.queue.pop()

    def top(self):
        """
        :rtype: int
        """
        return self.queue[-1]

    def empty(self):
        """
        :rtype: bool
        """
        return len(self.queue) == 0


# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()