class Solution:
    def numberOfLines(self, widths: List[int], s: str) -> List[int]:
        i, j, res = 0, 0, [1, 0]
        letters = "abcdefghijklmnopqrstuvwxyz"
        width = dict(zip(letters, widths))
        while i < len(s):
            if j + width[s[i]] <= 100: j += width[s[i]]
            else: 
                res[0] += 1
                j = width[s[i]]
            i += 1
        res[1] = j
        return res