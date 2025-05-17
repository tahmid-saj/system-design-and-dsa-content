class Solution:
    def matrixReshape(self, mat: List[List[int]], r: int, c: int) -> List[List[int]]:
        # 2 x 3 -> 3 x 2

        # 1 2 3 -> 1 2
        # 4 5 6    3 4
        #          5 6
        # 5 = (1, 1) -> (2, 0)
        # 6 = (1, 2) -> (2, 1)
        size = len(mat) * len(mat[0])
        if size != r * c: return mat

        res = [[0 for i in range(c)] for j in range(r)]

        x, y = 0, 0
        for i in range(0, r):
            for j in range(0, c):
                col = y % len(mat[0])
                row = y // len(mat[0])
                res[i][j] = mat[row][col]
                y += 1
                if y >= size: return res

        return res