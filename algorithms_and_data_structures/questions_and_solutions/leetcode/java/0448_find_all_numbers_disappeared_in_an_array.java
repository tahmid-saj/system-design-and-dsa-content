class Solution {
    public List<Integer> findDisappearedNumbers(int[] nums) {
        // 1 2 2 3 3 4 7 8
        // if (nums.length == 1) return new ArrayList<Integer>(); 
        // sort nums
        // if (nums[0] != 1): res.add(1);
        // loop through nums using i (1 to nums.length()), j = 0 (when num is missing):
        // if (nums[i] - nums[i - 1] > 1) && (nums[i] - nums[i - 1] > j + 1):
        //  res.add(nums[i - 1] + j + 1)
        //  j++
        // i++
        // if (nums[nums.length() - 1] != nums.length()) res.add(nums.length())
        // return res
        // 3 4 5 5 6 6 7 9 9 10
        List<Integer> res = new ArrayList<Integer>();
        if (nums.length == 1) return res;
        Arrays.sort(nums);

        for (int i = 1, j = 0; i < nums.length; ) {
            if (i == 1 && nums[0] - 1 > j) {
                res.add(nums[0] - j - 1);
                j++;
            } else if (nums[i] - nums[i - 1] > 1 && nums[i] - nums[i - 1] > j + 1) {
                res.add(nums[i - 1] + j + 1);
                j++;
            } else if (i == nums.length - 1 && nums.length - nums[nums.length - 1] > j) {
                res.add(nums[nums.length - 1] + j + 1);
                j++;
            } else {
                j = 0;
                i++;
            }
        }

        return res;
    }
}