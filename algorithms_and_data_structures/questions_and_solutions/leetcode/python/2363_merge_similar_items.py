from collections import defaultdict

class OrderedSet:
    def __init__(self):
        self.set = set()
        self.nums = []
    
    def add(self, x):
        if x[0] not in self.set:
            self.set.add(x[0])
            self.nums.append(x)
            self.nums.sort(key=lambda x: x[0])
        else:
            i = self.orderOfKey(x[0])
            self.nums[i][1] += x[1]
    
    def findByOrder(self, i):
        if i < 0 or i >= len(self.nums): return None
        return self.nums[i]
    
    def orderOfKey(self, x):
        return sum(1 for val in self.nums if val[0] < x)

class Solution:
    def mergeSimilarItems(self, items1: List[List[int]], items2: List[List[int]]) -> List[List[int]]:
        return self.orderedSet(items1, items2)
        # return self.orderedDict(items1, items2)

    def orderedSet(self, items1, items2):
        orderedSet = OrderedSet()
        for item in items1: orderedSet.add(item)
        for item in items2: orderedSet.add(item)
        return orderedSet.nums
    
    def orderedDict(self, items1, items2):
        merged = defaultdict(int)

        for v, w in items1: merged[v] += w
        for v, w in items2: merged[v] += w

        return sorted([[v, w] for v, w in merged.items()], key=lambda x: x[0])