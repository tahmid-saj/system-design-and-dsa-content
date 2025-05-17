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
    public boolean helper(TreeNode l, TreeNode r) {
        if (l != null && r != null) {
            if (helper(l.left, r.right) == false) return false;
            if (l.val != r.val) return false;
            if (helper(l.right, r.left) == false) return false;
        }

        if (l == null && r != null) return false;
        if (l != null && r == null) return false;

        return true;
    }

    public boolean isSymmetric(TreeNode root) {
        return helper(root.left, root.right);
    }
}