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
    bool isSymmetricHelper(TreeNode* l, TreeNode* r) {
        if (l != nullptr && r != nullptr) {
            if (l->val == r->val) {
                if (isSymmetricHelper(l->left, r->right) == false) {
                    return false;
                }
                if (isSymmetricHelper(l->right, r->left) == false) {
                    return false;
                }
            }
            else if (l->val != r->val) {
                return false;
            }
        }

        if (l == nullptr && r != nullptr) {
            return false;
        }

        if (l != nullptr && r == nullptr) {
            return false;
        }

        return true;
    }
    
    bool isSymmetric(TreeNode* root) {
        if (root != nullptr) {
            return isSymmetricHelper(root->left, root->right);
        }

        return true;
    }
};