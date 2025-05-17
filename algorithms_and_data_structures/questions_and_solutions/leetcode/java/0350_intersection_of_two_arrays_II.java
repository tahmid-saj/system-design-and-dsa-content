class Solution {
    public int[] intersect(int[] nums1, int[] nums2) {
        // Map<Integer, Integer> map1 = new HashMap<Integer, Integer>();
        // for (int i = 0; i < nums1.length; i++) {
        //     if (!map1.containsKey(nums1[i])) {
        //         map1.put(nums1[i], 1);
        //     } else if (map1.containsKey(nums1[i])) {
        //         map1.put(nums1[i], map1.get(nums1[i]) + 1);
        //     }
        // }

        // int[] res = new int[nums2.length];
        // int j = 0, prevNum = nums2[0];
        // for (int i = 0; i < nums2.length; i++) {
        //     if (map1.containsKey(nums2[i])) {
        //         if (map1.get(nums2[i]) == 1) {
        //             map1.remove(nums2[i]);
        //         } else {
        //             map1.put(nums2[i], map1.get(nums2[i]) - 1);
        //         }
        //         res[j++] = nums2[i];
        //     }
        // }

        // return Arrays.copyOfRange(res, 0, j);

        int i = 0, j = 0, k = 0;
        Arrays.sort(nums1);
        Arrays.sort(nums2);
        while (i < nums1.length && j < nums2.length) {
            if (nums1[i] < nums2[j]) {
                i++;
            } else if (nums1[i] > nums2[j]) {
                j++;
            } else {
                nums1[k++] = nums2[j++];
                i++;
            }
        }

        return Arrays.copyOfRange(nums1, 0, k);
    }
}