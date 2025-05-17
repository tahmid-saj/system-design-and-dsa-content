class TwoSum:
    def __init__(self):
        self.seen = {}

    def add(self, number: int) -> None:
        self.seen[number] = self.seen.get(number, 0) + 1

    def find(self, value: int) -> bool:
        for k, v in self.seen.items():
            complement = value - k
            if complement == k and v >= 2: return True
            elif complement == k and v < 2: continue

            if complement in self.seen: return True
        return False

# Your TwoSum object will be instantiated and called as such:
# obj = TwoSum()
# obj.add(number)
# param_2 = obj.find(value)