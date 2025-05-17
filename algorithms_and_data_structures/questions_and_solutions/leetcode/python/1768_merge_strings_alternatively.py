class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        res, i = [], 0
        length = max(len(word1), len(word2))
        for i in range(length):
            if i < len(word1): res.append(word1[i])
            if i < len(word2): res.append(word2[i])
        
        return "".join(res)