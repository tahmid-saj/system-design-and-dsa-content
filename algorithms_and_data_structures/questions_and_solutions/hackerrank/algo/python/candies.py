def candies(n, arr):
  # Write your code here
  # candies[0] = 1
  # loop through arr using i from (1, len(arr)):
  #   if arr[i - 1] < arr[i]: candies[i] = candies[i] + 1
  #   else: candies[i] = 1
  cand = [1 for _ in range(len(arr))]
  for i in range(1, len(arr)):
    if arr[i - 1] < arr[i]: cand[i] = cand[i - 1] + 1
  
  for i in range(len(arr) - 2, -1, -1):
    if arr[i] > arr[i + 1] and cand[i] <= cand[i + 1]: cand[i] += (cand[i + 1] - cand[i]) + 1
  
  return sum(cand)