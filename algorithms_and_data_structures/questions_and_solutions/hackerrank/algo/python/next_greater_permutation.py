def biggerIsGreater(w):
  # Write your code here
  # traverse from right to left using i looking for a decrease using ord, if no decrease is found, return "no answer", store as ele
  # if a decrease is found, find the first element greater than ele going from right, swap them
  # reverse the elements from the ele to the right
  w = list(w)
  ele, index = None, None
  for i in range(len(w) - 1, 0, -1):
    if ord(w[i - 1]) < ord(w[i]): 
      ele = w[i - 1]
      index = i - 1
      break
  if not ele: return "no answer"
  
  rightEle, rightIndex = None, None
  for i in range(len(w) - 1, index, -1):
    if ord(w[i]) > ord(ele):
      rightEle = w[i]
      rightIndex = i
      break
          
          
  w[index], w[rightIndex] = w[rightIndex], w[index]
  res = list(w[:index + 1]) + list(reversed(w[index + 1::]))
  return "".join(res)