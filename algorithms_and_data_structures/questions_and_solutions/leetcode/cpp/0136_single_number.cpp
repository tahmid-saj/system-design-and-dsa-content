class Solution {
public:
    int singleNumber(vector<int>& nums) {
        unordered_set<int> occurred;

        for (int i = 0; i < nums.size(); i++) {
            if (occurred.find(nums[i]) == occurred.end()) {
                occurred.insert(nums[i]);
            }
            else if (occurred.find(nums[i]) != occurred.end()) {
                occurred.erase(nums[i]);
            }
        }

        return *(occurred.begin());
    }
};