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
    int res = 0;
    public int sumOfLeftLeaves(TreeNode root) {
        if (root != null) {
            sumOfLeftLeaves(root.left);
            if (root.left != null && (root.left.left == null && root.left.right == null)) res += root.left.val;
            sumOfLeftLeaves(root.right);
        }

        return res;
    }
}