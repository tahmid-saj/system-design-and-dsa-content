class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        vector<int> inter;
        int currNum = -1;

        sort(nums1.begin(), nums1.end());
        sort(nums2.begin(), nums2.end());

        for (int i = 0; i < nums1.size(); i++) {
            if (nums1[i] == currNum) {
                continue;
            }

            for (int j = 0; j < nums2.size(); j++) {
                if (nums1[i] == nums2[j]) {
                    if (nums2[j] == currNum) {
                        continue;
                    }
                    else {
                        inter.push_back(nums2[j]);
                        currNum = nums2[j];
                    }
                }
            }
        }

        return inter;
    }
};