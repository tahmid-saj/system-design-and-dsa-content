# inorder traversal
class Solution:
  def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
    # return self.iterative(root)
    # return self.morrisTraversal(root)
    return self.constantSpaceParentPointers(root)

  def iterative(self, root):
    stk, res = [], []

    while stk or root:
      while root:
        stk.append(root)
        root = root.left
      root = stk.pop()

      res.append(root.val)
      root = root.right

    return res

  def constantSpaceParentPointers(self, root):
    res, prev = [], None

    while root:
      if root.parent == prev:
        if root.left: next = root.left
        else:
          res.append(root.val)
          next = root.right or root.parent
      elif root.left == prev:
        res.append(root.val)
        next = root.right or root.parent
      else: next = root.parent
      root, prev = next, root

    return res

# preorder traversal
class Solution:
  def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
    # return self.iterative(root)

    return self.morrisTraversal(root)

  def iterative(self, root):
    if not root: return []
    stk, res = [root], []

    while stk:
      node = stk.pop()
      res.append(node.val)
      if node.right: stk.append(node.right)
      if node.left: stk.append(node.left)

    return res

# postorder traversal
class Solution:
  def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
    # return self.iterativeTwoStacks(root)
    # return self.iterativeOneStack(root)
    return self.morrisTraversal(root)

  def iterativeTwoStacks(self, root):
    if not root: return []
    res, resPreorder, stk = [], [], [root]

    while stk:
      node = stk.pop()
      resPreorder.append(node.val)
      if node.left: stk.append(node.left)
      if node.right: stk.append(node.right)
    
    while resPreorder: res.append(resPreorder.pop())
    return res

  def iterativeOneStack(self, root):
    if not root: return []
    new, leftDone, rightDone = 0, 1, 2
    res, stk = [], [(root, new)]

    while stk:
      node, status = stk[-1]
      if status == rightDone:
        stk.pop()
        res.append(node.val)
      else:
        stk[-1] = (stk[-1][0], stk[-1][1] + 1)
        nextNode = node.left if status == new else node.right
        if nextNode: stk.append((nextNode, new))
    
    return res
