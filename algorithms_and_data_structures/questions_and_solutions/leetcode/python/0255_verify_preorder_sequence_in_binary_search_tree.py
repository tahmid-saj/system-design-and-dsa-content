class Solution:
    def verifyPreorder(self, preorder: List[int]) -> bool:
        # return self.monotonicStack(preorder)
        # return self.constantSpace(preorder)
        return self.recursive(preorder)
    
    def monotonicStack(self, preorder):
        if len(preorder) == 1: return True
        stk, minLimit = [], -math.inf

        for i in range(len(preorder)):
            while stk and stk[-1] < preorder[i]: minLimit = stk.pop()
            if preorder[i] <= minLimit: return False
            stk.append(preorder[i])
        return True

    def constantSpace(self, preorder):
        if len(preorder) == 1: return True
        i, minLimit = 0, -math.inf

        for j in range(len(preorder)):
            while i > 0 and preorder[i - 1] < preorder[j]:
                minLimit = preorder[i - 1]
                i -= 1
            if preorder[j] <= minLimit: return False
            preorder[i] = preorder[j]
            i += 1
        return True
    
    def recursive(self, preorder):
        self.i = 0
        def helper(minLimit, maxLimit):
            if self.i == len(preorder): return True
            root = preorder[self.i]
            if not minLimit < root < maxLimit: return False
            self.i += 1
            left = helper(minLimit, root)
            right = helper(root, maxLimit)
            return left or right

        return helper(-math.inf, math.inf)