class Solution {
    public int[] nextGreaterElement(int[] nums1, int[] nums2) {
        Stack<Integer> stack = new Stack<>();
        int[] nextgreat = new int[nums2.length];

        for (int i = nums2.length - 1; i >= 0; i--) {
            int ele = nums2[i];

            // Remove elements from the stack that are smaller than the current element
            while (!stack.isEmpty() && stack.peek() <= ele) {
                stack.pop();
            }

            if (stack.isEmpty()) {
                nextgreat[i] = -1;
            } else {
                nextgreat[i] = stack.peek();
            }

            stack.push(ele);
        }

        // Now, we have the next greater elements of nums2 in nextgreat
        // We can create a map for quick lookups
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums2.length; i++) {
            map.put(nums2[i], nextgreat[i]);
        }

        // Create the result array by looking up the map for each element in nums1
        int[] result = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) {
            result[i] = map.get(nums1[i]);
        }

        return result;
    }
}