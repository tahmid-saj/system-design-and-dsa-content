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
    List<String> res = new ArrayList<String>();

    public void helper(TreeNode node, String curr) {
        if (node == null) return;

        if (node.left == null && node.right == null) res.add(curr + "->" + node.val);

        helper(node.left, curr + "->" + node.val);
        helper(node.right, curr + "->" + node.val);
    }

    public List<String> binaryTreePaths(TreeNode root) {
        helper(root, "");

        for (int i = 0; i < res.size(); i++) {
            res.set(i, res.get(i).substring(2));
        }

        return res;
    }
}