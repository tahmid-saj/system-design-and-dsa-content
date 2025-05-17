class Solution:
  def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
    return self.constantSpaceParentPointers(root)
    
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