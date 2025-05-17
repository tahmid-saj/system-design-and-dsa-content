class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        map<int, int> hashMap;
        vector<int> ret;
        
        for (int i = 0; i < nums.size(); i++) {
            int diff = target - nums[i];
            
            if (hashMap.find(diff) != hashMap.end()) {
                auto secondIndex = (hashMap.find(diff))->second;
                ret.push_back(secondIndex);
                
                ret.push_back(i);
            }
            else {
                hashMap.insert(make_pair(nums[i], i));
            }
        }
        
        return ret;
    }
};