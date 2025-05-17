class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        currDead, currAlive, nextDead, nextAlive = 0, 1, 2, 3
        for i in range(len(board)):
            for j in range(len(board[0])):
                neighbours = self.numNeighbours(board, i, j, currAlive)
                if board[i][j] % 2 == 1 and neighbours < 2: board[i][j] = nextDead
                elif board[i][j] % 2 == 1 and 2 <= neighbours <= 3: board[i][j] = nextAlive
                elif board[i][j] % 2 == 1 and neighbours > 3: board[i][j] = nextDead
                elif board[i][j] % 2 == 0 and neighbours == 3: board[i][j] = nextAlive
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] % 2 == 1: board[i][j] = currAlive
                else: board[i][j] = currDead
    
    def numNeighbours(self, board, i, j, currAlive):
        res = 0
        if (i > 0 and j > 0) and board[i - 1][j - 1] == currAlive: res += 1
        if (i > 0 and j < len(board[0]) - 1) and board[i - 1][j + 1] == currAlive: res += 1
        if (i < len(board) - 1 and j > 0) and board[i + 1][j - 1] == currAlive: res += 1
        if (i < len(board) - 1 and j < len(board[0]) - 1) and board[i + 1][j + 1] == currAlive: res += 1
        if i > 0 and board[i - 1][j] == currAlive: res += 1
        if j > 0 and board[i][j - 1] == currAlive: res += 1
        if i < len(board) - 1 and board[i + 1][j] == currAlive: res += 1
        if j < len(board[0]) - 1 and board[i][j + 1] == currAlive: res += 1
        return res