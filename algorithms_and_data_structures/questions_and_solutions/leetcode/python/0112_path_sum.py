class Solution(object):
    def generate(self, numRows):
        """
        :type numRows: int
        :rtype: List[List[int]]
        """
        if numRows == 1: return [[1]]
        if numRows == 2: return [[1], [1, 1]]
        res = [[1], [1, 1]]

        for i in range(2, numRows):
            res.append([])
            for j in range(0, i + 1):
                if j == 0 or j == i:
                    res[i].append(1)
                else:
                    res[i].append(res[i - 1][j - 1] + res[i - 1][j])

        return res