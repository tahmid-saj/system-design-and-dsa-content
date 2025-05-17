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
    bool isSameTree(TreeNode* p, TreeNode* q) {
        if (p != nullptr && q != nullptr) {
            if (p->val != q->val) {
                return false;
            }
            else if (p->val == q->val) {
                if (isSameTree(p->left, q->left) == false) {
                    return false;
                }
                if (isSameTree(p->right, q->right) == false) {
                    return false;
                }
            }
        }

        if (p == nullptr && q != nullptr) {
            return false;
        }

        if (q == nullptr && p != nullptr) {
            return false;
        }

        return true;
    }
};