class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        return self.binarySearchConstantSpace(matrix, target)

    def binarySearchConstantSpace(self, matrix, target):
        i, j = len(matrix) - 1, 0
        while i >= 0 and i < len(matrix) and j >= 0 and j < len(matrix[0]):
            val = matrix[i][j]
            if val == target: return True
            elif val < target: j += 1
            else: i -= 1
        return False