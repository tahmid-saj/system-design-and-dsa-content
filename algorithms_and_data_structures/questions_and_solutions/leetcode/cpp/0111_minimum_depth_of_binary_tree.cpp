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
    int minDepthHelper(TreeNode* root, int& min, int& currMin) {
        if (root != nullptr) {
            currMin++;
            minDepthHelper(root->left, min, currMin);
        
            
            if ((currMin < min || min == 0) && root->left == nullptr && root->right == nullptr) {
                min = currMin;
            }

            minDepthHelper(root->right, min, currMin);
            currMin--;
        }

        return min;
    }
    
    int minDepth(TreeNode* root) {
        int min = 0, currMin = 0;

        if (root == nullptr) {
            return 0;
        }

        return minDepthHelper(root, min, currMin);
    }
};