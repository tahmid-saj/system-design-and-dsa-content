def maxMin(k, arr):
  # Write your code here
  # unfairness = math.inf
  # backtrack(k, arr, index, comb, currMin, currMax)
  arr.sort()
  res = math.inf
  for i in range(len(arr) - k + 1):
    j = i + k - 1
    if arr[j] - arr[i] < res: res = arr[j] - arr[i]
  
  return res