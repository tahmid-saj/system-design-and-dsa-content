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
    public int maxDepth(TreeNode node, int currHeight, int height) {
        if (node != null) {
            currHeight++;
            height = maxDepth(node.left, currHeight, height);
            if (height < currHeight) height = currHeight;
            height = maxDepth(node.right, currHeight, height);
            currHeight--;
        }

        return height;
    }

    public boolean isBalanced(TreeNode root) {
        if (root != null) {
            if (isBalanced(root.left) == false) return false;

            int lHeight = maxDepth(root.left, 0, 0);
            int rHeight = maxDepth(root.right, 0, 0);
            if (Math.abs(lHeight - rHeight) > 1) return false;

            if (isBalanced(root.right) == false) return false;
        }

        return true;
    }
}