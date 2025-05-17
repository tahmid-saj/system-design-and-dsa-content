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
    int maxDepthHelper(TreeNode* root, int& max, int& currMax) {
        if (root != nullptr) {
            currMax++;  

            maxDepthHelper(root->left, max, currMax);

            if (max < currMax) {
                max = currMax;
            }

            maxDepthHelper(root->right, max, currMax);
            currMax--;
        }

        return max;
    }
    
    int maxDepth(TreeNode* root) {
        int max = 0, currMax = 0;

        return maxDepthHelper(root, max, currMax);
    }
};