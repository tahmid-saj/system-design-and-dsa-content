from functools import reduce
class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        return reduce(lambda num, c: (num * 26) + (ord(c) - ord('A')) + 1, columnTitle, 0)