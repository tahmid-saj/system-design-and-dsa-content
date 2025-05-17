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
    TreeNode* balance(vector<int>& nums, int first, int last) {
        if (first > last) {
            return NULL;
        }
        
        int middle = (first + last) / 2;
        TreeNode* node = new TreeNode(nums[middle]);
        
        node->left = balance(nums, first, middle - 1);
        node->right = balance(nums, middle + 1, last);
        
        return node;
    }
    
    TreeNode* sortedArrayToBST(vector<int>& nums) {
        int sizeNum = nums.size() - 1;
        
        return balance(nums, 0, sizeNum);
    }
};