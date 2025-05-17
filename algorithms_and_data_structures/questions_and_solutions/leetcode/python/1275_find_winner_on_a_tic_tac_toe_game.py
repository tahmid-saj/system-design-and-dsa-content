class Solution:
    def tictactoe(self, moves: List[List[int]]) -> str:
        rows, cols = [0 for _ in range(3)], [0 for _ in range(3)]
        diag, antiDiag = 0, 0
        playerMove = 1

        for move in moves:
            i, j = move
            rows[i] += playerMove
            cols[j] += playerMove
            if i == j: diag += playerMove
            if i + j == 2: antiDiag += playerMove

            if rows[i] == (playerMove * 3) or cols[j] == (playerMove * 3) or diag == (playerMove * 3) or antiDiag == (playerMove * 3): return "A" if playerMove == 1 else "B"
            playerMove *= -1

        if len(moves) == 9: return "Draw"
        return "Pending"