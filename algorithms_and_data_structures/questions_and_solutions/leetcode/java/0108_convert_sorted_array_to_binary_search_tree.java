/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {

    public TreeNode helper(int[] nums, int l, int r) {
        while (l <= r) {
            int middle = l + (r - l) / 2;

            TreeNode node = new TreeNode(nums[middle]);
            node.left = helper(nums, l, middle - 1);
            node.right = helper(nums, middle + 1, r);

            return node;
        }

        return null;
    }

    public TreeNode sortedArrayToBST(int[] nums) {
        return helper(nums, 0, nums.length - 1);
    }
}