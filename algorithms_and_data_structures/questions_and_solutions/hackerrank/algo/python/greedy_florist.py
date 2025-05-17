def getMinimumCost(k, c):
  numFlowers = len(c)
  # if numFlowers <= k: sort c in ascending order and return the sum of c[:numFlowers]
  # else:
  # for i in range(k): add the most expensive flowers and numFlowers -= 1
  # for i in range(numFlowers): add the least expensive flowers and numFlowers -= 1
  c.sort()
  if numFlowers <= k: return sum(c[:numFlowers])
  else:
    res, lastFlower = 0, len(c) - 1
    kBought = []
    for i in range(k): 
      res += c[-(i + 1)]
      heappush(kBought, 1)
      lastFlower -= 1
      numFlowers -= 1
    
    i = lastFlower
    while numFlowers > 0:
      minKBoughtFlowers = heappop(kBought)
      res += (minKBoughtFlowers + 1) * c[lastFlower]
      heappush(kBought, minKBoughtFlowers + 1)
      lastFlower -= 1
      numFlowers -= 1
    
    return res