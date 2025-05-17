class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # return self.recursive(text1, text2, len(text1) - 1, len(text2) - 1)
        # return self.recursive2(text1, text2, 0, 0)
        # return self.bottomUp(text1, text2)
        # return self.bottomUp2(text1, text2)
        return self.bottomUpLinearSpace(text1, text2)

    def recursive(self, text1, text2, index1, index2):
        # base case: index1 < 0 or index2 < 0: return 0
        # 1. if text1[index1] == text2[index2]: self.recursive(text1, text2, index1 - 1, index2 - 1)
        # 2. else: call both self.recursive(text1, text2, index1 - 1, index2), self.recursive(text1, text2, index1, index2 - 1)
        if index1 < 0 or index2 < 0: return 0

        res1, res2 = 0, 0
        if text1[index1] == text2[index2]: res1 = 1 + self.recursive(text1, text2, index1 - 1, index2 - 1)
        else: res2 = max(self.recursive(text1, text2, index1 - 1, index2), self.recursive(text1, text2, index1, index2 - 1))

        return max(res1, res2)

    def recursive2(self, text1, text2, index1, index2):
        if index1 == len(text1) or index2 == len(text2): return 0

        res1, res2 = 0, 0
        first = text1.find(text2[index2], index1)
        if first != -1: res1 = 1 + self.recursive2(text1, text2, index1 + 1, index2 + 1)
        res2 = self.recursive2(text1, text2, index1, index2 + 1)

        return max(res1, res2)
    
    def bottomUp(self, text1, text2):
        dp = [[0 for _ in range(len(text2))] for _ in range(len(text1))]

        for i in range(len(text1)):
            if text2[0] in text1[:i + 1]: dp[i][0] = 1
        for j in range(1, len(text2)):
            if text1[0] in text2[:j + 1]: dp[0][j] = 1
        
        for i in range(1, len(text1)):
            for j in range(1, len(text2)):
                if text1[i] == text2[j]: dp[i][j] = dp[i - 1][j - 1] + 1
                else: dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        return dp[len(text1) - 1][len(text2) - 1]
    
    def bottomUp2(self, text1, text2):
        if len(text1) == 0 or len(text2) == 0: return 0
        dp = [[0 for j in range(len(text2) + 1)] for i in range(len(text1) + 1)]

        for i in range(len(text1) - 1, -1, -1):
            for j in range(len(text2) - 1, -1, -1):
                if text1[i] == text2[j]: dp[i][j] = dp[i + 1][j + 1] + 1
                else: dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
        
        return dp[0][0]
    
    def bottomUpLinearSpace(self, text1, text2):
        if len(text1) == 0 or len(text2) == 0: return 0
        if len(text1) < len(text2): text1, text2 = text2, text1

        prev = [0 for _ in range(len(text2) + 1)]
        
        for i in range(len(text1) - 1, -1, -1):
            curr = [0 for _ in range(len(text2) + 1)]
            for j in range(len(text2) - 1, -1, -1):
                if text1[i] == text2[j]: curr[j] = prev[j + 1] + 1
                else: curr[j] = max(prev[j], curr[j + 1])
            prev = curr

        return curr[0]