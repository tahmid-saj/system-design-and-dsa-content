class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        # can only add openPs when openPs < n, can only add closedPs when closedPs < openPs
        # self.backtrack(n, res, comb, index, openPs, closedPs)
        # if len(comb) == (n * 2): res.append(comb)
        # for i in range(index, (n * 2)):
        #   if openPs < n: 
        #       comb += "(":
        #       self.backtrack(n, res, comb, index + 1, openPs + 1, closedPs)
        #       comb = str(comb[:-1])
        #   if closedPs < openPs:
        #       comb += ")"
        #       self.backtrack(n, res, comb, index + 1, openPs, closedPs + 1)
        #       comb = str(comb[:-1])

        # res = []
        # comb = ["" for _ in range(2 * n)]
        # self.recursive(n, res, comb, 0, 0, 0)
        # return res

        # res = []
        # comb = []
        # self.backtrack(n, res, comb, 0, 0)
        # return res

        return self.divideAndConquer(n)
    
    def recursive(self, n, res, comb, openPs, closedPs):
        if openPs == n and closedPs == n:
            res.append("".join(comb))
            return

        if openPs < n: 
            comb[index] = "("
            self.recursive(n, res, comb, index + 1, openPs + 1, closedPs)
        if closedPs < openPs:
            comb[index] = ")"
            self.recursive(n, res, comb, index + 1, openPs, closedPs + 1)
    
    def backtrack(self, n, res, comb, openPs, closedPs):
        if len(comb) == (2 * n) and openPs == n and closedPs == n:
            res.append("".join(comb))
            return
        
        if openPs < n:
            comb.append("(")
            self.backtrack(n, res, comb, openPs + 1, closedPs)
            comb.pop()
        
        if closedPs < openPs:
            comb.append(")")
            self.backtrack(n, res, comb, openPs, closedPs + 1)
            comb.pop()
    
    def divideAndConquer(self, n):
        res = []
        if n == 0: return [""]

        for left_count in range(0, n):
            for left_str in self.divideAndConquer(left_count):
                for right_str in self.divideAndConquer(n - 1 - left_count):
                    res.append("(" + left_str + ")" + right_str)
        
        return res