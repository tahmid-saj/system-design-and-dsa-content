def inorder(root):
  res = []
  prev, curr = None, root

  while curr:
    if curr.left == None:
      res.append(curr.val)
      curr = curr.right
    else:
      prev = curr.left
      while prev.right: prev = prev.right

      prev.right = curr

      tmp = curr
      curr = curr.left
      tmp.left = None

  return res

def preorder(root):
  res = []
  prev, curr = None, root

  while curr:
    if curr.left == None:
      res.append(curr.val)
      curr = curr.right
    else:
      prev = curr.left
      while prev.right and prev.right != curr: prev = prev.right

      if prev.right == None:
        res.append(curr.val)
        prev.right = curr
        curr = curr.left
      else:
        prev.right = None
        curr = curr.right
  
  return res

def postorder(root):
  res = []
  prev, curr = None, root

  while curr:
    if curr.right == None:
      res.append(curr.val)
      curr = curr.left
    else:
      prev = curr.right
      while prev.left and prev.left != curr: prev = prev.left

      if prev.left == None:
        res.append(curr.val)
        prev.left = curr
        curr = curr.right
      else:
        prev.left = None
        curr = curr.left
  
  return res[::-1]