class Solution:
  def lengthOfLongestSubstring(self, s: str) -> int:
    # return self.slidingWindow(s)
    return self.slidingWindowOptimized(s)

  def slidingWindow(self, s):
    res = 0
    start = 0
    letters = Counter()

    for end in range(0, len(s)):
      letters[s[end]] += 1

      while letters[s[end]] > 1:
        letters[s[start]] -= 1
        start += 1
      
      res = max(res, end - start + 1)
    
    return res

  def slidingWindowOptimized(self, s):
    res = 0
    start = 0
    letters = {}

    for end in range(0, len(s)):
      if s[end] in letters and letters[s[end]] >= start: start = letters[s[end]] + 1

      res = max(res, end - start + 1)
      letters[s[end]] = end
    
    return res