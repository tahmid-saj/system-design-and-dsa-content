class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # return self.binarySearch2D(matrix, target)
        return self.binarySearchPivot(matrix, target)

    def binarySearch2D(self, matrix, target):
        l, r = [0, 0], [len(matrix) - 1, len(matrix[0]) - 1]

        while l[0] <= r[0]:
            if l[0] == r[0] and l[1] > r[1]: break

            lCol = l[1] + (l[0] * len(matrix[0]))
            rCol = r[1] + (r[0] * len(matrix[0]))
            middle = [l[0] + (r[0] - l[0]) // 2, (lCol + (rCol - lCol) // 2) % len(matrix[0])]

            if matrix[middle[0]][middle[1]] == target: return True
            if matrix[middle[0]][middle[1]] < target:
                l[0] = middle[0] + 1 if middle[1] == len(matrix[0]) - 1 else middle[0]
                l[1] = 0 if middle[1] == len(matrix[0]) - 1 else middle[1] + 1
            elif matrix[middle[0]][middle[1]] > target:
                r[0] = middle[0] - 1 if middle[1] == 0 else middle[0]
                r[1] = len(matrix[0]) - 1 if middle[1] == 0 else middle[1] - 1

            if l[0] < 0 or l[0] >= len(matrix) or l[1] < 0 or l[1] >= len(matrix[0]) \
                or r[0] < 0 or r[0] >= len(matrix) or r[1] < 0 or r[1] >= len(matrix[0]): break

        return False
    
    def binarySearchPivot(self, matrix, target):
        l, r = 0, len(matrix) * len(matrix[0]) - 1
        while l <= r:
            middle = l + (r - l) // 2
            i, j = (middle // len(matrix[0])), (middle % len(matrix[0]))
            if matrix[i][j] == target: return True
            if matrix[i][j] < target: l = middle + 1
            else: r = middle - 1
        return False