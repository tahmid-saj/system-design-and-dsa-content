def hackerlandRadioTransmitters(arr, k, n):
  arr.sort()
  i, res, last = 0, 0, -math.inf
  
  while i < n:
    if arr[i] <= last + k: 
      i += 1
      continue
    
    j = i
    while j < n and arr[i] >= arr[j] - k: j += 1
    
    res += 1
    last = arr[j - 1]
    
    if i == j: i += 1
    else: i = j
  
  return res