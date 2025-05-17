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

    public int helper(int currDepth, int res, TreeNode node) {
        if (node != null) {
            currDepth++;
            res = helper(currDepth, res, node.left);

            if (currDepth > res) res = currDepth;

            res = helper(currDepth, res, node.right);
            currDepth--;
        }

        return res;
    }

    public int maxDepth(TreeNode root) {
        int currDepth = 0, res = 0;
        return helper(currDepth, res, root);
    }
}