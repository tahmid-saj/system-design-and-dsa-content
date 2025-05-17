class Solution {
    public int searchInsert(int[] nums, int target) {
        int l = 0, r = nums.length - 1, middle = 0;

        while (l <= r) {
            middle = l + ((r - l) / 2);

            if (target > nums[middle]) {
                l = middle + 1;
            } else if (target < nums[middle]) {
                r = middle - 1;
            } else {
                return middle;
            }
        }

        return l;
    }
}