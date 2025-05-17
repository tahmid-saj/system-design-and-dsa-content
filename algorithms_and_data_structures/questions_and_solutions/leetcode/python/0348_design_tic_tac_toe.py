class TicTacToe:
    def __init__(self, n: int):
        self.rows = [0 for _ in range(n)]
        self.cols = [0 for _ in range(n)]
        self.diag = 0
        self.antiDiag = 0
        self.n = n

    def move(self, row: int, col: int, player: int) -> int:
        update = 1 if player == 1 else -1
        # update rows
        self.rows[row] += update
        if self.rows[row] == (update * self.n): return 1 if player == 1 else 2

        # update cols
        self.cols[col] += update
        if self.cols[col] == (update * self.n): return 1 if player == 1 else 2

        # update diag and antiDiag
        if col == row: self.diag += update
        if row + col == self.n - 1: self.antiDiag += update

        # check if the game is won on diags
        if self.diag == (update * self.n): return 1 if player == 1 else 2
        if self.antiDiag == (update * self.n): return 1 if player == 1 else 2

        return 0


# Your TicTacToe object will be instantiated and called as such:
# obj = TicTacToe(n)
# param_1 = obj.move(row,col,player)