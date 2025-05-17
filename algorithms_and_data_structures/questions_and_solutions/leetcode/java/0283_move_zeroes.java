class Solution {
    public void moveZeroes(int[] nums) {
        if (nums.length == 1) return;

        int i = 0, j = 1;
        while (j < nums.length) {
            if (nums[i] == 0 && nums[j] != 0) {
                int numJ = nums[j];
                nums[j] = nums[i];
                nums[i] = numJ;
                i++;
            } else if (nums[i] != 0) i++;
            j++;
        }
    }
}