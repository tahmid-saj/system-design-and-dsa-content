class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        # return self.recursive(word1, word2, len(word1) - 1, len(word2) - 1)

        # dp = [[math.inf for j in range(len(word2))] for i in range(len(word1))]
        # return self.topDown(word1, word2, len(word1) - 1, len(word2) - 1, dp)

        return self.bottomUp(word1, word2)
    
    def recursive(self, word1, word2, index1, index2):
        if index1 < 0 and index2 < 0: return 0
        if index1 < 0: return index2 + 1
        if index2 < 0: return index1 + 1

        res, res1, res2, res3 = math.inf, math.inf, math.inf, math.inf
        if word1[index1] == word2[index2]: res = self.recursive(word1, word2, index1 - 1, index2 - 1)
        else:
            res1 = 1 + self.recursive(word1, word2, index1 - 1, index2 - 1)
            res2 = 1 + self.recursive(word1, word2, index1 - 1, index2)
            res3 = 1 + self.recursive(word1, word2, index1, index2 - 1)
        
        return min(res, res1, res2, res3)

    def topDown(self, word1, word2, index1, index2, dp):
        if index1 < 0 and index2 < 0: return 0
        if index1 < 0: return index2 + 1
        if index2 < 0: return index1 + 1

        if dp[index1][index2] != math.inf: return dp[index1][index2]
        res, res1, res2, res3 = math.inf, math.inf, math.inf, math.inf
        if word1[index1] == word2[index2]: res = self.topDown(word1, word2, index1 - 1, index2 - 1, dp)
        else:
            res1 = 1 + self.topDown(word1, word2, index1 - 1, index2 - 1, dp)
            res2 = 1 + self.topDown(word1, word2, index1 - 1, index2, dp)
            res3 = 1 + self.topDown(word1, word2, index1, index2 - 1, dp)            

        dp[index1][index2] = min(res, res1, res2, res3)
        return dp[index1][index2]

    def bottomUp(self, word1, word2):
        if len(word1) == 0: return len(word2)
        if len(word2) == 0: return len(word1)

        dp = [[math.inf for _ in range(len(word2))] for _ in range(len(word1))]

        usedFirstLetter = False
        for i in range(len(word1)):
            if word2[0] == word1[i] and not usedFirstLetter: 
                dp[i][0] = (dp[i - 1][0] if i > 0 else 0)
                usedFirstLetter = True
            else: dp[i][0] = (dp[i - 1][0] if i > 0 else 0) + 1
        usedFirstLetter = False
        for j in range(1, len(word2)):
            if word1[0] == word2[j] and not usedFirstLetter: 
                dp[0][j] = dp[0][j - 1]
                usedFirstLetter = True
            else: dp[0][j] = dp[0][j - 1] + 1
        
        for i in range(1, len(word1)):
            for j in range(1, len(word2)):
                if word1[i] == word2[j]: dp[i][j] = dp[i - 1][j - 1]
                else: dp[i][j] = min(
                    dp[i - 1][j - 1] + 1,
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1
                )
        
        return dp[-1][-1]