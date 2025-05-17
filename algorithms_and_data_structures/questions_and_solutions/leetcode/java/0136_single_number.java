class Solution {
    public int singleNumber(int[] nums) {
        // sort nums
        // if nums.length == 1: return nums[1]
        // loop through nums using i (starting 0), j (starting 1)
        // if (j == nums.length) return nums[i]
        // if (nums[i] != nums[j]) return nums[i]
        // i++; j++;

        Arrays.sort(nums);
        if (nums.length == 1) return nums[0];
        int i = 0, j = 1, res = 0;

        while (j <= nums.length) {
            if (j == nums.length) {
                res = nums[i];
                break;
            }
            if (nums[i] != nums[j]) {
                res = nums[i];
                break;
            }

            i+=2;
            j+=2;
        }

        return res;
    }
}