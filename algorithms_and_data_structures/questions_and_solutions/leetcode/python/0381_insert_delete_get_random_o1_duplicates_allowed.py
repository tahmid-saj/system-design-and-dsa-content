from collections import defaultdict
class RandomizedCollection:
    def __init__(self):
        self.index = defaultdict(set)
        self.list = []

    def insert(self, val: int) -> bool:
        if val not in self.index: res = True
        else: res = False

        i = len(self.list)
        self.index[val].add(i)
        self.list.append(val)

        return res

    def remove(self, val: int) -> bool:
        if val not in self.index: return False

        i, j = self.index[val].pop(), len(self.list) - 1
        lastEle = self.list[j]
        if len(self.index[val]) == 0: self.index.pop(val)

        if i == j:
            self.list.pop()
        else:
            self.list[i], self.list[j] = self.list[j], self.list[i]
            self.list.pop()

            self.index[lastEle].remove(j)
            self.index[lastEle].add(i)

        return True

    def getRandom(self) -> int:
        return random.choice(self.list)

# Your RandomizedCollection object will be instantiated and called as such:
# obj = RandomizedCollection()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()