class Solution:
    def isToeplitzMatrix(self, matrix: List[List[int]]) -> bool:
        # return self.checkTopLeftValue(matrix)
        return self.checkDiagonalGroups(matrix)
    
    def checkTopLeftValue(self, matrix):
        for i in range(len(matrix) - 1, 0, -1):
            for j in range(len(matrix[0]) - 1, 0, -1):
                if matrix[i][j] != matrix[i - 1][j - 1]: return False
        return True
    
    def checkDiagonalGroups(self, matrix):
        diag = {}
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if i - j not in diag: diag[i - j] = matrix[i][j]
                elif diag[i - j] != matrix[i][j]: return False
        return True