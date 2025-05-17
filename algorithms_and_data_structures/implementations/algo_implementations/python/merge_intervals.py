
#class Interval:
#  def __init__(self, start, end):
#    self.start = start
#    self.end = end

#  def print_interval(self):
#    print("[" + str(self.start) + ", " + str(self.end) + "]", end='')

class Solution:
  def merge(self, intervals):
    if len(intervals) == 0: return []
    if len(intervals) == 1: return intervals
    
    intervals.sort(key=lambda x: x.start)
    start, end, res = intervals[0].start, intervals[0].end, []
    for i in range(1, len(intervals)):
      if intervals[i].start <= end:
        end = max(end, intervals[i].end)
      else:
        res.append(Interval(start, end))
        start = intervals[i].start
        end = intervals[i].end
    
    res.append(Interval(start, end))
    return res