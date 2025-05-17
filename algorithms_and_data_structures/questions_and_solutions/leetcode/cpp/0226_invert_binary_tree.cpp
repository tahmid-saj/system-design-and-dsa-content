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
    void invertTreeHelper(TreeNode* node) {
        if (node != nullptr) {
            invertTreeHelper(node->left);

            TreeNode* leftNode = node->left;
            node->left = node->right;
            node->right = leftNode;

            invertTreeHelper(node->left);
        }
    }

    TreeNode* invertTree(TreeNode* root) {
        invertTreeHelper(root);

        return root;
    }
};