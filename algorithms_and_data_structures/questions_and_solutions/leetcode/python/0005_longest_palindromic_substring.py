class Solution:
  def longestPalindrome(self, s: str) -> str:
    # return self.checkAllLengths(s)
    # return self.dp(s)
    return self.expandFromCenters(s)
  
  def checkAllLengths(self, s):
    res = ""

    if len(s) == 1: return s

    def isPalindrome(i, j):
      l, r = i, j - 1

      while l < r:
        if s[l] != s[r]: return False
        l += 1
        r -= 1
      
      return True

    for length in range(len(s), 0, -1):
      for start in range(0, len(s) - length + 1):
        if isPalindrome(start, start + length): return s[start:start + length]
    
    return res
  
  def dp(self, s):
    dp = [[False] * len(s) for _ in range(len(s))]
    res = [0, 0]

    for i in range(len(s)):
      dp[i][i] = True
    
    for i in range(len(s) - 1):
      if s[i] == s[i + 1]:
        dp[i][i + 1] = True
        res = [i, i + 1]
    
    for diff in range(2, len(s)):
      for i in range(0, len(s) - diff):
        j = i + diff
        if s[i] == s[j] and dp[i + 1][j - 1] == True: 
          dp[i][j] = True
          res = [i, j]
    
    return s[res[0]:res[1] + 1]

  def expandFromCenters(self, s):
    def expand(i, j):
      while i >= 0 and j < len(s) and s[i] == s[j]:
        i -= 1
        j += 1
      
      return j - i - 1
    
    res = [0, 0]

    for i in range(0, len(s)):
      oddLength = expand(i, i)
      if oddLength > res[1] - res[0] + 1:
        dist = oddLength // 2
        res = [i - dist, i + dist]

      evenLength = expand(i, i + 1)
      if evenLength > res[1] - res[0] + 1:
        dist = evenLength // 2 - 1 
        res = [i - dist, i + 1 + dist]
    
    return s[res[0]:res[1] + 1]