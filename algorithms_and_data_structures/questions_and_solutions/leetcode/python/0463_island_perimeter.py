class Solution:
    def islandPerimeter(self, grid: List[List[int]]) -> int:
        res = 0
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == 1:
                    if i == 0 or grid[i - 1][j] == 0: res += 1
                    if j == 0 or grid[i][j - 1] == 0: res += 1
                    if i == len(grid) - 1 or grid[i + 1][j] == 0: res += 1
                    if j == len(grid[i]) - 1 or grid[i][j + 1] == 0: res += 1

        return res