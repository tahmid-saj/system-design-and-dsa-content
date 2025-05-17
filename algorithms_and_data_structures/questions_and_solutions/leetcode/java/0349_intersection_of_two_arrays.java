class Solution {
    public int[] intersection(int[] nums1, int[] nums2) {
        Set<Integer> set1 = new HashSet<Integer>();

        for (int i = 0; i < nums1.length; i++) {
            set1.add(nums1[i]);
        }

        int[] res = new int[nums2.length];
        int prevNum = nums2[0], j = 0;
        Arrays.sort(nums2);
        for (int i = 0; i < nums2.length; i++) {
            if (set1.contains(nums2[i]) && (i == 0 || prevNum != nums2[i])) {
                res[j++] = nums2[i];
            }

            if (prevNum != nums2[i]) prevNum = nums2[i];
        }

        return Arrays.copyOfRange(res, 0, j);
    }
}