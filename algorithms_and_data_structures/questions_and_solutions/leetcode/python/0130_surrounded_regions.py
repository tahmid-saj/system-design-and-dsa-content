from itertools import product
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # fill bordering cells with E using DFS
        # loop through board and change O -> X and E -> O
        borders = list(product(range(len(board)), [0, len(board[0]) - 1])) + list(product([0, len(board) - 1], range(len(board[0]))))

        for i, j in borders: self.bfs(board, i, j)

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == "E": board[i][j] = "O"
                elif board[i][j] == "O": board[i][j] = "X"
    
    def dfs(self, board, i, j):
        if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]): return
        if board[i][j] != "O": return
        board[i][j] = "E"

        self.dfs(board, i - 1, j)
        self.dfs(board, i + 1, j)
        self.dfs(board, i, j - 1)
        self.dfs(board, i, j + 1)
    
    def bfs(self, board, i, j):
        queue = deque([(i, j)])

        while queue:
            i, j = queue.popleft()
            if board[i][j] != "O": continue
            board[i][j] = "E"

            if i - 1 > 0: queue.append((i - 1, j))
            if i + 1 < len(board) - 1: queue.append((i + 1, j))
            if j - 1 > 0: queue.append((i, j - 1))
            if j + 1 < len(board[0]) - 1: queue.append((i, j + 1))