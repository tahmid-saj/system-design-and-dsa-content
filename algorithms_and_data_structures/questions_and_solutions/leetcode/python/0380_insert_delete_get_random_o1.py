class RandomizedSet:
    def __init__(self):
        self.index = {}
        self.list = []

    def insert(self, val: int) -> bool:
        if val in self.index: return False

        length = len(self.list)
        self.index[val] = length
        self.list.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.index: return False

        i, j = self.index[val], len(self.list) - 1
        self.index[self.list[j]] = i
        self.list[i], self.list[j] = self.list[j], self.list[i]

        del self.list[-1]
        del self.index[val]
        return True
    
    def getRandom(self) -> int:
        return random.choice(self.list)

# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()