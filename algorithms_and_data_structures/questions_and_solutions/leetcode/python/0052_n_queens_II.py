class Solution:
    def totalNQueens(self, n: int) -> int:
        self.res = 0
        self.backtrack(n, 0, set(), set(), set())
        return self.res
    
    def backtrack(self, n, row, cols, diags, antiDiags):
        if row == n:
            self.res += 1
            return
        
        for col in range(n):
            diag, antiDiag = row - col, row + col
            if (col in cols) or (diag in diags) or (antiDiag in antiDiags): continue
            
            cols.add(col)
            diags.add(diag)
            antiDiags.add(antiDiag)

            self.backtrack(n, row + 1, cols, diags, antiDiags)

            cols.remove(col)
            diags.remove(diag)
            antiDiags.remove(antiDiag)