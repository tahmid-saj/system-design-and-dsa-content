import math
class Solution:
    def minimumIntervalCovering(self, intervals):
        intervals.sort(key=lambda x: x[1])
        prevEnd, res = -math.inf, 0
        for i in range(len(intervals)):
            if intervals[i][0] > prevEnd:
                prevEnd = intervals[i][1]
                res += 1
        return res