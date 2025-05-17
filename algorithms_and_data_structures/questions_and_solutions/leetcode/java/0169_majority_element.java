class Solution {
    public int majorityElement(int[] nums) {
        if (nums.length <= 2) return nums[0];
        
        Arrays.sort(nums);
        int i = 0, num = nums[0], currOccur = 0;

        for (; i < nums.length; i++) {
            if (num != nums[i]) {
                num = nums[i];
                currOccur = 0;
            }
            currOccur++;

            if (currOccur > (nums.length / 2)) return nums[i];
        } 

        return nums[i - 1];
    }
}