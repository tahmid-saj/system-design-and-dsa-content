class Solution:
    def countLetters(self, s: str) -> int:
        dp = [0 for _ in range(len(s))]
        dp[-1] = 1
        
        for i in range(len(s) - 2, -1, -1):
            if s[i] == s[i + 1]: dp[i] = dp[i + 1] + 1
            else: dp[i] = 1
        
        return sum(dp)