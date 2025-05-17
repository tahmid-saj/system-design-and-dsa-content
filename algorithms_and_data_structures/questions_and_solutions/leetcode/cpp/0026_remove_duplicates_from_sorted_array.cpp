class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int current = 0;

        for (int i = 1; i < nums.size(); i++) {
            if (nums[current] != nums[i]) {
                nums[++current] = nums[i];
            }
        }
        
        if (nums.empty()) {
            return 0;
        }
        
        return current + 1;
    }
};