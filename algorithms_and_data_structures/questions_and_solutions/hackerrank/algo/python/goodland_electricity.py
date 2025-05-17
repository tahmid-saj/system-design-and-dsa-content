def pylons(k, arr):
  count, last, limit, newPoint = 0, -1, k, -1
  
  while last + k < len(arr):
    newPoint = -1
    for i in range(limit - 1, last, -1):
      if arr[i] == 1:
        newPoint = i
        break
    if newPoint == -1: 
      count = -1
      break
    
    last = newPoint
    limit = min(len(arr), last + (2 * k))
    count += 1
  
  return count