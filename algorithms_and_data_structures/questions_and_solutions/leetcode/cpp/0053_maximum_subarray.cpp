class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int localMax = 0;
        int globalMax = INT_MIN;

        for (int i = 0; i < nums.size(); i++) {
            localMax = max(nums[i], nums[i] + localMax);
            if (localMax > globalMax) {
                globalMax = localMax;
            }
        }

        return globalMax;
    }
};