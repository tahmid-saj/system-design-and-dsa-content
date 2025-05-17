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
    public boolean helper(TreeNode p, TreeNode q) {
        if (p != null && q != null) {
            if (helper(p.left, q.left) == false) return false;
            if (p.val != q.val) return false;
            if (helper(p.right, q.right) == false) return false;
        }

        if (p == null && q != null) return false;
        if (p != null && q == null) return false;
        return true;
    }

    public boolean isSameTree(TreeNode p, TreeNode q) {
        return helper(p, q);
    }
}