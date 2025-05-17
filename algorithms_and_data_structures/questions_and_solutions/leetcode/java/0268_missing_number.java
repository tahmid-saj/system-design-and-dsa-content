class Solution {
    public int missingNumber(int[] nums) {
        // if nums.length == 1 && nums[0] == 0 return 1
        // if nums.length == 1 && nums[0] == 1 return 0
        // if nums[0] != 0 return 0
        // i = 1, while (i < nums.length):
        // if (nums[i] - 1 != nums[i - 1]) return nums[i] - 1;
        // return nums.length

        Arrays.sort(nums);
        if (nums.length == 1 && nums[0] == 0) return 1;
        if (nums.length == 1 && nums[0] == 1) return 0;
        if (nums[0] != 0) return 0;
        int i = 1;
        while (i < nums.length) {
            if (nums[i] - 1 != nums[i - 1]) return nums[i] - 1;
            i++;
        }

        return nums.length;
    }
}