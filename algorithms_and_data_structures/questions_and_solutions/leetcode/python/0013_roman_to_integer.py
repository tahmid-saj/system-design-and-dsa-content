from functools import reduce
class Solution:
    def romanToInt(self, s: str) -> int:
        romanToInt = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }

        res = romanToInt[s[-1]]
        for i in range(len(s) - 2, -1, -1):
            if romanToInt[s[i]] < romanToInt[s[i + 1]]: res -= romanToInt[s[i]]
            else: res += romanToInt[s[i]]
        return res