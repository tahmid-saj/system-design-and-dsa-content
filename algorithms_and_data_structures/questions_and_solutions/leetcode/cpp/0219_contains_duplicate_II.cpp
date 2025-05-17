class Solution {
public:
    bool containsNearbyDuplicate(vector<int>& nums, int k) {
        unordered_map<int, int> occurred;

        for (int i = 0; i < nums.size(); i++) {
            if (occurred.find(nums[i]) != occurred.end()) {
                if (abs(i - occurred.find(nums[i])->second) <= k) {
                    return true;
                }
                else {
                    auto index = occurred.find(nums[i]);
                    index->second = i;
                }
            }
            else if (occurred.find(nums[i]) == occurred.end()) {
                occurred.insert(make_pair(nums[i], i));
            }
        }

        return false;
    }
};