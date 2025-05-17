class Solution:
    def trap(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        res, lMax, rMax = 0, 0, 0

        while l < r:
            if height[l] < height[r]:
                lMax = max(lMax, height[l])
                res += lMax - height[l]
                l += 1
            else:
                rMax = max(rMax, height[r])
                res += rMax - height[r]
                r -= 1
        
        return res