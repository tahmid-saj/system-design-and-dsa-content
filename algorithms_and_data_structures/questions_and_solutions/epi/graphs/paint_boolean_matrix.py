from collections import deque
class Solution:
    def paintBooleanMatrix(self, x, y, image):
        colour = image[x][y]
        # return self.bfs(image, x, y, colour)
        return self.dfs(image, x, y, colour)
    
    def bfs(self, image, i, j, colour):
        queue = deque([(i, j)])
        image[i][j] = 0 if image[i][j] == 1 else 1
        while queue:
            i, j = queue.popleft()
            for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if x < 0 or x >= len(image) or y < 0 or y >= len(image[0]) or image[x][y] != colour: continue
                image[x][y] = 0 if image[i][j] == 1 else 1
                queue.append((x, y))
    
    def dfs(self, image, i, j, colour):
        if i < 0 or i >= len(image) or j < 0 or j >= len(image[0]) or image[i][j] != colour: return
        image[i][j] = 0 if image[i][j] == 1 else 1

        for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]: self.dfs(image, x, y, colour)