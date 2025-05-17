class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        # return self.recursive(s1, s2, s3, 0, 0, "")

        # dp = [[False for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]
        # return self.topDown(s1, s2, s3, 0, 0, "", dp)
    
        # return self.bottomUp(s1, s2, s3)
        return self.bottomUpLinearSpace(s1, s2, s3)

    def recursive(self, s1, s2, s3, index1, index2, curr):
        if index1 == len(s1) and index2 == len(s2) and curr == s3: return True

        if index1 + 1 <= len(s1) and self.recursive(s1, s2, s3, index1 + 1, index2, curr + s1[index1]): return True
        if index2 + 1 <= len(s2) and self.recursive(s1, s2, s3, index1, index2 + 1, curr + s2[index2]): return True

        return False
    
    def topDown(self, s1, s2, s3, index1, index2, curr, dp):
        if index1 == len(s1) and index2 == len(s2) and curr == s3: return True

        if index1 + 1 <= len(s1):
            if dp[index1][index2] == False:
                dp[index1][index2] = self.topDown(s1, s2, s3, index1 + 1, index2, curr + s1[index1], dp)
                if dp[index1][index2]: return True
        if index2 + 1 <= len(s2):
            if dp[index1][index2] == False:
                dp[index1][index2] = self.topDown(s1, s2, s3, index1, index2 + 1, curr + s2[index2], dp)
                if dp[index1][index2]: return True
        
        return dp[index1][index2]
    
    def bottomUp(self, s1, s2, s3):
        if len(s1) + len(s2) != len(s3): return False
        if len(s1) == 0 and s2 != s3: return False
        if len(s2) == 0 and s1 != s3: return False

        dp = [[False for j in range(len(s2) + 1)] for i in range(len(s1) + 1)]

        for i in range(len(s1) + 1):
            for j in range(len(s2) + 1):
                if i == 0 and j == 0:
                    dp[i][j] = True
                elif i == 0:
                    dp[i][j] = dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]
                elif j == 0:
                    dp[i][j] = dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]
                else:
                    dp[i][j] = (dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]) or (dp[i - 1][j] and s1[i - 1] == s3[i + j - 1])
        
        return dp[len(s1)][len(s2)]
    
    def bottomUpLinearSpace(self, s1, s2, s3):
        if len(s1) + len(s2) != len(s3): return False
        if len(s1) == 0 and s2 != s3: return False
        if len(s2) == 0 and s1 != s3: return False

        dp = [False for j in range(len(s2) + 1)]

        for i in range(len(s1) + 1):
            for j in range(len(s2) + 1):
                if i == 0 and j == 0:
                    dp[j] = True
                elif i == 0:
                    dp[j] = dp[j - 1] and s2[j - 1] == s3[i + j - 1]
                elif j == 0:
                    dp[j] = dp[j] and s1[i - 1] == s3[i + j - 1]
                else:
                    dp[j] = (dp[j - 1] and s2[j - 1] == s3[i + j - 1]) or (dp[j] and s1[i - 1] == s3[i + j - 1])
        
        return dp[len(s2)]