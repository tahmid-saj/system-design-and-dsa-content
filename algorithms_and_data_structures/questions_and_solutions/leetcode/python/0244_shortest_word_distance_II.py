from collections import defaultdict
class WordDistance:

    def __init__(self, wordsDict: List[str]):
        self.indexes = defaultdict(list)
        for i in range(len(wordsDict)): self.indexes[wordsDict[i]].append(i)

    def shortest(self, word1: str, word2: str) -> int:
        res = math.inf
        i, j = 0, 0
        while i < len(self.indexes[word1]) and j < len(self.indexes[word2]):
            iIndex, jIndex = self.indexes[word1][i], self.indexes[word2][j]
            res = min(res, abs(iIndex - jIndex))

            nextIIndex, nextJIndex = self.indexes[word1][i + 1] if i < len(self.indexes[word1]) - 1 else math.inf, self.indexes[word2][j + 1] if j < len(self.indexes[word2]) - 1 else math.inf
            if abs(nextIIndex - jIndex) < abs(nextJIndex - iIndex): i += 1
            else: j += 1
        
        return res

# Your WordDistance object will be instantiated and called as such:
# obj = WordDistance(wordsDict)
# param_1 = obj.shortest(word1,word2)