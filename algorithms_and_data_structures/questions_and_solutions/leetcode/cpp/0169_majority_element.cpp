class Solution {
public:
    int majorityElement(vector<int>& nums) {
        set<int> appeared;
        int retMajor = 0, curr = 0, elem = 0;

        sort(nums.begin(), nums.end());

        for (int i = 0; i < nums.size(); i++) {
            if (appeared.find(nums[i]) == appeared.end()) {
                appeared.insert(nums[i]);

                curr = 0; 
                curr++;
            }
            else {
                curr++;
            }

            if (curr > retMajor) {
                retMajor = curr;
                elem = nums[i];
            }
        }

        return elem;
    }
};