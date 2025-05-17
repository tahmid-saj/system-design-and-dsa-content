class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        # return self.monotonicStack(temperatures)
        return self.optimizedArray(temperatures)

    def monotonicStack(self, temperatures):
        res, stk = [0 for _ in range(len(temperatures))], []

        for i in range(len(temperatures)):
            while stk and stk[-1][0] < temperatures[i]:
                _, n = stk.pop()
                res[n] = i - n
            stk.append((temperatures[i], i))
        
        return res
    
    def optimizedArray(self, temperatures):
        res, hottest = [0 for _ in range(len(temperatures))], 0

        for i in range(len(temperatures) - 1, -1, -1):
            if temperatures[i] >= hottest:
                hottest = temperatures[i]
                continue
            
            days = 1
            while temperatures[i + days] <= temperatures[i]: days += res[i + days]
            res[i] = days
        
        return res