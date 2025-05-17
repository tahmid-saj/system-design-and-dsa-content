#class Interval:
#  def __init__(self, start, end):
#    self.start = start
#    self.end = end

class Solution:
  def insert(self, intervals, new_interval):
    i, res = 0, []

    while i < len(intervals):
      if intervals[i].end < new_interval.start: res.append(intervals[i])
      else: break
      i += 1
    
    start, end = new_interval.start, new_interval.end
    while i < len(intervals):
      if intervals[i].start <= end:
        start = min(start, intervals[i].start)
        end = max(end, intervals[i].end)
      else:
        res.append(Interval(start, end))
        start = intervals[i].start
        end = intervals[i].end
      i += 1
    
    res.append(Interval(start, end))
    
    return res