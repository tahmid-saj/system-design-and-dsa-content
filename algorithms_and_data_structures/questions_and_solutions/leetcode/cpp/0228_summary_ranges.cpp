class Solution {
public:
    vector<string> summaryRanges(vector<int>& nums) {
        vector<string> ret;
        string retStr = "";

        for (int i = 0; i < nums.size(); i++) {
            if (i == 0) {
                retStr += to_string(nums[i]);
            }
            else if (long(nums[i]) - long(nums[i - 1]) == 1) {
                if (i < nums.size() - 1 &&  long(nums[i + 1]) - long(nums[i]) == 1) {
                    continue;
                }
                else {
                    retStr += "->" + to_string(nums[i]);
                }
            }
            else if (long(nums[i]) - long(nums[i - 1]) != 1) {
                ret.push_back(retStr);
                retStr.clear();
                retStr += to_string(nums[i]);
            }

            if (i == nums.size() - 1) {
                ret.push_back(retStr);
            }
        }

        return ret;
    }
};