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
    int maxDepth(TreeNode* root, int &max, int &currMax) {
        if (root != nullptr) {
            currMax++;
            maxDepth(root->left, max, currMax);

            if (currMax > max) {
                max = currMax;
            }

            maxDepth(root->right, max, currMax);
            currMax--;
        }

        return max;
    }
    
    bool isBalanced(TreeNode* root) {
        int max = 0, currMax = 0;

        if (root != nullptr) {
            
            int maxDepthLeft = maxDepth(root->left, max, currMax);
            max = 0, currMax = 0;
            int maxDepthRight = maxDepth(root->right, max, currMax);
            max = 0, currMax = 0;
            
            if (maxDepthLeft - maxDepthRight < -1) {
                return false;
            }
            
            if (maxDepthLeft - maxDepthRight > 1) {
                return false;
            }
            
            
            if (maxDepthLeft - maxDepthRight >= -1 &&
                maxDepthLeft - maxDepthRight <= 1) {
                max = 0, currMax = 0;
                
                if (isBalanced(root->left) == false || isBalanced(root->right) == false) {
                    return false;
                }
                
            }
        }

        return true;
    }
};