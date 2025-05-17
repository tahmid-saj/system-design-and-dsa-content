class Solution {
    public int removeDuplicates(int[] nums) {
        if (nums.length == 1) return 1;

        int i = 0, j = 1;

        while (j < nums.length) {
            if (nums[i] != nums[j]) {
                int tmp = nums[i + 1];
                nums[i + 1] = nums[j];
                nums[j] = tmp;
                i++;
            }
            j++;
        }

        return i + 1;
    }
}