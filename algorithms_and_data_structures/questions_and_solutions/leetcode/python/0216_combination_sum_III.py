class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        if n == 1 and k != 1: return []
        elif n == 1 and k == 1: return [[1]]
        self.res = []
        self.backtrack(k, n, 1, [], 0)
        return self.res
    
    def backtrack(self, k, n, currNum, comb, currSum):
        if currSum == n and len(comb) == k:
            self.res.append(list(comb))
            return
        elif len(comb) >= k and currSum < n: return

        for num in range(currNum, 10):
            if currSum + num <= n:
                comb.append(num)
                self.backtrack(k, n, num + 1, comb, currSum + num)
                comb.pop()