from sortedcontainers import SortedList
class MyCalendarTwo:

    def __init__(self):
        self.single = SortedList()
        self.double = SortedList()

    def book(self, start: int, end: int) -> bool:
        j = self.double.bisect_right((start, end))
        if (j > 0 and start < self.double[j - 1][1]) or (j < len(self.double) and end > self.double[j][0]): return False

        i = self.single.bisect_right((start, end))
        if (i > 0 and start < self.single[i - 1][1]) or (i < len(self.single) and end > self.single[i][0]):
            # double booking
            s, e = start, end

            if i > 0 and start < self.single[i - 1][1]: s = min(start, self.single[i - 1][1])
            elif i > 0: s = self.single[i][0]

            if i < len(self.single) and end > self.single[i][0]: e = max(end, self.single[i][0])
            elif i < len(self.single): e = self.single[i - 1][1] 

            self.double.add((s, e))
        else:
            # single booking
            self.single.add((start, end))
        return True


# Your MyCalendarTwo object will be instantiated and called as such:
# obj = MyCalendarTwo()
# param_1 = obj.book(start,end)