class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # return self.threeStages(intervals, newInterval)
        return self.usingMergeIntervals(intervals, newInterval)

    def threeStages(self, intervals, newInterval):
        res, i = [], 0
        if not intervals: return [newInterval]

        # add intervals to res which come prior to newInterval
        while i < len(intervals):
            if intervals[i][1] < newInterval[0]:
                res.append([intervals[i][0], intervals[i][1]])
                i += 1
            else: break
        
        start, end = newInterval[0], newInterval[1]
        while i < len(intervals):
            if intervals[i][0] <= end:
                start = min(start, intervals[i][0])
                end = max(end, intervals[i][1])
            else:
                res.append([start, end])
                break
            i += 1
        
        
        while i < len(intervals):
            res.append([intervals[i][0], intervals[i][1]])
            i += 1
        
        return res
    
    def usingMergeIntervals(self, intervals, newInterval):
        i, res = 0, []

        while i < len(intervals):
            if intervals[i][1] < newInterval[0]: res.append(intervals[i])
            else: break
            i += 1
        
        start, end = newInterval[0], newInterval[1]
        while i < len(intervals):
            if intervals[i][0] <= end:
                start = min(start, intervals[i][0])
                end = max(end, intervals[i][1])
            else:
                res.append([start, end])
                start = intervals[i][0]
                end = intervals[i][1]
            i += 1
        
        res.append([start, end])
        
        return res