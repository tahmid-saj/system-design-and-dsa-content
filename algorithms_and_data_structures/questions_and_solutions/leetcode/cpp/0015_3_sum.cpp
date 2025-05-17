class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> op;

        if (nums.size() < 3) { //if number of elements inside nums is less than 3 return empty array.
            return op;
        }

        sort(nums.begin(), nums.end());

        for (int i = 0; i < nums.size() - 2; i++) {

            if (i > 0 && nums[i] == nums[i - 1]) { //remove dublicates for i to optimize the code
                continue;
            }

            int j = i + 1, k = nums.size() - 1;
            while (j < k) {
                int sum = nums[i] + nums[j] + nums[k];
                if (sum == 0) {

                    op.push_back({ nums[i], nums[j], nums[k] }); //if sum equal to zero push back the values
                    j++;
                    k--;

                    while (j < k && nums[j] == nums[j - 1]) j++; // Remove dublicates
                    while (j < k && nums[k] == nums[k + 1]) k--; // Remove dublicates
                }
                else if (sum < 0)
                    j++;    //if sum is negative increment j
                else
                    k--;    //if sum is positive increment k
            }
        }
        return op;
    }
};