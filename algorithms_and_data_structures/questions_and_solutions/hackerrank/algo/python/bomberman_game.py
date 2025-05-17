def bomberMan(n, grid):
  # Write your code here
  if n == 1: return grid
  
  # all cells will be filled with bombs
  if n % 2 == 0: return ["O"*len(grid[0]) for _ in range(len(grid))]
  
  # alternate states
  n //= 2
  
  for q in range((n + 1) % 2 + 1):
    newGrid = [["O" for _ in range(len(grid[0]))] for _ in range(len(grid))]
    
    # function for detonation
    def detonate(x, y):
      if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        newGrid[x][y] = "."
    
    xi = [0, 0, 0, 1, -1]
    yi = [0, -1, 1, 0, 0]
        
    for x in range(len(grid)):
      for y in range(len(grid[0])):
        # check for bomb
        if grid[x][y] == "O":
          # detonate the cell by calling the function
          for i, j in zip(xi, yi):
            detonate(x + i, y + j)

    grid = newGrid
  
  return ["".join(x) for x in grid]