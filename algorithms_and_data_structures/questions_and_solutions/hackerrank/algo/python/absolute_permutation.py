def absolutePermutation(n, k):
  # Write your code here
  if k == 0:
    return [str(i) for i in range(1, n + 1)]
  else:
    if n % k == 0 and (n // k) % 2 == 0:
      a = [0 for _ in range(n)]
        
      for cl in range(n // (2 * k)):
        for i in range(k):
          a[i + 2 * k * cl] = 2 * k * cl + i + k
          a[i + 2 * k * cl + k] = i + 2 * k * cl
      return [str(x + 1) for x in a]
    else:
      return [-1]