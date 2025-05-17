class Solution:
  def maxUniqueSplit(self, s: str) -> int:
    uniques = set()
    return self.backtrack(s, 0, uniques)
  
  def backtrack(self, s, start, uniques):
    if start == len(s): return len(uniques)

    maxSubstrs = 0
    for i in range(start, len(s)):
      substr = s[start:i + 1]
      if substr not in uniques:
        uniques.add(substr)
        maxSubstrs = max(maxSubstrs, self.backtrack(s, i + 1, uniques))
        uniques.remove(substr)
    
    return maxSubstrs