class Solution:
    def countSubstrings(self, s: str) -> int:
        dp = [[False for j in range(len(s))] for i in range(len(s))]
        res = len(s)

        for i in range(len(s)): dp[i][i] = True
        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                dp[i - 1][i] = True
                res += 1
        
        for length in range(2, len(s)):
            for i in range(0, len(s) - length):
                j = i + length
                if s[i] == s[j] and dp[i + 1][j - 1] == True:
                    dp[i][j] = True
                    res += 1
        
        return res