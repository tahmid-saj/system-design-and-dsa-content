class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        # return self.simulation(n)
        return self.adjustingDirection(n)

    def simulation(self, n):
        res = [[0 for _ in range(n)] for _ in range(n)]
        row, col, i = 0, 0, 1
        rightBounds = n
        downBounds = n
        leftBounds = -1
        upBounds = -1
        # loop through (1, (n ** 2) + 1) using i:
        #   while i < (n ** 2) + 1 and col < rightBounds:
        #       res[row, col] = i, i += 1, col += 1
        #   col -= 1, row += 1, rightBounds -= 1
        #   while i < (n ** 2) + 1 and row < downBounds:
        #       res[row, col] = i, i += 1, row += 1
        #   row -= 1, col -= 1, downBounds -= 1
        #   while i < (n ** 2) + 1 and col > leftBounds:
        #       res[row, col] = i, i += 1, col -= 1
        #   col += 1, row -= 1, leftBounds += 1
        #   while i < (n ** 2) + 1 and row > upBounds + 1:
        #       res[row, col] = i, i += 1, row -= 1
        #   row -= 1, col += 1, upBounds += 1
        while i < (n ** 2) + 1:
            while i < (n ** 2) + 1 and col < rightBounds:
                res[row][col] = i
                i += 1
                col += 1
            col -= 1
            row += 1
            rightBounds -= 1

            while i < (n ** 2) + 1 and row < downBounds:
                res[row][col] = i
                i += 1
                row += 1
            row -= 1
            col -= 1
            downBounds -= 1

            while i < (n ** 2) + 1 and col > leftBounds:
                res[row][col] = i
                i += 1
                col -= 1
            col += 1
            row -= 1
            leftBounds += 1

            while i < (n ** 2) + 1 and row > upBounds + 1:
                res[row][col] = i
                i += 1
                row -= 1
            row += 1
            col += 1
            upBounds += 1
        
        return res
    
    def adjustingDirection(self, length):
        m, n = length, length
        direction, i, j, c, res = 1, 0, -1, 1, [[0 for _ in range(n)] for _ in range(n)]

        while m * n > 0:
            for _ in range(m):
                j += direction
                res[i][j] = c
                c += 1
            n -= 1

            for _ in range(n):
                i += direction
                res[i][j] = c
                c += 1
            m -= 1
            direction *= -1
        
        return res