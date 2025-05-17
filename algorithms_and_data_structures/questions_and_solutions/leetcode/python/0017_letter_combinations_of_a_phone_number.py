class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        # if len(comb) == len(digits): res.append(comb)
        # loop through digits using i
        # loop through letters in digitsMap[digits[i]] using j
        #   comb += letter
        #   backtrack(digits, digitsMap, i + 1, comb, res)
        #   comb = comb[:-1]
      if len(digits) == 0: return []
      self.res = []
      digitsMap = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
      }

      self.backtrack(digits, digitsMap, 0, "")
      return self.res
    
    def backtrack(self, digits, digitsMap, index, comb):
      if len(comb) == len(digits):
        self.res.append(str(comb))
        return
      
      for i in range(index, len(digits)):
        for j in range(0, len(digitsMap[digits[i]])):
          comb += digitsMap[digits[i]][j]
          self.backtrack(digits, digitsMap, i + 1, comb)
          comb = str(comb[:-1])