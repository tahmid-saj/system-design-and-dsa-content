from collections import namedtuple
class Solution:
    coord = namedtuple("coord", ("i", "j"))
    def searchMaze(self, maze, s, e):
        global coord
        curr = coord(s[0], s[1])
        path = []
        return self.dfs(maze, s, e, curr, path)
    
    def dfs(self, maze, s, e, curr, path):
        if curr.i < 0 or curr.i >= len(maze) or curr.j < 0 or curr.j >= len(maze[0]) or maze[curr.i][curr.j] != 0: return False
        path.append(curr)
        maze[curr.i][curr.j] = 1
        if curr == e: return True

        if self.dfs(maze, s, e, coord(curr.i - 1, curr.j), path): return True
        if self.dfs(maze, s, e, coord(curr.i + 1, curr.j), path): return True
        if self.dfs(maze, s, e, coord(curr.i, curr.j - 1), path): return True
        if self.dfs(maze, s, e, coord(curr.i, curr.j + 1), path): return True
        del path[-1]
        
        return False