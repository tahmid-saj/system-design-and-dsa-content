class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        if len(intervals) <= 1: return True
        intervals.sort(key=lambda x: x[0])

        start, end = intervals[0][0], intervals[0][1]
        for i in range(1, len(intervals)):
            if intervals[i][0] < end: return False
            start = intervals[i][0]
            end = intervals[i][1]
        
        return True