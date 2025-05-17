class Solution:
    def closure(self):
        self.usingClosure()
        self.notUsingClosure()
    
    def usingClosure(self):
        increment_by_i = [lambda x: x + i for i in range(10)]
        print(increment_by_i[3](4))
    
    def notUsingClosure(self):
        def createIncrementFunction(x):
            return lambda y: y + x
        
        increment_by_i = [createIncrementFunction(i) for i in range(10)]
        print(increment_by_i[3](4))