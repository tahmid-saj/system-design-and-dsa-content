class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        if image[sr][sc] != color: self.dfs(image, sr, sc, color, image[sr][sc])
        return image
    
    def dfs(self, image, i, j, colour, initial):
        if i < 0 or i >= len(image) or j < 0 or j >= len(image[0]) or image[i][j] != initial: return
        if image[i][j] == initial: image[i][j] = colour

        self.dfs(image, i - 1, j, colour, initial)
        self.dfs(image, i + 1, j, colour, initial)
        self.dfs(image, i, j - 1, colour, initial)
        self.dfs(image, i, j + 1, colour, initial)