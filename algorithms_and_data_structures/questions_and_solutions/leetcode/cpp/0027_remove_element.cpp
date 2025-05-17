class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        sort(nums.begin(), nums.end());
        
        int c = 0;

        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] != val) {
                nums[c] = nums[i];
            }
        
            if (nums[c] != val) {
                c++;
            }
        }
        
        return c;
    }
};