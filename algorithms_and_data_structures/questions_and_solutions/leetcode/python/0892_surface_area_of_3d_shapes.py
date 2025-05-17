class Solution:
    def surfaceArea(self, grid: List[List[int]]) -> int:
        bottomTop, t, b, l, r, adj = 0, 0, 0, 0, 0, 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] > 0: bottomTop += 2
                if i == 0: t += grid[i][j]
                if i == len(grid) - 1: b += grid[i][j]

                # tower height higher than adjacent towers
                if i > 0 and grid[i - 1][j] < grid[i][j]: adj += grid[i][j] - grid[i - 1][j]
                if j > 0 and grid[i][j - 1] < grid[i][j]: adj += grid[i][j] - grid[i][j - 1]
                if i < len(grid) - 1 and grid[i + 1][j] < grid[i][j]: adj += grid[i][j] - grid[i + 1][j]
                if j < len(grid[0]) - 1 and grid[i][j + 1] < grid[i][j]: adj += grid[i][j] - grid[i][j + 1]

            l += grid[i][0]
            r += grid[i][len(grid[0]) - 1]
        return bottomTop + t + b + l + r + adj