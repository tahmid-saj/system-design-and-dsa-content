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
    void helperInorder(TreeNode* root, vector<int> &result) {
        if (root != nullptr) {
            helperInorder(root->left, result);
            result.push_back(root->val);
            helperInorder(root->right, result);
        }
    }
    
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> result;
        helperInorder(root, result);
        return result;
    }
};