class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        self.dp = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                self.dp[i][j] += matrix[i][j]
                if i > 0 and j > 0: self.dp[i][j] -= self.dp[i - 1][j - 1]
                if i > 0: self.dp[i][j] += self.dp[i - 1][j]
                if j > 0: self.dp[i][j] += self.dp[i][j - 1]
        
    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        row3, col3 = row2, col1
        row4, col4 = row1, col2
        dpLeft, dpTop, dpTopLeft = 0, 0, 0
        if col3 > 0: dpLeft = self.dp[row3][col3 - 1]
        if row4 > 0: dpTop = self.dp[row4 - 1][col4]
        if row1 > 0 and col1 > 0: dpTopLeft = self.dp[row1 - 1][col1 - 1]
        return self.dp[row2][col2] - dpLeft - dpTop + dpTopLeft

# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# param_1 = obj.sumRegion(row1,col1,row2,col2)