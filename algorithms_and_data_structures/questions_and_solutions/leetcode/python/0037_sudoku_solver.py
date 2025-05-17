class Solution:
  def solveSudoku(self, board: List[List[str]]) -> None:
    """
    Do not return anything, modify board in-place instead.
    """
    self.backtrack(board)
    return board
  
  def backtrack(self, board):
    for i in range(0, len(board)):
      for j in range(0, len(board[0])):
        if board[i][j] == '.':
          for n in range(1, 10):
            if self.validCell(board, i, j, str(n)): 
              board[i][j] = str(n)
              if self.backtrack(board): return True
              else: board[i][j] = '.'
          return False

    return True
  
  def validCell(self, board, row, col, n):
    for i in range(0, 9):
      if board[row][i] == n: return False
      if board[i][col] == n: return False
      if board[(row // 3)*3 + (i // 3)][(col // 3)*3 + (i % 3)] == n: return False

    return True