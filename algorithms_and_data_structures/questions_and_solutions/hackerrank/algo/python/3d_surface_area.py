def surfaceArea(A):
  # Write your code here
  bottomTop, front, back, l, r, adj = 0, 0, 0, 0, 0, 0
  
  for i in range(len(A)):
    for j in range(len(A[0])):
      if A[i][j] > 0: bottomTop += 2
      if i == 0: front += A[i][j]
      if i == len(A) - 1: back += A[i][j]
      
      # add differences of boxes higher than adjacent box heights
      if i > 0 and A[i - 1][j] > A[i][j]: adj += A[i - 1][j] - A[i][j]
      if i < len(A) - 1 and A[i + 1][j] > A[i][j]: adj += A[i + 1][j] - A[i][j]
      if j > 0 and A[i][j - 1] > A[i][j]: adj += A[i][j - 1] - A[i][j]
      if j < len(A[0]) - 1 and A[i][j + 1] > A[i][j]: adj += A[i][j + 1] - A[i][j]
    l += A[i][0]
    r += A[i][len(A[0]) - 1]
  
  return bottomTop + front + back + l + r + adj