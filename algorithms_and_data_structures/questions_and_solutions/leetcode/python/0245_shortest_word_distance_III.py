class Solution:
    def shortestWordDistance(self, wordsDict: List[str], word1: str, word2: str) -> int:
        # return self.binarySearch(wordsDict, word1, word2)
        # return self.mergingLists(wordsDict, word1, word2)
        return self.twoPointers(wordsDict, word1, word2)
    
    def binarySearch(self, wordsDict, word1, word2):
        index1, index2, res = [], [], math.inf
        for i in range(len(wordsDict)):
            if wordsDict[i] == word1: index1.append(i)
            if wordsDict[i] == word2: index2.append(i)
        
        for i in index1:
            j = self.bs(i, index2)

            if j != len(index2): res = min(res, abs(i - index2[j]))
            if j != 0 and index2[j - 1] != i: res = min(res, abs(i - index2[j - 1]))
        
        return res
    
    def bs(self, i, index2):
        l, r, res = 0, len(index2) - 1, len(index2)

        while l <= r:
            middle = l + (r - l) // 2
            if index2[middle] > i:
                res = middle
                r = middle - 1
            else: l = middle + 1
        return res
    
    def mergingLists(self, wordsDict, word1, word2):
        index, res = [], math.inf
        for i in range(len(wordsDict)):
            if wordsDict[i] == word1: index.append((i, 0))
            if wordsDict[i] == word2: index.append((i, 1))
        
        for i in range(len(index) - 1):
            if index[i][0] != index[i + 1][0] and index[i][1] != index[i + 1][1]: res = min(res, abs(index[i][0] - index[i + 1][0]))
        return res
    
    def twoPointers(self, wordsDict, word1, word2):
        i, j, res = 0, 0, math.inf

        while i < len(wordsDict) and j < len(wordsDict):
            while i < len(wordsDict) and wordsDict[i] != word1: i += 1
            while j < len(wordsDict) and wordsDict[j] != word2: j += 1
            if i >= len(wordsDict): break
            if j >= len(wordsDict): break
            if i != j: res = min(res, abs(i - j))
            if i < j: i += 1
            else: j += 1
        return res