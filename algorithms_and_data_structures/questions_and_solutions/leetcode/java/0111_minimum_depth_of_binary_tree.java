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
    public int helper(TreeNode node, int currDepth, int depth) {
        if (node != null) {
            currDepth++;
            depth = helper(node.left, currDepth, depth);

            if (currDepth < depth && (node.left == null && node.right == null)) depth = currDepth;

            depth = helper(node.right, currDepth, depth);
            currDepth--;
        }

        return depth;
    }

    public int minDepth(TreeNode root) {
        if (root == null) return 0;
        return helper(root, 0, Integer.MAX_VALUE);
    }
}