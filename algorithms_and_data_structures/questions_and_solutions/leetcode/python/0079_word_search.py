class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == word[0]:
                    if self.backtrack(board, word, i, j, 0): return True
        
        return False
    
    def backtrack(self, board, word, i, j, index):
        if index == len(word): return True
        if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]): return False
        if board[i][j] != word[index]: return False

        tmp, board[i][j] = board[i][j], '.'

        if self.backtrack(board, word, i + 1, j, index + 1) == True: return True
        if self.backtrack(board, word, i - 1, j, index + 1) == True: return True
        if self.backtrack(board, word, i, j + 1, index + 1) == True: return True
        if self.backtrack(board, word, i, j - 1, index + 1) == True: return True

        board[i][j] = tmp

        return False