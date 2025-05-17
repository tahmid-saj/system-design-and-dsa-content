class Solution:
    def getFactors(self, n: int) -> List[List[int]]:
      if n == 1: return []
      res = []
      self.backtrack(n, res, [], 2)
      return res
    
    def backtrack(self, n, res, comb, start):
      for factor in range(start, int(n ** 0.5) + 1):
        if (n % factor) == 0:
          comb.append(factor)
          res.append(list(comb + [n // factor]))
          self.backtrack(n // factor, res, comb, factor)
          comb.pop()