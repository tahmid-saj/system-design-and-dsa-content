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
    List<Integer> res = new ArrayList<Integer>();

    public void helper(TreeNode node) {
        if (node != null) {
            helper(node.left);
            res.add(node.val);
            helper(node.right);
        }
    }

    public List<Integer> inorderTraversal(TreeNode root) {
        helper(root);
        return res;
    }
}