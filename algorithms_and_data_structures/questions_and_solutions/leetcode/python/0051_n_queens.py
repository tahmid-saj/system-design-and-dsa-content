class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        self.res = []
        board = [["." for _ in range(n)] for _ in range(n)]
        self.backtrack(n, 0, set(), set(), set(), board)
        return self.res
    
    def backtrack(self, n, row, cols, diags, antiDiags, board):
        if row == n:
            self.res.append(self.format(board))
            return
        
        for col in range(n):
            diag, antiDiag = row - col, row + col
            if (col in cols) or (diag in diags) or (antiDiag in antiDiags): continue

            cols.add(col)
            diags.add(diag)
            antiDiags.add(antiDiag)
            board[row][col] = "Q"

            self.backtrack(n, row + 1, cols, diags, antiDiags, board)

            cols.remove(col)
            diags.remove(diag)
            antiDiags.remove(antiDiag)
            board[row][col] = "."

    def format(self, board):
        res = []
        for row in board: res.append("".join(row))
        return res