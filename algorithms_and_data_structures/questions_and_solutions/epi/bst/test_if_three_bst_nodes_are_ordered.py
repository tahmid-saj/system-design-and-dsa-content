class Solution:
    def testIfThreeBSTNodesAreOrdered(self, node1, node2, middle):
        # return self.bruteForce(node1, node2, middle)
        return self.interleavingSearch(node1, node2, middle)

    def bruteForce(self, node1, node2, middle):
        self.secondNodeFound = False
        self.middleFound = False
        if (node1 == node2) or (node1 == middle) or (node2 == middle): return False
        
        def dfsMiddle(node):
            if not self.secondNodeFound and node == node2: return False
            if node == middle:
                self.middleFound = True
                return True
            if node.left: return dfsMiddle(node.left)
            if node.right: return dfsMiddle(node.right)
        if not dfsMiddle(node1) or not self.middleFound: return False

        def dfsSecondNode(node):
            if node == node2:
                self.secondNodeFound = True
                return True
            if node.left: return dfsSecondNode(node.left)
            if node.right: return dfsSecondNode(node.right)
        if not dfsSecondNode(middle) or not self.secondNodeFound: return False
        return True

    def interleavingSearch(self, node1, node2, middle):
        n1, n2 = node1, node2
        while (n1 != node2 and n1 != middle) and (n2 != node1 and n2 != middle) and n1 and n2:
            if n1 and n1.val > middle.val: n1 = n1.left
            elif n1 and n1.val < middle.val: n1 = n1.right

            if n2 and n2.val > middle.val: n2 = n2.left
            elif n2 and n2.val < middle.val: n2 = n2.right
        if (n1 != middle and n2 != middle) or (n1 == node2) or (n2 == node1): return False

        target = n2 if n1 == middle else n1

        def dfs(node, target):
            if node.val > target.val: node = node.left
            elif node.val < target.val: node = node.right
            if node == target: return True
        
        return dfs(middle, target)