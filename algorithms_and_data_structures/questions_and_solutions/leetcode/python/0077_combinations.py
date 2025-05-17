class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        self.res = []
        self.backtrack(n, k, [], 1)
        return self.res

        # self.ans = []
        # self.backtrack2(n, k, [], 1)
        # return self.ans
    
    def backtrack(self, n, k, comb, index):
        if len(comb) == k:
            self.res.append(list(comb))
            return
        
        for i in range(index, n + 1):
            comb.append(i)
            self.backtrack(n, k, comb, i + 1)
            comb.pop()
    
    def backtrack2(self, n, k, curr, first_num):
        if len(curr) == k:
            self.ans.append(list(curr))
            return

        need = k - len(curr)
        remain = n - first_num + 1
        available = remain - need
        
        for num in range(first_num, first_num + available + 1):
            curr.append(num)
            self.backtrack2(n, k, curr, num + 1)
            curr.pop()

        return