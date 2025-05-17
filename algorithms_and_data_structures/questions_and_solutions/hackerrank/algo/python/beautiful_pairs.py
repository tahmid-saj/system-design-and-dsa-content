from collections import Counter
def beautifulPairs(A, B):
  A.sort()
  B.sort()
  
  ACounter = Counter(A)
  BCounter = Counter(B)
  
  res, canChange = 0, 0
  for k, v in ACounter.items():
    if k in BCounter: res += min(BCounter[k], v)
    else: canChange += 1
  
  if canChange > 0: res += 1
  else: res -= 1
  
  return res