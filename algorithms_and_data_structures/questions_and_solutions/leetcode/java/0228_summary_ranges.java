class Solution {
    public List<String> summaryRanges(int[] nums) {
        int start = 0, end = 0;
        List<String> res = new ArrayList<String>();
        boolean inInterval = false;

        if (nums.length == 1) {
            res.add(String.valueOf(nums[0]));
            return res;
        }

        for (int i = 0; i < nums.length; i++) {
            if (i == 0) {
                start = nums[i];
            }

            if (i != 0 && Long.valueOf(nums[i]) - Long.valueOf(nums[i - 1]) > 1) {
                if (start == nums[i - 1]) {
                    res.add(String.valueOf(start));
                } else {
                    end = nums[i - 1];
                    res.add(start + "->" + nums[i - 1]);
                    end = 0;
                }
                start = nums[i];

                if (end == 0 && i == nums.length - 1) {
                    res.add(String.valueOf(start));
                }
            }

            if (i == nums.length - 1) {
                if (nums[i] - nums[i - 1] == 1) {
                    res.add(start + "->" + nums[i]);
                }
            }
        }

        return res;
    }
}