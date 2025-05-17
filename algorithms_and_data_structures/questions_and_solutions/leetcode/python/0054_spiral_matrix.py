class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        # return self.simulatingSpiralOrder(matrix)
        return self.adjustingDirection(matrix)
    
    def simulatingSpiralOrder(self, matrix):
        i, row, col, res = 0, 0, 0, []
        rightBounds = (0, len(matrix[0]))
        downBounds = (len(matrix), len(matrix[0]))
        leftBounds = (len(matrix), -1)
        upBounds = (0, -1)
        origin = (0, 0)

        while i < len(matrix) * len(matrix[0]):
            row, col = origin[0], origin[1]
            while i < len(matrix) * len(matrix[0]) and col < rightBounds[1]:
                res.append(matrix[row][col])
                col += 1
                i += 1
            rightBounds = (rightBounds[0] + 1, rightBounds[1] - 1)
            row += 1
            col -= 1
            
            while i < len(matrix) * len(matrix[0]) and row < downBounds[0]:
                res.append(matrix[row][col])
                row += 1
                i += 1
            downBounds = (downBounds[0] - 1, downBounds[1] - 1)
            row -= 1
            col -= 1

            while i < len(matrix) * len(matrix[0]) and col > leftBounds[1]:
                res.append(matrix[row][col])
                col -= 1
                i += 1
            leftBounds = (leftBounds[0] - 1, leftBounds[1] + 1)
            row -= 1
            col += 1
            
            while i < len(matrix) * len(matrix[0]) and row > upBounds[0]:
                print(row, col)
                res.append(matrix[row][col])
                row -= 1
                i += 1
            upBounds = (upBounds[0] + 1, upBounds[1] + 1)
            origin = (origin[0] + 1, origin[1] + 1)
        
        return res
    
    def adjustingDirection(self, matrix):
        m, n = len(matrix), len(matrix[0])
        direction, i, j, res = 1, 0, -1, []

        while m * n > 0:
            for _ in range(n): # move horizontally
                j += direction
                res.append(matrix[i][j])
            m -= 1

            for _ in range(m): # move vertically
                i += direction
                res.append(matrix[i][j])
            n -= 1
            direction *= -1
        
        return res