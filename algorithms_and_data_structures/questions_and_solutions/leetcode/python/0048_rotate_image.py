class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        # return self.transposeFlip(matrix)
        return self.rotateGroupsOf4Cells(matrix)

    def transposeFlip(self, matrix):
        # find the transpose, flip the columns
        for i in range(0, len(matrix)):
            for j in range(i + 1, len(matrix[0])): matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        
        for i in range(0, len(matrix)):
            for j in range(0, (len(matrix[0]) // 2)): matrix[i][j], matrix[i][len(matrix[0]) - j - 1] = matrix[i][len(matrix[0]) - j - 1], matrix[i][j]
    
    def rotateGroupsOf4Cells(self, matrix):
        n = len(matrix)
        for i in range(n // 2 + n % 2):
            for j in range(n // 2):
                tmp = matrix[n - 1 - j][i]
                matrix[n - 1 - j][i] = matrix[n - 1 - i][n - j - 1]
                matrix[n - 1 - i][n - j - 1] = matrix[j][n - 1 - i]
                matrix[j][n - 1 - i] = matrix[i][j]
                matrix[i][j] = tmp