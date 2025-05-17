class Solution:
    def findBuildings(self, heights: List[int]) -> List[int]:
        currMax, res = -math.inf, []
        for i in range(len(heights) - 1, -1, -1):
            if heights[i] > currMax: 
                res.append(i)
                currMax = max(currMax, heights[i])
        
        return res[::-1]