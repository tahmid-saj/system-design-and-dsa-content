class Solution {
    public int islandPerimeter(int[][] grid) {
        // loop through grid using i:
        // loop through grid[i] using j:
        // if grid[i][j] == 1:
        //  if top side has water or is at the edge: perimeter++
        //  if right side has water or is at th eedge: perimeter++ ....
        int perimeter = 0;
        
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[i].length; j++) {
                if (grid[i][j] == 1) {
                    if (i == 0 || (grid[i - 1][j] == 0)) perimeter++;
                    if (j == grid[i].length - 1 || (grid[i][j + 1] == 0)) perimeter++;
                    if (i == grid.length - 1 || (grid[i + 1][j] == 0)) perimeter++;
                    if (j == 0 || (grid[i][j - 1] == 0)) perimeter++;
                }
            }
        }

        return perimeter;
    }
}