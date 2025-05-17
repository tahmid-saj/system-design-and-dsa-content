class Solution:
    def calculateTime(self, keyboard: str, word: str) -> int:
        keys = {}
        for i in range(len(keyboard)): keys[keyboard[i]] = i

        i, res = 0, 0
        for w in word:
            j = keys[w]
            res += abs(i - j)
            i = j
        return res