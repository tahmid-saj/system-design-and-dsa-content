class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = defaultdict(lambda: set())
        cols = defaultdict(lambda: set())
        grids = defaultdict(lambda: set())
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if board[i][j] == ".": continue
                if board[i][j] in rows[i]: return False
                rows[i].add(board[i][j])
                if board[i][j] in cols[j]: return False
                cols[j].add(board[i][j])
                if board[i][j] in grids[10 * (i // 3) + (j // 3)]: return False
                grids[10 * (i // 3) + (j // 3)].add(board[i][j])
        
        return True