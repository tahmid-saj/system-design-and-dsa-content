class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        # O(n) space
        # rows, cols = set(), set()
        # for i in range(len(matrix)):
        #     for j in range(len(matrix[0])):
        #         if matrix[i][j] == 0:
        #             rows.add(i)
        #             cols.add(j)
        
        # for i in range(len(matrix)):
        #     if i in rows: matrix[i] = [0 for _ in range(len(matrix[0]))]
        #     for j in range(len(matrix[0])):
        #         if j in cols: matrix[i][j] = 0

        # O(1) space
        setFirstColZero = False

        for i in range(len(matrix)):
            if matrix[i][0] == 0: setFirstColZero = True
            for j in range(1, len(matrix[0])):
                if matrix[i][j] == 0:
                    matrix[0][j] = 0
                    matrix[i][0] = 0
        
        for i in range(1, len(matrix)):
            for j in range(1, len(matrix[0])):
                if matrix[i][0] == 0 or matrix[0][j] == 0: matrix[i][j] = 0
        
        # first row
        if matrix[0][0] == 0:
            for j in range(len(matrix[0])): matrix[0][j] = 0
        
        # first col
        if setFirstColZero == True:
            for i in range(len(matrix)): matrix[i][0] = 0