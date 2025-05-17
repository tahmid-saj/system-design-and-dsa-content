import re
class Solution:
    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        banned, freq = set(banned), {}
        i, j = 0, 1
        while j < len(paragraph):
            if paragraph[j] in " !?',;." or j + 1 == len(paragraph):
                word = paragraph[i:j + 1].lower() if paragraph[j].isalpha() else paragraph[i:j].lower()
                if word and word.isalpha() and word not in banned: freq[word] = freq.get(word, 0) + 1
                i = j = self.findStart(paragraph, j + 1)
            j += 1

        res, count = None, 0
        for k, v in freq.items():
            if count < v:
                count = v
                res = k
        return res

    def findStart(self, paragraph, j):
        while j < len(paragraph) and paragraph[j] in " !?',;.": j += 1
        return j