class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> occurred;

        for (int i = 0; i < nums.size(); i++) {
            if (occurred.find(nums[i]) == occurred.end()) {
                occurred.insert(nums[i]);
            }
            else {
                return true;
            }
        }

        return false;
    }
};