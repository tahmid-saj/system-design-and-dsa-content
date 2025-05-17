/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    bool sumHelper(TreeNode* root, int targetSum, int& currSum) {
        if (root != nullptr) {
            currSum += root->val;
            if (sumHelper(root->left, targetSum, currSum) == true) {
                return true;
            }

            if (root->left == nullptr && root->right == nullptr && currSum == targetSum) {
                return true;
            }

            if (sumHelper(root->right, targetSum, currSum) == true) {
                return true;
            }
            currSum -= root->val;
        }

        return false;
    }
    
    bool hasPathSum(TreeNode* root, int targetSum) {
        int currSum = 0;

        return sumHelper(root, targetSum, currSum);
    }
};