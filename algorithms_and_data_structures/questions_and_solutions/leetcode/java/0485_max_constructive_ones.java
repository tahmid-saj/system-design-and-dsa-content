class Solution {
    public int findMaxConsecutiveOnes(int[] nums) {
        if (nums.length == 1) return nums[0] == 1 ? 1: 0;

        int currConsecutives = 0, maxConsecutives = 0;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] == 1) currConsecutives++;
            if (nums[i] == 0 || i == nums.length - 1) {
                maxConsecutives = Math.max(currConsecutives, maxConsecutives);
                currConsecutives = 0;
            }
        }

        return maxConsecutives;
    }
}