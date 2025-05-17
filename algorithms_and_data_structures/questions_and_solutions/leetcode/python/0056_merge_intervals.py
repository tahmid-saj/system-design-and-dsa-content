class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x: x[0])

        i, start, end, res = 1, intervals[0][0], intervals[0][1], []
        while i < len(intervals):
            if end >= intervals[i][0]:
                end = max(end, intervals[i][1])
            else:
                res.append([start, end])
                start = intervals[i][0]
                end = intervals[i][1]
            i += 1
        
        res.append([start, end])

        return res