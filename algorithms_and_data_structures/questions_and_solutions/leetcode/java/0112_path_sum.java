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
    int currSum = 0;
    
    public boolean hasPathSum(TreeNode root, int targetSum) {
        // helper(node, targetSum, currSum) -> returns true if node is a leaf node and targetSum == currSum
    
        if (root != null) {
            currSum += root.val;
            if (hasPathSum(root.left, targetSum) == true) return true;

            if (currSum == targetSum && (root.left == null && root.right == null)) return true;

            if (hasPathSum(root.right, targetSum) == true) return true;
            currSum -= root.val;
        }

        return false;
    }
}