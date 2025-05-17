class Solution:
    def projectionArea(self, grid: List[List[int]]) -> int:
        # xArea = count of v that is v > 0
        # yArea = sum of max v in each row
        # zArea = sum of max v in each column
        xArea, yArea, zArea = 0, 0, 0
        for i in range(len(grid)):
            currMax = 0
            for j in range(len(grid[0])):
                if grid[i][j] > 0: xArea += 1
                currMax = max(currMax, grid[i][j])
            yArea += currMax
        
        for j in range(len(grid[0])):
            currMax = 0
            for i in range(len(grid)): currMax = max(currMax, grid[i][j])
            zArea += currMax
        
        return xArea + yArea + zArea