class Solution(object):
    def cherryPickup(self, grid):
        N = len(grid)
        dp = [[float('-inf')] * N for _ in xrange(N)]
        dp[0][0] = grid[0][0]
        for t in xrange(1, 2 * N - 1):
            dp2 = [[float('-inf')] * N for _ in xrange(N)]
            for i in xrange(max(0, t - (N - 1)), min(N - 1, t) + 1):
                for j in xrange(max(0, t - (N - 1)), min(N - 1, t) + 1):
                    if grid[i][t - i] == -1 or grid[j][t - j] == -1:
                        continue
                    val = grid[i][t - i]
                    if i != j:
                        val += grid[j][t - j]
                    dp2[i][j] = max(dp[pi][pj] + val
                                    for pi in (i - 1, i) for pj in (j - 1, j)
                                    if pi >= 0 and pj >= 0)
            dp = dp2
        return max(0, dp[N - 1][N - 1])
    
    def cherryPickup(self, grid):
        N = len(grid)
        memo = [[[None] * N for _1 in range(N)] for _2 in range(N)]
        def dp(r1, c1, c2):
            r2 = r1 + c1 - c2
            if (N == r1 or N == r2 or N == c1 or N == c2 or
                    grid[r1][c1] == -1 or grid[r2][c2] == -1):
                return float('-inf')
            elif r1 == c1 == N-1:
                return grid[r1][c1]
            elif memo[r1][c1][c2] is not None:
                return memo[r1][c1][c2]
            else:
                ans = grid[r1][c1] + (c1 != c2) * grid[r2][c2]
                ans += max(dp(r1, c1 + 1, c2 + 1), dp(r1 + 1, c1, c2 + 1),
                           dp(r1, c1 + 1, c2), dp(r1 + 1, c1, c2))

            memo[r1][c1][c2] = ans
            return ans

        return max(0, dp(0, 0, 0))