class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        # return self.recursive(triangle, 0, 0)

        # @lru_cache(None)
        # def topDown(i, j):
        #     if i == len(triangle): return 0

        #     path1, path2 = math.inf, math.inf
        #     path1 = triangle[i][j] + topDown(i + 1, j)
        #     path2 = triangle[i][j] + topDown(i + 1, j + 1)

        #     return min(path1, path2)

        # return topDown(0, 0)
    
        # return self.bottomUpInPlace(triangle)
        return self.bottomUpLinearSpace(triangle)

    def recursive(self, triangle, i, j):
        if i == len(triangle): return 0

        path1, path2 = math.inf, math.inf
        path1 = triangle[i][j] + self.recursive(triangle, i + 1, j)
        path2 = triangle[i][j] + self.recursive(triangle, i + 1, j + 1)

        return min(path1, path2)
    
    def bottomUpInPlace(self, triangle):
        for i in range(1, len(triangle)):
            for j in range(len(triangle[i])):
                if j == 0: 
                    triangle[i][j] += triangle[i - 1][0]
                elif j == len(triangle[i]) - 1: 
                    triangle[i][j] += triangle[i - 1][-1]
                else:
                    triangle[i][j] += min(triangle[i - 1][j - 1], triangle[i - 1][j])
        
        return min(triangle[len(triangle) - 1])
    

    def bottomUpLinearSpace(self, triangle):
        prev = triangle[0]

        for i in range(1, len(triangle)):
            curr = []
            for j in range(len(triangle[i])):
                if j == 0:
                    curr.append(triangle[i][j] + prev[0])
                elif j == len(triangle[i]) - 1:
                    curr.append(triangle[i][j] + prev[-1])
                else:
                    curr.append(triangle[i][j] + min(prev[j - 1], prev[j]))
            prev = curr
        
        return min(prev)