class Solution:
    def commonChars(self, words: List[str]) -> List[str]:
        if len(words) == 1: return words

        res, word1 = [], set(words[0])
        for c in word1:
            freq = min([word.count(c) for word in words])
            res.extend(list(freq * c))
        return res