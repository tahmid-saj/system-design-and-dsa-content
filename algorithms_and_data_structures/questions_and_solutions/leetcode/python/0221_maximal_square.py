class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        # return self.bottomUp(matrix)
        return self.bottomUpOptimized(matrix)
    
    def bottomUp(self, matrix):
        dp = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
        maxLen = 0

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == "1":
                    dp[i][j] = min(dp[i - 1][j], dp[i - 1][j - 1], dp[i][j - 1]) + 1
                    maxLen = max(maxLen, dp[i][j])
        
        return maxLen * maxLen
    
    def bottomUpOptimized(self, matrix):
        dp = [0 for _ in range(len(matrix[0]))]
        maxLen, prev = 0, 0

        for j in range(len(matrix[0])):
            if matrix[0][j] == "1": 
                dp[j] = 1
                maxLen = max(maxLen, dp[j])
        
        for i in range(1, len(matrix)):                
            for j in range(len(matrix[0])):
                tmp = dp[j]
                if j == 0:
                    if matrix[i][j] == "1": 
                        dp[j] = 1
                        maxLen = max(maxLen, dp[j])
                    else: dp[j] = 0
                elif matrix[i][j] == "1":
                    dp[j] = min(dp[j], dp[j - 1], prev) + 1
                    maxLen = max(maxLen, dp[j])
                else: dp[j] = 0
                prev = tmp
        
        return maxLen * maxLen