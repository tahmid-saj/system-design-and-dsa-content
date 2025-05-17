class Solution:
    def countNumberOfScoreCombinations(self, scores, score):
        dp = [[0 for _ in range(len(scores))] for _ in range(score + 1)]
        # return self.recursive(scores, score, 0, 0, dp)
        # return self.topDown(scores, 0, 0, dp)
        return self.bottomUp(scores, score, dp)
    
    def recursive(self, scores, score, s, i):
        if s == score: return 1
        if i >= len(scores) or s > score: return 0
        comb1, comb2 = 0, 0
        if s + scores[i] <= score and i + 1 <= len(scores): comb1 += self.recursive(scores, score, s + scores[i], i + 1)
        if i + 1 <= len(scores): comb2 += self.recursive(scores, score, s, i + 1)
        return comb1 + comb2
    
    def topDown(self, scores, s, i, dp):
        if s == 0: return 1
        if i >= len(scores) or s < 0: return 0
        if dp[i][s] == 0:
            if s + scores[i] >= 0 and i + 1 <= len(scores): dp[i][s] += self.topDown(scores, s + scores[i], i + 1, dp)
        if i + 1 <= len(scores): dp[i][s] += self.topDown(scores, s, i + 1, dp)
        return dp[i][s]
    
    def bottomUp(self, scores, score, dp):
        for i in range(len(scores)): dp[i][0] += 1
        for s in range(1, score + 1):
            if dp[0][0] % s == 0: dp[0][s] += 1
        
        for i in range(1, len(scores)):
            for s in range(1, score + 1):
                dp[i][s] += dp[i - 1][s]
                if s - scores[i] >= 0: dp[i][s] += dp[i][s - scores[i]] 