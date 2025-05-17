class Solution(object):
    def getRow(self, rowIndex):
        """
        :type rowIndex: int
        :rtype: List[int]
        """
        if rowIndex == 0: return [1]
        if rowIndex == 1: return [1, 1]
        prev = [1, 1]
        for i in range(2, rowIndex + 1):
            res = []
            for j in range(0, i + 1):
                if j == 0 or j == i:
                    res.append(1)
                else:
                    res.append(prev[j - 1] + prev[j])
            prev = res

        return res