# sorted array to BST using sorted array
class Solution:
  def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
    def helper(l, r):
      if l > r: return None
      middle = l + (r - l) // 2
      node = TreeNode(nums[middle])
      node.left = helper(l, middle - 1)
      node.right = helper(middle + 1, r)
      return node

    return helper(0, len(nums) - 1)

# sorted linked list to binary search tree
class Solution:
    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        # return self.recursiveArray(head)
        # return self.recursiveArray2(head)
        # return self.recursive(head)
        return self.inorderSimulation(head)
    
    def recursiveArray(self, head):
        if head == None: return None
        nodes = []
        while head:
            nodes.append(head.val)
            head = head.next
        
        def helper(nodes):
            mid = len(nodes) // 2
            if len(nodes) == 0: return None
            middle = TreeNode(nodes[mid])

            middle.left = helper(nodes[:mid])
            middle.right = helper(nodes[mid + 1:])

            return middle

        return helper(nodes)
    
    def recursiveArray2(self, head):
        if head == None: return None
        nodes = []
        while head:
            nodes.append(head.val)
            head = head.next
        
        def helper(l, r):
            if l > r: return None
            mid = (l + r) // 2
            middle = TreeNode(nodes[mid])
            if l == r: return middle

            middle.left = helper(l, mid - 1)
            middle.right = helper(mid + 1, r)

            return middle

        return helper(0, len(nodes) - 1)
    
    def recursive(self, head):
        if head == None: return None

        def findMiddle(start):
            prev, slow, fast = None, start, start

            while fast and fast.next:
                prev = slow
                slow = slow.next
                fast = fast.next.next
            
            if prev: prev.next = None

            return slow

        mid = findMiddle(head)
        middle = TreeNode(mid.val)
        if head == mid: return middle

        middle.left = self.recursive(head)
        middle.right = self.recursive(mid.next)

        return middle
    
    def inorderSimulation(self, head):
        if head == None: return None
        length, n = 0, head
        while n:
            length += 1
            n = n.next
        
        def helper(l, r):
            nonlocal head
            if l > r: return None

            mid = (l + r) // 2

            left = helper(l, mid - 1)

            middle = TreeNode(head.val)
            middle.left = left
            head = head.next

            middle.right = helper(mid + 1, r)

            return middle
        
        return helper(0, length - 1)
      
# inorder and preorder arrays to binary tree
class Solution:
  def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    inorderNodes = {}
    for i, v in enumerate(inorder): inorderNodes[v] = i
    preorderIndex = 0

    def helper(l, r):
      nonlocal preorderIndex
      if l > r: return None
      rootVal = preorder[preorderIndex]
      node = TreeNode(rootVal)
      preorderIndex += 1
      
      node.left = helper(l, inorderNodes[rootVal] - 1)
      node.right = helper(inorderNodes[rootVal] + 1, r)
      return node
      
    return helper(0, len(inorder) - 1)

# inorder and postorder arrays to binary tree
def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
  inorder_nodes = {}
  for i, v in enumerate(inorder): inorder_nodes[v] = i
  postorder_index = len(postorder) - 1

  def helper(l, r):
    nonlocal postorder_index
    if l > r: return None

    rootVal = postorder[postorder_index]
    mid = inorder_nodes[rootVal]
    postorder_index -= 1

    right = helper(mid + 1, r)
    left = helper(l, mid - 1)

    node = TreeNode(rootVal)
    node.right = right
    node.left = left

    return node
    
  return helper(0, len(inorder) - 1)