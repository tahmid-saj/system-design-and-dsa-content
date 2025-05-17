class OrderedSet:
    def __init__(self):
        self.set = []
    
    def add(self, element):
        if element not in self.set:
            self.set.append(element)
            self.set.sort(key=lambda x: x[0])
    
    def findByOrder(self, k):
        if k < 0 or k >= len(self.set): return None
        return self.set[k]

    def orderByKey(self, start, end, granularity):
        return [x[1] for x in self.set if x[0][:granularity] <= end[:granularity] and x[0][:granularity] >= start[:granularity]]

class LogSystem:
    def __init__(self):
        self.os = OrderedSet()
        self.granularity = {
            "Year": 4,
            "Month": 7,
            "Day": 10,
            "Hour": 13,
            "Minute": 16,
            "Second": 19
        }

    def put(self, id: int, timestamp: str) -> None:
        self.os.add([timestamp, id])

    def retrieve(self, start: str, end: str, granularity: str) -> List[int]:
        return self.os.orderByKey(start, end, self.granularity[granularity])


# Your LogSystem object will be instantiated and called as such:
# obj = LogSystem()
# obj.put(id,timestamp)
# param_2 = obj.retrieve(start,end,granularity)