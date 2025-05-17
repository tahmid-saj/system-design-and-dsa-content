from sortedcontainers import SortedList
class MyCalendar:
    def __init__(self):
        # manually sorted list
        # self.list = []

        # sortedlist module
        self.sortedList = SortedList()

    def book(self, start: int, end: int) -> bool:
        # manually sorted list
        # if not self.list:
        #     self.list.append([start, end])
        #     return True
        # else:
        #     for i in range(len(self.list)):
        #         s, e = self.list[i]
        #         if not (end <= s or e <= start): return False
        #     self.list.append([start, end])
        #     self.list.sort(key=lambda x: x[0])
        # return True
        
        # sortedlist module
        if len(self.sortedList) == 0: 
            self.sortedList.add((start, end))
            return True
        i = self.sortedList.bisect_right((start, end))
        if (i - 1 >= 0 and start < self.sortedList[i - 1][1]) or (i < len(self.sortedList) and end > self.sortedList[i][0]): return False
        self.sortedList.add((start, end))
        return True


# Your MyCalendar object will be instantiated and called as such:
# obj = MyCalendar()
# param_1 = obj.book(start,end)