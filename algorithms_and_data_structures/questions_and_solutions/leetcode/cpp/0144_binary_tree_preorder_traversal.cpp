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
    vector<int> preorderTraversalHelper(TreeNode* root, vector<int>& ret) {
        if (root != nullptr) {
            ret.push_back(root->val);
            preorderTraversalHelper(root->left, ret);
            preorderTraversalHelper(root->right, ret);
        }

        return ret;
    }
    
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> ret;

        return preorderTraversalHelper(root, ret);
    }
};