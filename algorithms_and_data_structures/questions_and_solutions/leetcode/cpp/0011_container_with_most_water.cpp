class Solution {
public:
    int maxArea(vector<int>& height) {
        int l = 0;
        int r = height.size() - 1;
        int area = 0;

        while (l < r)
        {
            // Calculating the max area
            area = max(area, min(height[l], height[r]) * (r - l));

            if (height[l] < height[r])
                l += 1;

            else
                r -= 1;
        }
        
        return area;
    }
};