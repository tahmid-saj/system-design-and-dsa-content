class Solution {
    public int removeElement(int[] nums, int val) {
        if (nums.length == 0) return 0;
        if (nums.length == 1) {
            return nums[0] == val ? 0 : 1;
        }

        int i = 0, j = 1;

        while (j < nums.length) {
            if (nums[i] == val && nums[j] != val) {
                int tmp = nums[i];
                nums[i] = nums[j];
                nums[j] = tmp;
            }
            if (nums[i] != val) {
                i++;
            }
            j++;
        }

        if (nums[i] != val) {
            return i + 1;
        }

        return i;
    }
}