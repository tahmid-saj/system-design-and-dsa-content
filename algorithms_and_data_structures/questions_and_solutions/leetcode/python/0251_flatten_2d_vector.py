class Vector2D:
    def __init__(self, vec: List[List[int]]):
        self.vec = vec
        self.j = 0
        self.i = -1
        self.moveToNextValid1DVec()

    def next(self) -> int:
        res = self.vec[self.i][self.j]
        if self.j + 1 < len(self.vec[self.i]): self.j += 1
        else:
            self.moveToNextValid1DVec()
            self.j = 0

        return res

    def hasNext(self) -> bool:
        if self.i < len(self.vec) and self.j < len(self.vec[self.i]): return True
        else: return False
    
    def moveToNextValid1DVec(self):
        self.i += 1
        while self.i < len(self.vec) and len(self.vec[self.i]) == 0: self.i += 1

# Your Vector2D object will be instantiated and called as such:
# obj = Vector2D(vec)
# param_1 = obj.next()
# param_2 = obj.hasNext()