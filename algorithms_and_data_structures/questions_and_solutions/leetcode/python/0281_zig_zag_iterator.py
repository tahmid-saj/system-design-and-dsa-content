class ZigzagIterator:
    def __init__(self, v1: List[int], v2: List[int]):
        self.v1 = v1
        self.v2 = v2
        self.i = 0
        self.j = 0
        self.currVec = 0 if v1 else 1

    def hasNext(self) -> bool:
        if self.currVec == 0 and self.i < len(self.v1): return True
        elif self.currVec == 1 and self.j < len(self.v2): return True
        return False

    def next(self) -> int:
        res = None
        if self.currVec == 0: 
            res = self.v1[self.i]
            self.i += 1
            self.currVec = 1 if self.j < len(self.v2) else self.currVec
        elif self.currVec == 1:
            res = self.v2[self.j]
            self.j += 1
            self.currVec = 0 if self.j < len(self.v1) else self.currVec
        
        return res

# Your ZigzagIterator object will be instantiated and called as such:
# i, v = ZigzagIterator(v1, v2), []
# while i.hasNext(): v.append(i.next())