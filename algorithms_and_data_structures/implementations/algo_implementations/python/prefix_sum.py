def prefixSum(arr):
  prefix = [0 for _ in range(len(arr))]
  prefix[0] = arr[0]
  
  for i in range(1, len(arr)):
    prefix[i] = prefix[i - 1] + arr[i]
  
  return prefix
  