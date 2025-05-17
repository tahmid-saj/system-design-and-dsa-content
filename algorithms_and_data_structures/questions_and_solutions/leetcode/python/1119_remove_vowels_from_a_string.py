class Solution:
    def removeVowels(self, s: str) -> str:
        res = []
        for c in s:
            if c in "aeiou": continue
            res.append(c)
        return "".join(res)