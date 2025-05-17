class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        # return self.comparingTwoWords(words, order)
        return self.editorial(words, order)

    def comparingTwoWords(self, words, order):
        orderMap = {}
        for i in range(len(order)): orderMap[order[i]] = i

        for i in range(1, len(words)):
            word1, word2 = words[i - 1], words[i]
            if word1 == word2: continue
            wordLength = min(len(word1), len(word2))
            for j in range(wordLength):
                if orderMap[word1[j]] < orderMap[word2[j]]: break
                elif orderMap[word1[j]] > orderMap[word2[j]]: return False
                if j == wordLength - 1 and j < len(word1) - 1: return False
            
        return True
    
    def editorial(self, words, order):
        order_map = {}
        for index, val in enumerate(order):
            order_map[val] = index

        for i in range(len(words) - 1):
            for j in range(len(words[i])):
                if j >= len(words[i + 1]): return False

                if words[i][j] != words[i + 1][j]:
                    if order_map[words[i][j]] > order_map[words[i + 1][j]]: return False
                    break

        return True