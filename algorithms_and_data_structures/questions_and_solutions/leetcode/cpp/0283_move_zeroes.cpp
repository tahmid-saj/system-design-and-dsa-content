class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        // Have one for loop that iterates through nums, with i
        // have a second iterator that increments only when the current nums[j] != 0
        // if nums[j] == 0 && nums[i] != 0, swap their values
        // exit the loop when i == nums.size()
        
        for (int i = 1, j = 0; i < nums.size(); i++) {
            if (nums[j] == 0 && nums[i] != 0) {
                int tmp = nums[j];
                nums[j] = nums[i];
                nums[i] = tmp;
            }
            
            if (nums[j] != 0) {
                j++;
            }
        }
    }
};