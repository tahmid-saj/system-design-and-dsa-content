class Solution:
    def isAdditiveNumber(self, num: str) -> bool:
        if len(num) < 3: return False
        return self.backtrack(num, None, None, None, 0)
    
    def backtrack(self, num, first=None, second=None, curr=None, index=0):
        if index == len(num) and curr != None: return True

        for i in range(index, len(num)):
            s = num[index: i + 1]
            if first == None: 
                if s.isnumeric():
                    if len(s) > 1 and s[0] == "0": continue
                    first = int(s)
                    if self.backtrack(num, first, second, curr, i + 1): return True
                    first = None
                else: continue
            elif second == None: 
                if s.isnumeric():
                    if len(s) > 1 and s[0] == "0": continue
                    second = int(s)
                    if self.backtrack(num, first, second, curr, i + 1): return True
                    second = None
                else: continue
            elif first != None and second != None: 
                if s.isnumeric():
                    if len(s) > 1 and s[0] == "0": continue
                    curr = int(s)
                    if first + second == curr and self.backtrack(num=num, first=second, second=curr, curr=0, index=i + 1): return True
                    elif first + second < curr: return False
                    elif first + second > curr: continue

        return False